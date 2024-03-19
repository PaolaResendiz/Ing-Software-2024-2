from flask import Blueprint, request, render_template, flash, redirect, url_for
from sqlalchemy.exc import IntegrityError

from alchemyClasses.Pelicula import Pelicula, db

pelicula_blueprint = Blueprint('pelicula', __name__, url_prefix='/pelicula')

@pelicula_blueprint.route('/', methods=['GET'])
def raiz():
    return render_template('Pelicula/raiz.html')

@pelicula_blueprint.route('/ver_todos', methods=['GET'])
def ver_peliculas():
    peliculas = Pelicula.query.all()
    return render_template('Pelicula/ver_todos.html', peliculas=peliculas)

"""
@pelicula_blueprint.route('/id/<int:id_usuario>/<string:nombre>')
def ver_usuario_id(id_usuario, nombre):
    usuario = Usuario.query.filter_by(idUsuario=id_usuario).first()
    if usuario:
        return f"Nombre: {usuario.nombre}, Email: {usuario.email}"
    else:
        return "Usuario no encontrado"

"""

@pelicula_blueprint.route('/agregar', methods=['GET', 'POST'])
def agregar_pelicula():
    if request.method == 'POST':
        nombre = request.form['nombre']
        genero = request.form['genero']
        duracion = request.form['duracion']
        inventario = request.form['inventario']

        #Si no funciona, agregar dos e en nombre y dos l en email

        nueva_pelicula = Pelicula(nombre=nombre, genero=genero, duracion=duracion, inventario=inventario)
        try:
            db.session.add(nueva_pelicula)
            db.session.commit()
            flash('Película agregada correctamente', 'success')
            return redirect(url_for('pelicula.agregar_pelicula'))
        except IntegrityError:
            db.session.rollback()  # Revertir los cambios realizados en la transacción
            flash('Error: El correo electrónico ya está registrado', 'error')
            return redirect(url_for('pelicula.agregar_pelicula'))

    return render_template('Pelicula/add_pelicula.html')


@pelicula_blueprint.route('/borrar', methods=['GET', 'POST'])
def borrar_pelicula():
    if request.method == 'GET':
        return render_template('Pelicula/borrar.html')
    else:
        idPelicula = request.form['idPelicula']

        pelicula_a_eliminar = Pelicula.query.get(idPelicula)
        if pelicula_a_eliminar:
            db.session.delete(pelicula_a_eliminar)
            db.session.commit()
            flash('Pelicula eliminado correctamente', 'success')
            return redirect(url_for('pelicula.borrar_pelicula'))
        else:
            flash('Error: No se encontró la película', 'error')
            return redirect(url_for('pelicula.borrar_pelicula'))


@pelicula_blueprint.route('/actualizar', methods=['GET', 'POST'])
def actualizar_pelicula():
    if request.method == 'POST':
        id_pelicula = int(request.form['idPelicula'])
        actualiza = request.form['campoActualizar']
        nuevo_valor = request.form['nuevoValor']

        pelicula = Pelicula.query.get(id_pelicula)
        if pelicula:
            if hasattr(pelicula, actualiza):
                setattr(pelicula, actualiza, nuevo_valor)
                db.session.commit()
                flash('¡pelicula actualizada correctamente!', 'success')
                return render_template('Pelicula/actualizar.html')
            else:
                flash('No se puede actualizar el campo', 'error')
        else:
            flash('Pelicula no encontrada', 'error')
    return render_template('Pelicula/actualizar.html')