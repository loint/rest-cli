import re
import json
import os.path
import mysql.connector

__author__ = "Loi Nguyen <loinguyentrung@gmail.com>"


class Helper:
    def __init__(self):
        pass

    @staticmethod
    def get_absolute_path(local_path):
        """
        Resolve absolute path
        :param local_path:
        :return:
        """
        real_path = os.path.abspath(local_path)
        return real_path

    @staticmethod
    def convert_camel_to_description(camel_name):
        """
        Convert camel name to description
        For example: UserRepository => User Repository
        :param camel_name:
        :return:
        """
        name_components = Helper.split_camel_case(camel_name)
        description_with_space = ''
        for name_component in name_components:
            description_with_space += name_component + ' '
        return description_with_space.strip()

    @staticmethod
    def camel_case_to_snake_case(name):
        """
        Convert camel case to snake case

        :param name: string
        :return: string
        """
        string = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
        string = re.sub('(.)([0-9]+)', r'\1_\2', string)
        result = re.sub('([a-z0-9])([A-Z])', r'\1_\2', string).lower()
        return result

    @staticmethod
    def snake_case_to_camel_case(name):
        """
        Convert snake case to camel case

        :param name: string
        :return: string
        """
        name_components = name.split('_')
        camel_case_name = ''
        for name_component in name_components:
            camel_case_name += name_component[0].upper() + name_component[1:]
        return camel_case_name

    @staticmethod
    def split_camel_case(camel_case_name):
        """
        Split camel case word to single words
        For example: UserRepository will be split to ["User", "Repository"]
        :param camel_case_name:
        :return:
        """
        return re.sub('(?!^)([A-Z][a-z]+)', r' \1', camel_case_name).split()

    @staticmethod
    def get_absolute_path_from_local_path(local_path):
        """
        Resolve absolute path from local path
        :param local_path:
        :return:
        """
        absolute_path = Helper.get_absolute_path(os.getcwd() + "/" + local_path)
        return absolute_path

    @staticmethod
    def read_configuration(config_file):
        """
        Read configuration from .env file

        :param config_file: string
        :return: dict
        """
        config_file = Helper.get_absolute_path_from_local_path(config_file)
        if not os.path.isfile(config_file):
            print("Rest configuration does not exist !")
            exit(1)
        config = {}
        with open(config_file, 'r') as f:
            config = json.load(f)
        return config

    @staticmethod
    def connect_database():
        """
        Establish new connection to mysql
        :return: config, connection, cursor
        """
        config = Helper.read_configuration("./rest.json")
        db_host = ''
        db_name = ''
        db_username = ''
        db_password = ''
        if config['mysql']['host']:
            db_host = config['mysql']['host']
        if config['mysql']['database']:
            db_name = config['mysql']['database']
        if config['mysql']['username']:
            db_username = config['mysql']['username']
        if config['mysql']['database']:
            db_password = config['mysql']['password']
        connection = mysql.connector.connect(
            user=db_username,
            password=db_password,
            host=db_host,
            database=db_name,
            raise_on_warnings=True
        )
        cursor = connection.cursor()
        cursor.execute("USE `" + db_name + "`")
        return config, connection, cursor

    @staticmethod
    def execute_with_cursor(cursor, query):
        cursor.execute(query)
        return cursor.fetchall()

    @staticmethod
    def bind(template, params):
        """
        Bind params in to template

        :param template:
        :param params:
        :return: string
        """
        for variable in params:
            template = template.replace('{' + variable + '}', str(params[variable]))
        return template.strip()