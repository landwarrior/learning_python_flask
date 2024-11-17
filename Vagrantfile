# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure("2") do |config|
  config.vm.box = "bento/almalinux-8"
  config.vm.hostname = "flask-app.local"
  config.vm.network "private_network", ip: "192.168.33.33"

  config.vm.provider "virtualbox" do |vb|
  #   # Display the VirtualBox GUI when booting the machine
  #   vb.gui = true
  #
    # Customize the amount of memory on the VM:
    vb.memory = "2048"
    vb.cpus = 2
  end

  config.vm.provision "shell", inline: <<-SHELL
    # タイムゾーンを日本にする
    timedatectl set-timezone Asia/Tokyo
  SHELL
end
