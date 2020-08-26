from flask import jsonify


def crud_error_handler(blueprint, app):
    @blueprint.app_errorhandler(Exception)
    def handle_error(error):
        if hasattr(error, 'code'):
            status_code = error.code
            response = {
                'success': False,
                'error': {
                    'type': error.__class__.__name__,
                    'message': error.description,
                },
            }

            return jsonify(response), status_code
        else:
            response = {
                'success': False,
                'error': {
                    'type': error.__class__.__name__,
                    'message': error.args[0],
                },
            }
            return jsonify(response), 500

    app.register_blueprint(blueprint)
