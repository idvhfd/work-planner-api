import os

from flask import Blueprint, Flask
from flask_migrate import Migrate
from flask_rest_jsonapi import Api
from flask_sqlalchemy import SQLAlchemy

from planner.settings import env_configs

db = SQLAlchemy()
migrate = Migrate(db=db)


def create_app(env: str = None, agent: bool = False) -> Flask:
    """Create and initialize a Flask application object."""

    if env is None:
        env = os.environ.get('PLANNER_API_ENV', 'development')
        assert env is not None

    app = Flask(__name__)

    app.config['ENV'] = env
    app.config.from_object(env_configs[env])
    app.config.from_envvar('PLANNER_API_SETTINGS', silent=True)

    if agent:
        return app

    db.init_app(app)

    # register API blueprint
    from planner.routes import register_routes
    api = Api()
    api_app = Blueprint('api_app', __name__, url_prefix='/api')
    register_routes(api)
    api.init_app(app=app, blueprint=api_app)

    from planner.controllers.workers_shifts_stats import workers_shifts_stats
    app.register_blueprint(workers_shifts_stats)

    from planner.cli import create_workers
    app.cli.add_command(create_workers)

    from planner.cli import create_shifts
    app.cli.add_command(create_shifts)

    from planner.cli import create_workers_shifts
    app.cli.add_command(create_workers_shifts)

    migrate.init_app(app)

    return app
