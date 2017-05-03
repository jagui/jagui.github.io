---
layout: post
title: Hosting Several Wordpress in a VPS
categories: hosting
tags: [ wordpress, VPS]
comments: true
---
# Configuring the VPS
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
Enable mod rewrite

```
sudo a2enmod rewrite
```

## VirtualHosts

TODO

# Configuring mysql

Install mysql server:
```
sudo apt-get install mysql-server
```

Then run mysql as root and add create databases, users and grant them permissions.

```
CREATE DATABASE 'dosancom_mydoctor';
CREATE USER 'dosancom_mydocto'@'localhost' IDENTIFIED BY 'password';
GRANT ALL PRIVILEGES ON `dosancom\_mydoctor`.* TO 'dosancom_mydocto'@'localhost' WITH GRANT 
OPTION;
```
 
# Configuring php
```
sudo apt-get install php5
sudo apt-get install php5-mysql
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
