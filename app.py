from flask import Flask, request, jsonify
from tennis_reservation import get_disponibilites, reserver_creneau

app = Flask(__name__)

@app.route("/")
def home():
    return "🎾 Serveur de réservation tennis actif"

@app.route("/disponibilites")
def disponibilites():
    return jsonify(get_disponibilites())

@app.route("/reserver", methods=["GET"])
def reserver():
    jour = request.args.get("jour")
    heure = request.args.get("heure")
    result = reserver_creneau(jour, heure)
    return jsonify(result)