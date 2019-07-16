import yaml
from sqlalchemy import create_engine
from sqlalchemy_utils import create_database, database_exists
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()
from sqlalchemy.orm.session import sessionmaker

class Db():
    _session = None

    @staticmethod
    def load_db_config(file = 'config.yaml'):
        """ Load the database configuration.

        :param file: The path of the config file.
        :return: Database host, database name, database user and database password
        """

        with open(file, 'r') as stream:
            config = yaml.safe_load(stream)
            db_config = config['database']
            return db_config['db_host'], db_config['db_name'], db_config['db_user'], db_config['db_pw']

    @staticmethod
    def setup_db():
        """ Sets up the database session according to the config.yaml file.

        :return: The setup database session.
        """
        db_host, db_name, db_user, db_password = Db.load_db_config()
        database_string = 'mysql://%s:%s@%s/%s' % (db_user, db_password, db_host, db_name)
        print(db_host)
        print('_'*30)
        #if not database_exists(database_string):
        #    create_database(database_string)

        engine = create_engine(database_string, echo=True)
        Base.metadata.create_all(engine)
        Session = sessionmaker(bind=engine)
        print("Connected to db")
        return Session()

    @staticmethod
    def get_db_session():
        if Db._session is None:
            session = Db.setup_db()
            return session
        else:
            return Db._session
