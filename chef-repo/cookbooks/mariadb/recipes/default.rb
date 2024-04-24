# install MariaDB
package 'mariadb-server' do
    action :install
end

template '/etc/my.cnf.d/mariadb-server.cnf' do
    source 'mariadb-server.cnf.erb'
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
