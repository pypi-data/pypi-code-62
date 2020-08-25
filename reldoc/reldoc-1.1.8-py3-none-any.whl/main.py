# -*- coding: utf-8 -*-
import git
import re
import os
import argparse
import re


def print_head_and_body(prev, head, lines):
    GREEN = '\033[34m'
    END = '\033[0m'
    print(GREEN + prev + '..' + head + END)
    for line in lines:
        print(line)
    print('\n')


def generate_body(prev, head):
    root = get_git_root('./')
    repo_name = os.path.basename(root)
    repo = git.Repo(root)
    lines = []
    for item in repo.iter_commits(prev + '..' + head, min_parents=2):
        if ('Merged in' in item.message and 'pull request #' in item.message and 'Approved-by:' in item.message) or (
                'Merge pull request #' in item.message):
            message = item.message.splitlines()[2]
            result = re.search('#\d+', item.message.splitlines()[0])
            pullreq_no = result.group()[1:]
            author = item.author.name
            if 'Merged in' in item.message and 'pull request #' in item.message and 'Approved-by:' in item.message:
                lines.append(
                    '- [{0}](https://bitbucket.org/uzabase/{1}/pull-requests/{2}) @{3}'.format(message,
                                                                                               repo_name,
                                                                                               pullreq_no,
                                                                                               author))
            if 'Merge pull request #' in item.message:
                lines.append(
                    '- [{0}](https://github.com/newspicks/{1}/pull/{2}) @{3}'.format(message,
                                                                                     repo_name,
                                                                                     pullreq_no,
                                                                                     author))
    return lines


def get_git_root(path):
    git_repo = git.Repo(path, search_parent_directories=True)
    git_root = git_repo.git.rev_parse("--show-toplevel")
    return git_root


def main():
    parser = argparse.ArgumentParser(description='display commit message',
                                     usage='reldoc [--max-count=<num> | -m=<num>]')
    parser.add_argument('-m', '--max-count', action='store', help='maximum number of tags to display. default is 2')
    parser.add_argument('-i', '--ignore', action='store',
                        help='ignore prev-tags with argment(regex pattern). default is ".*_infra|.*_infra_hotfix"')
    args = parser.parse_args()
    max_count = 1 if args.max_count is None else int(args.max_count)
    pattern = re.compile('.*_infra|.*_infra_hotfix') if args.ignore is None else re.compile(args.ignore)

    g = git.Git('./')
    tags = g.execute(['git', 'tag', '--sort=-taggerdate']).splitlines()
    head = 'HEAD'
    print_head = 'HEAD'
    count = -1
    body = []
    for i, prev in enumerate(tags):
        body = body + generate_body(prev, head)
        head = prev
        if pattern is not None and re.fullmatch(pattern, prev):
            continue
        else:
            print_head_and_body(prev, print_head, body)
            print_head = prev
            body = []
            count += 1
            if count >= max_count - 1:
                break


if __name__ == '__main__':
    main()
