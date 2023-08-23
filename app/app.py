#!/usr/bin/env python
from dotenv import load_dotenv
import eventlet
import os

eventlet.monkey_patch(socket=True)
from flask import Flask, render_template

from .websocket import socketio


load_dotenv()

REDIS_PASSWORD = os.environ["REDIS_PASSWORD"]
REDIS_ADDRESS = f"redis://:{REDIS_PASSWORD}@redis:6379/0"


def create_app(main=True, debug=False):
    """Initialize Flask app."""
    app = Flask(__name__)

    async_mode = None

    app.config["SECRET_KEY"] = "secret!"

    if main:
        socketio.init_app(
            app,
            logger=True,
            engineio_logger=True,
            message_queue=REDIS_ADDRESS,
        )
    else:
        socketio.init_app(
            None,
            logger=True,
            engineio_logger=True,
            message_queue=REDIS_ADDRESS,
            async_mode="threading",
        )

    @app.route("/")
    def index():
        return render_template("index.html", async_mode=socketio.async_mode)

    @app.route("/start_task/", methods=["GET", "POST"])
    def start_task():
        """
        Process request in a detached
        context using Celery.
        """
        from .tasks import initial_celery_task

        initial_celery_task.delay()
        return "Processing.."

    return app
