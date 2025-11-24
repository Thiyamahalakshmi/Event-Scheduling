import os
from flask import Flask
from .extensions import db, migrate
def create_app():
    app = Flask(__name__, instance_relative_config=True, static_folder='static', template_folder='templates')
    app.config.from_object('config.Config')
   
    try:
        os.makedirs(app.instance_path, exist_ok=True)
    except OSError:
        pass
    db.init_app(app)
    migrate.init_app(app, db)
 
    from .event.routes import bp as event_bp
    from .resource.routes import bp as resource_bp
    from .allocation.routes import bp as allocation_bp
    from .reports.routes import bp as reports_bp
    from .api.routes import bp as api_bp

    app.register_blueprint(event_bp, url_prefix='/events')
    app.register_blueprint(resource_bp, url_prefix='/resources')
    app.register_blueprint(allocation_bp, url_prefix='/allocations')
    app.register_blueprint(reports_bp, url_prefix='/reports')
    app.register_blueprint(api_bp, url_prefix='/api')

    @app.route('/')
    def index():
        return app.send_static_file('index.html')

    return app
