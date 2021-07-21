from flask import Flask

from app.mandirimcm.routes import urls as mandirimcm
from app.mandirikupu2.routes import urls as mandirikupu2
from app.ibankbca.routes import urls as ibankbca
from routes import urls as default_routes

app = Flask(__name__)
app.register_blueprint(default_routes)
app.register_blueprint(mandirimcm, url_prefix='/mandirimcm')
app.register_blueprint(mandirikupu2, url_prefix='/mandirikupu2')
app.register_blueprint(ibankbca, url_prefix='/ibankbca')

if __name__ == '__main__':
    app.run()
