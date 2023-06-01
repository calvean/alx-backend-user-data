#!/usr/bin/env python3
""" Session DB Authentication """
from api.v1.auth.session_exp_auth import SessionExpAuth
from models.user_session import UserSession
from datetime import datetime, timedelta
from typing import Optional
from flask import Request


class SessionDBAuth(SessionExpAuth):
    """ Session DB Authentication """

    def create_session(self, user_id: Optional[str] = None) -> Optional[str]:
        """ Creates and stores new instance of UserSession """
        session_id = super().create_session(user_id)
        if session_id:
            session = UserSession(user_id=user_id, session_id=session_id)
            session.save()
            return session_id
        return None

    def user_id_for_session_id(
      self, session_id: Optional[str] = None) -> Optional[str]:
        """ Returns the User ID by requesting UserSession
         in the database based on session_id """
        if session_id is None:
            return None
        user_id = super().user_id_for_session_id(session_id)
        if user_id:
            session = UserSession.get(session_id)
            if session:
                session.updated_at = datetime.utcnow()
                session.save()
            return user_id
        return None

    def destroy_session(self, request: Optional[Request] = None) -> bool:
        """ Destroys the UserSession based on the Session ID
         from the request cookie """
        if request is None:
            return False
        session_id = self.session_cookie(request)
        if session_id:
            user_id = self.user_id_for_session_id(session_id)
            if user_id:
                session = UserSession.get(session_id)
                if session:
                    session.remove()
                    return True
        return False
