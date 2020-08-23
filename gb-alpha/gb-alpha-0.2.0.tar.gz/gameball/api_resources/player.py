from gameball.api_requestor import APIRequestor
import gameball.constants
import gameball.utils
from gameball.models.player_object import playerObject

def initialize_player(player):
    api_requestor_instance = APIRequestor()

    body={
    "playerUniqueId": player.player_unique_id,
    "playerAttributes": player.player_attributes
    }

    if player.player_type_id is not None:
        body["playerTypeId"] = player.player_type_id

    if player.device_token is not None:
        body["deviceToken"] = player.device_token

    if player.os_type is not None:
        body["osType"] = player.os_type

    if player.is_deleted is not None:
        body["isDeleted"] = player.is_deleted

    if player.creation_date is not None:
        body["creationDate"] = player.creation_date

    if player.last_update is not None:
        body["lastUpdate"] = player.last_update

    response = api_requestor_instance.request(method='POST',url=gameball.constants.create_player, params = body)
    return response


def get_player_info(player_unique_id):
    api_requestor_instance = APIRequestor()

    body_hashed = gameball.utils.hash_body(player_unique_id)

    body={
    "playerUniqueId": player_unique_id,
    "hash": body_hashed
    }

    response = api_requestor_instance.request(method='POST',url=gameball.constants.player_info, params = body)
    return response