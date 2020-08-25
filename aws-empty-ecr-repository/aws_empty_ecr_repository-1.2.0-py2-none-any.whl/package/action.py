import boto3
import logging

from typing import Any, Dict

logger = logging.getLogger()
logger.setLevel(logging.INFO)


class Action:
    @staticmethod
    def create(**kwargs) -> Dict[str, Any]:
        logger.info('Not doing anything since this backend only deletes files upon delete event.')
        return {'status': 'skipped'}

    @staticmethod
    def update(**kwargs) -> Dict[str, Any]:
        logger.info('Not doing anything since this backend only deletes files upon delete event.')
        return {'status': 'skipped'}

    @staticmethod
    def delete(**kwargs: Dict[str, Any]) -> Dict[str, Any]:
        repository = kwargs.get('repositoryName', kwargs.get('RepositoryName', kwargs.get('repository_name')))
        client = boto3.client('ecr')
        iterations_left = 100

        logger.info(f'Deleting all images for repository {repository}...')

        while iterations_left > 0:
            images = client.list_images(
                repositoryName=repository,
                maxResults=1000,
            )['imageIds']

            if len(images) > 0:
                client.batch_delete_image(
                    repositoryName=repository,
                    imageIds=images
                )
            else:
                break

            iterations_left -= 1

        return {'status': 'deleted'}
