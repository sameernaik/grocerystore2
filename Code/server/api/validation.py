from flask import make_response
class NotFoundError(Exception):
    code=404
    description="Not Found Error"
    
class InternalServerError(Exception):
    code=500
    description="Internal Server Error"