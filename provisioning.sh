#!/usr/bin/env bash

set -e

# 補完してくれるやつ
if ! [[ $(rpm -qa | grep bash-completion) ]] ; then
    echo "  - dnf install bash-completion"
    sudo dnf install -y bash-completion
fi
