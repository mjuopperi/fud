from fabric.api import *
from fabric.contrib import django, files, console

django.project('fud')
server_root = '/home/fud/'
server_dir = server_root + 'server'
virtualenv_dir = server_root + 'env/'
virtualenv = virtualenv_dir + 'bin/activate'
conf_dir = server_dir + '/tools/deploy/conf/'
server_package = 'fud.tar.gz'

project_files = [
    'fud/',
    'restaurants/',
    'manage.py',
    'requirements.txt',
    'tools/deploy/conf/',
]
excluded_files = [
    'fud/lib/',
    'fud/settings/dev.py',
    'fud/settings/test.py',
    'fud/settings/travis.py',
    'fud/settings/secrets.py.example',
    'restaurants/static/src/',
    '__pycache__',
    '*.pyc',
]


def server_target():
    git_hash = local('git rev-parse --short HEAD', capture=True)
    return server_root + 'versions/server_{}'.format(git_hash)


def python_command(args):
    run('source {} && {}'.format(virtualenv, args))


def django_command(args):
    python_command('python manage.py {} --settings=fud.settings.prod'.format(args))


def init_dir(dir, clear=False):
    if not files.exists(dir):
        run('mkdir -p ' + dir)
    elif clear:
        if files.exists(dir):
            run('rm -rf ' + dir)
        run('mkdir -p ' + dir)


def create_link(source, target):
    if files.exists(target):
        run('rm -f ' + target)
    run('ln -s {} {}'.format(source, target))


def check_deployed_version():
    if files.exists(server_target()):
        return console.confirm('Current version is already deployed, continue anyway?')
    return True


def gulp():
    local('gulp clean && gulp build')


def pack():
    included = ' '.join(project_files)
    excluded = ' '.join(map(lambda file: '--exclude \'' + file + '\'', excluded_files))
    local('tar zcf {} {} {}'.format(server_package, excluded, included))


def send_files():
    put(server_package, server_root)


def unpack():
    init_dir(server_target(), clear=True)
    run('tar zxf {} -C {}'.format(server_root + server_package, server_target()))
    create_link(server_target(), server_dir)
    run('rm ' + server_root + server_package)


def create_virtualenv():
    init_dir(virtualenv_dir, clear=True)
    run('virtualenv -p python3 ' + virtualenv_dir)


def setup_server():
    create_virtualenv()
    with cd(server_dir):
        python_command('pip install -r requirements.txt --quiet')
        python_command('pip install gunicorn')
        django_command('migrate')
        django_command('collectstatic -v0 --noinput')
    sudo('mv {} {}'.format(conf_dir + 'fud.service', '/etc/systemd/system/'), shell=False)
    sudo('chmod 755 /etc/systemd/system/fud.service')
    sudo('mv {} {}'.format(conf_dir + 'nginx.conf', '/etc/nginx/'), shell=False)
    sudo('chown nginx:nginx /etc/nginx/nginx.conf', shell=False)
    sudo('chown nginx:nginx /etc/nginx/fud/*', shell=False)


def enable_service():
    sudo('systemctl restart fud', shell=False)
    sudo('systemctl enable fud', shell=False)
    sudo('systemctl restart nginx', shell=False)
    sudo('systemctl enable nginx', shell=False)


def clean():
    local('rm ' + server_package)


def deploy():
    if check_deployed_version():
        gulp()
        pack()
        send_files()
        unpack()
        setup_server()
        enable_service()
        clean()
