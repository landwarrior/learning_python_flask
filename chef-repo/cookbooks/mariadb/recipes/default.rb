# Add MariaDB official repository for RockyLinux 9 (RHEL 9 compatible)
yum_repository 'MariaDB' do
    description 'MariaDB Repository'
    baseurl 'http://yum.mariadb.org/12.0/rhel8-amd64'
    gpgkey 'https://yum.mariadb.org/RPM-GPG-KEY-MariaDB'
    gpgcheck true
    enabled true
    action :create
end

# install MariaDB 12.0.2
package 'MariaDB-server' do
    action :install
end

template '/etc/my.cnf.d/server.cnf' do
    source 'server.cnf.erb'
    owner 'root'
    group 'root'
    mode '0644'
    action :create
end

template '/etc/my.cnf.d/client.cnf' do
    source 'client.cnf.erb'
    owner 'root'
    group 'root'
    mode '0644'
    action :create
end

# create directory
%w[
    /var/log/mysql
    /run/mariadb
].each do |path|
    directory path do
        owner 'root'
        group 'root'
        mode '0777'
        action :create
    end
end

service 'mariadb' do
    action [:enable, :start]
end

# set up MariaDB
execute 'create database if not exists mydb' do
    command 'mysql -uroot -e"create database if not exists mydb"'
end
cookbook_file "/#{Chef::Config[:file_cache_path]}/init.sql" do
    source 'init.sql'
    mode 0644
    owner 'root'
    group 'root'
    action :create
end
execute 'initializing mydb' do
    command "mysql -uroot -Dmydb < #{Chef::Config[:file_cache_path]}/init.sql"
end
