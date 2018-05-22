from fabric.contrib.files import append, exists, sed
from fabric.api import env, local, run
import random

REPOSITORY_URL = 'https://github.com/souzantero/super-to-do-lists-with-django.git'

def deploy():
    env.key_filename = '~/Cloud/Dropbox/technologies/aws/super-to-do-lists-with-django-aws-key-pair.pem'
    site_directory = f'/home/souzantero/sites/{env.host}'
    source_directory = site_directory + '/source'

    _create_directory_structure_if_necessary(site_directory)
    _get_latest_source(source_directory)
    _update_settings(source_directory, env.host)
    _update_virtualenv(source_directory)
    _update_static_files(source_directory)
    _update_database(source_directory)

def _create_directory_structure_if_necessary(site_directory):
    for subdirectory in ('database', 'static', 'virtualenv', 'source'):
        run(f'mkdir -p {site_directory}/{subdirectory}')

def _get_latest_source(source_directory):
    if exists(source_directory + '/.git'):
        run(f'cd {source_directory} && git fetch')
    else:
        run(f'git clone {REPOSITORY_URL} {source_directory}')

    current_commit = local("git log -n 1 --format=%H", capture=True)
    run(f'cd {source_directory} && git reset --hard {current_commit}')

def _update_settings(source_directory, site_name):
    settings_path = source_directory + '/app/settings.py'
    sed(settings_path, "DEBUG = True", "DEBUG = False")
    sed(settings_path, 'ALLOWED_HOSTS = .+$', f'ALLOWED_HOSTS = ["{site_name}"]')
    secrete_key_file = source_directory + '/app/secret_key.py'

    if not exists(secrete_key_file):
        chars = 'abcdefghijklmnopqrstuvwxyz0123456789!@#$%ˆ&*(-_=+)'
        key = ''.join(random.SystemRandom().choice(chars) for _ in range(50))
        append(secrete_key_file, f'SECRET_KEY = "{key}"')
    
    append(settings_path, '\nfrom .secret_key import SECRET_KEY')

def _update_virtualenv(source_directory):
    virtualenv_directory = source_directory + '/../virtualenv'
    
    if not exists(virtualenv_directory + '/bin/pip'):
        run(f'python3.6 -m venv {virtualenv_directory}')

    run(f'{virtualenv_directory}/bin/pip install -r {virtualenv_directory}/requirements.txt')

def _update_static_files(source_directory):
    run(
        f'cd {source_directory}'
        ' && ../virtualenv/bin/python manage.py collectstatic --noinput'
    )

def _update_database(source_directory):
    run(
        f'cd {source_directory}'
        ' && ../virtualenv/bin/python manage.py migrate --noinput'
    )