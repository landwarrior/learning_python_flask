# install docker-ce
%w[
    yum-utils
].each do |pkg|
    dnf_package pkg do
        action :install
    end
end

execute 'add docker-ce.repo' do
    command "yum-config-manager --add-repo https://download.docker.com/linux/centos/docker-ce.repo"
    not_if do File.exist?("/etc/yum.repos.d/docker-ce.repo") end
end

%w[
    docker-ce
    docker-ce-cli
    containerd.io
    docker-buildx-plugin
    docker-compose-plugin
].each do |docker|
    dnf_package docker do
        options "--enablerepo=docker-ce-stable"
        action :install
    end
end

service 'docker' do
    action [:start, :enable]
end

# ディレクトリを作っても結局使ってない
%w[
    /var/app
    /var/app/docker
    /var/app/docker/backend
    /var/app/docker/frontend
    /var/app/docker/nginx
    /var/app/docker/batch
].each do |path|
    directory path do
        owner 'root'
        group 'root'
        mode '0755'
        action :create
    end
end
