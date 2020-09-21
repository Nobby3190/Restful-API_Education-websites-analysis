import flask
from flask_restful import Api, Resource
from flask import jsonify
from flask import request
from resources.test import tests,test


app = flask.Flask(__name__)
app.config["DEBUG"] = True
app.config['JSON_AS_ASCII'] = False
api = Api(app)
api.add_resource(tests,'/tests')
api.add_resource(test,'/test/<title>')



# @app.route('/',methods = ['GET'])
# def home():
#     return "<h2>hello world</h2>"

# @app.errorhandler(Exception)
# def handle(error):
#     code = 500
#     if type(error.__name__=="NotFound"):
#         code = 404
#     return {
#         'msg':type(error).__name__
#     },code

# @app.before_request
# def auth():
#     token = request.headers.get('auth')
#     if token == 'Pn123456':
#         pass
#     else:
#         code = 401
#         return{
#             'msg':'invalid token',
#         },code

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=3333)

        
    