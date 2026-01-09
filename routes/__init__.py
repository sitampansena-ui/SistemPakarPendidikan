from .konsultasi import konsultasi_bp
from flask import render_template

def register_routes(app):
    app.register_blueprint(konsultasi_bp)

    # Rute Home
    @app.route('/')
    def index():
        return render_template('index.html')
    
    @app.route('/about')
    def about(): # Nama fungsi ini harus 'about'
        return render_template('about.html')