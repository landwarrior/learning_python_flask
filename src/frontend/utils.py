"""ユーティリティ関数."""

import datetime


def get_common_data() -> dict:
    """汎用データ取得.

    本来はここでログインユーザの情報を取得したり、メニューの出し分けを取得したりしたいかも.

    Returns:
        dict: 汎用データの辞書データ.
    """
    common_data = {"now": {"year": datetime.datetime.now().year}}
    return common_data
