Flask front end for InjuryFX.

Dependencies:

Flask - pip install flask
Flask-wtf - pip install flask-wtf

To run on your local machine:  

python run.py
runs on local host:  127.0.0.1:5000

To run on an AWS EC2 instance with the UCB w205 AMI:

>> yum install httpd
>> yum install mod_wsgi

Put symbolic link to folder under /var/www/html/

(ensure that all points in path to folder have chmod o+x)

edit Apache configuration in /etc/httpd/conf/httpd.conf to add:

<VirtualHost *:80>

WSGIDaemonProcess site threads=5
WSGIScriptAlias / /var/www/html/site/site.wsgi

<Directory site>
    WSGIProcessGroup site
    WSGIApplicationGroup %{GLOBAL}
#    Order deny,allow
#    Allow from all
    Require all granted
</Directory>

</VirtualHost>

>> service httpd start
