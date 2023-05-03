import pytest
from app import create_app
from app import db
from flask.signals import request_finished

#De la carpeta app, se ejecuta este archivo si se quiere trabajar
#en test envi
@pytest.fixture
def app():
    app = create_app({"TESTING": True})

#Cuando termines de hacer cada request y te permita ver updates 
#(sirve especialmente para method=UPDATE)
    @request_finished.connect_via(app)
    def expire_session(sender, response, **extra):
        db.session.remove()

#(Varias funciones de Flask determinan cual es la app que se
# esta ejecutando. Esto es importante para acceder a la base 
# de datos asociada con la app (app.app_context). El create_all
#recrea todas las tablas que se necesitan para nuestros modelos.
    with app.app_context():
        db.create_all()
        yield app

#Esta linea se ejecutara despues de q los test de app pasen (fixture)
#despues de los tests, toda la data usada para el test sera borrada
    with app.app_context():
        db.drop_all()

#Se encargara de ver primero que corra la app 
#Lo que retorna nos ayuda a crear un objeto cliente que simulara
#hacer HTTP requests
@pytest.fixture
def client(app):
    return app.test_client()
