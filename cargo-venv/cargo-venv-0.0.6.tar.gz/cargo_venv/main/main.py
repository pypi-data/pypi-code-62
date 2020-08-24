import os
import subprocess

import click

from constants import ROOT_DIR


def make_executable(path):
    mode = os.stat(path).st_mode
    mode |= (mode & 0o444) >> 2  # copy R bits to X
    os.chmod(path, mode)


@click.command('cli')
@click.argument('name')
def main(name):
    os.makedirs(name, exist_ok=True)
    os.makedirs(f'{name}/bin', exist_ok=True)

    venv_directory = f'{os.getcwd()}/{name}'
    shell = os.environ['SHELL']

    with open(f'{ROOT_DIR}/cargo_venv/main/templates/activate.fish', 'r') as fish_template:
        template_file = fish_template.read()

        with open(f'{name}/bin/activate.fish', 'w') as fish_activate:
            new_template = template_file.replace('%{VENV_NAME}%', name).replace('%{VENV_DIRECTORY}%',
                                                                                venv_directory)
            fish_activate.write(new_template)
            make_executable(f'{name}/bin/activate.fish')

    with open(f'{ROOT_DIR}/cargo_venv/main/templates/activate', 'r') as bash_template:
        template_file = bash_template.read()

        with open(f'{name}/bin/activate', 'w') as bash_activate:
            new_template = template_file.replace('%{VENV_NAME}%', name).replace('%{VENV_DIRECTORY}%',
                                                                                venv_directory)
            bash_activate.write(new_template)
            make_executable(f'{name}/bin/activate')

    with open(f'{ROOT_DIR}/cargo_venv/main/templates/activate.csh', 'r') as csh_template:
        template_file = csh_template.read()

        with open(f'{name}/bin/activate.csh', 'w') as csh_activate:
            new_template = template_file.replace('%{VENV_NAME}%', name).replace('%{VENV_DIRECTORY}%',
                                                                                venv_directory)
            csh_activate.write(new_template)
            make_executable(f'{name}/bin/activate.csh')

    commands = []
    if 'fish' in shell:
        commands += [f'. {name}/bin/activate.fish']
    elif 'csh' in shell:
        commands += [f'source {name}/bin/activate.csh']
    else:
        commands += [f'source {name}/bin/activate']

    rust_toolchain_file = f'{os.getcwd()}/rust-toolchain'

    if os.path.exists(rust_toolchain_file):
        with open(rust_toolchain_file, 'r') as toolchain_file:
            toolchain_version = toolchain_file.read().rstrip()
            # commands += [f'rustup toolchain install {toolchain_version}']
            commands += [f'curl https://sh.rustup.rs -sSf | sh -s -- -y --default-toolchain {toolchain_version}']
    else:
        commands += ['curl https://sh.rustup.rs -sSf | sh -s -- -y --default-toolchain stable']

    commands += ['deactivate']
    subprocess.run(' && '.join(commands), shell=True, executable=shell)


if __name__ == '__main__':
    main()
