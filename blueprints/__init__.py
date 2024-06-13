
from .comic import comic
from .finish import finish
from .main import main
from .update import update
from .watch import watch


def register_blueprints(app):
    app.register_blueprint(comic)
    app.register_blueprint(finish)
    app.register_blueprint(main)
    app.register_blueprint(update)
    app.register_blueprint(watch)
