from utils import pipeline, watcher
import click
import ruamel.yaml
import os
import time

class FrameGenerator():
    def __init__(self, location):
        self.yaml = ruamel.yaml
        self.location = location
        self.steps = [
            ('utils', 'utils'),
            ('.gitlab-ci', '.gitlab-ci.yml'),
            ('_gitlab-ci', '_gitlab-ci.yml'),
            ('cloudbuild', 'cloudbuild.yaml')
        ]

    def utils_generator(self, filepath):
        os.system('mkdir -p %s/%s' % (self.location, filepath))

        os.system('cp -r %s %s/%s/watcher.py' % (
            watcher.__file__, self.location, filepath))
        os.system('cp -r %s %s/%s/pipeline.py' % (
            pipeline.__file__, self.location, filepath))

        click.echo("\ncopying watcher.py to %s/%s/watcher.py..." % (self.location, filepath))
        click.echo("\ncopying pipeline.py to %s/%s/pipeline.py..." % (self.location, filepath))

    def main_ci_generator(self, filepath):
        content = """
            stages:
              - test
              - build
              - deploy-pipe
              - deploy

            variables:
              GITLAB_PERS_TOKEN:
              WORKCHAT_ID:
              WORKCHAT_TYPE:
              PIPE_NAME:
              PIPE_DESC:
              EXP_NAME:
              EXP_DESC:
              JOB_NAME:
              PIPE_VER_NAME:
              TRAIN_NODE_KEY:
              TRAIN_NODE_VAL:
              USE_GPU:
              IMG_NAME_1:
              LOCAL_SRC_1:
              IMAGE_REGISTRY: asia.gcr.io/warung-support
              COMPONENTS: |
                [
                  ["Component 1", "$IMAGE_REGISTRY/$IMG_NAME_1:$CI_COMMIT_REF_NAME"]
                ]

            include:
              - 'comp_1/_gitlab-ci.yaml'
        """

        ci_path = "%s/%s" % (self.location, filepath)
        with open(ci_path, 'w') as wfile:
            data = self.yaml.round_trip_load(content)
            self.yaml.round_trip_dump(
                data, wfile, indent=4,
                block_seq_indent=3)

        click.echo("\ncreating %s to %s/%s..." % (filepath, self.location, filepath))

    def comp_ci_generator(self, filepath):
        content = """
            comp_1_build:
              stage: build
              image: asia.gcr.io/warung-support/google-sdk:latest
              only:
                - master
              tags:
                - gke-ml
              script:
                - |
                  gcloud builds submit \\
                  --config comp_1/cloudbuild.yaml \\
                  --substitutions _IMAGE_TAG=$IMAGE_REGISTRY/$IMG_NAME_1:$CI_COMMIT_REF_NAME,\\
                  _LOCAL_SRC_1=$LOCAL_SRC_1

            comp_1_kubepipe:
              stage: deploy-pipe
              image: asia.gcr.io/warung-support/google-sdk:latest
              only:
                - master
              tags:
                - gke-ml
              before_script:
                - kubectl version --client
                - apk add python3-dev
                - apk add py3-pip
                - pip3 install requests
                - pip3 install kfp --upgrade
                - export PATH=$PATH:~/.local/bin
                - which dsl-compile
              script:
                - python3 -m utils.pipeline
        """

        directory = "%s/comp_1" % self.location
        if not os.path.exists(directory):
            os.makedirs(directory)

        ci_path = "%s/%s" % (directory, filepath)
        with open(ci_path, 'w') as wfile:
            data = self.yaml.round_trip_load(content)
            self.yaml.round_trip_dump(
                data, wfile, indent=4,
                block_seq_indent=3)

        click.echo("\ncreating %s to %s/%s..." % (filepath, directory, filepath))

    def cloudbuild_generator(self, filepath):
        content = """
            steps:
              - name: 'gcr.io/cloud-builders/docker'
                args: ['build', '-t', '${_IMAGE_TAG}', '${_LOCAL_SRC_1}']
            substitutions:
                _IMAGE_TAG: IMAGE_TAG
                _LOCAL_SRC_1: LOCAL_SRC_1
            images:
              - '${_IMAGE_TAG}'
        """

        directory = "%s/comp_1" % self.location
        if not os.path.exists(directory):
            os.makedirs(directory)

        ci_path = "%s/%s" % (directory, filepath)
        with open(ci_path, 'w') as wfile:
            data = self.yaml.round_trip_load(content)
            self.yaml.round_trip_dump(
                data, wfile, indent=4,
                block_seq_indent=3)

        click.echo("\ncreating %s to %s/%s..." % (filepath, directory, filepath))

    def main(self, step, filepath):
        if step == 'utils':
            self.utils_generator(filepath)
        elif step == 'pipeline':
            self.pipeline_generator(filepath)
        elif step == '.gitlab-ci':
            self.main_ci_generator(filepath)
        elif step == '_gitlab-ci':
            self.comp_ci_generator(filepath)
        elif step == 'cloudbuild':
            self.cloudbuild_generator(filepath)

@click.command()
@click.option('--location', required=True, help='Path of framework will be generated')
def main(location):
    gen = FrameGenerator(location)

    with click.progressbar(gen.steps, bar_template='%(label)s [%(bar)s] %(info)s',
                           label='Generate framework to %s' % location) as bar:
        for step, filepath in bar:
            time.sleep(0.5)
            gen.main(step, filepath)

if __name__ == '__main__':
    main(prog_name='kubextract')
