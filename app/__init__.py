from flask import Flask
from flask_cors import CORS
from app.config import Config

rapi = Flask ("Routers API")
rapi.config.from_object (Config ())
cors = CORS (rapi, resources={r"/*": {"origins": "*"}})

from app import routes
