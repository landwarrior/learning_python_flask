# learning_python_flask

Flaskの勉強のため作ったやつ。  
Visual Studio 2017 Communityで生成したものからやろうかと思ったが、うまくいかなくて放置してたら時間がたちすぎたので改めて作り直す。

# 環境構築

vagrant で VM を作成し、その上に docker swarm でアプリを構築します。  
必要な環境は以下です。バージョンは任意。

- VirtualBox
- Vagrant

VirtualBox と Vagrant がすでにインストール済みであるものとして続けます。

## コマンドプロンプトで VM を立ち上げる

このリポジトリを git clone したか、もしくは zip としてダウンロードして解凍した後のディレクトリで作業します。  
ディレクトリが `C:\Users\user\git_src\learning_python_flask` という仮定で進めます。

VM を立ち上げるため、コマンドプロンプトを立ち上げて以下のコマンドを実行します。

```bash
cd C:\Users\user\git_src\learning_python_flask
vagrant up
```

Vagrantfile に記載された内容で VM がセットアップされ立ち上がります。

## プロビジョニングする

Vagrantfile には最小限の記述しかしていないので、別途 VM の構築をしていきます。  
先ほどに続けてコマンドプロンプトで以下のコマンドを実行します。

```bash
vagrant ssh
```

そうすると VM に ssh でログインします。  
VM にログイン後、ユーザーを切り替えて必要なものをインストールします。  
コマンドは以下です。

```bash
sudo su
/vagrant/provisioning.sh
```

chef infra client により docker がインストールされ、 docker が使えるようになったと思います。
