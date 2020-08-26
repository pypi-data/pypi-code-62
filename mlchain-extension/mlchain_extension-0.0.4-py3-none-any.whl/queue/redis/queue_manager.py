import redis
from flask import Flask, send_file, jsonify, Response,request
from flask_swagger_ui import get_swaggerui_blueprint
from mlchain.base.serializer import MsgpackSerializer
from pymongo.mongo_client import MongoClient
import os

def load_app():
    serializer = MsgpackSerializer()

    redis_host = os.getenv('REDIS_HOST', 'localhost')
    redis_port = os.getenv('REDIS_PORT', 6379)
    redis_db = int(os.getenv('REDIS_DB', 0))
    redis_pass = os.getenv('REDIS_PASSWORD', '')
    mongo_connection = os.getenv("MONGO_CONNECTION")
    client = redis.Redis(host=redis_host, port=redis_port, db=redis_db, password=redis_pass)
    mongo_client = MongoClient(mongo_connection)
    collection = mongo_client['mlchain']['task_queue']
    app = Flask(__name__)

    SWAGGER_URL = '/swagger'
    API_URL = '/config'


    @app.route(API_URL, methods=['GET'])
    def swagger_config():
        return send_file(os.path.join(os.path.dirname(__file__), 'swagger.yml'))


    SWAGGERUI_BLUEPRINT = get_swaggerui_blueprint(SWAGGER_URL, API_URL)
    app.register_blueprint(SWAGGERUI_BLUEPRINT, url_prefix=SWAGGER_URL)


    def scan_prefix(prefix):
        result = []
        for key in client.scan_iter('{0}*'.format(prefix), count=None):
            if isinstance(key, bytes):
                key = key.decode()
            result.append(key)
        return result


    @app.route('/model/listing', methods=['GET'])
    def model_listing():
        keys = scan_prefix('mlchain_queue_')
        models = []
        for key in keys:
            key = key[len('mlchain_queue_'):]
            print(key)
            if ':' in key:
                name, version = key.split(':', 1)
            else:
                continue
            models.append({
                'name': name,
                'version': version
            })
        return jsonify(models)


    @app.route('/model/<name>/<version>', methods=['GET'])
    def model_info(name, version):
        config = client.get('mlchain_queue_{0}:{1}'.format(name, version))
        if config is None:
            return Response('Not found model', status=404)
        config = serializer.decode(config)
        pending = 0
        funcs = []
        for c in config:
            count = client.llen(c['input'])
            funcs.append({
                'function': c['function_name'],
                'pending': count
            })
            pending += count
        return jsonify({'name': name, 'version': version, 'functions': funcs, 'pending': pending})


    def group_tree(root, children):
        root_children = []
        other_children = []
        for child in children:
            if child['context']['parent_id'] == root['uid']:
                root_children.append(child)
            else:
                other_children.append(child)
        root['children'] = root_children
        for child in root_children:
            group_tree(child, other_children)


    def get_status(task_id,max_dept = 10,filter_done = False):
        pipeline = [
            {
                "$match": {
                    "task_id": task_id,
                }
            },
            {
                "$graphLookup": {
                    "from": "task_queue",
                    "startWith": "$sub_tasks",
                    "connectFromField": "sub_tasks",
                    "connectToField": "task_id",
                    "as": "children",
                    "maxDepth": max_dept,
                    "restrictSearchWithMatch":{"status":{"$ne":"SUCCESS" if filter_done else ""}}
                }
            }
        ]
        data = collection.aggregate(pipeline)
        d = None
        for d in data:
            break
        if d is None:
            return None
        children = d.pop('children')
        if '_id' in d:
            d.pop('_id')
        for c in children:
            if '_id' in c:
                c.pop('_id')
        children = {c['task_id']: c for c in children}
        d['children'] = [children[sub_task] for sub_task in d['sub_tasks'] if sub_task in children]
        for v in children.values():
            v['children'] = [children[sub_task] for sub_task in v['sub_tasks'] if sub_task in children]
        return d


    @app.route('/task/listing', methods=['GET'])
    def task_listing():
        offset = request.args.get('offset',0,type=int)
        limit = request.args.get('limit',20,type=int)
        status = request.args.get('status',None, type=str)
        name = request.args.get("name",None,type=str)
        function = request.args.get("function",None,type=str)
        query = {'type': 'root'}
        if status is not None:
            query['status'] = status
        if name is not None:
            query['name'] = name
        if function is not None:
            query['function'] = function
        data = collection.find(query, projection={'_id': 0},sort = [('_id',-1)]).skip(offset).limit(limit)
        return jsonify(list(data))


    @app.route('/status/<task_id>', methods=['GET'])
    def status_task(task_id):
        max_dept = request.args.get('max_dept',10,type=int)
        filter_done = request.args.get('filter_done',False,type=bool)
        return jsonify(get_status(task_id,max_dept,filter_done=filter_done))

    return app
if __name__ == '__main__':
    app = load_app()
    app.run(host='0.0.0.0', port=8033)
