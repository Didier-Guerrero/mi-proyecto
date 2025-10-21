from flask import Flask, request, jsonify
from app.validator import (
    validar_cedula,
    validar_datos,
    validar_con_tiempo,
    verificar_en_servicio_externo
)


app = Flask(__name__)

@app.route("/")
def home():
    """Ruta de prueba para verificar si la API está viva."""
    return jsonify({"mensaje": "API de validación activa"}), 200
@app.route("/status")
def status():
    """Devuelve el estado de la API (para pruebas de Jenkins)."""
    return jsonify({"status": "ok", "message": "API funcionando correctamente"}), 200


@app.route("/validar", methods=["POST"])
def validar_cedula_endpoint():
    """
    Endpoint que valida una cédula ecuatoriana.
    Ejemplo de entrada JSON:
        { "cedula": "1710034065" }
    """
    data = request.get_json()
    if not data or "cedula" not in data:
        return jsonify({"error": "Debe incluir el campo 'cedula'"}), 400

    resultado = validar_cedula(data["cedula"])
    return jsonify(resultado), 200


@app.route("/validar_datos", methods=["POST"])
def validar_datos_endpoint():
    """
    Endpoint que valida un conjunto de datos personales.
    Ejemplo:
        { "name": "Anthony", "email": "anthony@example.com", "age": 23 }
    """
    data = request.get_json()
    if not data:
        return jsonify({"error": "Debe enviar un cuerpo JSON válido"}), 400

    resultado = validar_con_tiempo(data)
    return jsonify(resultado), 200


@app.route("/verificar_externo", methods=["GET"])
def verificar_externo_endpoint():
    """
    Endpoint que simula una verificación externa usando requests.
    Ejemplo: /verificar_externo?email=anthony@example.com
    """
    email = request.args.get("email", "demo@correo.com")
    resultado = verificar_en_servicio_externo(email)
    return jsonify(resultado), 200


if __name__ == "__main__":
    app.run(debug=True)
