"""初期パスワード設定スクリプト.

init.sql で作成されたユーザー(パスワードが空のユーザー)に
初期パスワードを設定するスクリプトです。
"""

import logging
import os

from argon2 import PasswordHasher
from models import Database, mst_user
from mylogger import UniqueKeyFormatter


def main():
    """全ユーザーに初期パスワードを設定する."""
    # 初期パスワード
    new_password = "password"

    logger = logging.getLogger(os.path.splitext(os.path.basename(__file__))[0])
    logger.setLevel(logging.DEBUG)
    handler = logging.StreamHandler()
    formatter = UniqueKeyFormatter()
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    # Argon2 のパスワードハッシャーを初期化
    ph = PasswordHasher(
        time_cost=2,  # 反復回数: パスワードハッシュ化の計算コストを制御。値が大きいほど強力だが処理時間も増える
        memory_cost=65536,  # メモリ使用量(KB): 65536KB = 64MB。メモリハードな計算によりGPU攻撃を防ぐ
        parallelism=2,  # 並列度: 並列処理に使用するスレッド数。メモリ使用量に影響する
    )

    db = Database("mysql+mysqlconnector://myaccount:myaccount@192.168.33.33/mydb")
    db.Base.prepare(autoload_with=db.engine)
    db.mst_user = db.Base.classes.mst_user

    logger.info("初期パスワード設定を開始します...")
    updated_count = 0

    for user in mst_user.get_all_data(logger, db.engine, db):
        # パスワードが空または未設定のユーザーのみ更新
        if not user.ignition_key or user.ignition_key == "":
            logger.info(f"ユーザーID: {user.user_id} に初期パスワードを設定します")
            user.ignition_key = ph.hash(new_password)
            updated_count += 1
        else:
            logger.info(f"ユーザーID: {user.user_id} は既にパスワードが設定されています(スキップ)")

    if updated_count > 0:
        db.session.commit()
        logger.info(f"初期パスワード設定が完了しました。更新ユーザー数: {updated_count}")
    else:
        logger.info("パスワードを設定するユーザーはありませんでした。")


if __name__ == "__main__":
    main()
