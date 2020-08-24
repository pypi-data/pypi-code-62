from flask import Blueprint, render_template

def blue_admin(version):
    blueprint = Blueprint('admin', __name__, template_folder="templates", static_folder=None)

    # You can override the templates... with the central templates of the application
    @blueprint.route('', methods=['GET'])
    def index():
        return render_template("index.html", version=version)

    return blueprint