
import os

from src import create_app

app = create_app(os.environ['FLASK_CONFIG'])
