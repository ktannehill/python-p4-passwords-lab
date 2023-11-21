#!/usr/bin/env python3

from flask import request, session
from flask_restful import Resource

from config import app, db, api
from models import User

class ClearSession(Resource):

    def delete(self):
    
        session['page_views'] = None
        session['user_id'] = None

        return {}, 204

class Signup(Resource):
    
    def post(self):
        json = request.get_json()
        user = User(
            username=json['username'],
            password_hash=json['password']
        )
        db.session.add(user)
        db.session.commit()
        return user.to_dict(), 201

class CheckSession(Resource):

    def get(self):
        user_id = session.get('user_id')
        if user_id:
            user = db.session.get(User, user_id)
            return user.to_dict(), 200
        return {'error': f'No user {id}'}, 404

class Login(Resource):
    
    def post(self):
        username = request.get_json().get('username')
        user = User.query.filter_by(username=username).first()

        if user:
            session['user_id'] = user.id
            return user.to_dict(), 200
        return {}, 401

class Logout(Resource):
    
    def delete(self):
        session['user_id'] = None
        return {}, 204

api.add_resource(ClearSession, '/clear', endpoint='clear')
api.add_resource(Signup, '/signup', endpoint='signup')

if __name__ == '__main__':
    app.run(port=5555, debug=True)
