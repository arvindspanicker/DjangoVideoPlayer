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

sudo yum -y install postgresql-server postgresql-contrib
sudo postgresql-setup initdb
sudo sed -i "s'host    all             all             127.0.0.1/32            ident'host    all             all             127.0.0.1/32            trust'g" /var/lib/pgsql/data/pg_hba.conf
sudo systemctl start postgresql
sudo systemctl enable postgresql

configure_postgresql
