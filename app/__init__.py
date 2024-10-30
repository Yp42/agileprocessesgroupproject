
""""

from flask import Flask



def app():
    app = Flask(__name__)

    from .routes import main
    app.register_blueprint(main)

    return app
"""

from flask import Flask
from flask_pymongo import PyMongo
import os
from flask_cors import CORS

mongo = None 

def create_app():
    global mongo
    app = Flask(__name__)
    app.secret_key = "0b698d7d-e77c-46d8-9d18-093d739c6749"

    app.config['MONGO_URI'] = os.getenv('MONGO_URI', 'mongodb://localhost:27017/Foodie')
    mongo = PyMongo(app)
    CORS(app)

    with app.app_context():
        mongo.db.customers.create_index("email", unique=True)
        mongo.db.owners.create_index("email", unique=True)

 

    from .routes import main 
    app.register_blueprint(main)

    return app

