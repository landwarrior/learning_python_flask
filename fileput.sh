#!/usr/bin/env bash

rm -fr /var/app/flask/backend
rm -fr /var/app/flask/frontend

mkdir -p /var/app/flask/backend/logs
mkdir -p /var/app/flask/frontend/logs

cp -fr /vagrant/src/backend/* /var/app/flask/backend
cp -fr /vagrant/src/common/* /var/app/flask/backend
cp -fr /vagrant/src/frontend/* /var/app/flask/frontend
cp -fr /vagrant/src/common/* /var/app/flask/frontend
