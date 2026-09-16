"""カスタムロガー.

Flask で利用する場合はリクエストを判断するためのユニークキーを付与する.
Flask 環境でなければ、ユニークキーを使わずにログ出力する.
機密値は mask_sensitive() と MaskingFilter でマスクする.

変更してよい定数は MASK と SENSITIVE_KEYS だけ.
マスク対象を増やすときは SENSITIVE_KEYS にキー名を小文字で追加する.
置換文字列を変えたいときは MASK を変更する.
"""

import logging
import re
import uuid
from collections.abc import Mapping


# --- 変更してよい定数 ---

# ログに出すときの置換文字列. 元の値の長さは残さない (長さから推測されないようにする).
MASK = "********"

# マスクするキー名. 判定は str(key).lower() との完全一致なので、追加する値は小文字にする.
# 部分一致ではない. "token" を足しても "my_token" や "user_token" はマスクされない.
# 新しい機密項目をリクエスト JSON / ヘッダ / session に足したら、ここにキー名を追加する.
SENSITIVE_KEYS = frozenset(
    {
        "ignition_key",  # ログイン時のパスワード (本アプリの項目名)
        "password",  # 一般的なパスワード項目
        "old_password",  # パスワード変更 API の旧パスワード
        "new_password",  # パスワード変更 API の新パスワード
        "authorization",  # Authorization ヘッダ (Bearer トークンなど)
        "cookie",  # Cookie ヘッダ全体
        "set-cookie",  # Set-Cookie ヘッダ全体
        "csrf_token",  # Flask-WTF の CSRF トークン (session に入る)
        "token",  # 汎用トークン項目
        "secret",  # 汎用シークレット項目
    }
)


def _compile_mask_pattern() -> re.Pattern[str]:
    """SENSITIVE_KEYS から文字列マスク用の正規表現を組み立てる.

    内部実装なのでこの関数は変更しない. 対象キーを増やすときは SENSITIVE_KEYS を更新する.
    文字列化されたログの "key": "value" / 'key': 'value' / key=value / Cookie: value を拾う.
    長いキー名を先に置き、csrf_token が token より優先されるようにする.

    Returns:
        コンパイル済みのマスク用正規表現.
    """
    key_alt = "|".join(sorted((re.escape(key) for key in SENSITIVE_KEYS), key=len, reverse=True))
    return re.compile(
        rf"""
        (?P<prefix>
            (?<![A-Za-z0-9_-])
            ['\"]?(?:{key_alt})['\"]?
            \s*[:=]\s*
        )
        (?:
            (?P<quote>['\"])(?P<quoted>.*?)(?P=quote)
            |
            (?P<unquoted>[^,}}]+)
        )
        """,
        re.IGNORECASE | re.VERBOSE,
    )


# --- 変更しない定数 (SENSITIVE_KEYS から生成する内部用) ---
_MASK_PATTERN = _compile_mask_pattern()


def _is_sensitive_key(key: object) -> bool:
    """キー名が機密項目かどうかを返す.

    Args:
        key: 判定対象のキー.

    Returns:
        機密キーなら True.
    """
    return str(key).lower() in SENSITIVE_KEYS


def _replace_sensitive(match: re.Match[str]) -> str:
    """正規表現で見つけた機密値を MASK に置換する.

    Args:
        match: 機密キーと値のマッチ結果.

    Returns:
        値をマスクした文字列.
    """
    quote = match.group("quote") or ""
    return f"{match.group('prefix')}{quote}{MASK}{quote}"


def mask_message(message: str) -> str:
    """完成済みログメッセージから機密値をマスクする.

    Args:
        message: ログメッセージ.

    Returns:
        マスク済みメッセージ.
    """
    return _MASK_PATTERN.sub(_replace_sensitive, message)


def _mask_mapping(value: Mapping[object, object]) -> dict[object, object]:
    """マッピングの機密値をマスクした dict を返す.

    Args:
        value: マスク対象のマッピング.

    Returns:
        マスク済みの dict. 元のオブジェクトは変更しない.
    """
    masked: dict[object, object] = {}
    for key, item in value.items():
        if _is_sensitive_key(key):
            masked[key] = MASK
        else:
            masked[key] = mask_sensitive(item)
    return masked


def mask_sensitive(value: object) -> object:
    """機密キーの値をマスクしたコピーを返す.

    dict / list は再帰的に処理する. 文字列はキー名パターンでマスクする.
    元のオブジェクトは変更しない.

    Args:
        value: マスク対象.

    Returns:
        マスク済みの値.
    """
    if isinstance(value, Mapping):
        return _mask_mapping(value)
    if isinstance(value, list):
        return [mask_sensitive(item) for item in value]
    if isinstance(value, tuple):
        return tuple(mask_sensitive(item) for item in value)
    if isinstance(value, str):
        return mask_message(value)
    return value


class MaskingFilter(logging.Filter):
    """完成済みログメッセージから機密値をマスクするフィルタ."""

    def filter(self, record: logging.LogRecord) -> bool:
        """ログレコードのメッセージをマスクする.

        Args:
            record: ログレコード.

        Returns:
            常に True. ログ出力は抑制しない.
        """
        record.msg = mask_message(record.getMessage())
        record.args = ()
        return True


class UniqueKeyFormatter(logging.Formatter):
    """カスタムログフォーマット."""

    def __init__(self):
        """コンストラクタ."""
        log = "%(asctime)s [%(levelname)-7s](%(name)s)%(unique_key)s | %(message)s [in %(pathname)s:%(lineno)d]"
        super().__init__(log)
        try:
            from flask import g

            self.has_g = bool(g)
        except Exception:
            self.has_g = False

    def format(self, record: logging.LogRecord) -> str:
        """ログフォーマットに unique_key を追加して出力できるようにする.

        Args:
            record (logging.LogRecord): ログレコード

        Returns:
            str: ログフォーマット
        """
        if self.has_g:
            from flask import g

            if not hasattr(g, "count"):
                g.count = 1
            if not hasattr(g, "unique_key"):
                g.unique_key = uuid.uuid4().hex[0:7]
            record.unique_key = f"[{g.unique_key}:{g.count:02}]"
            g.count += 1
        else:
            record.unique_key = ""
        return super().format(record)


def build_stream_handler() -> logging.StreamHandler:
    """マスク Filter と UniqueKeyFormatter を付けた StreamHandler を返す.

    Returns:
        設定済みの StreamHandler.
    """
    handler = logging.StreamHandler()
    handler.setFormatter(UniqueKeyFormatter())
    handler.addFilter(MaskingFilter())
    return handler
