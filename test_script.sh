#!/usr/bin/env bash


PROJECT_ROOT="${HOME}/DjangoVideoPlayer/videoplayer"
SUPERVISOR_FILE="/etc/supervisord.conf"
GUNICORN_DIR="${HOME}/DjangoVideoPlayer/server_conf/gunicorn"
NGINX_DIR="/etc/nginx/sites-enabled"
SOURCE_DIR="${HOME}/DjangoVideoPlayer/server_conf"
APPLICATION_DB="djangovideoplayer"
DB_HOST="localhost"
DB_USER="djangovideoplayer_user"
DB_PASSWORD="f5j*kM@l"
POSTGRES_PASSWORD="postgres"


export DJANGO_SETTINGS_MODULE="videoplayer.settings.production"

function install_postgresql {
sudo yum update -y
sudo yum install -y epel-release
sudo rpm -ivh https://download.postgresql.org/pub/repos/yum/10/redhat/rhel-7-x86_64/pgdg-centos10-10-2.noarch.rpm
sudo yum install -y postgresql10-server postgis24_10 postgis24_10-client
sudo systemctl enable postgresql-10
sudo /usr/pgsql-10/bin/postgresql-10-setup initdb
sudo systemctl start postgresql-10
sudo sed -i "s'host    all             all             127.0.0.1/32            ident'host    all             all             127.0.0.1/32            trust'g" /var/lib/pgsql/10/data/pg_hba.conf
sudo systemctl restart postgresql-10
}




function configure_postgresql {
    export PGPASSWORD="${POSTGRES_PASSWORD}"; psql -U postgres -h 127.0.0.1 << EOF
    CREATE DATABASE ${APPLICATION_DB};
    CREATE USER "${DB_USER}" WITH PASSWORD '${DB_PASSWORD}';
    ALTER ROLE "${DB_USER}" SET default_transaction_isolation TO 'read committed';
    ALTER ROLE "${DB_USER}" SET timezone TO 'UTC';
    ALTER USER "${DB_USER}" WITH SUPERUSER;
    GRANT ALL PRIVILEGES ON DATABASE ${APPLICATION_DB} TO "${DB_USER}";
    \c ${APPLICATION_DB};
    CREATE EXTENSION postgis;

EOF
}

install_postgresql
configure_postgresql
