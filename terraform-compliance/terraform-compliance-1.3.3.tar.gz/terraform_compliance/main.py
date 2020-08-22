import os
from argparse import ArgumentParser
from tempfile import mkdtemp
from git import Repo
from terraform_compliance import __app_name__, __version__
from terraform_compliance.common.readable_dir import ReadableDir
from terraform_compliance.common.readable_plan import ReadablePlan
from radish.main import main as call_radish
from radish.utils import console_write
from terraform_compliance.common.defaults import Defaults
from terraform_compliance.common.helper import python_version_check

#
# This is used to override some stuff that does not fit our needs within radish-bdd.
# Better not to touch anything here.
from terraform_compliance.extensions.override_radish_step import Step as StepOverride
from radish.stepmodel import Step
Step.run = StepOverride.run

from terraform_compliance.extensions.override_radish_hookerrors import handle_exception as handle_exception_override
from radish import errororacle
errororacle.handle_exception = handle_exception_override
##
#

if __version__ == "{{VERSION}}":
    __version__ = "\blocal development version"
print('{} v{} initiated\n'.format(__app_name__, Defaults().yellow(__version__)))


class ArgHandling(object):
    pass


def cli(arghandling=ArgHandling(), argparser=ArgumentParser(prog=__app_name__,
                                                            description='BDD Test Framework for Hashicorp terraform')):
    args = arghandling
    parser = argparser
    parser.add_argument('--terraform', '-t', dest='terraform_file', metavar='terraform_file', type=str, nargs='?',
                        help='The absolute path to the terraform executable.', required=False)
    parser.add_argument('--features', '-f', dest='features', metavar='feature directory', action=ReadableDir,
                        help='Directory (or git repository with "git:" prefix) consists of BDD features', required=True)
    parser.add_argument('--planfile', '-p', dest='plan_file', metavar='plan_file', action=ReadablePlan,
                        help='Plan output file generated by Terraform', required=True)
    parser.add_argument('--quit-early', '-q', dest='exit_on_failure', action='store_true',
                        help='Stops executing any more steps in a scenario on first failure.', required=False)
    parser.add_argument('--no-failure', '-n', dest='no_failure', action='store_true',
                        help='Skip all the tests that is failed, but giving proper failure message', required=False)
    parser.add_argument('--silent', '-S', dest='silence', action='store_true',
                        help='Do not output any scenarios, just write results or failures', required=False)
    parser.add_argument('--identity', '-i', dest='ssh_key', metavar='ssh private key', type=str, nargs='?',
                        help='SSH Private key that will be use on git authentication.', required=False)
    parser.add_argument('--debug', '-d', dest='debug', action='store_true', help='Turns on debugging mode', required=False)

    parser.add_argument('--version', '-v', action='version', version=__version__)

    _, radish_arguments = parser.parse_known_args(namespace=args)

    steps_directory = os.path.join(os.path.split(os.path.abspath(__file__))[0], 'steps')

    python_version_check()

    # SSH Key is given for git authentication
    ssh_cmd = {}
    if args.ssh_key:
        ssh_cmd = {'GIT_SSH_COMMAND': 'ssh -l {} -i {}'.format('git', args.ssh_key)}

    features_dir = '/'
    # A remote repository used here
    if args.features.startswith(('http', 'https', 'ssh')):
        # Default to master branch and full repository
        if args.features.endswith('.git'):
            features_git_repo = args.features
            features_git_branch = 'master'

        # Optionally allow for directory and branch
        elif '.git//' in args.features and '?ref=' in args.features:
            # Split on .git/
            features_git_list = args.features.split('.git/', 1)
            # Everything up to .git is the repository
            features_git_repo = features_git_list[0] + '.git'

            # Split the directory and branch ref
            features_git_list = features_git_list[1].split('?ref=', 1)
            features_dir = features_git_list[0]
            features_git_branch = features_git_list[1]

        else:  # invalid
            raise ValueError("Bad feature directory:" + args.features)

        # Clone repository
        args.features = mkdtemp()
        Repo.clone_from(url=features_git_repo, to_path=args.features, env=ssh_cmd, depth=1, branch=features_git_branch)

    features_directory = os.path.join(os.path.abspath(args.features) + features_dir)

    commands = ['radish',
                '--write-steps-once',
                features_directory,
                '--basedir', steps_directory,
                '--user-data=plan_file={}'.format(args.plan_file),
                '--user-data=exit_on_failure={}'.format(args.exit_on_failure),
                '--user-data=terraform_executable={}'.format(args.terraform_file),
                '--user-data=no_failure={}'.format(args.no_failure),
                '--user-data=silence_mode_enabled={}'.format(args.silence),
                '--user-data=debugging_mode_enabled={}'.format(args.debug),
                ]
    commands.extend(radish_arguments)

    console_write('{} {} {}{}'.format(Defaults().icon,
                                      Defaults().yellow('Features\t:'),
                                      features_directory,
                                       (' ({})'.format(features_git_repo) if 'features_git_repo' in locals() else '')))

    console_write('{} {} {}'.format(Defaults().icon,
                                    Defaults().green('Plan File\t:'),
                                    args.plan_file))

    if args.silence is True:
        console_write('{} Suppressing output enabled.'.format(Defaults().icon))
        commands.append('--formatter=dotter')

    if args.exit_on_failure is True:
        console_write('{} {}\t\t: Scenario executions will stop on first step {}.'.format(Defaults().info_icon,
                                                                                          Defaults().info_colour('INFO'),
                                                                                          Defaults().failure_colour('failure')))

    if args.no_failure is True:
        console_write('{} {}\t: {}ping all {} steps, exit code will always be {}.'.format(Defaults().warning_icon,
                                                                                          Defaults().warning_colour('WARNING'),
                                                                                          Defaults().skip_colour('SKIP'),
                                                                                          Defaults().failure_colour('failure'),
                                                                                          Defaults().info_colour(0)))

    if Defaults().interactive_mode is False:
        console_write('{} Running in non-interactive mode.'.format(Defaults().info_icon))

    if args.silence is False:
        console_write('\n{} Running tests. {}\n'.format(Defaults().icon,
                                                        Defaults().tada))

    try:
        result = call_radish(args=commands[1:])
    except IndexError as e:
        print(e)

    return result


if __name__ == '__main__':
    cli()
