from flask import render_template, url_for, redirect, flash, abort
from aplicacao import app, database, bcrypt
from aplicacao.models import Usuario, Chamado
from flask_login import login_required, login_user, logout_user, current_user
from aplicacao.forms import FormCriarConta, FormLogin, FormChamado
from datetime import datetime

@app.route("/", methods=["GET", "POST"])
def homepage():
    form_login = FormLogin()

    if form_login.validate_on_submit():
        usuario = Usuario.query.filter_by(email=form_login.email.data).first()
        if usuario and bcrypt.check_password_hash(usuario.senha, form_login.senha.data):
            login_user(usuario, remember=form_login.remember.data)
            flash('Usuário logado com sucesso')
            return redirect(url_for("perfil", id_usuario=usuario.id))
        flash('Email ou senha incorretos')
    return render_template("homepage.html", form=form_login)

@app.route("/criarconta", methods=['GET', 'POST'])
def criarconta():
    form_criarconta = FormCriarConta()
    if form_criarconta.validate_on_submit():
        senha = bcrypt.generate_password_hash(form_criarconta.senha.data).decode('utf-8')
        usuario = Usuario(
                matricula=form_criarconta.matricula.data,
                departamento=form_criarconta.departamento.data, 
                username=form_criarconta.username.data,
                senha=senha, 
                email=form_criarconta.email.data)
        database.session.add(usuario)
        database.session.commit()
        login_user(usuario, remember=True)
        flash('Novo usuário adicionado')
        return redirect(url_for("homepage"))
    return render_template("criarconta.html", form=form_criarconta)

@app.route("/perfil/<id_usuario>", methods=["GET", "POST"])
@login_required
def perfil(id_usuario):
    form_chamado = FormChamado()

    if not(int(id_usuario) == int(current_user.id)):
        abort(403)
    
    if form_chamado.validate_on_submit():
        print(form_chamado.problema)
        chamado = Chamado(problema=form_chamado.problema.data, 
                            descricao=form_chamado.descricao.data, 
                            data_criacao=datetime.utcnow(),
                            id_usuario=current_user.id)
        database.session.add(chamado)
        database.session.commit()
        flash('Novo chamado adicionado')
        return redirect(url_for("feed"))
    return render_template("perfil.html", usuario=current_user, form=form_chamado)
    
@app.route("/feed", methods=['GET'])
@login_required
def feed():
    chamados = Chamado.query.filter_by(id_usuario=current_user.id).all()
    return render_template("feed.html", chamados=chamados)

@app.route("/detalhes/<id>")
@login_required
def detalhes(id):
    chamado = Chamado.query.get(id)
    if current_user.id == chamado.id_usuario:
        return render_template('detalhes.html', chamado=chamado)
    return redirect(url_for("feed"))

@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash('Usuário saiu com sucesso')
    return redirect(url_for("homepage"))