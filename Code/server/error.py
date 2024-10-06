from flask import render_template,jsonify
from api.validation import NotFoundError,InternalServerError
def defineErrorRoutes(app):
       
        @app.errorhandler(404) 
        def invalid_route(e): 
                return render_template('404.html'),404
        
        
        @app.errorhandler(NotFoundError)
        def handle_exception(err):
                response = {
                "error": err.description, 
                }
                if len(err.args) > 0:
                        response["message"] = err.args[0]
                return response["message"], err.code
        
        @app.errorhandler(InternalServerError)
        def handle_server_exception(err):
                response = {
                "error": err.description, 
                }
                if len(err.args) > 0:
                        response["message"] = err.args[0]
                return response["message"], err.code