# AGENTS.md

Flask 学習用 Web アプリ。Windows 上で編集し、Vagrant VM 上の Docker Swarm で実行する。

## ディレクトリ構成

```
src/
  backend/     REST API (uWSGI, port 5000)
  frontend/    画面 (Jinja2 + Bootstrap + Vue, uWSGI)
  common/      backend / frontend / batch で共有するコード
  batch/       バッチ処理
tests/
  backend/     backend API の pytest
```

- `src/common/*` は実行時に `fileput.sh` により各サービス配下へコピーされる。
- backend の実行基点は `src/backend/uwsgi.ini` の `chdir = /var/app/flask/backend`、`module = backend:app`。実行時の import 起点は backend 直下になる。
- 共有コードはリポジトリ上では `src/common/` に置くが、実行時は `models` や `mylogger` などトップレベルモジュールとして import する。
- `models/__init__.py` は公開 API の窓口として扱う。

## 開発・実行

### ローカル編集

- エディタ: Windows 上の **Zed**（メイン）。たまに **Cursor** IDE も使う。
- エージェント操作: Zed 利用時も **Cursor CLI** を使う（この `AGENTS.md` は CLI からも読まれる）。
- Python 仮想環境: `.venv`（型チェック・lint 用）
- Python 3.14、設定は `pyproject.toml`

### VM / Docker での実行

```bash
vagrant up
vagrant reload
vagrant ssh
sudo su
/vagrant/provisioning.sh
```

コード変更をコンテナへ反映する場合:

```bash
/vagrant/fileput.sh
docker rm -f $(docker ps -q --filter name=frontend)
docker rm -f $(docker ps -q --filter name=backend)
```

アプリ URL: http://192.168.33.33/login

## コーディング規約

### Python

- **import**: 親方向の相対 import（`from ..`）は使わず、絶対 import を使う。
- **永続化**: `models` は永続化レイヤーとして扱う。
  - `models/orm/` — SQLAlchemy テーブル定義（ファイル名: `*_model.py`）
  - `models/repositories/` — DB アクセス処理（ファイル名: `*_repository.py`）
  - 外部コードからは `from models import ...` を優先する（`__init__.py` の `__all__` を更新する）。
- **API**: `src/backend/apis/` に Blueprint 単位で配置し、`routes.py` で登録する。
- **型**: 型注釈を付ける。`typed_flask` のヘルパー（`get_db` など）を利用する。
- **将来**: Pydantic を導入する場合は、API の入出力モデルを `schemas` へ配置する方針を検討する。
- **Docstring**: Google スタイル。Ruff の pydocstyle ルールに従う。
- **整形・lint**: Ruff（`pyproject.toml` の設定に従う。行長 120、循環的複雑度上限 10）。
- **型チェック**: Pyright（`pyproject.toml` の `[tool.pyright]`。`extraPaths` に `src/common` を含む）。

### JavaScript

- `src/frontend/static/assets/js/` 配下
- 整形・lint: Biome（`biome.jsonc`）
- `.jinja` テンプレート内の JS は Biome 対象外

### フロントエンド

- テンプレート: Jinja2（`src/frontend/templates/`）
- 画面ロジック: `src/frontend/views/` に Blueprint 単位で配置

## テスト

テストは `tests/backend/` に置く。VM 内では `fileput.sh` により `/var/app/flask/tests/` へコピーされる。

```bash
# VM 内の backend コンテナ等で実行
cd /var/app/flask/tests
pytest
```

- 命名: `test_*.py`、関数 `test_*`
- 設定: `tests/backend/pytest.ini`（coverage 対象: `../backend`, `../common`）
- テスト DB: 環境変数 `POSITION=test`（`conftest.py` で設定）
- fixture: `conftest.py` の `app`, `client`, `db`, `clean_mst_user_table`

ローカルで pytest を走らせる場合は、`pyproject.toml` の `executionEnvironments` に合わせて `src/backend` と `src/common` が import 解決できることを確認する。

## 変更時の注意

- `src/common/` を変更した場合、backend・frontend・batch のいずれにも影響する。
- 新しい ORM モデルやリポジトリを追加したら `src/common/models/__init__.py` の `__all__` を更新する。
- DB スキーマ変更後は MariaDB ボリュームの再作成が必要な場合がある（詳細は `README.md`）。
- コミット・PR の作成はユーザーが明示的に依頼したときのみ行う。

## 関連ファイル

- 人間向けセットアップ手順: `README.md`
- Cursor / Cursor CLI 向けの追加ルール: `.cursor/rules/project-structure.mdc`
