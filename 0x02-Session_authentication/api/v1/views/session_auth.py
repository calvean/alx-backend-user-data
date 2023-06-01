#!/usr/bin/env python3
"""
Session Auth module for the API
"""
from api.v1.views import app_views
from flask import abort, jsonify, request
from models.user import User


@app_views.route(
  '/auth_session/login',
  methods=['POST'],
  strict_slashes=False)
@app_views.route(
  '/auth_session/login/',
  methods=['POST'],
  strict_slashes=False)
def session_login() -> str:
    """ POST /auth_session/login
    Authenticate a user and create a session for them
    Return:
      - User object JSON represented
      - 400 if email or password is missing
      - 404 if no user found for the email
      - 401 if the password is incorrect
    """
    email = request.form.get('email')
    password = request.form.get('password')

    if not email:
        return jsonify({'error': 'email missing'}), 400
    if not password:
        return jsonify({'error': 'password missing'}), 400

    user = User.search({'email': email})
    if not user:
        return jsonify({'error': 'no user found for this email'}), 404

    if not user.is_valid_password(password):
        return jsonify({'error': 'wrong password'}), 401

    from api.v1.app import auth
    session_id = auth.create_session(user.id)
    response = jsonify(user.to_json())
    response.set_cookie(key=auth.SESSION_NAME, value=session_id)

    return response
