#!/bin/bash
secret_key=L1sGylot3UqsL0hA9UWv # Please set your own secret_key
host=anishare.com		# Please set your domain anishare will be available
user=user			# enter your linux username			
group=www-data			# www-data is the apache group. you don't need to edit this


sudo apt-get update
sudo apt-get install git python3 python3-dev python3-ldap python3-pip default-libmysqlclient-dev mysql-client ldap-utils libldap2-dev libsasl2-dev apache2 redis pipenv libapache2-mod-wsgi-py3 -y
cd /var/www/
git clone https://gitlab.leibniz-fli.de/fmonheim/animatch.git
mv animatch AniShare
cd AniShare
virtualenv ./
source bin/activate
pip install -r requirements.txt
sed -e 's/%SECRET_KEY%/'$secret_key'/' \
    -e 's/%HOST%/'$host'/'< anishare/local_settings.py.template > anishare/local_settings.py
python manage.py collectstatic
python manage.py makemigrations
python manage.py migrate
chmod 664 /var/www/AniShare/db/db.sqlite3
chmod g+w /var/www/AniShare/db
cd /var/www/
chown $user:$group AniShare -R
rm /etc/apache2/sites-enabled/000-default.conf
cp /var/www/AniShare/apache_conf.template /etc/apache2/sites-available/anishare.conf
ln -s /etc/apache2/sites-available/anishare.conf /etc/apache2/sites-enabled/anishare.conf
service apache2 restart
#sudo cp -a /etc/redis/default.conf.example /etc/redis/anishare.conf
#sudo chown root:redis  /etc/redis/anishare.conf
#sudo chmod u=rw,g=r,o=  /etc/redis/anishare.conf
#sudo install -d -o redis -g redis -m 0750 /var/lib/redis/anishare/
#systemctl start redis@anishare
