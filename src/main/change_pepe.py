
import os
import random


class PepeImage:
    """
    This class provides a method to change the pepe image. This method is used by
    a cron job which is scheduled with APScheduler.
    """

    images = [f'static/pepe/{img}' for img in os.listdir('src/static/pepe')]

    @classmethod
    def change(cls):
        choices = [img for img in cls.images if img != os.environ['PEPE_IMAGE']]
        os.environ['PEPE_IMAGE'] = random.choice(choices)
