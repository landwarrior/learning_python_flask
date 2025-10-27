# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure("2") do |config|
  config.vm.define "flask-app" do |flask_app|
    flask_app.vm.box = "bento/almalinux-8"
    flask_app.vm.hostname = "flask-app.local"
    flask_app.vm.network "private_network", ip: "192.168.33.33"

    flask_app.vm.provider "virtualbox" do |vb|
      vb.memory = "1024"
      vb.cpus = 1
    end

    # 初期設定
    flask_app.vm.provision "shell", inline: <<-SHELL
      sudo timedatectl set-timezone Asia/Tokyo
      sudo sed -i 's/SELINUX=enforcing/SELINUX=disabled/' /etc/selinux/config
    SHELL
  end
end
