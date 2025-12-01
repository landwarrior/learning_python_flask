"""カスタムロガー.

Flask で利用する場合はリクエストを判断するためのユニークキーを付与する.
Flask 環境でなければ、ユニークキーを使わずにログ出力する.
"""

import logging
import uuid


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
