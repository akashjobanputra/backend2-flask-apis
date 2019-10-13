from flask import jsonify


def set_errors(app):

    @app.errorhandler(404)
    def page_not_found(e):
        response = jsonify({'error': 'not found'})
        response.status_code = 404
        return response

    @app.errorhandler(500)
    def internal_server_error(e):
        response = jsonify({'error': 'internal server error'})
        response.status_code = 500
        return response
