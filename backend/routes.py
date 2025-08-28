from . import app
import os
import json
from flask import jsonify, request, make_response, abort, url_for  # noqa; F401

SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
json_url = os.path.join(SITE_ROOT, "data", "pictures.json")
data: list = json.load(open(json_url))

######################################################################
# RETURN HEALTH OF THE APP
######################################################################


@app.route("/health")
def health():
    return jsonify(dict(status="OK")), 200

######################################################################
# COUNT THE NUMBER OF PICTURES
######################################################################


@app.route("/count")
def count():
    """return length of data"""
    if data:
        return jsonify(length=len(data)), 200

    return {"message": "Internal server error"}, 500


######################################################################
# GET ALL PICTURES
######################################################################
@app.route("/picture", methods=["GET"])
def get_pictures():
    return jsonify(data)

######################################################################
# GET A PICTURE
######################################################################


@app.route("/picture/<int:id>", methods=["GET"])
def get_picture_by_id(id):
    picture = get_picture_from_list(id, data)
    if picture:
        return picture
    
    return {"message": "picture not found"}, 404


######################################################################
# CREATE A PICTURE
######################################################################
@app.route("/picture", methods=["POST"])
def create_picture():
    picture = request.json

    picture_in_list = get_picture_from_list(picture.get('id'), data)
    if picture_in_list:
        return {"Message": f"picture with id {picture['id']} already present"},302

    data.append(picture)
    return picture, 201

######################################################################
# UPDATE A PICTURE
######################################################################


@app.route("/picture/<int:id>", methods=["PUT"])
def update_picture(id):
    picture = request.json

    picture_in_list = get_picture_from_list(picture.get('id'), data)
    if picture_in_list == None:
        return {"message": "picture not found"}, 404

    data.remove(picture_in_list)
    data.append(picture)
    return picture, 201

######################################################################
# DELETE A PICTURE
######################################################################
@app.route("/picture/<int:id>", methods=["DELETE"])
def delete_picture(id):
    picture_in_list = get_picture_from_list(id, data)
    if picture_in_list == None:
        return {"message": "picture not found"}, 404

    data.remove(picture_in_list)
    return "", 204

def get_picture_from_list(id, list_data):
    for picture in list_data:
        if picture['id'] == id:
            return picture

    return None