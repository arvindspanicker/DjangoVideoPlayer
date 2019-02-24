# DjangoVideoPlayer
## A video player using django, jquery, plyr.js, nginx, gunicorn and supervisor

## Installation Steps:
### For CentOs 7
**Please note that if there are any exisiting applications, the installation of this might corrupt the database, nginx services or supervisor**
**Also note that the SE of Centos needs to be disabled and also incoming traffic should be allowed**

### How to Disable SE of CentOS - [Disable SE on CentOS 7](https://linuxize.com/post/how-to-disable-selinux-on-centos-7/)
### Allow IP tables Incoming Traffic 
**This should be done on every restart**
- iptables -I INPUT -j ACCEPT
- iptables -F
#### Script Installation
**Note : The user should have sudo permission and the script should not be executed from root for permission rights**
- git clone the repository to the home  (~/)
- cd ~/DjangoVideoPlayer
- ./server_initial_setup_CentOS_7.sh

### Manual Installation
**Note - Use in case where already posgres or other dependencies needed are installed.**
### Git clone
- git clone the repository to home (~/)

#### Install python 3 (Ignore if already present) - Check by typing python3 on terminal to see if it exists
- sudo yum -y update 
- sudo yum -y install yum-utils
- sudo yum -y groupinstall development
- sudo yum -y install https://centos7.iuscommunity.org/ius-release.rpm
- sudo yum -y install python36u
- sudo yum -y install python36u-pip
- sudo yum -y install python36u-devel


#### Install Postgres (Ignore if installed) 
- sudo yum install -y epel-release
- sudo rpm -ivh https://download.postgresql.org/pub/repos/yum/10/redhat/rhel-7-x86_64/pgdg-centos10-10-2.noarch.rpm
- sudo yum install -y postgresql10-server postgis24_10 postgis24_10-client
- sudo systemctl enable postgresql-10
- sudo /usr/pgsql-10/bin/postgresql-10-setup initdb
- sudo systemctl start postgresql-10
**The below step to change ident authentication to trust for localhost is done so that the application can access the database**
- sudo sed -i "s'host    all             all             127.0.0.1/32            ident'host    all             all             127.0.0.1/32            - trust'g" /var/lib/pgsql/10/data/pg_hba.conf
- sudo systemctl restart postgresql-10


#### Install Other Dependency Packages (Ignore each installation based on what is already installed)
-**wget**
- sudo yum -y install wget
-**nginx**
- sudo yum  -y install epel-release
- sudo yum -y install nginx
-**supervisor**
- sudo yum -y install supervisor
- sudo systemctl start supervisord
- sudo systemctl enable supervisord

-**other dependencies**
- sudo yum -y install gdal gdal-devel 
- sudo yum -y localinstall --nogpgcheck https://download1.rpmfusion.org/free/el/rpmfusion-free-release-7.noarch.rpm https://download1.rpmfusion.org/nonfree/el/rpmfusion-nonfree-release-7.noarch.rpm
- sudo yum -y install ffmpeg ffmpeg-devel


#### Create Virutal Environment and Install Requirements.txt
**Note - here ${HOME} denotes the home directory (~/)**
python3.6 -m venv ${HOME}/.videoplayer
source ${HOME}/.videoplayer/bin/activate
pip install -r requirements.txt


#### Configuring Gunicorn
- In the server_conf/gunicorn/ folder of the repo, replace all '${HOME}' to current home directory

#### Configuring Postgres 
- Get into the database using the command **sudo su - postgres** 
- Then **type psql**
- Now create a database called 'djangovideoplayer' using the command **CREATE DATABASE djangovideoplayer;**
- Now create a user called 'djangovideoplayer_user' using the command CREATE USER djangovideoplayer_user WITH PASSWORD 'f5j*kM@l';
**Note the password should match the password in**
- ALTER ROLE djangovideoplayer_user SET default_transaction_isolation TO 'read committed';
- ALTER ROLE djangovideoplayer_user SET timezone TO 'UTC';
- ALTER USER djangovideoplayer_user WITH SUPERUSER;
- GRANT ALL PRIVILEGES ON DATABASE djangovideoplayer TO djangovideoplayer_user;
- \c djangovideoplayer;
- CREATE EXTENSION postgis;
- Now exit from the postgres by presseing Cntrl + D 


#### Configuring Supervisor
- Go to server_conf folder inside the cloned repo
- Replace all '${HOME}' and '${USER}' with the current home directoy and user
- If there is super visor already existing in the database, do the following
  * Copy the below code:
  *     [program:videoplayer]
	command = ${HOME}/DjangoVideoPlayer/server_conf/gunicorn/gunicorn.run
	user = ${USER}
	stdout_logfile = ${HOME}/DjangoVideoPlayer/videoplayer/log/gunicorn_supervisor.log
	redirect_stderr = true
	enviornment=LANG=en_US.UTF-8,LC_ALL=en_US.UTF-8
  * Paste this in the conf folder that you have specified in /etc/supervisor.conf (under the [include] tag)
  * If there is no folder under include tag, then add or change the line  **files=conf.d/*.conf** and create a folder conf 
    if it doesn't exist in '/etc/supervisor/' folder
- If there is no supervisor existing, replace the supervisor.conf file in the /etc/ folder by this file
- Run the command ** sudo supervisorctl reread **  followed by ** sudo supervisorctl update **

#### Configuring Nginx
- If nginx is not configured in your system , add the file 'nginx.conf' from server_conf/ in the repo to the directory
  '/etc/nginx/' after replacing all the '${HOME}' and '${USER}' with the current home directoy and user.
- If nginx is configured, copy the server{} part of the server_conf/nginx.conf and create a new file in the conf file specified
  in the '/etc/nginx/nginx.conf' you pre configured and put the contens of the server {} to that file after replacing
  all the '${HOME}' and '${USER}' with the current home directoy and user.
- Now set user permission to all nginx related files
- Run the following commands - Replace ${USER} with Current User.
 * sudo chown -R ${USER}:${USER} /home
 * sudo chmod -R ug+r /home
 * sudo chown -R ${USER}:${USER} /var/log/nginx
 * sudo chown -R ${USER}:${USER} /etc/nginx
 * sudo chown -R ${USER}:${USER}  /var/lib/nginx
- Run the command **sudo systemctl start nginx** and if any error pops up, your nginx configuration was not set up correctly.

#### Migrations, SuperUser and Static Files
- Run the following commands inside the directory ~/DjangoVideoPlayer/videoplayer
- python manage.py migrate --settings=videoplayer.settings.production
- python manage.py createsuperuser --settings=videoplayer.settings.production
- **Note the above command will prompt a super user creation - with this details only you can log in initially**
- python manage.py collectstatic --settings=videoplayer.settings.production
- sudo scp -r ${PROJECT_ROOT}/videoplayer/staticserve/*  ${PROJECT_ROOT}/videoplayer/static/ 

#### Restart services and Enable servies to be run on system restart
- sudo supervisorctl restart all
- su - 
- sudo systemctl restart nginx
- sudo systemctl enable nginx


## Application Usage:
- **Acces the application by typing the system IP address on browser**
- **Log in using the super user credentials**
- **Access admin panel of the application by typine the IPAdress followed by '/admin'**


## Features of Application:
- **Dedicated Admin panel to manage everything on the application**
- **Able to upload and play videos**
- **Has thumbnails of various intervals of video to skip to**
- **Ability to load private videos**

**Please note that there is no encryption of the video files, users can simply download them**

## Pending Features
- **Delete option in front-end ( Only available right now in admin page )**
- **Search option in front-end (Only available right now in admin page)**
- **Celery configuration for heavy tasks to run in background automatically**

