import time
from flask_socketio import SocketIO
from .celery import create_celery_app
from .app import REDIS_ADDRESS

celery = create_celery_app()


@celery.task(bind=True)
def initial_celery_task(self):
    """
    Initial celery task
    TODO: Fill this with functionality
    """
    sio = SocketIO(
        logger=True,
        engineio_logger=True,
        message_queue=REDIS_ADDRESS,
        async_mode="threading",
    )
    message = None
    self.update_state(state="PROGRESS", meta={"current": "working"})
    i = 0
    while i < 5:
        sio.emit("resp", {"data": f"message {i}"}, namespace="/a")
        time.sleep(1)
        i -= -1

    return "done"
