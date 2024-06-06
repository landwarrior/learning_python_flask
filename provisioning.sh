#!/usr/bin/env bash

set -e

# タイムゾーンを日本にする
if ! [[ $(date | grep "JST") ]]; then
    echo "  - timedatectl set-timezone Asia/Tokyo"
    timedatectl set-timezone Asia/Tokyo
fi

# 補完してくれるやつ
if ! [[ $(rpm -qa | grep bash-completion) ]] ; then
    echo "  - dnf install bash-completion"
    sudo dnf install -y bash-completion
fi

# chef インストール
if [[ $(rpm -qa | grep chef) ]]; then
    echo "  * skip installing chef"
else
    echo "  - chef installing"
    curl -L https://omnitruck.chef.io/install.sh | sudo bash -s --
fi

echo ""

# なぜ用意したのか覚えていない
# SCRIPT_DIR=$(cd $(dirname $0);pwd)

# chef 実行
sudo echo yes | chef-client -z -c /vagrant/chef-repo/solo.rb -j /vagrant/chef-repo/nodes/flask_app.json

# file 配置
bash /vagrant/fileput.sh


# docker swarm init 実行 NOTE: Vagrantfile に記載された IP アドレスと同じものを指定する
if ! [[ $(docker node ls -q) ]]; then
    echo "  - docker swarm init"
    docker swarm init --advertise-addr 192.168.33.33
else
    echo "  * skip docker swarm init"
fi

# docker build
if ! docker images | grep -q frontend; then
    echo "  - docker build frontend"
    docker build -t frontend /vagrant/docker/frontend
fi

if ! docker images | grep -q backend; then
    echo "  - docker build backend"
    docker build -t backend /vagrant/docker/backend
fi

if ! docker images | grep -q batch; then
    echo "  - docker build batch"
    docker build -t batch /vagrant/docker/batch
fi

if ! docker images | grep -q mynginx; then
    echo "  - docker build mynginx"
    docker build -t mynginx /vagrant/docker/nginx
fi

# docker stack deploy
if ! docker stack ls | grep -q test; then
    docker stack deploy -c /vagrant/docker/docker-stack-local.yml test
fi
