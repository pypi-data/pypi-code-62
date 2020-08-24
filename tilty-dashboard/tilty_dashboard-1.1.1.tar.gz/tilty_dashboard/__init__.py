# -*- coding: utf-8 -*-
""" The main method, handles all initialization """
import logging
import os
from datetime import datetime, timedelta

from flask import Flask, render_template, session
from flask_bootstrap import Bootstrap
from flask_cors import CORS
from flask_socketio import SocketIO, emit
from sqlalchemy import and_
from werkzeug.contrib.fixers import ProxyFix

from flask_session import Session
from tilty_dashboard.model import Tilt, db

logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger(__name__)


app = Flask(__name__)
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)
socketio = SocketIO(app, manage_session=False)


def init_webapp(config):
    """ Initialize the web application. """
    app.wsgi_app = ProxyFix(app.wsgi_app)
    app.config['SQLALCHEMY_DATABASE_URI'] = config['webapp']['database_uri']
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'abc123')
    CORS(app, supports_credentials=True)
    Bootstrap(app)
    db.app = app
    db.init_app(app)
    db.create_all()

    return app


@socketio.on('save settings')
def save_settings(message):
    """ Save the settings into the cookie """
    session["settings"] = message['settings']


@app.route('/settings', methods=['GET', 'POST'])
def settings():
    """ Settings Page. """
    return render_template(
        'settings.html',
        gravity_meas=session.get('settings', {}).get('gravity_meas'),
        gravity_offset=session.get('settings', {}).get(
            'gravity_offset',
            -0.001
        ),
        temp_meas=session.get('settings', {}).get('temp_meas'),
    )


@app.route('/')
def index():
    """A landing page.

    Nothing too interesting here.

    """
    return render_template(
        'index.html',
        gravity_meas=session.get('settings', {}).get('gravity_meas'),
        gravity_offset=session.get('settings', {}).get(
            'gravity_offset',
            -0.001
        ),
        temp_meas=session.get('settings', {}).get('temp_meas'),
    )


@socketio.on('refresh')
def refresh():
    """ Query The DB and refresh the socket """

    since = datetime.now() - timedelta(days=1)
    last_pulse = db.session.query(  # pylint:disable=E1101
        Tilt.color,
        Tilt.gravity,
        Tilt.temp,
        Tilt.mac,
        Tilt.timestamp,
        db.func.max(Tilt.timestamp)  # pylint:disable=E1101
    ).group_by(Tilt.mac).subquery()
    _data = Tilt.query.join(
        last_pulse,
        and_(
            Tilt.mac == last_pulse.c.mac,
            Tilt.timestamp == last_pulse.c.timestamp
        )
    ).filter(Tilt.timestamp > since).all()
    _tilt_data = [d.serialize() for d in _data]
    emit('refresh', {'data': _tilt_data})
