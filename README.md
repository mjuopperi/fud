<div align="center">
  <img src="https://cloud.githubusercontent.com/assets/6764054/14056040/992bcfd8-f2ef-11e5-9f9d-83cc118fe830.png" alt="logo" width="400">
</div>

Development server setup [![Build Status](https://magnum.travis-ci.com/mjuopperi/fud.svg?token=vQUUTgeveVz3wPSNPQET&branch=master)](https://magnum.travis-ci.com/mjuopperi/fud)
========================

### Install dependencies

The local server uses a PostgreSQL database running inside a Ubuntu 14.04 virtual machine
configured by Vagrant and Ansible. VirtualBox is used by Vagrant to run the VM.

Install [VirtualBox](https://www.virtualbox.org/) and [Vagrant](https://www.vagrantup.com/)

##### Debian:
```
apt-get install virtualbox
apt-get install vagrant
```

##### Arch:
```
pacman -S virtualbox virtualbox-host-modules
pacman -S vagrant
```

You might have to install the `net-tools` package because virtualbox currently requires the older `ifconfig` etc. programs for setting up networks.

Use either `modprobe` to load the kernel modules below manually or create the file `/etc/modules-load.d/virtualbox.conf` and add the lines to it to have them available at boot.
```
vboxdrv
vboxnetadp
vboxnetflt
vboxpci
```

##### OS X using [Homebrew](http://brew.sh/):
```
brew cask install virtualbox
brew cask install vagrant
```

##### Or download the binaries:
* [VirtualBox](https://www.virtualbox.org/wiki/Downloads)
* [Vagrant](https://www.vagrantup.com/downloads.html)

Install [Ansible](https://github.com/ansible/ansible) 1.9

    pip install ansible

### Create virtualenv for python3

Install [virtualenv](https://virtualenv.pypa.io/en/latest/installation.html), [virtualenvwrapper](http://virtualenvwrapper.readthedocs.org/en/latest/install.html#basic-installation) and [psycopg2](http://initd.org/psycopg/docs/install.html).

Create a virtual env for the project

    mkvirtualenv --python=/usr/bin/python3 fud

or

    mkvirtualenv --python=`which python3` fud

Install python dependencies in project root

    pip install -r requirements.txt

### Install gulp

Install gulp globally to be able to use the `gulp` command anywhere

    npm install --global gulp

Install dependencies

    npm install

### Run the application

Start the virtual machine in project root

    vagrant up

Configure local database

    python manage.py migrate --settings=fud.settings.dev

Start gulp

    gulp

Start the server in development mode

    python manage.py runserver --settings=fud.settings.dev


## Running tests

Install [PhantomJS](http://phantomjs.org/) globally with npm

    npm -g install phantomjs-prebuilt

Run all tests

    py.test

Run a specific test

    py.test <path/to/python_file.py>::<SpecName>::<test_name>
