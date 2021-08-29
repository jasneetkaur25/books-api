from .books import booksAPI, booksById, RegisterApi, LoginApi

def initialize_route(api):
    api.add_resource(booksAPI,'/books')
    api.add_resource(booksById,'/books/<id>')
    api.add_resource(RegisterApi,'/auth/register')
    api.add_resource(LoginApi,'/auth/login')