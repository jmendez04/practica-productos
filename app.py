# ==========================================================
# IMPORTACIONES
# ==========================================================

from flask import Flask, render_template, request, redirect, url_for, flash
from db import get_connection
import psycopg2.extras


# ==========================================================
# CONFIGURACION GENERAL DE FLASK
# BASE.HTML UTILIZA FLASH PARA MOSTRAR MENSAJES
# ==========================================================

app = Flask(__name__)

app.secret_key = "clave-desarrollo"


# ==========================================================
# INDEX.HTML
# MOSTRAR TODOS LOS PRODUCTOS
# ==========================================================

@app.route("/")
def index():

    conexion = get_connection()

    cursor = conexion.cursor(
        cursor_factory=psycopg2.extras.RealDictCursor
    )

    cursor.execute(
        "SELECT * FROM productos ORDER BY id DESC"
    )

    productos = cursor.fetchall()

    cursor.close()
    conexion.close()

    return render_template(
        "index.html",
        productos=productos
    )


# ==========================================================
# FORM.HTML
# CREAR NUEVO PRODUCTO
# ==========================================================

@app.route("/productos/nuevo", methods=["GET", "POST"])
def nuevo_producto():

    # ------------------------------------------------------
    # RECIBIR DATOS DEL FORMULARIO
    # ------------------------------------------------------

    if request.method == "POST":

        nombre = request.form["nombre"]
        codigo = request.form["codigo"]
        precio = request.form["precio"]
        stock = request.form["stock"]
        categoria = request.form["categoria"]

        activo = "activo" in request.form


        # --------------------------------------------------
        # GUARDAR PRODUCTO EN POSTGRESQL
        # --------------------------------------------------

        conexion = get_connection()
        cursor = conexion.cursor()

        cursor.execute(
            """
            INSERT INTO productos
            (nombre, codigo, precio, stock, categoria, activo)
            VALUES (%s, %s, %s, %s, %s, %s)
            """,
            (
                nombre,
                codigo,
                precio,
                stock,
                categoria,
                activo
            )
        )

        conexion.commit()

        cursor.close()
        conexion.close()


        # --------------------------------------------------
        # MENSAJE Y REGRESAR AL INDEX
        # --------------------------------------------------

        flash("Producto creado correctamente.")

        return redirect(url_for("index"))


    # ------------------------------------------------------
    # MOSTRAR FORMULARIO VACIO
    # ------------------------------------------------------

    return render_template(
        "form.html",
        producto=None
    )


# ==========================================================
# FORM.HTML
# EDITAR PRODUCTO
# ==========================================================

@app.route("/productos/editar/<int:id>", methods=["GET", "POST"])
def editar_producto(id):

    conexion = get_connection()

    cursor = conexion.cursor(
        cursor_factory=psycopg2.extras.RealDictCursor
    )


    # ------------------------------------------------------
    # ACTUALIZAR PRODUCTO
    # ------------------------------------------------------

    if request.method == "POST":

        nombre = request.form["nombre"]
        codigo = request.form["codigo"]
        precio = request.form["precio"]
        stock = request.form["stock"]
        categoria = request.form["categoria"]

        activo = "activo" in request.form

        cursor.execute(
            """
            UPDATE productos
            SET nombre = %s,
                codigo = %s,
                precio = %s,
                stock = %s,
                categoria = %s,
                activo = %s
            WHERE id = %s
            """,
            (
                nombre,
                codigo,
                precio,
                stock,
                categoria,
                activo,
                id
            )
        )

        conexion.commit()

        cursor.close()
        conexion.close()

        flash("Producto actualizado correctamente.")

        return redirect(url_for("index"))


    # ------------------------------------------------------
    # BUSCAR PRODUCTO PARA MOSTRAR SUS DATOS
    # ------------------------------------------------------

    cursor.execute(
        "SELECT * FROM productos WHERE id = %s",
        (id,)
    )

    producto = cursor.fetchone()

    cursor.close()
    conexion.close()


    # ------------------------------------------------------
    # ENVIAR PRODUCTO AL FORMULARIO
    # ------------------------------------------------------

    return render_template(
        "form.html",
        producto=producto
    )


# ==========================================================
# INDEX.HTML
# ELIMINAR PRODUCTO
# ==========================================================

@app.route(
    "/productos/eliminar/<int:id>",
    methods=["POST"]
)
def eliminar_producto(id):

    conexion = get_connection()
    cursor = conexion.cursor()

    cursor.execute(
        "DELETE FROM productos WHERE id = %s",
        (id,)
    )

    conexion.commit()

    cursor.close()
    conexion.close()

    flash("Producto eliminado correctamente.")

    return redirect(url_for("index"))


# ==========================================================
# EJECUTAR APLICACION
# ==========================================================

if __name__ == "__main__":
    app.run(debug=True)