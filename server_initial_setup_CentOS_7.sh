#!/usr/bin/env bash

function print_info {
        echo -n $1
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

sudo yum -y localinstall http://yum.postgresql.org/9.5/redhat/rhel-7-x86_64/pgdg-centos95-9.5-2.noarch.rpm
sudo yum list postgres*
sudo yum -y install postgresql95-server.x86_64 postgresql95-contrib.x86_64 postgresql95-libs.x86_64 
sudo /usr/pgsql-9.5/bin/postgresql95-setup initdb
sudo systemctl enable postgresql-9.5.service
sudo systemctl start postgresql-9.5.service 

#wget https://download.postgresql.org/pub/repos/yum/9.6/redhat/rhel-7-x86_64/pgdg-centos96-9.6-3.noarch.rpm
#sudo yum -y install pgdg-centos96-9.6-3.noarch.rpm epel-release
#sudo yum update
#sudo yum -y install postgresql96-server postgresql96-contrib
#sudo systemctl start postgresql-9.6
#sudo systemctl enable postgresql-9.6
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
GUNICORN_DIR="${HOME}/DjangoVideoPlayer//server_conf/gunicorn"
NGINX_DIR="/etc/nginx/sites-enabled"
SOURCE_DIR="${HOME}/DjangoVideoPlayer/server_conf"
APPLICATION_DB="djangovideoplayer"
DB_HOST="localhost"
DB_USER="djangovideoplayer_user"
DB_PASSWORD="f5j*kM@l"
POSTGRES_PASSWORD="postgres"


export DJANGO_SETTINGS_MODULE="videoplayer.settings.production"

function configure_postgresql {
    sudo -u postgres psql -c "ALTER USER postgres WITH PASSWORD '${POSTGRES_PASSWORD}';"
    export PGPASSWORD="${POSTGRES_PASSWORD}"; psql -U postgres -h localhost << EOF
    CREATE DATABASE ${APPLICATION_DB};
    CREATE USER "${DB_USER}" WITH PASSWORD '${DB_PASSWORD}';
    ALTER ROLE "${DB_USER}" SET default_transaction_isolation TO 'read committed';
    ALTER ROLE "${DB_USER}" SET timezone TO 'UTC';
    ALTER USER "${DB_USER}" WITH SUPERUSER;
    GRANT ALL PRIVILEGES ON DATABASE ${APPLICATION_DB} TO "${DB_USER}";

EOF
}


function configure_gunicorn {
    sudo sed --in-place "s'\${HOME}'$HOME'g" ${GUNICORN_DIR}/gunicorn.run
}

function configure_nginx {
    CONFIG_FILE="/etc/nginx/sites-enabled/nginx_videoplayer.conf"
    sudo cp -f ${SOURCE_DIR}/nginx_videoplayer.conf ${NGINX_DIR}
    sudo rm -rf /etc/nginx/sites-enabled/default
    sudo sed --in-place "s'\${HOME}'$HOME'g" ${NGINX_DIR}/nginx_videoplayer.conf
    
    print_info "Restarting Nginx..."
    sudo systemctl restart nginx
}

function configure_supervisor {
	CONFIG=${SOURCE_DIR}/supervisor_videoplayer.conf
	
	sudo cat "$CONFIG" >> "$SUPERVISOR_FILE"

	sudo sed --in-place "s'\${HOME}'$HOME'g" ${SUPERVISOR_FILE}
	sudo sed --in-place "s'\${USER}'$USER'g" ${SUPERVISOR_FILE}


	sudo supervisorctl reread
	print_info "Updating supervisor configuration files..."

	sudo supervisorctl restart all
	print_info "Restarting all supervisor programs ..."
}



print_info "Starting installation script..."

print_info "Updating apt packages ..."
sudo yum update

sleep 5

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
python manage.py collectstatic --no-input ---settings=videoplayer.settings.production

print_info "Restarting all services..."
sudo supervisorctl restart all
sudo systemctl start nginx
sudo systemctl enable nginx

