# Runtime Context

このドキュメントは、開発環境と実行環境の前提をまとめたものです。  
AI 支援ツールを使うときは、この内容を前提として判断してください。

## 1. 開発と実行の分離

- 編集環境: Windows
- 実行環境: Vagrant VM 上の Docker コンテナ

## 2. 配置とマウント

- ホスト上のソースは VM 側へ配置される。
- `fileput.sh` で `src/common/*` を backend / frontend / batch 各実行ディレクトリへコピーする。
- backend コンテナは `/var/app/flask/backend` をマウントして実行する。

## 3. backend 実行基点

- `src/backend/uwsgi.ini`:
  - `chdir = /var/app/flask/backend`
  - `module = backend:app`

このため、実行時 import の起点は backend 直下になる。

## 4. Python import 方針

- `src/common/models` の公開窓口は `models/__init__.py`。
- 外部コードは `from models import ...` を基本とする。
- 親方向の相対 import（`from ..`）は避け、絶対 import を使う。

## 5. モデル構成

- `models/orm`: SQLAlchemy ORM のテーブル定義
- `models/repositories`: DB アクセス処理

今後 Pydantic を導入する場合は、API の入出力モデルを `schemas` へ配置する方針を検討する。
