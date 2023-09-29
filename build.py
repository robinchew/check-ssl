from eluthia.decorators import chmod, copy_files, file, git_clone, empty_folder
from eluthia.defaults import control
from eluthia.functional import pipe
from eluthia.py_configs import deb822, cron

SUNDAY = 0
WEDNESDAY = 3

@chmod(0o644)
@file
def cron_file(full_path, package_name, apps):
    user = 'ubuntu'
    env_line = ' '.join(
        f"{k}='{v}'"
        for k, v in apps[package_name]['env'].items())

    command = env_line + " python3 /home/ubuntu/system/check_ssl/check_ssl.py"

    return cron([
        {'weekday': WEDNESDAY, 'user': user, 'command': command},
        {'weekday': SUNDAY, 'user': user, 'command': command},
    ])

def get_package_tree(package_name, apps):
    return {
        'DEBIAN': {
            'control': file(pipe(
                control,
                lambda d: {**d, 'Description': 'Check SSL of ciaobella.obsi.com.au periodically'},
                deb822)),
        },
        'home': {
            'ubuntu': {
                'system': {
                    'check_ssl': copy_files(apps[package_name]['_app_folder'], [
                        'check_ssl.py',
                    ]),
                }
            },
        },
        'etc': {
            'cron.d': {
                package_name: cron_file,
            }
        }
    }
