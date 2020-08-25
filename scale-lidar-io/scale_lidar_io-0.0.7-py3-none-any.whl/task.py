import os

import numpy as np
import requests
import ujson
from scaleapi import ScaleClient, Task

from .scene import LidarScene


def parse_xyz(obj):
    return np.array([obj['x'], obj['y'], obj['z']])


def parse_cuboid_frame(frame):
    return np.array([parse_xyz(p) for p in [c['position'] for c in frame['cuboids']]])


def read_cuboid_points(filename):
    # Read from result file
    with open(filename, 'r') as json_file:
        return np.array([parse_cuboid_frame(frame) for frame in ujson.load(json_file)])


def get_api_client() -> ScaleClient:
    assert os.getenv('SCALE_API_KEY'), 'No API key, please set SCALE_API_KEY environment variable'
    return ScaleClient(os.getenv('SCALE_API_KEY'))


def get_default_template():
    return {
        'task_id': None,
        'callback_url': 'http://example.com',
        'instruction': 'Please label all objects',
        'labels': [
            'Object'
        ],
        'meters_per_unit': 1,
        'max_distance_meters': 20
    }


class LidarAnnotationTask(Task):
    scene: LidarScene = None

    def __init__(self, param_dict, client):
        super(LidarAnnotationTask, self).__init__(param_dict, client)

    @staticmethod
    def from_scene(scene: LidarScene, template=None, client=None):
        assert scene.public_url, 'No public URL on scene, please upload or save the scene first'

        # Get client using environ api key
        if client is None:
            client = get_api_client()

        # Starting with default template as params
        param_dict = get_default_template()

        # Load scene params
        scene_dict = scene.to_dict(scene.public_url)
        param_dict['attachments'] = scene_dict['frames']
        param_dict['attachment_type'] = 'json'

        if isinstance(template, dict):
            param_dict.update(template)

        elif isinstance(template, str):
            param_dict.update(ujson.load(open(template)))

        elif template is not None:
            raise AttributeError('Template error')

        return LidarAnnotationTask(param_dict, client)

    @staticmethod
    def from_id(task_id):
        task = get_api_client().fetch_task(task_id)
        return LidarAnnotationTask(task.param_dict, task.client)

    def get_annotations(self):
        assert 'response' in self.param_dict, 'Task without response'
        url = self.param_dict['response']['annotations']['url']
        response = requests.get(url)
        return ujson.loads(response.text)

    def get_cuboid_positions_by_frame(self):
        annotations = self.get_annotations()
        return np.array([
            np.array([
                parse_xyz(p)
                for p in [c['position'] for c in frame['cuboids']]
            ])
            for frame in annotations
        ])

    def publish(self, task_type='lidarannotation'):
        task = self.client.create_task(task_type, **self.param_dict)
        print('Task created: %s' % task)
        return task


class LidarTopDownTask(Task):
    scene: LidarScene = None

    def __init__(self, param_dict, client):
        super(LidarTopDownTask, self).__init__(param_dict, client)

    @staticmethod
    def from_scene(scene: LidarScene, template=None, client=None):
        assert scene.public_url, 'No public URL on scene, please upload or save the scene first'

        # Get client using environ api key
        if client is None:
            client = get_api_client()

        # Starting with default template as params
        param_dict = get_default_template()

        # Load scene params
        scene_dict = scene.to_dict(scene.public_url)
        param_dict['attachments'] = scene_dict['frames']
        param_dict['attachment_type'] = 'json'

        if isinstance(template, dict):
            param_dict.update(template)

        elif isinstance(template, str):
            param_dict.update(ujson.load(open(template)))

        elif template is not None:
            raise AttributeError('Template error')

        return LidarTopDownTask(param_dict, client)

    @staticmethod
    def from_id(task_id):
        task = get_api_client().fetch_task(task_id)
        return LidarTopDownTask(task.param_dict, task.client)

    def publish(self, task_type='lidartopdown'):
        task = self.client.create_task(task_type, **self.param_dict)
        print('Task created: %s' % task)
        return task
