from aplicacao import database, app
#from aplicacao.models import Usuario, Foto

with app.app_context():
    database.create_all()