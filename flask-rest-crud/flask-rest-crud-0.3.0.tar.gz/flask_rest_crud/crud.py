from flask import request, Response, jsonify
from mongoengine import ReferenceField
import bson
import json


def check_route_permission(func):
    def wrapper(*args, **kwargs):
        if func.__name__ not in args[0].roles:
            return jsonify(
                error=f'{args[0].name} {func.__name__} is forbidden'
            )
        else:
            return func(*args, **kwargs)

    return wrapper


def deserialize_object_id_fields(obj):
    for k, v in obj.items():
        if isinstance(v, bson.objectid.ObjectId):
            obj[k] = str(v)
    return obj


def normalize_list(query):
    response = list(query.as_pymongo())
    for key, value in enumerate(response):
        response[key] = deserialize_object_id_fields(value)
        response[key]['id'] = str(value['_id'])
        del response[key]['_id']
    return json.dumps(response)


def normalize_item(query):
    response = query.to_mongo().to_dict()
    response['id'] = str(response['_id'])
    response = deserialize_object_id_fields(response)
    del response['_id']
    return json.dumps(response)


class Crud:
    def __init__(self, app, model, name, prefix='/'):
        self.app = app
        self.model = model
        self.name = name
        self.prefix = prefix
        self.roles = ['list', 'find', 'create', 'update', 'delete']
        self.create_routes()

    def create_routes(self):
        self.app.add_url_rule(
            f'{self.prefix}/{self.name}',
            f'${self.name}_list',
            self.list,
            methods=['GET'],
        )
        self.app.add_url_rule(
            f'{self.prefix}/{self.name}',
            f'${self.name}_create',
            self.create,
            methods=['POST'],
        )
        self.app.add_url_rule(
            f'{self.prefix}/{self.name}/<model_id>',
            f'${self.name}_find',
            self.find,
            methods=['GET'],
        )
        self.app.add_url_rule(
            f'{self.prefix}/{self.name}/<model_id>',
            f'${self.name}_update',
            self.update,
            methods=['PUT'],
        )
        self.app.add_url_rule(
            f'{self.prefix}/{self.name}/<model_id>',
            f'${self.name}_delete',
            self.delete,
            methods=['DELETE'],
        )

    @check_route_permission
    def create(self):
        data = request.get_json()
        model = self.model()
        normalized_data = {}
        for k, v in data.items():
            if '_id' in k:
                normalized_data[k.replace('_id', '')] = v
            else:
                normalized_data[k] = v

        for field, cls in self.model._fields.items():
            if field in normalized_data:
                if isinstance(cls, ReferenceField):
                    model[
                        field
                    ] = self.model.category.document_type_obj.objects.get(
                        id=normalized_data[field]
                    )
                else:
                    model[field] = normalized_data[field]
        model.save()
        return normalize_item(model)

    @check_route_permission
    def update(self, model_id):
        data = request.get_json()
        model = self.model.objects.get_or_404(id=model_id)
        for field in self.model._fields:
            if field in data:
                model[field] = data[field]
        model.save()
        return normalize_item(model)

    @check_route_permission
    def find(self, model_id):
        model = self.model.objects.get_or_404(id=model_id)
        return normalize_item(model)

    @check_route_permission
    def delete(self, model_id):
        model = self.model.objects.get(id=model_id)
        model.delete()
        return normalize_item(model)

    @check_route_permission
    def list(self):
        count = self.model.objects.count()
        start = 0
        end = count
        if request.args.get('range'):
            pagination = json.loads(request.args.get('range'))
            start = pagination[0]
            end = pagination[1]

        if request.args.get('filter'):
            filters = json.loads(request.args.get('filter'))
            normalized_filters = {}
            for key, value in filters.items():
                if type(value) is list:
                    normalized_filters[f'{key}__in'] = value
                else:
                    normalized_filters[f'{key}'] = value
            items = self.model.objects(**normalized_filters)
        else:
            items = self.model.objects

        if request.args.get('sort'):
            sort = json.loads(request.args.get('sort'))
            direction = '-' if sort[1] == 'DESC' else ''
            items = (
                items.skip(start)
                .limit(end - start)
                .order_by(f'{direction}{sort[0]}')
            )
        else:
            items = items.skip(start).limit(end - start)

        res = Response(normalize_list(items))
        res.headers['Access-Control-Expose-Headers'] = 'Content-Range'
        res.headers['Content-Range'] = f'{self.name} {start}-{end}/{count}'
        return res
