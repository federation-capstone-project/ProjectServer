#!/usr/bin/env python3

# If you're reading this it probably failed, hopefully you're familiar
# with linux system administration, otherwise good luck, this was tested
# against a bone stock ubuntu server 18.04 install, you can do the steps
# manually and adapt them if you need any other distro, you shouldn't need
# help if you're elite enough to have distro preferences. This was mostly
# written at 1am.
#   - Nine

import os
import sys

#
# check if we have root
#

if not os.geteuid() == 0:
    sys.exit("\nPlease try again as root.\n")

#
# installconfig
#

domain = input("enter the server domain:")
ip = input("enter the server ip:")
path = os.path.dirname(os.path.realpath(__file__))
installdir = "/var/www/html/capstoneserver"

#
# configure unix system
#

# install the dependencies
os.system("apt update && apt install -y python3-pip nginx")
os.system("pip3 install -r {}/requirements.txt".format(path))

# create a django user and add him to www-data group
os.system("adduser --system --ingroup www-data django")

# make a new directory in /var/www/html/ and assign it to the www-data group
os.system("mkdir -p {}".format(installdir))

# copy the app in there
os.system("cp -r {}/* {}".format(path, installdir))

# change the owner
os.system("chown -R :www-data {}".format(installdir))

# install systemd unit file
with open(installdir+"/unix_configs/systemd_template", "r") as template:
    with open(installdir+"/unix_configs/systemd", "w+") as config:
        config.write(template.read().format(installdir))

os.system("ln -s {} /etc/systemd/system/projectserver.service".format(os.path.join(installdir, "unix_configs/systemd")))
os.system("systemctl enable projectserver && systemctl start projectserver")

# install nginx configuration
with open(installdir+"/unix_configs/nginx_template", "r") as template:
    with open(installdir+"/unix_configs/nginx", "w+") as config:
        config.write(template.read().format(domain, installdir, installdir))

os.system("ln -s {} /etc/nginx/sites-available/projectserver".format(os.path.join(installdir, "unix_configs/nginx")))
os.system("ln -s {} /etc/nginx/sites-enabled/projectserver".format(os.path.join(installdir, "unix_configs/nginx")))
os.system("rm /etc/nginx/sites-enabled/default")
os.system("systemctl enable nginx && systemctl start nginx")

#
# configure the app
#

os.system("cd {}".format(installdir))

#generate a new secret key
os.system('python3 manage.py generate_secret_key --replace')

#add server to allowed hosts
os.system("rm hosts.txt")
with open(os.path.join(installdir, 'hosts.txt'), "w+") as f:
    f.write("{}\n{}".format(domain, ip))

# set up static files
os.system("python3 manage.py collectstatic")

# init database and add admin account
os.system('python3 manage.py makemigrations jsonapi')
os.system('python3 manage.py migrate')
os.system('python3 manage.py createsuperuser --username administrator --email ""')

print("\nInstall possibly complete, have a wonderful day! :D")
