from flask import Response, request
from database.models import books, User
from flask_restful import Resource
import datetime
from flask_jwt_extended import create_access_token
from flask_jwt_extended.view_decorators import jwt_required

class booksAPI(Resource):

    @jwt_required
    def get(self):
        book = books.objects().to_json()
        return Response(book, mimetype="application/json", status=200)
    
    @jwt_required
    def post(self):
        body = request.get_json()
        book = books(**body).save()
        b_id =  book.b_id
        return {'id' : str(b_id)}, 200
    
class booksById(Resource):

    @jwt_required
    def get(self, id):
        book = books.objects.get(b_id= id).to_json()
        return Response(book, mimetype="application/json", status=200)
    
    @jwt_required
    def put(self, id):
        body = request.get_json()
        books.objects.get(b_id=id).update(**body)
        return {'Book data updated Successfull!!': body}

    @jwt_required
    def delete(self, id):
        book = books.objects.get(b_id=id).delete()
        return ('Book deleted successfully')

class RegisterApi(Resource):
    
    def post(self):
        body = request.get_json()
        user = User(**body)
        user.hash_password()
        user.save()
        id = user.id
        return {'id': str(id)}, 200

class LoginApi(Resource):

    def post(self):
        body = request.get_json()
        user = User.objects.get(email = body.get('email'))
        authorised = user.check_password(body.get('password'))
        if not authorised:
            return {'error': 'Invalid Credentials'}, 401
        expiry = datetime.timedelta(days=1)
        access_token = create_access_token(identity= str(user.id), expires_delta= expiry)
        return {'token': access_token}, 200