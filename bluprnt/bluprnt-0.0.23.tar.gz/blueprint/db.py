from google.cloud import firestore

client = firestore.Client()


class Types:
    WORKSPACES = "workspaces"
    CONFIGURATIONS = "configurations"
    STATES = "states"
    PARAM_SETS = "paramSets"


def _workspace(wid=None):
    return client.collection(Types.WORKSPACES).document(wid)


def _configuration(wid, cid=None):
    return _workspace(wid).collection(Types.CONFIGURATIONS).document(cid)


def generate_id():
    return client.collection("").document().id


def add_configuration(wid, name, cid=None):
    ref = _configuration(wid, cid)
    ref.set({"name": name})
    return ref.id


def get_configuration_by_name(wid, name):
    query = (
        _workspace(wid)
        .collection(Types.CONFIGURATIONS)
        .where("name", "==", name)
        .limit(1)
    )
    result = next(query.stream(), None)
    return result.to_dict() if result else None
