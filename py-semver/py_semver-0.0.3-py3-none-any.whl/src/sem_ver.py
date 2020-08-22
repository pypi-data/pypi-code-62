#!/usr/bin/env python
import os
import re
import subprocess
import logging

logging.basicConfig(level=logging.WARNING)


def main():
    logging.debug("CWD %s", os.getcwd())
    latest_tag = get_latest_tag()
    if latest_tag is None:
        latest_tag = "v0.0.0"
        logging.debug("Defaulting to tag: %s", latest_tag)
        cmd_git_logs = ["git", "log", "--pretty=format:%s"]
    else:
        cmd_git_logs = ["git", "log", "--pretty=format:%s", f"{latest_tag}..HEAD"]

    commits = get_commits(cmd_git_logs)

    if commits is None:
        logging.error("Error can't find any commits")
        return

    major, minor, patch = parse_commits(commits)

    sem_ver = generate_next_tag(latest_tag, major, minor, patch)

    print(sem_ver)


def get_latest_tag():
    try:
        result = subprocess.check_output(['git', "describe", "--tags", "--abbrev=0"],
                                         stderr=subprocess.STDOUT).strip()
        latest_tag = result.decode('utf-8')
        logging.debug("Found latest tag: %s", latest_tag)
        return latest_tag
    except subprocess.CalledProcessError as e:
        logging.debug("No existing tags found.")
        logging.debug(e)


def parse_commits(commits):
    major = minor = patch = False

    for commit in commits:
        if "!:" in commit:
            major = True
            break

        if commit.startswith("feat:"):
            minor = True
        elif commit.startswith("fix:"):
            patch = True

    logging.debug("found major? %s, found minor? %s, found patch? %s", major, minor, patch)
    return major, minor, patch


def generate_next_tag(current_tag, found_major, found_minor, found_patch):
    regex = 'v?(?P<major>\d+)\.(?P<minor>\d+)\.(?P<patch>\d+)'
    matches = re.match(regex, current_tag)
    logging.debug("matches: %s", matches)
    if not matches:
        logging.error("%s is not a valid semantic version format. [v]1.0.1")
        exit(1)

    current_semver = {}
    current_semver.update(matches.groupdict())
    logging.debug("current_semver: %s", current_semver)

    if found_major:
        major = int(current_semver['major']) + 1
        minor = 0
        patch = 0
    elif found_minor:
        major = int(current_semver['major'])
        minor = int(current_semver['minor']) + 1
        patch = 0
    else:
        major = int(current_semver['major'])
        minor = int(current_semver['minor'])
        patch = int(current_semver['patch']) + 1

    new_semver = f"{major}.{minor}.{patch}"

    return new_semver


def get_commits(args):
    try:
        output = subprocess.check_output(args,
                                         stderr=subprocess.STDOUT).strip()
        commits = output.decode("utf-8").splitlines(keepends=False)
        logging.debug("Found commits: %s", commits)
        return commits

    except subprocess.CalledProcessError as e:
        logging.error(e)
        return None


if __name__ == '__main__':
    main()
