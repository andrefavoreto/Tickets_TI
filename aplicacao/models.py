from aplicacao import database ,login_manager
from flask import abort
from datetime import datetime
from flask_login import UserMixin, current_user
from flask_admin.contrib.sqla import ModelView
from flask_admin.menu import MenuLink
from aplicacao import admin, database

@login_manager.user_loader
def load_usuario(id_usuario):
    return Usuario.query.get(int(id_usuario))

# modelo do usuario
class Usuario(database.Model, UserMixin):
    id = database.Column(database.Integer, primary_key=True)
    matricula = database.Column(database.Integer, nullable=False, unique=True)
    departamento = database.Column(database.String, nullable=False)
    username = database.Column(database.String, nullable=False)
    email = database.Column(database.String, nullable=False, unique=True)
    senha = database.Column(database.String, nullable=False)
    chamados = database.relationship("Chamado", backref="usuario", lazy=True)
    e_admin = database.Column(database.Boolean, nullable=False, default=False)

    def __repr__(self):
        return (self.username)

# modelo do chamado
class Chamado(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    problema = database.Column(database.String)
    descricao = database.Column(database.String(800))
    data_criacao = database.Column(database.DateTime, nullable=False, default=datetime.utcnow())
    id_usuario = database.Column(database.Integer, database.ForeignKey('usuario.id'), nullable=False)
    status = database.Column(database.String, default="Não Resolvido")

    def __repr__(self):
        return (self.problema)

# modelos interface admin
class ControlUsuario(ModelView):

    def is_accessible(self):
        if current_user.e_admin == True:
            return current_user.is_authenticated
        else:
            return abort(404)
        
    def not_auth(self):
        return "acesso negado, para poder acessar peça para o admin"
    
    column_filters = ['matricula', 'e_admin']
    form_excluded_columns = ['id','chamados']
    create_modal = True
    edit_modal = True
    can_view_details = True
    can_edit = False
    can_create = False
    can_delete = False


class ControlChamado(ModelView):

    def is_accessible(self):
        if current_user.e_admin == True:
            return current_user.is_authenticated
        else:
            return abort(404)
        
    def not_auth(self):
        return "acesso negado, para poder acessar peça para o admin"
    
    column_list = ['id', 'data_criacao', 'usuario.username','status', 'problema', 'descricao']
    column_filters = ['data_criacao', 'status']
    column_details_list = ['id', 'data_criacao', 'usuario.username','status', 'problema', 'descricao']
    column_editable_list = ['data_criacao','status', 'problema', 'descricao']
    create_modal = True
    edit_modal = True
    can_view_details = True
    can_create = False
    form_choices = {
        'status': [
            ('Resolvido', 'Resolvido'),
            ('Não Resolvido', 'Não Resolvido')
        ]
    }

#interface admin views
admin.add_view(ControlChamado(Chamado, database.session, name='Chamados'))
admin.add_view(ControlUsuario(Usuario, database.session, name='Usuarios'))
admin.add_link(MenuLink(name='Voltar', url='/feed'))
admin.add_link(MenuLink(name='Sair', url='/logout'))

