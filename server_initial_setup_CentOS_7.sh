#!/usr/bin/env bash

function print_info {
        printf '\e[1;34m%-6s\e[m' $1 
}

function create_virtal_environment {
print_info "============CREATING VIRTUAL ENVIRONMENT=============="
python3.6 -m venv ${HOME}/.videoplayer
sleep 5
source ${HOME}/.videoplayer/bin/activate
}


function install_dependency_packages {
print_info "============INSTALLING DEPENDENCIES PACKAGES============"
sudo yum -y install wget
sudo yum  -y install epel-release
sudo yum -y install nginx
sudo yum -y install supervisor
sudo systemctl start supervisord
sudo systemctl enable supervisord
sudo yum -y install gdal gdal-devel 
sudo yum -y localinstall --nogpgcheck https://download1.rpmfusion.org/free/el/rpmfusion-free-release-7.noarch.rpm https://download1.rpmfusion.org/nonfree/el/rpmfusion-nonfree-release-7.noarch.rpm
sudo yum -y install ffmpeg ffmpeg-devel
}

function install_python {
print_info "============INSTALLING PYTHON AND IT'S PACKAGES============"
sudo yum -y update
sudo yum -y install yum-utils
sudo yum -y groupinstall development
sudo yum -y install https://centos7.iuscommunity.org/ius-release.rpm
sudo yum -y install python36u
sudo yum -y install python36u-pip
sudo yum -y install python36u-devel

}

PROJECT_ROOT="${HOME}/DjangoVideoPlayer/videoplayer"
SUPERVISOR_FILE="/etc/supervisord.conf"
GUNICORN_DIR="${HOME}/DjangoVideoPlayer/server_conf/gunicorn"
NGINX_DIR="/etc/nginx/nginx.conf"
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


function configure_gunicorn {
    sudo sed --in-place "s'\${HOME}'$HOME'g" ${GUNICORN_DIR}/gunicorn.run
}

function configure_nginx {
    sudo cp -f ${SOURCE_DIR}/nginx.conf ${NGINX_DIR}
    sudo rm -rf /etc/nginx/sites-enabled/default
    sudo rm -rf /etc/nginx/nginx.conf.default
    sudo sed --in-place "s'\${HOME}'$HOME'g" ${NGINX_DIR}/nginx.conf
    sudo sed --in-place "s'\${USER}'$USER'g" ${NGINX_DIR}/nginx.conf
    
    print_info "Restarting Nginx..."
    sudo systemctl restart nginx
}

function configure_supervisor {
	CONFIG=${SOURCE_DIR}/supervisord.conf

	sudo scp  ${CONFIG} /etc/

	sudo sed --in-place "s'\${HOME}'$HOME'g" ${SUPERVISOR_FILE}
	sudo sed --in-place "s'\${USER}'$USER'g" ${SUPERVISOR_FILE}


	sudo supervisorctl reread
	print_info "Updating supervisor configuration files..."

	sudo supervisorctl restart all
	print_info "Restarting all supervisor programs ..."
}



print_info "Starting installation script..."

print_info "Updating apt packages ..."
sudo yum -y update

sleep 5

print_info "Installing Postgres........."
install_postgresql

print_info "Installing Python "
install_python

sleep 5

print_info "Installing dependency packages..."
install_dependency_packages

print_info "Service stop"
sudo supervisorctl stop all

print_info "Installing virtual environment packages..."
create_virtal_environment 

pip install -r requirements.txt

sleep 5

print_info "Configuring gunicorn ..."
configure_gunicorn

sleep 5

print_info "Configuring postgreSQL..."
configure_postgresql

sleep 5

print_info "Configuring supervisor..."
configure_supervisor

sleep 5
		
print_info "Configuring Nginx..."
configure_nginx

print_info "Starting application configuration"
print_info "Migrating database changes.........................................."


cd ${PROJECT_ROOT}
python manage.py migrate --settings=videoplayer.settings.production


###execute this command after makemigration and migrate command
python manage.py createsuperuser --settings=videoplayer.settings.production

print_info "Running application collect static..."
python manage.py collectstatic --settings=videoplayer.settings.production

print_info "Restarting all services..."
sudo supervisorctl reread
sudo supervisorctl update
sudo systemctl start nginx
sudo systemctl enable nginx

sudo chown -R ${USER}:${USER} /home
sudo chmod -R ug+r /home

