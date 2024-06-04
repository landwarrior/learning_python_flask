"""カスタムロガー.

Flask で利用する場合はリクエストを判断するためのユニークキーを付与する.
Flask 環境でなければ、ユニークキーを使わずにログ出力する.
"""

import logging


class UniqueKeyFormatter(logging.Formatter):
    """カスタムログフォーマット."""

    def __init__(self):
        log = "%(asctime)s [%(levelname)-7s](%(name)s)%(unique_key)s | %(message)s [in %(pathname)s:%(lineno)d]"
        super().__init__(log)
        try:
            from flask import g

            self.has_g = True if g is not None else False
        except Exception:
            self.has_g = False

    def format(self, record):
        """ログフォーマットに unique_key を追加して出力できるようにする."""
        if self.has_g:
            from flask import g

            if not hasattr(g, "count"):
                g.count = 1
            record.unique_key = f"[{g.unique_key}:{g.count:02}]"
            g.count += 1
        else:
            record.unique_key = ""
        return super().format(record)
