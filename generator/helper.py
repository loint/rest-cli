import re
import os.path
import mysql.connector

__author__ = "Loi Nguyen <loinguyentrung@gmail.com>"

ENV_PATH = ".env"
BIND_PATH = "config/bind.php"
MODEL_PATH = "app/Models"
REPOSITORY_PATH = "app/Repositories"


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
        absolute_path = Helper.get_absolute_path(__file__ + "/../../" + local_path)
        return absolute_path

    @staticmethod
    def read_configuration(config_file):
        """
        Read configuration from .env file

        :param config_file: string
        :return: dict
        """
        config_file = Helper.get_absolute_path_from_local_path(config_file)
        config = {}
        with open(config_file, 'r') as stream:
            lines = stream.read()
            key_value_pairs = lines.split('\n')
            for key_value_pair in key_value_pairs:
                if len(key_value_pair) > 0:
                    pair = key_value_pair.split('=')
                    if len(pair) == 2:
                        config[pair[0]] = pair[1]
        return config

    @staticmethod
    def connect_database():
        """
        Establish new connection to mysql
        :return: config, connection, cursor
        """
        config = Helper.read_configuration(ENV_PATH)
        db_host = 'localhost'
        db_name = 'test'
        db_username = ''
        db_password = ''
        if config['DB_HOST']:
            db_host = config['DB_HOST']
        if config['DB_DATABASE']:
            db_name = config['DB_DATABASE']
        if config['DB_USERNAME']:
            db_username = config['DB_USERNAME']
        if config['DB_PASSWORD']:
            db_password = config['DB_PASSWORD']
        connection = mysql.connector.connect({
            'user': db_username,
            'password': db_password,
            'host': db_host,
            'database': db_name,
            'raise_on_warnings': True,
        })
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