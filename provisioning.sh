#!/usr/bin/env bash

set -e

IP=$(ip -4 addr show dev enp0s8 | grep -oP '(?<=inet\s)\d+(\.\d+){3}')

# 補完してくれるやつ
if ! [[ $(rpm -qa | grep bash-completion) ]] ; then
    echo "  - dnf install bash-completion"
    dnf install -y bash-completion
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

# firewalld 無効化
echo "  - disable and stop firewalld"
systemctl disable firewalld --now
# docker と競合するパッケージを削除
if [[ $(rpm -qa | grep podman) ]]; then
    echo "  - remove podman packages"
    dnf remove -y podman
fi
if [[ $(rpm -qa | grep runc) ]]; then
    echo "  - remove runc packages"
    dnf remove -y runc
fi

# chef 実行
if [[ -f /vagrant/chef-repo/nodes/flask_app.json ]]; then
    sudo echo yes | chef-client -z -c /vagrant/chef-repo/solo.rb -j /vagrant/chef-repo/nodes/flask_app.json
else
    echo "  * skip chef-client"
fi
# file 配置
if [[ $(ls /vagrant/fileput.sh) ]]; then
    echo "  - fileput.sh"
    bash /vagrant/fileput.sh
fi


# docker swarm init 実行 NOTE: Vagrantfile に記載された IP アドレスと同じものを指定する
if docker node ls -q > /dev/null 2>&1; then
    echo "  * skip docker swarm init"
else
    echo "  - docker swarm init"
    docker swarm init --advertise-addr $IP
fi

# docker build
for image in frontend backend batch mynginx myfluentd; do
    if ! docker images --format "{{.Repository}}" | grep -q $image; then
        echo "  - docker build $image"
        docker build -t $image /vagrant/docker/$image
    else
        echo "  * skip docker build $image"
    fi
done

# docker stack deploy
if ! docker stack ls | grep -q test; then
    docker stack deploy -c /vagrant/docker/docker-stack-local.yml test
fi

# メモ書き
rm -f /etc/logrotate.d/fluentd
touch /etc/logrotate.d/fluentd
echo "/var/log/fluent/fluentd.log {" >> /etc/logrotate.d/fluentd
echo "    daily" >> /etc/logrotate.d/fluentd
echo "    rotate 30" >> /etc/logrotate.d/fluentd
echo "    compress" >> /etc/logrotate.d/fluentd
echo "    missingok" >> /etc/logrotate.d/fluentd
echo "    notifempty" >> /etc/logrotate.d/fluentd
echo "    copytruncate" >> /etc/logrotate.d/fluentd
echo "}" >> /etc/logrotate.d/fluentd
