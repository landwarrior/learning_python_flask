# dnf-plugins-core のインストール
package 'dnf-plugins-core' do
    action :install
end

execute 'add docker-ce.repo' do
    command "dnf config-manager --add-repo https://download.docker.com/linux/centos/docker-ce.repo"
    not_if { File.exist?("/etc/yum.repos.d/docker-ce.repo") }
end

# パッケージキャッシュを更新
execute 'update package cache' do
    command 'dnf makecache'
    action :run
end

# Dockerパッケージのインストール（最新バージョンをインストールする）
%w[
    docker-ce
    docker-ce-cli
    containerd.io
    docker-buildx-plugin
    docker-compose-plugin
].each do |docker|
    dnf_package docker do
        # enablerepo を書かないと、初回実行がうまくいかないので書いておく
        options "--enablerepo=docker-ce-stable"
        action :install
    end
end

# Dockerサービスの起動
service 'docker' do
    action [:start, :enable]
end

%w[
    /var/log/fluent
].each do |path|
    directory path do
        owner 'root'
        group 'root'
        mode '0777'
        action :create
    end
end
