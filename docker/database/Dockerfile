FROM mariadb:11.4

COPY init.sql /docker-entrypoint-initdb.d/init.sql
COPY logging.cnf /etc/mysql/conf.d/logging.cnf

RUN mkdir -p /var/log/mysql \
    && chown -R mysql:mysql /var/log/mysql
