# Ansible ディレクトリ構成

このディレクトリは、Vagrant VM および別ホストへの環境構築を Ansible で行うためのものです。

## 全体像

Ansible は「制御ノード（ansible-playbook を実行する場所）」から「管理対象ホスト（設定を適用する先）」へ処理を行います。
このプロジェクトでは playbook や roles を共通化し、inventory で接続先を切り替えます。

| 用語 | 役割 | このプロジェクトでの例 |
|------|------|----------------------|
| playbook | 全体の手順書（入口） | `site.yml` |
| role（ロール） | 手順のまとまり | `common`, `docker`, `app_deploy` |
| task（タスク） | 具体的な 1 ステップ | 「Docker をインストールする」など |
| inventory | 対象ホストの一覧 | `inventory/local.ini`, `inventory/remote.ini` |
| vars（変数） | 環境ごとに変わる値 | `group_vars/all.yml` |
| ansible.cfg | Ansible 自体の設定 | デフォルト inventory パスなど |

```
provisioning.sh（実行の入口）
    │
    ▼
ansible.cfg ──► site.yml（playbook）
                    │
    inventory/*.ini ┤
    group_vars/     ┤
                    ▼
              roles/
                ├── common       … OS 初期設定
                ├── docker       … Docker インストール
                └── app_deploy   … アプリ配置・起動
```

## フォルダ構成

```
ansible/
├── README.md                … このファイル
├── ansible.cfg              … Ansible の動作設定
├── site.yml                 … 実行の起点（playbook）
├── inventory/
│   ├── local.ini            … VM 内から実行するとき用
│   └── remote.ini           … 別ホストから SSH 実行するとき用
├── group_vars/
│   └── all.yml              … 全ホスト共通の変数
└── roles/
    ├── common/              … OS の初期設定
    │   └── tasks/main.yml
    ├── docker/              … Docker インストール
    │   └── tasks/main.yml
    └── app_deploy/          … アプリ配置・デプロイ
        ├── tasks/main.yml
        └── templates/fluentd.logrotate.j2
```

## 各ファイルの説明

### site.yml — 入口の playbook

どのホストに、どのロールを、どの順番で実行するかを定義します。

```yaml
- name: Provision application host
  hosts: app_servers
  roles:
    - common
    - docker
    - app_deploy
```

- `hosts: app_servers` … inventory の `[app_servers]` グループが対象
- `roles:` … `common` → `docker` → `app_deploy` の順に実行

### ansible.cfg — Ansible の設定ファイル

毎回コマンドにオプションを付けなくてよいよう、デフォルト値を定めます。

| 設定 | 意味 |
|------|------|
| `inventory = inventory/local.ini` | デフォルトで `local.ini` を使う |
| `roles_path = roles` | ロールは `roles/` フォルダを参照する |
| `become = True` | タスクを `sudo` 付きで実行する |

### inventory/ — 対象ホストの名簿

同じ playbook でも、接続先を切り替えられます。

#### local.ini（VM 内の provisioning.sh 用）

```ini
[app_servers]
localhost ansible_connection=local
```

- `localhost` … VM 自身を対象にする
- `ansible_connection=local` … SSH せず VM 内で直接実行する

#### remote.ini（別ホストから実行するとき用）

```ini
[app_servers]
flask-app ansible_host=192.168.33.33 ansible_user=vagrant
```

- `ansible_host` … 接続先 IP
- `ansible_user` … SSH ユーザー
- `ansible_ssh_private_key_file` … SSH 秘密鍵のパス

playbook は同じ `site.yml` を使い、`-i` オプションで inventory だけ切り替えます。

### group_vars/all.yml — 共通の変数

環境によって変わりうる値を、タスク本体から分離して書きます。

```yaml
vagrant_mount: /vagrant
docker_images:
  - frontend
  - backend
  # ...
docker_stack_name: test
```

タスク側では `{{ docker_images }}` のように参照します。

### roles/ — 処理のまとまり

関連するタスクを 1 つの単位にまとめたものです。

#### common — OS の初期設定

- bash-completion のインストール
- firewalld の無効化
- podman / runc の削除（Docker と競合するため）

#### docker — Docker のインストール

旧 Chef の `docker` レシピに相当します。

- Docker CE リポジトリの追加
- docker-ce などのパッケージインストール
- Docker サービスの起動
- `/var/log/fluent` ディレクトリ作成

#### app_deploy — アプリの配置と起動

- `fileput.sh` の実行（ソース配置）
- MariaDB 用ログディレクトリ作成
- Docker Swarm の初期化
- Docker イメージのビルド
- `docker stack deploy`
- logrotate 設定

`templates/` フォルダには Jinja2 テンプレート（`.j2`）があり、変数を埋め込んだ設定ファイルを生成します。

### roles/*/tasks/main.yml — 各ロールの実際の処理

タスクの書き方の例:

```yaml
- name: Install Docker packages
  ansible.builtin.dnf:
    name:
      - docker-ce
      - docker-ce-cli
    state: present
```

- `name:` … タスクの説明（ログに表示される）
- `ansible.builtin.dnf:` … 使うモジュール
- `state: present` … 「インストールされている状態にする」

## 実行方法

### パターン A: Windows → Vagrant VM（通常の手順）

Windows 側に Ansible は不要です。VM 内で `provisioning.sh` が Ansible をインストールし、playbook を実行します。

```bash
# Windows
vagrant up
vagrant reload
vagrant ssh

# VM 内
sudo su
/vagrant/provisioning.sh
```

実行の流れ:

```
provisioning.sh
  ① dnf install ansible-core（未インストール時）
  ② ansible-playbook site.yml
       → inventory/local.ini（localhost）
       → common → docker → app_deploy を順に実行
```

### パターン B: 別ホストから SSH 実行

制御ノードに Ansible をインストールしたうえで、同じ playbook を実行します。

```bash
cd ansible
ansible-playbook -i inventory/remote.ini site.yml
```

`remote.ini` の `ansible_ssh_private_key_file` は、実行環境に合わせて変更してください。

## ログの見方

`ansible-playbook` は各タスクの結果を次のように表示します。

| 表示 | 意味 |
|------|------|
| `ok` | すでに望ましい状態だった（変更なし） |
| `changed` | 何かを変更した（初回実行では多くなる） |
| `skipped` | 条件により実行しなかった |
| `failed` | 失敗 |

末尾の `PLAY RECAP` は全体の集計です。`failed=0` なら成功です。

```
PLAY RECAP *****************************************************************
localhost    : ok=22   changed=13   unreachable=0   failed=0   skipped=0
```

- **初回実行** … `changed` が多いのは正常（Docker インストール、イメージビルドなどが初めて実行された）
- **2 回目以降** … すでに構築済みなら `ok` や `skipped` が増え、`changed` は少なくなる

### 各処理のログを見る

Ansible はデフォルトではタスク名と `ok` / `changed` だけを表示します。
`provisioning.sh` は `-v`（verbose）付きで playbook を実行するため、`command` や `shell` モジュールが変更を行ったときは、コマンドの標準出力も表示されます。

`app_deploy` ロールでは、旧 `provisioning.sh` と同様の進捗メッセージも `debug` タスクで出力します。

```
TASK [app_deploy : Report Docker image build plan] ***
ok: [localhost] => (item=frontend) => {
    "msg": "  - docker build frontend"
}
```

さらに詳しい Ansible 内部ログが必要な場合は、手動で次を実行します。

```bash
ANSIBLE_CONFIG=/vagrant/ansible/ansible.cfg ansible-playbook -vv /vagrant/ansible/site.yml
```

`-v` の数を増やすほど詳細になります（`-vv`, `-vvv`）。

## 覚えておくポイント

1. **`site.yml` が入口** … まずここを見れば全体の流れが分かる
2. **inventory = 誰に**、**roles = 何をするか**、**group_vars = 設定値**
3. **`tasks/main.yml`** が各ロールの実際の処理
4. **環境の違いは inventory と vars で吸収** … playbook 本体は共通化
5. **`provisioning.sh` は Ansible のラッパー** … Ansible のインストールと playbook 実行を担当

## 旧 Chef との対応

| 旧 Chef | 新 Ansible |
|---------|-----------|
| `chef-repo/cookbooks/docker/recipes/default.rb` | `roles/docker/tasks/main.yml` |
| `chef-repo/nodes/flask_app.json`（run_list） | `site.yml`（roles 一覧） |
| `chef-repo/solo.rb`（設定） | `ansible.cfg` |
| `provisioning.sh` 内の shell 処理 | `roles/common/`, `roles/app_deploy/` |
