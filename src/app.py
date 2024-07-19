"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_cors import CORS
from utils import APIException, generate_sitemap
from datastructures import FamilyStructure
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app)

# create the jackson family object
jackson_family = FamilyStructure("Jackson")

jackson_family.add_member({
                "first_name": "John",
                "last_name": "Jackson",
                "age": 33,
                "lucky_numbers": [7,13,22]
            })
jackson_family.add_member(   {
                "first_name": "Jane",
                "last_name": "Jackson",
                "age": 35,
                "lucky_numbers": [10,14,3]
            })
jackson_family.add_member({
                "first_name": "Jimmy",
                "last_name": "Jackson",
                "age": 5,
                "lucky_numbers": [1]
            })
# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)


@app.route('/member', methods=['POST'])
def create_one_member():

    # this is how you can use the Family datastructure by calling its methods
    body = request.get_json()
    if body is None:
        return jsonify({"error": "not members"}), 400
    id = body.get("id",None)
    first_name = body.get("first_name",None)
    age = body.get("age",None)
    lucky_numbers = body.get("lucky_numbers",None)

    if first_name is None:
        return jsonify({"error": "first name is required"}), 400
    
    if age is None:
        return jsonify({"error": "age is required"}), 400
    
    if lucky_numbers is None:
        return jsonify({"error": "lucky numbers is required"}), 400
    
    jackson_family.add_member(body)
    return "memeber created",200
    

@app.route('/members', methods=['GET'])
def get_all_members():
    members = jackson_family.get_all_members()
    if members is not None:
        return jsonify(members),200
    else:
        return jsonify({"Not members"}),400
    

@app.route('/member/<int:member_id>', methods=['GET'])
def get_member(member_id):
    member_family = jackson_family.get_member(member_id)
    if not member_family:
        return jsonify({"member not exist"}),400
    return jsonify(member_family),200


@app.route('/member/<int:member_id>', methods=['DELETE'])
def delete_family_member(member_id):
    delete_member_family = jackson_family.delete_member(member_id)
    if not delete_member_family:
        return jsonify({"msg":"Familiar no encontrado"}), 400
    return jsonify({"done": delete_member_family}) , 200

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)
