#!/usr/bin/env python3
""" Flask module """
from flask import Flask, jsonify, request, abort, redirect, make_response
from sqlalchemy.orm.exc import NoResultFound
from auth import Auth

app = Flask(__name__)
AUTH = Auth()


@app.route('/reset_password', methods=['PUT'])
def update_password() -> str:
    """ Changes the password.

    Returns:
        JSON response with email and message if the password is updated successfully.
        200 status code if the update is successful, otherwise 403 status code.
    """
    try:
        email = request.form['email']
        reset_token = request.form["reset_token"]
        new_password = request.form['new_password']
    except KeyError:
        abort(403)

    try:
        AUTH.update_password(reset_token, new_password)
    except ValueError:
        abort(403)

    return jsonify({"email": email, "message": "Password updated"}), 200


@app.route('/reset_password', methods=['POST'])
def reset_password() -> str:
    """ Resets the password and generates a reset password token.

    Returns:
        JSON response with email and reset_token if the token is generated successfully.
        200 status code if the token is generated, otherwise 403 status code.
    """
    try:
        email = request.form['email']
    except KeyError:
        abort(403)

    try:
        reset_token = AUTH.get_reset_password_token(email)
    except ValueError:
        abort(403)

    return jsonify({"email": email, "reset_token": reset_token}), 200


@app.route('/profile', methods=['GET'])
def profile() -> str:
    """ Retrieves the user profile based on the session ID.

    Returns:
        JSON response with email if the user is found.
        200 status code if the user is found, otherwise 403 status code.
    """
    session_id = request.cookies.get('session_id', None)

    if session_id is None:
        abort(403)

    user = AUTH.get_user_from_session_id(session_id)

    if user is None:
        abort(403)

    return jsonify({"email": user.email}), 200


@app.route('/sessions', methods=['DELETE'])
def logout() -> str:
    """ Logs out the user session.

    Returns:
        Redirects to the main page with a 302 status code.
        403 status code if the session ID is not found or the user is not found.
    """
    session_id = request.cookies.get('session_id', None)

    if session_id is None:
        abort(403)

    user = AUTH.get_user_from_session_id(session_id)

    if user is None:
        abort(403)

    AUTH.destroy_session(user.id)

    return redirect('/', code=302)


@app.route('/sessions', methods=['POST'])
def login() -> str:
    """ Logs in the user with the provided credentials.

    Returns:
        JSON response with email and message if the login is successful.
        Sets the session ID cookie.
        401 status code if the login credentials are invalid.
    """
    try:
        email = request.form['email']
        password = request.form['password']
    except KeyError:
        abort(401)

    if AUTH.valid_login(email, password):
        session_id = AUTH.create_session(email)
        if session_id is not None:
            response = jsonify({"email": email, "message": "logged in"})
            response.set_cookie("session_id", session_id)
            return response

    abort(401)


@app.route('/', methods=['GET'])
def hello_world() -> str:
    """ Greets the user.

    Returns:
        JSON response with a greeting message.
    """
    message = {"message": "Bienvenue"}
    return jsonify(message)


@app.route('/users', methods=['POST'])
def register_user() -> str:
    """ Registers a new user.

    Returns:
        JSON response with email and message if the user is created successfully.
        400 status code if the email or password is missing.
        400 status code if the email is already registered.
    """
    try:
        email = request.form['email']
        password = request.form['password']
    except KeyError:
        abort(400)

    try:
        user = AUTH.register_user(email, password)
    except ValueError:
        message = {"message": "email already registered"}
        return jsonify(message), 400

    message = {"email": user.email, "message": "user created"}
    return jsonify(message)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
