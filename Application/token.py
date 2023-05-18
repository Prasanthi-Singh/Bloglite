# flask imports
from flask import Flask, request, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from flask import current_app as app
#import uuid # for public id
from flask_restful import abort
from  werkzeug.security import generate_password_hash, check_password_hash
# imports for PyJWT authentication
import jwt
from datetime import datetime, timedelta
from functools import wraps
from Application.models import User

def token_r(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
    
        if 'Token' in request.headers:
            token = request.headers['Token']
        
        # print(token)
        if not token:
            abort(401, message='Token is not passed')

        try:
            
            data = jwt.decode(token, app.config['SECRET_KEY'],algorithms = ["HS256"])
        except jwt.ExpiredSignatureError :
           
            abort(401, message='Token is invalid')
            
       
        return  f( *args, **kwargs)
  
    return decorated
