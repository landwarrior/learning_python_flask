# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure("2") do |config|
  config.vm.define "flask-app" do |flask_app|
    flask_app.vm.box = "bento/almalinux-8"
    flask_app.vm.hostname = "flask-app.local"
    flask_app.vm.network "private_network", ip: "192.168.33.33"

    flask_app.vm.provider "virtualbox" do |vb|
      # Display the VirtualBox GUI when booting the machine
      vb.gui = true

      # Customize the amount of memory on the VM:
      vb.memory = "2048"
      vb.cpus = 2
    end
    flask_app.vm.provision "shell", inline: <<-SHELL
      # タイムゾーンを日本にする
      sudo timedatectl set-timezone Asia/Tokyo
    SHELL
  end

end
