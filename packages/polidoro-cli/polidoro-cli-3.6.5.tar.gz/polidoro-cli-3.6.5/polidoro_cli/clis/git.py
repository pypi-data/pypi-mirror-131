import os

from polidoro_argument import Command
from string import Template

from polidoro_cli import CLI


class Git(object):
    @staticmethod
    def _get_git_projects():
        for dir in os.listdir():
            if os.path.isdir(dir):
                os.chdir(dir)
                if os.path.exists('.git'):
                    yield dir
                os.chdir('..')

    @staticmethod
    @Command(
        help='Run "git COMMAND" in all git projects',
        aliases=['a']
    )
    def in_all(*_remainder):
        try:
            os.system('setterm -cursor off')
            command = ' '.join(_remainder)
            for dir in Git._get_git_projects():
                print(f'\x1b[KRunning "git {command}" in "{dir}"...', end='\r')
                out, _ = CLI.execute(f'git {command}', show_cmd=False, capture_output=True)
                print('\x1b[K', end='')
                if out:
                    print(dir)
                    print(out)
        finally:
            os.system('setterm -cursor on')

    @staticmethod
    @Command(
        help='Commit helper',
        aliases=['bc']
    )
    def build_commit(*args, **kwargs):
        template = '''$type($scope): $short'''

        types = dict(
            build='Build related changes',
            ci='CI related changes',
            chore='Build process or auxiliary tool changes',
            docs='Documentation only changes',
            feat='A new feature',
            fix='A bug fix',
            perf='A code change that improves performance',
            refactor='A code change that neither fixes a bug or adds a feature',
            revert='Reverting things',
            style='Markup, white-space, formatting, missing semi-colons...',
            test='Adding missing tests',
        )

        dict_types = {}
        for i, (_type, desc) in enumerate(types.items()):
            if i > 9:
                i = chr(ord('A') - 10 + i)
            print(f'{i} - {_type}: {desc}')
            dict_types[str(i)] = _type

        _type = input('Type: ')
        if _type is None:
            return

        _type = dict_types[_type.upper()]

        scope = input('Scope: ')
        if not scope:
            template = template.replace('($scope)', '')

        short = input('Short Description: ')

        long = input('Long Description: ')
        if long:
            template += '\n\n$long'

        commit_message = Template(template).safe_substitute(
            type=_type,
            scope=scope,
            short=short,
            long=long
        )

        CLI.execute(f'git commit -m "{commit_message}"')
