import peewee as pee


class ZormPgConnect():

    @classmethod
    def db_config(cls,
                  db_name: str = None,
                  user: str = None,
                  password: str = None,
                  host: str = None,
                  port: int = 5432,
                  autorollback: bool = True,
                  ):
        cls.db = pee.PostgresqlDatabase(
            db_name,
            user=user,
            password=password,
            host=host,
            port=port,
            autorollback=autorollback
        )

    db = None
