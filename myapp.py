from flask import Flask

from app.mandirimcm.routes import urls as mandirimcm
from routes import urls as default_routes

app = Flask(__name__)
app.register_blueprint(default_routes)
app.register_blueprint(mandirimcm, url_prefix='/mandirimcm')

if __name__ == '__main__':
    app.run()
