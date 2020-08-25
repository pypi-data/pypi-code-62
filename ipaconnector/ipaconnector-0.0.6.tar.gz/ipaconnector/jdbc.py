import jaydebeapi

from ipaconnector.klass import LoggingClass


class JdbcDriver(LoggingClass):
    HIVE_DRIVER = "org.apache.hive.jdbc.HiveDriver"

    def __init__(self, host, principal, port=10000, db="default"):
        self.url = f"jdbc:hive2://{host}:{port}/{db};principal={principal};ssl=true"
        self.connection = None
        self.cursor = None

    def connect(self):
        if not self.connection:
            self.connection = jaydebeapi.connect(self.HIVE_DRIVER, self.url)

    def disconnect(self):
        self.connection.close()

    def query(self, sql):
        self._log.debug(f"HIVE: {sql}")
        self.cursor.execute(sql)
        output = self.cursor.fetchall()
        self._log.debug(f"HIVE_output: {output}")
        return output

    def __enter__(self):
        if not self.connection:
            self.connect()
        if not self.cursor:
            self.cursor = self.connection.cursor()
        return self.cursor

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.cursor:
            self.cursor.close()
        self.disconnect()


class Hive(LoggingClass):
    def __init__(self, jdbc: JdbcDriver):
        self._jdbc = jdbc
        if not self._jdbc.connection:
            self._jdbc.connect()

    def show_databases(self):
        output = self._jdbc.query("show databases")
        return [db_name[0] for db_name in output]

    def show_role_grant_group(self, group):
        output = self._jdbc.query(f"SHOW ROLE GRANT GROUP `{group}`")
        return [grant[0] for grant in output]

    def show_grant_role(self, role):
        output = self._jdbc.query(f"SHOW GRANT ROLE `{role}`")
        return [grant[0] for grant in output]

    def create_database(self, dbname, uri=None, description="DB created automatically"):
        if not uri:
            uri = self._generate_uri(dbname)
        self._log.info(f"Creating DB {dbname} at {uri} with comment {description}")
        self._jdbc.query(f"CREATE DATABASE `{dbname}` COMMENT `{description}` LOCATION '{uri}'")
        return dbname, uri

    def create_role(self, role_name):
        self._log.info(f"Creating role {role_name}")
        self._jdbc.query(f"CREATE ROLE `{role_name}`")

    def grant_access_to_db(self, db, uri, role, permissions="ALL"):
        permissions = permissions.upper()
        self._log.info(f"Grant {permissions} to DB {db} on {uri} to {role}")
        self._jdbc.query(f"GRANT {permissions} ON DATABASE `{db}` TO ROLE `{role}`")
        # Grant ALL on URI only if necessary
        if any(perm in ["ALL", "CREATE", "INSERT"] for perm in permissions.upper().split(',')):
            self._jdbc.query(f"GRANT ALL ON URI '{uri}' TO ROLE `{role}`")

    def add_group_to_role(self, group, role):
        self._log.info(f"Adding group {group} to {role}")
        self._jdbc.query(f"GRANT ROLE `{role}` TO GROUP `{group}`")

    def revoke_old_role(self, role):
        self._log.info(f"Revoke role {role}")
        self._jdbc.query(f"REVOKE ROLE `{role}`")

    def _generate_uri(self, dbname):
        splitted_name = dbname.split("_")
        first_part = "_".join(splitted_name[:2])
        return f"/data/{first_part}/{splitted_name[2]}/{splitted_name[3]}"
