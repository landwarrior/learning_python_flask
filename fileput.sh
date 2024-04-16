#!/usr/bin/env bash

rm -fr /var/app/flask/backend
rm -fr /var/app/flask/frontend

mkdir -p /var/app/flask/backend
mkdir -p /var/app/flask/frontend

cp -fr /vagrant/src/backend/* /var/app/flask/backend
cp -fr /vagrant/src/frontend/* /var/app/flask/frontend
