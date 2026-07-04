#!/usr/bin/env bash

set -ex

rm -fr /var/app/flask/backend/*
rm -fr /var/app/flask/frontend/*
rm -fr /var/app/batch/*

mkdir -p /var/app/flask/backend/logs
mkdir -p /var/app/flask/frontend/logs
mkdir -p /var/app/batch

cp -fr /vagrant/src/backend/* /var/app/flask/backend
cp -fr /vagrant/src/common/* /var/app/flask/backend
cp -fr /vagrant/src/frontend/* /var/app/flask/frontend
cp -fr /vagrant/src/common/* /var/app/flask/frontend
cp -fr /vagrant/src/batch/* /var/app/batch
cp -fr /vagrant/src/common/* /var/app/batch

# ビルド用
rm -fr /var/app/build
mkdir -p /var/app/build
cp -fr /vagrant/docker /var/app/build/
cp -fr /vagrant/src /var/app/build/docker/backend
cp -fr /vagrant/src /var/app/build/docker/frontend
cp -fr /vagrant/src /var/app/build/docker/batch

# テスト用 (リポジトリの tests/backend/ を /var/app/flask/tests/ 直下へ配置)
rm -fr /var/app/flask/tests
mkdir -p /var/app/flask/tests
cp -fr /vagrant/tests/backend/* /var/app/flask/tests/
