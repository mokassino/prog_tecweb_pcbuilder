from flask import Flask

def create_app():
    app = Flask(__name__, instance_relative_config=True)

    from app.controller import (
        main
    )
    app.register_blueprint(main.bp)

    return app