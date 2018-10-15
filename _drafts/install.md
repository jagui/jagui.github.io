---
layout: post
title: Hosting Several Wordpress in a VPS
categories: hosting
tags: [ wordpress, VPS]
comments: true
---
# A migration from hosted to selfhosted on a VPS
As root, create a new user

```
# adduser juan
```

Add it to the sudo group

```
# gpasswd -a juan sudo
```
su juan

generate ssh-key pair on local machine

__keep the private key safe__

copy pub key and

```
chmod 700 .ssh
```

copy pub key to authorized_keys

```
chmod 600 .ssh/authorized_keys
```
Disable Root Login and password authentication in /etc/ssh/sshd_config

```
PermitRootLogin no
PasswordAuthentication no
```

# Configuring Apache

We're using Apache 2.4

List apache modules
 ```
 sudo apache2ctl -M | sort
 ```




Enable mod rewrite

```
sudo a2enmod rewrite
```

## VirtualHosts

Use `/etc/apache2/sites-available/000-default.conf` as a template

```
<VirtualHost *:80>
     # The ServerName directive sets the request scheme, hostname and port that
     # the server uses to identify itself. This is used when creating
     # redirection URLs. In the context of virtual hosts, the ServerName
     # specifies what hostname must appear in the request's Host: header to
     # match this virtual host. For the default virtual host (this file) this
     # value is not decisive as it is used as a last resort host regardless.
     # However, you must set it for any further virtual host explicitly.
     #ServerName www.example.com

     ServerAdmin tech@clinicasantamarta.com
     ServerName mydoctorinmadrid.com
     ServerAlias www.mydoctorinmadrid.com
     DocumentRoot /home/juan/web/mydoctorinmadrid.com/
     ErrorLog ${APACHE_LOG_DIR}/mydoctorinmadrid.error.log
     CustomLog ${APACHE_LOG_DIR}/mydoctorinmadrid.access.log combined

     <Directory /home/juan/web/mydoctorinmadrid.com/>

          # Configures what features are available in a particular directory
          # Indexes If a URL which maps to a directory is requested and there is no DirectoryIndex
          # will return a formatted listing of the directory. Disabled.

          Options -Indexes

          # Types of directives that are allowed in .htaccess files
          # When this directive is set to All, then any directive which has the .htaccess Context
          # is allowed in .htaccess files.

          AllowOverride All

          # Tests whether an authenticated user is authorized by an authorization provider
          # In this case access is allowed unconditionally.

          Require all granted

     </Directory>
</VirtualHost>

```

Enable site
```
sudo a2ensite mydoctorinmadrid.com.conf
```

Reload Apache
```
sudo service apache2 reload
```

Disable site
```
sudo a2dissite mydoctorinmadrid.com.conf

```

##### Disabling default virtual host

Modify the default VirtualHost to display a forbidden error.

```
<VirtualHost _default_:80>
       <Location />       
          Deny from all
          Options None
          ErrorDocument 403 Forbidden.
       </Location>
</VirtualHost>
```

#### Configuring SSL

https://www.digitalocean.com/community/tutorials/how-to-create-a-self-signed-ssl-certificate-for-apache-in-ubuntu-16-04


```
sudo openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout /etc/ssl/private/apache-selfsigned.key -out /etc/ssl/certs/apache-selfsigned.crt
```


```
<VirtualHost *:443>

  SSLEngine on
  SSLCertificateKeyFile etc/ssl.key/server.key
  SSLCertificateFile etc/ssl.crt/server.crt
```


# Configuring mysql

Install mysql server:
```
sudo apt-get install mysql-server
```

Then run mysql as root and add create databases, users and grant them permissions.

```
CREATE DATABASE 'dosancom_mydoctor';
CREATE USER 'dosancom_mydoctor'@'localhost' IDENTIFIED BY 'password';
GRANT ALL PRIVILEGES ON `dosancom\_mydoctor`.* TO 'dosancom_mydocto'@'localhost' WITH GRANT OPTION;
```
Import the database
```
mysql -u username -p database_name < file.sql
```

# Configuring php
```
sudo apt-get install php5
sudo apt-get install php5-mysql
```

## Default Charset

Starting on php 5.6, the default_charset is set to UTF-8, hence will always print a Content-Type response header set to UTF-8:
```
Content-Type: text/html; charset=UTF-8
```
-
This can be overriden by a custom php config value in the `.htaccess` file of the website, without touching the server's php.ini file
```
php_value default_charset " "
```
*Not if you're using fastcgi*

# Configuring phpmyadmin

https://www.digitalocean.com/community/tutorials/how-to-install-and-secure-phpmyadmin-on-ubuntu-12-04
http://stackoverflow.com/questions/2631269/how-to-secure-phpmyadmin


```
sudo apt-get install phpmyadmin apache2-utils
```

Edit `/etc/apache2/apache2.conf` and include the phpmyadmin config:

```
Include /etc/phpmyadmin/apache.conf
```


Change the alias to something not predictable by changing
```
Alias /phpmyadmin /usr/share/phpmyadmin
```
to
```
Alias /somethingnotpredictable
```

Restrict access to your IP by
```
<Directory /usr/share/phpmyadmin>
    Require all denied
    Require ip your_ip
```

Configure default vhost to listen in 443 and add SSL support

```
SSLEngine on
SSLCertificateKeyFile /etc/ssl/private/apache-selfsigned.key
SSLCertificateFile /etc/ssl/certs/apache-selfsigned.crt
```

Choose a strong password for the  phpmyadmin user

Force SSL Within PhpMyAdmin
sudo nano /etc/phpmyadmin/config.inc.php
$cfg['ForceSSL'] = true;

Restart apache
```
sudo service apache2 restart
```


# Configuring Wordpress
Add user to www-data (apache2) group

```
sudo usermod -a -G www-data juan
```

Then change the group of your files
```
sudo chown -R juan:www-data .
```

And grant write access to the group

```
sudo chmod -R g+w .
```

Allow accessing filesystem in `wp-config.php`

```
define('FS_METHOD','direct');¬
```
# Configuring Prestashop

mcrypt (for redsys)
```
sudo apt install php5-mcrypt
sudo php5enmod mcrypt
sudo service apache2 restart
```

php5-curl (for paypal) due to `Connect failed with fsockopen method`
```
sudo apt install php5-curl
sudo service apache2 restart
```

## Performance
http://doc.prestashop.com/display/PS16/System+Administrator+Guide

* Smarty Cache
  * Templates Compilation:  Recompile templates if the files have been updates
  * Caching Type: Filesystem
  * Cache: Yes
  * Clear Cache: Clear cache everytime something has been modified

* Optional features
  * Disable all

* CCC
  * __TODO__
  * Never enable all at once
  * Turn them on one by one and measure

* Ciphering
  * Use Rijndael with mcrypt lib. (you must install the Mcrypt extension)

* OPCache
  * http://php.net/manual/en/opcache.installation.php
  * __TODO__

* Images
  * __TODO__
  * upload images on display size
  * use comprespng.com

* Displayed blocks
  * __TODO__
  *  Use hotjar.com

 * Truncate big (useless) tables
```
TRUNCATE TABLE `ms_connections`;

TRUNCATE TABLE `ms_connections_page`;

TRUNCATE TABLE `ms_connections_source`;

TRUNCATE TABLE `ms_guest`;
```

* Truncate cart tables
```
TRUNCATE TABLE ms_cart_product;
TRUNCATE TABLE ms_cart;
TRUNCATE TABLE ms_cart_discount;
```

## Security
__TODO__

http://doc.prestashop.com/display/PS16/Making+your+PrestaShop+installation+more+secure



# Certificates

Create CSR

```
openssl req -new -newkey rsa:2048 -nodes -keyout yourdomain.key -out yourdomain.csr
```

Then install and configure as per above with the self signed.


# Performance

# Php and Apache
https://wiki.apache.org/httpd/php
https://www.linode.com/docs/web-servers/apache/install-php-fpm-and-apache-on-debian-8
http://blog.starcklin.com/2013/08/install-mod-fastcgi-and-php5-fpm-on-ubuntu/
http://stackoverflow.com/questions/30762854/specify-php-ini-file-per-vhost-with-fastcgi-php-fpm-configuration
http://stackoverflow.com/a/30824878/168435


I thought I may as-well post the whole process I took to configure fpm with pools, as @ChristianM mentioned, because I've not yet found a full explanation on how to do it.

The first part of this is mostly a copy of an AskUbuntu post: https://askubuntu.com/questions/378734/how-to-configure-apache-to-run-php-as-fastcgi-on-ubuntu-12-04-via-terminal/527227#comment905702_527227

The last part is how to configure pools, and get the vhost to use the relevent pool settings

Here it goes:

Install the apache mpm worker (Explanation of prefork/wroker and event at http://www.vps.net/blog/2013/04/08/apache-mpms-prefork-worker-and-event/):
```
sudo apt-get install apache2-mpm-worker
```

Install fastcgi and php5-fpm:
```
sudo apt-get install libapache2-mod-fastcgi php5-fpm
```

Now enable mods you need, and disable those you don't:

sudo a2dismod php5 mpm_prefork
sudo a2enmod actions fastcgi alias mpm_worker

Create the php5.fcgi file and give the webserver permission to use it.
```
mkdir /var/www/cgi-bin
touch /var/www/cgi-bin/php5.fcgi
chown -R www-data:www-data /var/www/cgi-bin
```
Create a global config for fastcgi


sudo nano /etc/apache2/mods-enabled/fastcgi.conf

paste in the following (we'll use a socket instead of IP address)

```
<IfModule mod_fastcgi.c>
  FastCgiIpcDir /var/lib/apache2/fastcgi

  # Creates the /php5.fcgi alias for the /var/www/cgi-bin/php5.fcgi
  Alias /php5.fcgi /var/www/cgi-bin/php5.fcgi

  # Activates a CGI script for a particular handler or content-type
  # Syntax: Action action-type cgi-script
  Action php5.fcgi /php5.fcgi

  #	Maps the filename extensions to the specified handler
  # Syntax: AddHandler handler-name extension [extension] ...
  AddHandler php5.fcgi .php

  FastCGIExternalServer /var/www/cgi-bin/php5.fcgi -socket /var/run/php5-fpm.sock -pass-header Authorization -idle-timeout 3600

  <Directory "/var/www/cgi-bin">
    Require all granted
  </Directory>
</IfModule>
```


Note: Ensure all configs follow the same new 'Require all granted'/'Require all denied' syntax ... Otherwise you'll feel the pain after restarting ...


Restart apache and fpm

sudo service apache2 restart && sudo service php5-fpm restart

This setup essentially creates a global fastcgi configuration for php, which uses the file /etc/php5/fpm/php.ini file.

If you have multiple vhosts, that are going to need different php configurations, continue with the example below

First, within the /etc/php5/fpm/pool.d dir, you will find the default www.conf file. Copy this, naming it something relevent:

sudo cp /etc/php5/fpm/pool.d/www.conf /etc/php5/fpm/pool.d/domain2.conf

Edit this file, changing the pool name:

[...]

[domain2]

[...]

And change name of the listen socket to something relevent:

[...]

listen = /var/run/php5-fpm-domain2.sock

[...]

Then copy the /usr/lib/cgi-bin/php5.fcgi file, again naming it something relevent:

cp /usr/lib/cgi-bin/php5.fcgi /usr/lib/cgi-bin/php5-domain2.fcgi

Now you're ready to add the mod_fastcgi module to the domain2 vhost. It's almost the same as the one described above, but notice the changes for 'Alias','FastCgiServer' and '-socket'

```
<VirtualHost *:80>
   ServerName domain2.com

   [...]

   <IfModule mod_fastcgi.c>
     AddHandler php5.fcgi .php
     Action php5.fcgi /php5.fcgi
     Alias /php5.fcgi /usr/lib/cgi-bin/php5-domain2.fcgi
     FastCgiExternalServer /usr/lib/cgi-bin/php5-domain2.fcgi -socket /var/run/php5-fpm-domain2.sock -pass-header Authorization -idle-timeout 3600
    <Directory /usr/lib/cgi-bin>
      Require all granted
    </Directory>
  </IfModule>

  [...]

</VirtualHost>
```

Test configuration

```
  apache2ctl configtest
```

Expect for `Syntax OK`



Restart apache and fpm

sudo service apache2 restart && sudo service php5-fpm restart



First, within the /etc/php5/fpm/pool.d dir, you will find the default www.conf file. Copy this, naming it something relevent:

sudo cp /etc/php5/fpm/pool.d/www.conf /etc/php5/fpm/pool.d/domain2.conf

Edit this file, changing the pool name:

[...]

[domain2]

[...]

And change name of the listen socket to something relevent:

[...]

listen = /var/run/php5-fpm-domain2.sock

[...]

Then copy the /usr/lib/cgi-bin/php5.fcgi file, again naming it something relevent:

cp /usr/lib/cgi-bin/php5.fcgi /usr/lib/cgi-bin/php5-domain2.fcgi

Now you're ready to add the mod_fastcgi module to the domain2 vhost. It's almost the same as the one described above, but notice the changes for 'Alias','FastCgiServer' and '-socket'

```
<VirtualHost *:80>
   ServerName domain2.com

   [...]

   <IfModule mod_fastcgi.c>
     AddHandler php5.fcgi .php
     Action php5.fcgi /php5.fcgi
     Alias /php5.fcgi /usr/lib/cgi-bin/php5-domain2.fcgi
     FastCgiExternalServer /usr/lib/cgi-bin/php5-domain2.fcgi -socket /var/run/php5-fpm-domain2.sock -pass-header Authorization -idle-timeout 3600
    <Directory /usr/lib/cgi-bin>
      Require all granted
    </Directory>
  </IfModule>

  [...]

</VirtualHost>
```

Restart apache and fpm

sudo service apache2 restart && sudo service php5-fpm restart

Now to test changes.

In your new /etc/php5/fpm/pool.d/domain2.conf file, add a php value change (I've chosen the session.name value):

[...]

php_admin_value[session.name] = 'DOMAIN2'

[...]

OR

```
php_value[default_charset] = " "
```

Now test the configuration before restarting fpm:

sudo php5-fpm -t

It will tell you if the configuration fails, but more importantly will tell you if your configuration is fine. Then you can go ahead and restart fpm:

sudo service php5-fpm restart

And finally, if you want to be super sure the php value has been set, create info.php within your site, and just add:

```
<?php
  phpinfo();
?>
```

Now to test changes.

In your new /etc/php5/fpm/pool.d/domain2.conf file, add a php value change (I've chosen the session.name value):
```
[...]
php_admin_value[session.name] = 'DOMAIN2'
[...]
```
Now test the configuration before restarting fpm:

`sudo php5-fpm -t`

It will tell you if the configuration fails, but more importantly will tell you if your configuration is fine. Then you can go ahead and restart fpm:

`sudo service php5-fpm restart`

And finally, if you want to be super sure the php value has been set, create info.php within your site, and just add:
```
<?php
  phpinfo();
?>
```

# Maintenance

Checking memory consumption

```
ps -eo size,pid,user,command | sort -k1 -rn | head -20 | awk '{ hr=$1/1024 ; printf("%13.6f Mb ",hr) } { for ( x=4 ; x<=NF ; x++ ) { printf("%s ",$x) } print "" }'
```


# Docker

`sudo docker run -h dosan-dev --user juan -it dosan /bin/bash`

`sudo docker run -h dosan-dev --user juan -v /home/juan/projects/moremadrid.com/:/home/juan/web/dodepecho.com -it dosan /bin/bash`

`sudo docker run -h dosan-dev --user juan \
--dns 127.0.0.1 --dns 8.8.8.8 \
-v /home/juan/projects/moremadrid.com/:/home/juan/web/dodepecho.com \
-v /home/juan/projects/vanilla.com/:/home/juan/web/vanilla.com \
-it dosan /bin/bash`

add `--dns 127.0.0.1` to avoid slow connections when the host has no network

`sudo docker run -h dosan-dev --user juan --dns 127.0.0.1 --dns 8.8.8.8 -v /home/juan/projects:/home/juan/web -it dosan /bin/bash`

# Memcached

Install on php5
```
sudo apt install php5-memcached memcached
sudo service memcached start
sudo service php5-fpm restart
```

Ensure it starts on boot
```
sudo update-rc.d memcached enable
sudo update-rc.d memcached defaults
```

# PHP7

* `apt-get install php5-cli php5-comon php5-cli -o Dpkg::Options::=--force-confmiss`


## FPM

`apt-get -y install libapache2-mod-fastcgi php7.0-fpm php7.0`

or

`apt-get -y install libapache2-mod-fastcgi php-fpm php php-mbstring php-xml php-gd php-mcrypt php-curl php-imap php-mysql -o Dpkg::Options::=--force-confmiss`

```
mkdir /var/www/cgi-bin
touch /var/www/cgi-bin/php7.fcgi
chown -R www-data:www-data /var/www/cgi-bin
```

edit `/etc/apache2/mods-enabled/fastcgi.conf`

```
<IfModule mod_fastcgi.c>
  FastCgiIpcDir /var/lib/apache2/fastcgi

  # Creates the /php7.fcgi alias for the /var/www/cgi-bin/php7.fcgi
  Alias /php7.fcgi /var/www/cgi-bin/php7.fcgi

  # Activates a CGI script for a particular handler or content-type
  # Syntax: Action action-type cgi-script
  Action php7.fcgi /php7.fcgi virtual

  #	Maps the filename extensions to the specified handler
  # Syntax: AddHandler handler-name extension [extension] ...
  AddHandler php7.fcgi .php

  FastCGIExternalServer /var/www/cgi-bin/php7.fcgi -socket /var/run/php/php7.0-fpm.sock -pass-header Authorization -idle-timeout 3600

  <Directory "/var/www/cgi-bin">
    Require all granted
  </Directory>
</IfModule>
```

no need to create `/var/www/cgi-bin/php7.fcgi` if we append `virtual` to the action line

This annoying thing

NOTICE: Not enabling PHP 7.0 FPM by default.
NOTICE: To enable PHP 7.0 FPM in Apache2 do:
NOTICE: a2enmod proxy_fcgi setenvif
NOTICE: a2enconf php7.0-fpm
NOTICE: You are seeing this message because you have apache2 package installed.

## http2
[on ubuntu](https://techwombat.com/enable-http2-apache-ubuntu-16-04/)
[on debian](https://http2.pro/doc/Apache)

```
sudo a2dismod mpm_prefork
sudo a2enmod mpm_event
sudo a2enmod http2
```
on vhost
`Protocols h2 h2c http/1.1`

## mysql

`sudo apt-get install php-mysql`


edit config `/etc/php/7.0/pfm/php.ini` and uncomment `;extension=php_mysqli.dll`

# XDEBUG

`sudo apt install php-xdebug`

Config on `/etc/php/7.0/mods-available/xdebug.ini`

```
zend_extension=xdebug.so
xdebug.remote_enable=1
# So that it doesn't collide with fastcgi port 9000
xdebug.remote_port=9001
xdebug.remote_connect_back=1
```
Then restart
`service php7.0-fpm restart`

# Prestashop specific

## MPDF

mbstring

```
sudo apt-get install php-mbstring
phpenmod mbstring
```

Enable mbstring in /etc/php/7.0/fpm/php.ini: `zend.multibyte = On`

## xml

`sudo apt-get install php-xml`

## GD

`sudo apt-get install php-gd`

## mcrypt

`sudo apt-get install php-mcrypt`

## curl

`sudo apt-get install php-curl`

## imap

`sudo apt-get install php-imap`

#mysql 5.7

https://dev.mysql.com/doc/mysql-apt-repo-quick-guide/en/#repo-qg-apt-replacing

### Let's encrypt

[Guide to certbot on debian stretch and apache](https://certbot.eff.org/lets-encrypt/debianstretch-apache)

- create the Certificates
`sudo certbot certonly --authenticator webroot --installer apache`

- configure apache virtual host
```
SSLEngine on
SSLCertificateFile /etc/letsencrypt/live/moremadrid.com/cert.pem
SSLCertificateKeyFile /etc/letsencrypt/live/moremadrid.com/privkey.pem
SSLCertificateChainFile /etc/letsencrypt/live/moremadrid.com/fullchain.pem
```
- reload apache

`systemctl reload apache2`

check the renewal will work
`certbot renew --dry-run`

Checklist
1. Crear certificados y configurar apache2
 `sudo certbot certonly --authenticator webroot --installer apache`
2. Config apache
```
SSLEngine on
SSLCertificateFile /etc/letsencrypt/live/moremadrid.com/cert.pem
SSLCertificateKeyFile /etc/letsencrypt/live/moremadrid.com/privkey.pem
SSLCertificateChainFile /etc/letsencrypt/live/moremadrid.com/fullchain.pem
```

2. Habilitar http2
  `Protocols h2 h2c http/1.1`
3. Revisar que carga con
  1. https://tools.keycdn.com/http2-test
  2. https://http2.pro/client
4. Configurar wordpress
5. Redirigir http
    `Redirect permanent / https://teslacoollab.com`
5. Añadir https version en google search console
6. Añadir https version en google analytics
7. Cambiar URLs en google ads
8. Revisar los errores en la consola
9. Qué pasa con amp






-[ ] clinicasantamarta.com - hecho, revisar errores
-[ ] dosanaudiovisuales.com - hecho, revisar errores
-[ ] herniasindolor.com - hecho, revisar errores
-[ ] teslacoollab.com - hecho, revisar errores
-[ ] urgenciasadomicilio.com  - hecho, revisar errores
-[ ] mydoctorinmadrid.com - hecho, revisar errores
-[ ] vamoscamino.com
-[ ] viajesdosan.com
-[ ] amp.urgenciasadomicilio.com
