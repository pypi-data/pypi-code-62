#Copyright 2018 Infosys Ltd.
#Use of this source code is governed by Apache 2.0 license that can be found in the LICENSE file or at
#http://www.apache.org/licenses/LICENSE-2.0  .
# This is the component which has all the snowflake execution functions
# Get a snowflake connection
# Run a query against snowflake and get the results
# Set the database, schema and warehouse for execution

import snowflake.connector as sf
import logging as logger
import logging
import os
from constants import constants
from utilities import sfconnection, read_conf_file, queryresult

logger.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.StreamHandler()
    ]
)

class Snowflakeconnection:


    def __init__(self,profilename,privatekey=''):
        self.profilename = profilename
        self.privatekey = privatekey
        queryresult.clear()


    def get_snowflake_connection_withpk(self,conf_file_path=None):
        """
        This function will be used to setup a connection using private key
        :return: Returns the snowflake connection mentioned in the .ini file. The calling program must pass the
        private key to make the connection
        """
        queryresult.clear()
        configparser = read_conf_file(conf_file_path)
        userid = configparser.get(self.profilename,'userid')
        privatekey = self.privatekey
        account = configparser.get(self.profilename,'account')
        role = configparser.get(self.profilename, 'role')
        warehouse = configparser.get(self.profilename,'warehouse')
        database = configparser.get(self.profilename,'database')
        schema = configparser.get(self.profilename,'schema')

        try:
            connection = sf.connect(user=userid,private_key=privatekey,account=account)
            self.use_role(connection, role)
            self.use_database(connection,database)
            self.use_schema(connection,schema)
            self.use_warehouse(connection,warehouse)
            sfconnection['connection'] = connection
            statusmessage = "Successfully connected to database {dbname}".format(dbname=database)
            sfconnection['statusmessage'] = statusmessage
            statuscode = constants.CON000
            sfconnection['statuscode'] = statuscode
            print('--------------------------------------------------')
            print('--------------Connection Established--------------')
            print('--------------------------------------------------')
            return sfconnection
        except Exception as e:
            connresult = 'Error message is {exception}'.format(exception=e)
            sfconnection['connection'] = connresult
            statusmessage = "Failed to conect database {dbname}".format(dbname=database)
            sfconnection['statusmessage'] = statusmessage
            statuscode = constants.CON002
            sfconnection['statuscode'] = statuscode
            print('--------------------------------------------------')
            print('----------------Connection Failed-----------------')
            print('--------------------------------------------------')
            return sfconnection

    def get_snowflake_connection(self, conf_file_path=None):

        """
        This function will be used to setup a connection using password. Password needs to be in conf file

        """
        queryresult.clear()
        configparser = read_conf_file(conf_file_path)
        userid = configparser.get(self.profilename,'userid')
        password = configparser.get(self.profilename,'password')
        role = configparser.get(self.profilename,'role')
        account = configparser.get(self.profilename,'account')
        warehouse = configparser.get(self.profilename,'warehouse')
        database = configparser.get(self.profilename,'database')
        schema = configparser.get(self.profilename,'schema')


        try:
            connection = sf.connect(user=userid,password=password,account=account)
            self.use_role(connection,role)
            self.use_database(connection,database)
            self.use_schema(connection,schema)
            self.use_warehouse(connection,warehouse)

            sfconnection['connection'] = connection
            statusmessage = "Successfully connected to database: {dbname} schema: {schemaname} warehouse: {whname}".format(dbname=database,schemaname=schema,whname=warehouse)
            sfconnection['statusmessage'] = statusmessage
            statuscode = constants.CON000
            sfconnection['statuscode'] = statuscode
            print('--------------------------------------------------')
            print('--------------Connection Established--------------')
            print('Database :{}'.format(database))
            print('Role :{}'.format(role))
            print('Schema :{}'.format(schema))
            print('Warehouse :{}'.format(warehouse))
            print('--------------------------------------------------')
            return sfconnection
        except Exception as e:
            connresult = 'Error message is {exception}'.format(exception=e)
            sfconnection['connection'] = connresult
            statusmessage = "Failed to conect database {dbname}".format(dbname=database)
            sfconnection['statusmessage'] = statusmessage
            statuscode = constants.CON002
            sfconnection['statuscode'] = statuscode
            print('--------------------------------------------------')
            print('----------------Connection Failed-----------------')
            print('--------------------------------------------------')
            return sfconnection

    def use_database(self,connection,database):
        """
        This function will set the database for the session

        """
        queryresult.clear()
        try:
            snowquerystring = 'use {dbname}'.format(dbname=database)
            result = self.execute_snowquery(connection,snowquerystring)
            queryresult['result'] = result
            statusmessage = 'Query executed successfully'
            queryresult['statusmessage'] = statusmessage
            statuscode = constants.EXE000
            queryresult['statuscode'] = statuscode
            return queryresult
        except Exception as e:
            result = 'Error message is {exception}'.format(exception=e)
            queryresult['result'] = result
            statusmessage = 'Query failed to execute'
            queryresult['statusmessage'] = statusmessage
            statuscode = constants.EXE001
            queryresult['statuscode'] = statuscode
            return queryresult

    def use_role(self,connection,role):
        """
        This function will set the role for the session

        """
        queryresult.clear()
        try:
            snowquerystring = 'use role {rolename}'.format(rolename=role)
            result = self.execute_snowquery(connection,snowquerystring)
            queryresult['result'] = result
            statusmessage = 'Query executed successfully'
            queryresult['statusmessage'] = statusmessage
            statuscode = constants.EXE000
            queryresult['statuscode'] = statuscode
            return queryresult
        except Exception as e:
            result = 'Error message is {exception}'.format(exception=e)
            queryresult['result'] = result
            statusmessage = 'Query failed to execute'
            queryresult['statusmessage'] = statusmessage
            statuscode = constants.EXE001
            queryresult['statuscode'] = statuscode
            return queryresult


    def use_schema(self,connection,schema):
        """
        This function will set the schema for the session

        """
        queryresult.clear()
        try:
            snowquerystring = 'use schema {schemaname}'.format(schemaname=schema)
            result = self.execute_snowquery(connection,snowquerystring)
            queryresult['result'] = result
            statusmessage = 'Query executed successfully'
            queryresult['statusmessage'] = statusmessage
            statuscode = constants.EXE000
            queryresult['statuscode'] = statuscode
            return queryresult

        except Exception as e:
            result = 'Error message is {exception}'.format(exception=e)
            queryresult['result'] = result
            statusmessage = 'Query failed to execute'
            queryresult['statusmessage'] = statusmessage
            statuscode = constants.EXE001
            queryresult['statuscode'] = statuscode
            return queryresult

    def use_warehouse(self,connection,warehouse):
        """
        This function will set the warehouse for the session

        """
        queryresult.clear()
        try:
            snowquerystring = 'use warehouse {whname}'.format(whname=warehouse)
            result = self.execute_snowquery(connection,snowquerystring)
            queryresult['result'] = result
            statusmessage = 'Query executed successfully'
            queryresult['statusmessage'] = statusmessage
            statuscode = constants.EXE000
            queryresult['statuscode'] = statuscode
            return queryresult
        except Exception as e:
            result = 'Error message is {exception}'.format(exception=e)
            queryresult['result'] = result
            statusmessage = 'Query failed to execute'
            queryresult['statusmessage'] = statusmessage
            statuscode = constants.EXE001
            queryresult['statuscode'] = statuscode
            return queryresult

    def execute_snowquery(self,connection,snowquerystring,asyncflag=False):
        """
        This function takes the query as input and outputs the result of query. If the asyncflag is true
        the function will submit the query to snowflake and will immediately return without waiting for the
        results of the query. It will return the query id which can be tracked to find out the completion of the
        query. The async method can be used in case of large queries that may take a longer time to execute
        :param connection: The sonowflake connection that will be used to execute the query
        :param snowquerystring: The actual query to be executed
        :param asyncflag: True - query will be submitted in asynchronous mode, False is default
        :return: Return the queryresult dictionary
        """


        queryresult.clear()

        if asyncflag:
            try:
                print('-------------Asynchronous call to snowflake-------------')
                cursor = connection.cursor()
                result= cursor.execute(snowquerystring,_no_results=True)
                queryid = cursor.sfqid
                queryresult['queryid'] = queryid
                queryresult['result'] = result
                statusmessage = 'Query submitted to snowflake'
                queryresult['statusmessage']=statusmessage
                statuscode = constants.EXE000
                queryresult['statuscode']=statuscode
                return queryresult
            except Exception as e:
                result = 'Error message is {exception}'.format(exception=e)
                queryresult['result'] = result
                statusmessage = 'Query failed to execute'
                queryresult['statusmessage'] = statusmessage
                statuscode = constants.EXE001
                queryresult['statuscode'] = statuscode
                return queryresult
            finally:
                if connection is None:
                    pass
                else:
                    cursor.close()


        try:
            cursor = connection.cursor()
            cursor.execute(snowquerystring)
            result = cursor.fetchall()
            queryresult['queryid'] = cursor.sfqid
            queryresult['result'] = result
            statusmessage = 'Query executed successfully'
            queryresult['statusmessage']=statusmessage
            statuscode = constants.EXE000
            queryresult['statuscode']=statuscode
            return queryresult
        except Exception as e:
            result = 'Error message is {exception}'.format(exception=e)
            queryresult['queryid'] = cursor.sfqid
            queryresult['result'] = result
            statusmessage = 'Query failed to execute'
            queryresult['statusmessage']=statusmessage
            statuscode = constants.EXE001
            queryresult['statuscode']=statuscode
            return queryresult
        finally:
            if connection is None:
                pass
            else:
                cursor.close()

    def execute_stream(self,connection,queryfile):
        """
        This function will take a script file as input and will execute all the queries in the file
        one by one. The calling program must retrieve the result from the queryresult dictionary
        and loop through the result to get the output of each query
        :param connection: The connection that will be used to execute the script
        :param queryfile: The text file which has all the queries that will be executed
        :return: Returns queryresult dictionary
        """
        queryresult.clear()
        try:
            filename = open(queryfile,'r',encoding='utf-8')
            result = connection.execute_stream(filename)
            queryresult['queryid'] = ''
            queryresult['result'] = result
            statusmessage = 'Script successfully executed'
            queryresult['statusmessage']=statusmessage
            statuscode = constants.EXE000
            queryresult['statuscode']=statuscode
            return queryresult
        except Exception as e:
            result = 'Error message is {exception}'.format(exception=e)
            queryresult['queryid'] = ''
            queryresult['result'] = result
            statusmessage = 'Script failed to execute'
            queryresult['statusmessage']=statusmessage
            statuscode = constants.EXE001
            queryresult['statuscode']=statuscode
            return queryresult

    def execute_put_cmd(self, connection=None, local_file_path=None, sf_stage_type="NAMED_STAGE",
                        stage_name=None, table_name=None, user_stage_folder=None,
                        num_of_threads=None):
        """
        This function will take a local file path and internal stage name as inputs and will upload(PUT command)
        the local files to snowflake internal stage. The calling program must retrieve the result from the queryresult
        dictionary and loop through the result to get the status of the PUT command
        :param connection: The connection that will be used to execute the script
        :param local_file_path: Local path of the files to be uploaded or staged
        :param sf_stage_type: Type of internal snowflake stage i.e NAMED_STAGE, USER_STAGE, TABLE_STAGE
        :param table_name: Name of the table stage, when sf_stage_type = TABLE_STAGE
        :param user_stage_folder: Name of the user subfolder, when sf_stage_type = USER_STAGE
        :param num_of_threads: Number of parallel threads for PUT Command
        :return: Returns queryresult dictionary
        """
        queryresult = {}
        try:
            # Fetch default SF connection, if not provided as input
            if not connection:
                logger.info("Fetching default snowflake connection ")
                connection = self.get_snowflake_connection()
                if not connection:
                    status_message = "Error fetching default snowflake connection"
                    logger.error(status_message)
                    raise Exception(status_message)

            logger.info("Constructing PUT command with the provided function parameters")

            # Validating and adding Local file path in PUT command
            if not local_file_path:
                status_message = constants.NO_LOCAL_FILE_PATH
                logger.error(status_message)
                raise Exception(status_message)
            local_file_path = local_file_path.replace(os.sep, '/')
            put_cmd_str = str("put ").__add__("'").__add__('file://').__add__(local_file_path).__add__("' ")

            # Validation of SF stage type & associated input parameters and adding the same in PUT command
            if constants.SF_NAMED_STAGE.__eq__(sf_stage_type.upper()):
                if stage_name:
                    logger.info("Altering PUT command to support Named Stage")
                    put_cmd_str = put_cmd_str.__add__("@").__add__(stage_name)
                else:
                    status_message = "Named Stage name is not provided"
                    raise Exception(status_message)
            elif constants.SF_TABLE_STAGE.__eq__(sf_stage_type.upper()):
                if table_name:
                    logger.info("Altering PUT command to support Table Stage")
                    put_cmd_str = put_cmd_str.__add__("@%").__add__(table_name)
                else:
                    status_message = "Table Name is not provided for table stage"
                    raise Exception(status_message)
            elif constants.SF_USER_STAGE.__eq__(sf_stage_type.upper()):
                if user_stage_folder:
                    logger.info("Adding staging to specific user folder in PUT command : " + user_stage_folder)
                    put_cmd_str = put_cmd_str.__add__("@~/").__add__(user_stage_folder)
                else:
                    logger.info("Adding staging to default user folder in PUT command")
                    put_cmd_str = put_cmd_str.__add__("@~/").__add__("staged")
            else:
                status_message = "SF Stage provided is invalid "
                raise Exception(status_message)

            # Adding PARALLELISM and compression in PUT command
            if num_of_threads:
                logger.getLogger().info("Adding parallelism in PUT command")
                put_cmd_str = put_cmd_str.__add__(" PARALLEL = ").__add__(str(num_of_threads))

            logger.info("Constructed PUT comand : "+ put_cmd_str)
            # Executing PUT command using snowflake connection
            queryresult = self.execute_snowquery(connection, put_cmd_str)
            return queryresult
        except Exception as e:
            result = 'Error message is {exception}'.format(exception=e)
            queryresult['queryid'] = ''
            queryresult['result'] = result
            statusmessage = 'Script failed to execute'
            queryresult['statusmessage'] = statusmessage
            statuscode = constants.EXE001
            queryresult['statuscode'] = statuscode
            logger.error(result)
            return queryresult
