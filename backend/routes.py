from backend import app
import json
import os
from flask import jsonify, request, abort
with open(os.path.join(os.path.dirname(__file__), "data", "pictures.json")) as source:
    data = json.load(source)

@app.route("/health")
def health():
    return jsonify(status="OK"), 200

@app.route("/count")
def count():
    return jsonify(length=len(data)), 200

@app.route("/picture", methods=["GET"])
def get_pictures():
    return jsonify(data), 200

@app.route("/picture/<int:id>", methods=["GET"])
def get_picture_by_id(id):
    item = next((item for item in data if item["id"] == id), None)
    if item is None:
        abort(404)
    return jsonify(item), 200

@app.route("/picture", methods=["POST"])
def create_picture():
    item = request.get_json()
    if any(row["id"] == item["id"] for row in data):
        return jsonify(Message=f"picture with id {item['id']} already present"), 302
    data.append(item)
    return jsonify(item), 201

@app.route("/picture/<int:id>", methods=["PUT"])
def update_picture(id):
    for index, row in enumerate(data):
        if row["id"] == id:
            item = request.get_json()
            item["id"] = id
            data[index] = item
            return jsonify(item), 200
    abort(404)

@app.route("/picture/<int:id>", methods=["DELETE"])
def delete_picture(id):
    for index, row in enumerate(data):
        if row["id"] == id:
            data.pop(index)
            return "", 204
    abort(404)

