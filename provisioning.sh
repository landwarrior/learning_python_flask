#!/usr/bin/env bash

set -e

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
    curl -L https://omnitruck.chef.io/install.sh | sudo bash -s -- -v 18.3.0
fi

echo ""

SCRIPT_DIR=$(cd $(dirname $0);pwd)

# chef 実行
sudo echo yes | chef-client -z -c /vagrant/chef-repo/solo.rb -j /vagrant/chef-repo/nodes/flask_app.json
