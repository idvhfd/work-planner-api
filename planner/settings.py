import os


class DefaultConfig:
    SQLALCHEMY_DATABASE_URI = ''
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevelopmentConfig(DefaultConfig):
    DEBUG = True

    dev_db_host = os.environ.get('PLANNER_DEV_DB_HOST', 'localhost')
    dev_db_port = os.environ.get('PLANNER_API_DEV_DB_PORT', '5432')

    SQLALCHEMY_DATABASE_URI = f'postgresql://planner:planner@{dev_db_host}:{dev_db_port}/planner'

    del dev_db_host
    del dev_db_port


class TestingConfig(DefaultConfig):
    DEBUG = True

    test_db_host = os.environ.get('PLANNER_TEST_DB_HOST', 'localhost')
    SQLALCHEMY_DATABASE_URI = f'postgresql://planner:planner@{test_db_host}:5432/planner_test'

    del test_db_host


env_configs = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
}
