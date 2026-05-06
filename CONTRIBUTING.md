# Contributing

このリポジトリに変更を加えるときの基本方針です。

## 1. ディレクトリ責務

- `src/common/models/orm`: SQLAlchemy のテーブル定義
- `src/common/models/repositories`: DB アクセス処理
- `src/backend`: Flask API
- `src/frontend`: フロントエンド API
- `src/batch`: バッチ処理

## 2. import ルール

- 外部コードは `from models import ...` を優先する。
- `models` 配下は絶対 import を使う（親方向の相対 import は使わない）。
- `models/__init__.py` は公開 API の窓口として扱う。

## 3. 命名ルール

- ORM 定義: `*_model.py`
- Repository: `*_repository.py`

## 4. 実行環境の前提

- 編集は Windows で行う。
- 実行は Vagrant VM 上の Docker で行う。
- backend 実行基点は `/var/app/flask/backend`。

詳細は `docs/runtime-context.md` を参照。
