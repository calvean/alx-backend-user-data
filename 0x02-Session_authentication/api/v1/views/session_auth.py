#!/usr/bin/env python3
""" Session Authentication routes """
from flask import abort, jsonify, request
from api.v1.views import app_views
from models.user import User
from api.v1.app import auth
import os


@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def session_login():
    """ Session login method """
    email = request.form.get('email')
    password = request.form.get('password')

    if not email:
        return jsonify({"error": "email missing"}), 400
    if not password:
        return jsonify({"error": "password missing"}), 400

    users = User.search({'email': email})
    if not users:
        return jsonify({"error": "no user found for this email"}), 404

    user = users[0]
    if not user.is_valid_password(password):
        return jsonify({"error": "wrong password"}), 401

    session_id = auth.create_session(user.id)
    user_json = user.to_json()
    response = jsonify(user_json)
    session_cookie_name = os.getenv("SESSION_NAME", "_my_session_id")
    response.set_cookie(key=session_cookie_name, value=session_id)

    return response


@app_views.route(
  '/auth_session/logout', methods=['DELETE'], strict_slashes=False)
def session_logout():
    """ Session logout method """
    if not auth.destroy_session(request):
        abort(404)
    return jsonify({})
