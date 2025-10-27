#!/usr/bin/env bash

set -e

# 補完してくれるやつ
if ! [[ $(rpm -qa | grep bash-completion) ]] ; then
    echo "  - dnf install bash-completion"
    dnf install -y bash-completion
fi

# firewalld 無効化
echo "  - disable and stop firewalld"
systemctl disable firewalld --now

# docker インストール
if ! [[ $(rpm -qa | grep docker) ]] ; then
    echo "  - install docker"
    dnf remove -y docker \
        docker-client \
        docker-client-latest \
        docker-common \
        docker-latest \
        docker-latest-logrotate \
        docker-logrotate \
        docker-engine \
        podman \
        runc
    dnf -y install dnf-plugins-core
    dnf config-manager --add-repo https://download.docker.com/linux/centos/docker-ce.repo
    dnf install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
    systemctl enable --now docker
else
    echo "  * skip installing docker"
fi

# mariadb インストール
if ! [[ $(rpm -qa | grep -i mariadb) ]] ; then
    echo "  - install mariadb"
    dnf module disable mariadb -y
    dnf -y install dnf-plugins-core
    # catコマンドでリポジトリファイルを作成
cat > /etc/yum.repos.d/mariadb.repo << 'EOF'
[mariadb]
name=MariaDB
baseurl=https://rpm.mariadb.org/11.4/rhel/$releasever/$basearch
gpgkey=https://rpm.mariadb.org/RPM-GPG-KEY-MariaDB
gpgcheck=1
repo_gpgcheck=1
module_hotfixes=1
enabled=1
EOF
    dnf clean all
    dnf makecache
    dnf install -y MariaDB-server MariaDB-client
    systemctl enable --now mariadb
else
    echo "  * skip installing mariadb"
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
    docker swarm init --advertise-addr 192.168.33.33
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
