from flask import Flask
from config import Config
import db as database

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    app.config["MYSQL_HOST"]     = Config.MYSQL_HOST
    app.config["MYSQL_PORT"]     = Config.MYSQL_PORT
    app.config["MYSQL_USER"]     = Config.MYSQL_USER
    app.config["MYSQL_PASSWORD"] = Config.MYSQL_PASSWORD
    app.config["MYSQL_DB"]       = Config.MYSQL_DB
    app.secret_key = Config.SECRET_KEY

    database.init_app(app)

    app.jinja_env.filters["enumerate"] = enumerate

    from routes.dashboard import bp as dashboard_bp
    from routes.reports   import bp as reports_bp
    from routes.filters   import bp as filters_bp

    app.register_blueprint(dashboard_bp)
    app.register_blueprint(reports_bp)
    app.register_blueprint(filters_bp)

    return app

app = create_app()

if __name__ == "__main__":
    app.run(debug=False)
