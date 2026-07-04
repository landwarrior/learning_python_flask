#!/usr/bin/env bash

set -e

if command -v ansible-playbook &>/dev/null; then
    echo "  * skip installing ansible-core"
else
    echo "  - dnf install ansible-core"
    dnf install -y ansible-core
fi

echo ""
echo "  - ansible-playbook"
ANSIBLE_CONFIG=/vagrant/ansible/ansible.cfg \
    ansible-playbook -v /vagrant/ansible/site.yml
