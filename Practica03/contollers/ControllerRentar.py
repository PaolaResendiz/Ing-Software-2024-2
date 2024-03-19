from flask import Blueprint, request, render_template, flash, redirect, url_for
from sqlalchemy.exc import IntegrityError

from alchemyClasses.Rentar import Rentar, db

rentar_blueprint = Blueprint('rentar', __name__, url_prefix='/rentar')

@rentar_blueprint.route('/', methods=['GET'])
def raiz():
    return render_template('Rentar/raiz.html')

@rentar_blueprint.route('/ver_todos', methods=['GET'])
def ver_rentas():
    rentas = Rentar.query.all()
    return render_template('Rentar/ver_todos.html', rentas=rentas)

"""
@rentar_blueprint.route('/id/<int:id_usuario>/<string:nombre>')
def ver_usuario_id(id_usuario, nombre):
    usuario = Usuario.query.filter_by(idUsuario=id_usuario).first()
    if usuario:
        return f"Nombre: {usuario.nombre}, Email: {usuario.email}"
    else:
        return "Usuario no encontrado"

"""

@rentar_blueprint.route('/agregar', methods=['GET', 'POST'])
def agregar_renta():
    if request.method == 'POST':
        nombre = request.form['nombre']
        genero = request.form['genero']
        duracion = request.form['duracion']
        inventario = request.form['inventario']

        #Si no funciona, agregar dos e en nombre y dos l en email

        nueva_renta = Rentar(nombre=nombre, genero=genero, duracion=duracion, inventario=inventario)
        try:
            db.session.add(nueva_renta)
            db.session.commit()
            flash('Película agregada correctamente', 'success')
            return redirect(url_for('rentar.agregar_renta'))
        except IntegrityError:
            db.session.rollback()  # Revertir los cambios realizados en la transacción
            flash('Error: El correo electrónico ya está registrado', 'error')
            return redirect(url_for('rentar.agregar_renta'))

    return render_template('Rentar/add_renta.html')


@rentar_blueprint.route('/borrar', methods=['GET', 'POST'])
def borrar_renta():
    if request.method == 'GET':
        return render_template('Rentar/borrar.html')
    else:
        idRentar = request.form['idRentar']

        renta_a_eliminar = Rentar.query.get(idRentar)
        if renta_a_eliminar:
            db.session.delete(renta_a_eliminar)
            db.session.commit()
            flash('Renta eliminada correctamente', 'success')
            return redirect(url_for('renta.borrar'))
        else:
            flash('Error: No se encontró la película', 'error')
            return redirect(url_for('renta.borrar_renta'))
