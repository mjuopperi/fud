Development server setup
========================

### Install dependencies

The local server uses a PostgreSQL database running inside a Ubuntu 14.04 virtual machine
configured by Vagrant and Ansible. VirtualBox is used by Vagrant to run the VM.

Install [VirtualBox](https://www.virtualbox.org/) and [Vagrant](https://www.vagrantup.com/)

Debian:
```
    sudo apt-get install virtualbox
    sudo apt-get install vagrant
```

OS X using [Homebrew](http://brew.sh/):
```
    brew cask install virtualbox
    brew cask install vagrant
```

Or download the binaries:
* [VirtualBox](https://www.virtualbox.org/wiki/Downloads)
* [Vagrant](https://www.vagrantup.com/downloads.html)

Install [Ansible](https://github.com/ansible/ansible) 1.9

    pip install ansible

### Create virtualenv for python3

Install [virtualenv](https://virtualenv.pypa.io/en/latest/installation.html) and [virtualenvwrapper](http://virtualenvwrapper.readthedocs.org/en/latest/install.html#basic-installation).

Create a virtual env for the project

    mkvirtualenv --python=/usr/bin/python3 fud

or

    mkvirtualenv --python=`which python3` fud

Install python dependencies in project root

    pip install -r requirements.txt

### Run the application

Start the virtual machine in project root

    vagrant up

Configure local database

    python manage.py migrate --settings=fud.settings.dev

Start the server in development mode

    python manage.py runserver --settings=fud.settings.dev
