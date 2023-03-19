# FLASK DATABASE APP

## Project Description
The aim of this repo is to act as a reference for deploying a database server that can be used with the
[flask framework](https://flask.palletsprojects.com/en/2.2.x/)
in python3.

## Table of Contents

1. [Setup database server](#setup-database-server)
   * [Install database software](#install-database-software)
   * [Setup database to listen to remote connections](#setup-database-to-listen-to-remote-connections)
   * [Set a password for the database user](#set-a-password-for-the-database-user)
   * [Firewall: Allow incoming database connections](#firewall--allow-incoming-database-connections)
2. [Test your database server connection](#test-your-database-server-connection)
   * [Using psql](#using-psql)
   * [Using GUI](#using-pgadmin)

## Setup database server
Before you can start building out a flask app, you will need a server that can be used as a database server. You may use
a spare laptop/computer that you may have lying around or you can rent one out via the numerous services available
online - [Linode](https://www.linode.com/), [AWS](https://aws.amazon.com/), 
[Google Cloud Platform](https://cloud.google.com/) etc.

Once you have a server that you can use, SSH into it. This repo uses a Ubuntu 20.04 LTS machine image.

The following needs to be setup on the server:
### Install database software
You may choose any database software of your liking such as MySQL, PostgreSQL, MS SQL Server etc.
For this repo, PostgreSQL is the choice of database.

To setup PostgreSQL on Ubuntu 20.04 you may use the guide: 
[How to Install PostgreSQL on Ubuntu 20.04](https://www.digitalocean.com/community/tutorials/how-to-install-postgresql-on-ubuntu-20-04-quickstart)

### Setup database to listen to remote connections
For PostgreSQL on Ubuntu 20.04 navigate to `/etc/postgresql/<version number>/main/` and edit the `postgresql.conf` file.
Look for the line:

`#listen_addresses='localhost'`

under the section 'CONNECTIONS AND AUTHENTICATION'

Change it to:

`listen_address = '*'`



By default, postgresql is set up to only listen for requests from the localhost. The argument `'*'` grants permission to
listen to all ip addresses.

Next, we need to grant access to all databases for all users with an encrypted password. To do this open file
`/etc/postgresql/<version number>/main/pg_hba.conf` and add the following:
```commandline
# TYPE    DATABASE    USER    ADDRESS    METHOD
  host    all     all     0.0.0.0/0    md5
```

### Set a password for the database user
By default, postgresql comes with a 'postgres' user. You can either create a new user and give it a password or you can
create a password for the default user and use it for your flask app. To assign a password to the default user SSH into
your server and enter the below commands:

```commandline
sudo -u postgres psql
```

You should now see the postgresql prompt that takes SQL queries. Then enter, making sure to substitute `'your_password'`
with a password of your choice:

```
ALTER USER postgres with encrypted password 'your_password';
```

For more details refer to [Install and Configure PostgreSQL](https://ubuntu.com/server/docs/databases-postgresql)

### Firewall: Allow incoming database connections

Next, your server needs to allow connections on the port where the database software is listening. For PostgreSQL
this port is 5432 be default. To allow connections to this port, SSH into your server as 'root' and then run the following command:

```commandline
sudo ufw allow 5432
```

```commandline
sudo ufw enable
```


## Test your database server connection

You can test either using the command line tool 
[psql](https://www.postgresql.org/docs/current/app-psql.html#:~:text=psql%20is%20a%20terminal%2Dbased,or%20from%20command%20line%20arguments.)
or using a GUI like [pgAdmin](https://www.pgadmin.org/) (for postgresql).

Power ON your server before running the below on your local machine:

### Using psql
Assuming that 'psql' is already installed on your local machine, run after making the necessary substitutions:

```commandline
psql -h <host ip addr> -p <remote port> -U <db-username> -W
```

On prompt, enter user password.

### Using GUI

Using [pgAdmin](https://www.pgadmin.org/):

1. Register new server
2. Under the 'General' tab assign the server a name (pgadmin will use that name to display your server connection)
3. Under the 'Connection' tab:
    - Enter host ip address
    - Port Number: 5432
    - Username
    - Password
    - Hit 'Save'

If you have followed along so far and have no errors when you test your connection (using psql or gui) then your
database server is ready for use with Flask.