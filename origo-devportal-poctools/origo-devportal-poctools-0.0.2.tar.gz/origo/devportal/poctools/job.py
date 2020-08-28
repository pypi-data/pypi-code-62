import subprocess
import base64
import yaml

from .env import SECRETS, envVarToYaml


def encodeString(raw):
    return base64.b64encode(raw.encode('utf-8')).decode()


class Job(object):
    @classmethod
    def loadFile(cls, path, env):
        job_template = ''
        with open(path, 'r') as f:
            job_template = f.read()

        interpolated_template = subprocess.run(
            ['envsubst'],
            capture_output=True,
            env=env,
            input=job_template.encode('utf-8')
        )

        return cls(interpolated_template.stdout.decode(), env)

    def __init__(self, template, env):
        self.template = yaml.load(template, Loader=yaml.FullLoader)
        self.env = env
        self.required_environment_vars = list()

    @property
    def name(self):
        raise NotImplementedError

    @property
    def args(self):
        raise NotImplementedError

    def __str__(self):
        env = list()

        for item in self.required_environment_vars:
            env.append({
                'name': item,
                'value': self.env[item]
            })

        for item in SECRETS:
            if item in self.env:
                env.append({
                    'name': item,
                    'valueFrom': {
                        'secretKeyRef': {'name': f'{self.name}', 'key': envVarToYaml(item)}
                    }
                })

        computed_template = {**self.template}
        computed_template['metadata']['name'] = self.name
        computed_template['spec']['jobTemplate']['spec']['template']['spec']['containers'][0]['env'] = env
        computed_template['spec']['jobTemplate']['spec']['template']['spec']['containers'][0]['args'] = self.args

        return yaml.dump(computed_template)

    def generateSecret(self):
        secret = {
            'apiVersion': 'v1',
            'kind': 'Secret',
            'metadata': {'name': self.name},
            'type': 'Opaque',
            'data': dict()
        }

        for item in SECRETS:
            if item in self.env:
                secret['data'][envVarToYaml(item)] = encodeString(self.env[item])

        return yaml.dump(secret)


class HarvestJob(Job):
    def __init__(self, template, env):
        super().__init__(template, env)
        self.required_environment_vars = ['SOURCE_NAME', 'SOURCE_IDENTIFIER']

    @property
    def name(self):
        return '-'.join([
            'harvest',
            self.env['SOURCE_NAME'],
            self.env['STACK'],
            self.env['STACK_NAME']
        ])

    @property
    def args(self):
        return [
            '/bin/sh -c',
            f'python /app/{self.env["STACK"]}.py > /tmp/output.json',
            '&&',
            f'mv /tmp/output.json /data/dataservice/10_raw/{self.name}'
        ]


class DistributeJob(Job):
    def __init__(self, template, env):
        super().__init__(template, env)

    @property
    def name(self):
        return '-'.join([
            'distribute',
            self.env['STACK']
        ])

    @property
    def args(self):
        return [
            '/bin/sh -c',
            f'cat /data/dataservice/30_result/public.json | python {self.env["STACK"]}.py'
        ]

