import os
from helper import Helper
from model_template import MODEL_TEMPLATE, MODEL_CONSTRUCTOR_TEMPLATE, SETTER_GETTER_TEMPLATE
from model_template import REPOSITORY_IMPLEMENTATION_TEMPLATE
from model_template import SERVICE_IMPLEMENTATION_TEMPLATE
from model_template import REPOSITORY_IMPLEMENTATION_BUILTIN_TEMPLATE
from model_template import REPOSITORY_IMPLEMENTATION_FILTER_TEMPLATE
from model_template import REPOSITORY_INTERFACE_TEMPLATE
from model_template import SERVICE_INTERFACE_TEMPLATE
from model_template import REPOSITORY_INTERFACE_BUILTIN_TEMPLATE
from model_template import REPOSITORY_INTERFACE_FILTER_TEMPLATE

__author__ = "Loi Nguyen <loinguyentrung@gmail.com>"


class SchemaUtil:
    """
    Provide a set of functionality manipulate with database schema
    Support data type conversion between PHP and MySQL
    """
    def __init__(self):
        pass

    @staticmethod
    def mysql_to_php_type(mysql_table_name, mysql_column_name, mysql_column_type):
        """
        Convert data type in mysql to php data type
        This is an interceptor allow us to customize when migration
        has new data types

        :param mysql_table_name: string
        :param mysql_column_name: string
        :param mysql_column_type: string
        :return: string
        """
        if mysql_column_type.startswith('tinyint'):
            return 'boolean'
        if mysql_column_type.startswith('smallint'):
            return 'int'
        if mysql_column_type.startswith('int'):
            return 'int'
        if mysql_column_type.startswith('mediumint'):
            return 'int'
        if mysql_column_type.startswith('bigint'):
            return 'int'
        if mysql_column_type.startswith('decimal'):
            return 'float'
        if mysql_column_type.startswith('char'):
            return 'string'
        if mysql_column_type.startswith('varchar') or mysql_column_type.startswith('text'):
            return 'string'
        if mysql_column_type.startswith('time'):
            return '\DateTime'
        if mysql_column_type.startswith('date'):
            return '\DateTime'
        if mysql_column_type.startswith('datetime'):
            return '\DateTime'
        if mysql_column_type.startswith('timestamp'):
            return '\DateTime'
        return 'undefined'

    @staticmethod
    def mysql_default_value(mysql_column_type):
        """
        MySQL Default value for not nullable fields

        :param mysql_column_type: string
        :return: mixed
        """
        if mysql_column_type.startswith('tinyint'):
            return 0
        if mysql_column_type.startswith('smallint'):
            return 0
        if mysql_column_type.startswith('int'):
            return 0
        if mysql_column_type.startswith('mediumint'):
            return 0
        if mysql_column_type.startswith('bigint'):
            return 0
        if mysql_column_type.startswith('decimal'):
            return 0
        if mysql_column_type.startswith('char'):
            return ''
        if mysql_column_type.startswith('varchar') or mysql_column_type.startswith('text'):
            return ''
        if mysql_column_type.startswith('time'):
            return "\Illuminate\Support\Facades\DB::raw('CURRENT_TIMESTAMP')"
        if mysql_column_type.startswith('date'):
            return "\Illuminate\Support\Facades\DB::raw('CURRENT_TIMESTAMP')"
        if mysql_column_type.startswith('datetime'):
            return "\Illuminate\Support\Facades\DB::raw('CURRENT_TIMESTAMP')"
        if mysql_column_type.startswith('timestamp'):
            return 0
        return ''

    @staticmethod
    def convert_table_to_camel_name(table_name):
        """
        Convert table name to camel case
        This is an interceptor allow us to standardize when the
        table names do not have same rules

        :param table_name: string
        :return: string
        """
        return Helper.snake_case_to_camel_case(table_name)

    @staticmethod
    def convert_column_to_camel_name(column_name):
        """
        Convert column name to camel case
        This is an interceptor allow us to standardize when the
        column names are lower or do not have same rules

        :param column_name: string
        :return: string
        """
        return Helper.snake_case_to_camel_case(column_name)

    @staticmethod
    def intercept_filter_set(
            php_model_name,
            php_property_name,
            php_property_type,
            mysql_table_name,
            mysql_column_name,
            mysql_column_type):
        """
        Set filter interceptor
        This is an interceptor allow us to intercept to setter base
        on php types and mysql types

        :param php_model_name: string
        :param php_property_name: string
        :param php_property_type: string
        :param mysql_table_name: string
        :param mysql_column_name: string
        :param mysql_column_type: string
        :return: string
        """
        if mysql_column_type == 'datetime':
            return '''if (null === ${camel_variable_name}) {
            $this->attributes[self::{constant_field_name}] = null;
        } else {
            $this->attributes[self::{constant_field_name}] = ${camel_variable_name}->format(\'Y-m-d H:i:s\');
        }'''
        if mysql_column_type == 'date':
            return '''if (null === ${camel_variable_name}) {
            $this->attributes[self::{constant_field_name}] = null;
        } else {
            $this->attributes[self::{constant_field_name}] = ${camel_variable_name}->format(\'Y-m-d\');
        }'''
        if php_property_type == 'float':
            return '''if (null === ${camel_variable_name}) {
            $this->attributes[self::{constant_field_name}] = null;
        } else {
            $this->attributes[self::{constant_field_name}] = (float) ${camel_variable_name};
        }'''
        if php_property_type == 'int':
            return '''if (null === ${camel_variable_name}) {
            $this->attributes[self::{constant_field_name}] = null;
        } else {
            $this->attributes[self::{constant_field_name}] = (int) ${camel_variable_name};
        }'''
        return '$this->attributes[self::{constant_field_name}] = ${camel_variable_name};'

    @staticmethod
    def intercept_filter_get(
            php_model_name,
            php_property_name,
            php_property_type,
            mysql_table_name,
            mysql_column_name,
            mysql_column_type):
        """
        Get filter interceptor
        This is an interceptor allow us to intercept to getter base
        on php types and mysql types

        :param php_model_name: string
        :param php_property_name: string
        :param php_property_type: string
        :param mysql_table_name: string
        :param mysql_column_name: string
        :param mysql_column_type: string
        :return: string
        """
        if mysql_column_type == 'datetime':
            return '''$dateTimeStringValue = $this->attributes[self::{constant_field_name}];
        if (empty($dateTimeStringValue)) {
            return null;
        }
        $dateTimeObject = \DateTime::createFromFormat(\'Y-m-d H:i:s\', $dateTimeStringValue);
        return $dateTimeObject;'''
        if mysql_column_type == 'date':
            return '''$dateTimeStringValue = $this->attributes[self::{constant_field_name}];
        if (empty($dateTimeStringValue)) {
            return null;
        }
        $dateTimeObject = \DateTime::createFromFormat(\'Y-m-d\', $dateTimeStringValue);
        return $dateTimeObject;'''
        if php_property_type == 'float':
            return """$floatValue = $this->attributes[self::{constant_field_name}];
        if (null === $floatValue) {
            return null;
        }
        return (float) $this->attributes[self::{constant_field_name}];"""
        if php_property_type == 'int':
            return """$intValue = $this->attributes[self::{constant_field_name}];
        if (null === $intValue) {
            return null;
        }
        return (int) $this->attributes[self::{constant_field_name}];"""
        return 'return $this->attributes[self::{constant_field_name}];'


class ModelGenerator:
    """
    Model generator
    This generator will collect information from model and
    database then generate setters, getters and constants
    automatically for models
    """
    _model_path = ''
    _repository_path = ''
    _service_path = ''
    _controller_path = ''
    _bind_path = ''
    _config_path = ''
    _identifier = ''
    _models = {}
    _tables = {}
    _config = {}
    _generated_model = ''

    def __init__(self):
        pass

    def set_identifier(self, identifier):
        """
        Set identifier use to separate generated and modified source code

        :param identifier:
        :return:
        """
        self._identifier = identifier

    def config_paths(self):
        require_folders = [
            "src/Model",
            "src/Repository",
            "src/Service",
            "src/Controller"
        ]
        for require_folder in require_folders:
            if not os.path.isdir(require_folder):
                os.makedirs(require_folder)
        self._model_path = Helper.get_absolute_path_from_local_path("src/Model")
        self._repository_path = Helper.get_absolute_path_from_local_path("src/Repository")
        self._service_path = Helper.get_absolute_path_from_local_path("src/Service")
        self._controller_path = Helper.get_absolute_path_from_local_path("src/Controller")
        self._bind_path = Helper.get_absolute_path_from_local_path("src/Dependencies.php")

    def get_tables(self):
        return self._tables

    def get_models(self):
        return self._models

    def scan_models(self):
        """
        Scan all models and collect existing code
        """
        if len(self._model_path) == 0:
            print 'Please set_model_path !'
            exit(1)
        if len(self._identifier) == 0:
            print 'Please set_identifier !'
            exit(1)
        if len(self._generated_model) > 0:
            self.scan_by_model_file_name(self._generated_model + '.php')
        else:
            for model_file_name in os.listdir(self._model_path):
                if model_file_name.endswith('.php'):
                    self.scan_by_model_file_name(model_file_name)

    @staticmethod
    def find_annotations_by_content(model_content):
        """
        Find all annotations by model content

        :return: dict
        """
        selects = []
        updates = []
        deletes = []
        counts = []
        lines = model_content.split('\n')
        for line in lines:
            line = line.strip()
            filter_components = line.split(' ')
            if len(filter_components) > 2:
                if line.startswith('* @select'):
                    selects.append(filter_components[2:])
                if line.startswith('* @update'):
                    updates.append(filter_components[2:])
                if line.startswith('* @delete'):
                    deletes.append(filter_components[2:])
                if line.startswith('* @count'):
                    counts.append(filter_components[2:])
        annotations = {
            '@selects': selects,
            '@updates': updates,
            '@deletes': deletes,
            '@counts': counts
        }
        return annotations

    def scan_by_model_file_name(self, model_file_name):
        """
        Scan by model file name
        :param model_file_name:
        :return:
        """
        # Model name is not include extension ".php" so
        # we need to subtract 4 characters from the end
        model_name = model_file_name[:-4]
        model_file_path = Helper.get_absolute_path(self._model_path + '/' + model_file_name)
        with open(model_file_path, 'r') as stream:
            lines = stream.read().strip()
            model_components = lines.split(self._identifier)
            if len(model_components) != 2:
                print 'Identifier not found in model : ', model_name
                exit(1)
            else:
                model_content = model_components[0]
                annotations = self.find_annotations_by_content(model_content)
                self._models[model_name] = {
                    'content': model_content,
                    'filters': annotations,
                    'file_path': model_file_path
                }

    def scan_database(self):
        """
        Scan database schemas and collect information
        """
        _, _, cursor = Helper.connect_database()
        tables = Helper.execute_with_cursor(cursor, 'SHOW TABLES;')
        for table_name in tables:
            table_name = table_name[0]
            if table_name.startswith('view'):
                continue
            columns = Helper.execute_with_cursor(cursor, 'SHOW COLUMNS FROM ' + table_name + ';')
            if table_name == '_migrations':
                continue
            self._tables[table_name] = []
            for column in columns:
                column_name = column[0]
                column_type = column[1]
                column_default = column[4]
                column_null = True
                if column[2] == "NO":
                    column_null = False
                table = {
                    'php_model_name': SchemaUtil.convert_table_to_camel_name(table_name),
                    'php_property_name': SchemaUtil.convert_column_to_camel_name(column_name),
                    'php_property_type': SchemaUtil.mysql_to_php_type(table_name, column_name, column_type),
                    'mysql_table_name': table_name,
                    'mysql_column_name': column_name,
                    'mysql_column_type': column_type,
                    'mysql_allow_null': column_null,
                    'mysql_column_default': column_default
                }
                self._tables[table_name].append(table)

    @staticmethod
    def __generate_constructor(model_name, columns):
        """
        Generate default constructor and default constructor for model

        :param model_name:
        :param columns:
        """
        default_setters = ''
        for field in columns:
            constant_name = Helper.camel_case_to_snake_case(field['php_property_name']).upper()
            default_value = 'null'
            if not field['mysql_allow_null']:
                default_value = SchemaUtil.mysql_default_value(field['mysql_column_type'])
            if field['mysql_column_default'] is not None:
                default_value = field['mysql_column_default']
            if len(str(default_value)) == 0:
                default_value = '""'
            if default_value == '{}':
                default_value = '"{}"'
            if constant_name.upper() is 'id':
                default_value = 'null'
            default_setters += '        $this->attributes[self::' + constant_name + '] = ' + str(default_value) + ';\n'

        constructor = Helper.bind(MODEL_CONSTRUCTOR_TEMPLATE, {
            'default_setters': default_setters,
            'model_name': model_name
        })
        return constructor

    @staticmethod
    def __generate_setter_getter(model_name, fields):
        """
        Generate setter and getter for models

        :param: model_name string
        :param:  fields array
        :return: string
        """
        set_get_content = ''
        for field in fields:
            camel_field_name = field['php_property_name']
            snake_field_name = Helper.camel_case_to_snake_case(camel_field_name)
            field_set_get_content = SETTER_GETTER_TEMPLATE
            setter_name = camel_field_name
            getter_name = camel_field_name
            if setter_name.startswith('Is'):
                setter_name = 'set' + setter_name[2:]
                getter_name = camel_field_name[0].lower() + camel_field_name[1:]
            else:
                setter_name = 'set' + setter_name
                getter_name = 'get' + getter_name
            # Bind template variables
            field_set_get_content = field_set_get_content.replace(
                '{intercept_filter_set}',
                SchemaUtil.intercept_filter_set(
                    php_model_name=model_name,
                    php_property_name=field['php_property_name'],
                    php_property_type=field['php_property_type'],
                    mysql_table_name=field['mysql_table_name'],
                    mysql_column_name=field['mysql_column_name'],
                    mysql_column_type=field['mysql_column_type']
                )
            )
            field_set_get_content = field_set_get_content.replace(
                '{intercept_filter_get}',
                SchemaUtil.intercept_filter_get(
                    php_model_name=model_name,
                    php_property_name=field['php_property_name'],
                    php_property_type=field['php_property_type'],
                    mysql_table_name=field['mysql_table_name'],
                    mysql_column_name=field['mysql_column_name'],
                    mysql_column_type=field['mysql_column_type']
                )
            )
            field_set_get_content = Helper.bind(field_set_get_content, {
                'table_name': model_name,
                'field_name': field['mysql_column_name'],
                'field_type': field['php_property_type'],
                'camel_field_name': camel_field_name,
                'camel_variable_name': camel_field_name[0].lower() + camel_field_name[1:],
                'constant_field_name': snake_field_name.upper(),
                'method_name': snake_field_name.replace('_', ' '),
                'setter_name': setter_name,
                'getter_name': getter_name
            })
            set_get_content += field_set_get_content + "\n\n    "
        return set_get_content

    def create_model(self, table_name):
        """
        Create model for table if does not exist
        :param table_name:
        """
        if table_name == '_migrations':
            return
        model_name = SchemaUtil.convert_table_to_camel_name(table_name)
        model_name_with_space = ' '.join(Helper.split_camel_case(model_name))
        if model_name not in self._models:
            print 'Detect new table ', table_name
            model_content = Helper.bind(MODEL_TEMPLATE, {
                'model_name': model_name,
                'table_name': table_name,
                'model_name_with_space': model_name_with_space
            })
            model_file_path = self._model_path + '/' + model_name + '.php'
            model = open(model_file_path, 'w')
            model.write(model_content)
            model.close()
            print 'Created new model ', model_name

    def generate_models(self):
        """
        Generate models
        If table in database does not have model then
        we need to create model for developer to use
        If created model does not exist in database
        we need to inform for developer to check the migrations
        """
        for table in self._tables:
            if table not in self._models:
                self.create_model(table)
        for model in self._models:
            table_name = Helper.camel_case_to_snake_case(model)
            if table_name not in self._tables:
                print 'Table ', table_name, ' in database does not exist !'
                exit(1)
            content = self._models[model]['content']
            content += self._identifier + '\n    '
            content += self.__generate_constructor(model, self._tables[table_name])
            content += self.__generate_setter_getter(model, self._tables[table_name])
            content += '\n}\n'
            model_file = open(self._models[model]['file_path'], "w")
            model_file.write(content)
            model_file.close()
            print 'Generated model: ', model

    def scan_model_annotation(self):
        for model in self._models:
            table_name = Helper.camel_case_to_snake_case(model)
            columns = self._tables[table_name]
            filters = self._models[model]['filters']
            filter_fields = {}
            # Filter fields represents set of unique field name in all filters inside one model
            for filter in filters:
                for type in filters[filter]:
                    for field_name in type:
                        filter_fields[field_name] = 1
            # Check field name consistent with database schema
            for filter_field in filter_fields:
                consistent = False
                for column in columns:
                    if filter_field == column['php_property_name']:
                        consistent = True
                        break
                if not consistent:
                    print 'Sorry, can not filter by column "' + model + '.' + filter_field \
                          + '" because it does not exist in database !'
                    exit(1)

    @staticmethod
    def create_service_files(service_folder_path, service_name, model_name):
        """
        Create service files includes: interface and implementation

        :param service_folder_path:
        :param service_name:
        :param model_name:
        """
        service_interface_file_path = Helper.get_absolute_path(
            service_folder_path + '/' + service_name + '.php'
        )
        repository_implementation_file_path = Helper.get_absolute_path(
            service_folder_path + '/' + service_name + 'Impl.php'
        )
        service_name_with_space = Helper.convert_camel_to_description(
            service_name
        )
        service_interface_content = Helper.bind(
            SERVICE_INTERFACE_TEMPLATE, {
                'model_name': model_name,
                'service_name': service_name,
                'service_name_with_space': service_name_with_space
            }
        )
        service_implementation_content = Helper.bind(
            SERVICE_IMPLEMENTATION_TEMPLATE, {
                'model_name': model_name,
                'model_name_variable': model_name[0].lower() + model_name[1:],
                'service_name': service_name,
                'service_name_with_space': service_name_with_space
            }
        )
        # Write interface file
        service_interface_file = open(service_interface_file_path, "w")
        service_interface_file.write(service_interface_content)
        service_interface_file.close()
        # Write implementation file
        service_implementation_file = open(repository_implementation_file_path, "w")
        service_implementation_file.write(service_implementation_content)
        service_implementation_file.close()

    @staticmethod
    def create_repository_files(repository_folder_path, repository_name, model_name):
        """
        Create repository files includes: interface and implementation

        :param repository_folder_path:
        :param repository_name:
        :param model_name:
        """
        repository_interface_file_path = Helper.get_absolute_path(
            repository_folder_path + '/' + repository_name + '.php'
        )
        repository_implementation_file_path = Helper.get_absolute_path(
            repository_folder_path + '/' + repository_name + 'Impl.php'
        )
        repository_name_with_space = Helper.convert_camel_to_description(
            repository_name
        )
        repository_interface_content = Helper.bind(
            REPOSITORY_INTERFACE_TEMPLATE, {
                'model_name': model_name,
                'repository_name': repository_name,
                'repository_name_with_space': repository_name_with_space
            }
        )
        repository_implementation_content = Helper.bind(
            REPOSITORY_IMPLEMENTATION_TEMPLATE, {
                'model_name': model_name,
                'repository_name': repository_name,
                'repository_name_with_space': repository_name_with_space
            }
        )
        # Write interface file
        repository_interface_file = open(repository_interface_file_path, "w")
        repository_interface_file.write(repository_interface_content)
        repository_interface_file.close()
        # Write implementation file
        repository_implementation_file = open(repository_implementation_file_path, "w")
        repository_implementation_file.write(repository_implementation_content)
        repository_implementation_file.close()

    @staticmethod
    def get_repository_builtin_content(template, repository_name, model_name):
        repository_name_with_space = Helper.convert_camel_to_description(repository_name)
        model_name_plural = model_name + 's'
        if model_name[-1:] == 'y':
            model_name_plural = model_name[:-1] + 'ies'
        repository_implementation_content = Helper.bind(template, {
            'model_name': model_name,
            'model_name_plural': model_name_plural,
            'repository_name': repository_name,
            'repository_name_with_space': repository_name_with_space
        })
        return repository_implementation_content

    def get_repository_filter_content(self, template, repository_name, model_name):
        """
        Get repository filter content
        This method will base on model information about filters
        then generate corresponding methods for them

        :param template:
        :param repository_name:
        :param model_name:
        :return:
        """
        filters = self._models[model_name]['filters']
        repository_implementation_content = ''
        for annotation_name in filters:
            if len(filters[annotation_name]) == 0:
                continue
            table_name = Helper.camel_case_to_snake_case(model_name)
            table = self._tables[table_name]
            # Get column type mapping
            type_mapping = {}
            for field in table:
                type_mapping[field['php_property_name']] = field['php_property_type']
            repository_name_with_space = Helper.convert_camel_to_description(repository_name)
            model_name_plural = model_name + 's'
            if model_name[-1:] == 'y':
                model_name_plural = model_name[:-1] + 'ies'
            for fields in filters[annotation_name]:
                if len(fields) == 0:
                    continue
                query_type = annotation_name[1:-1]
                returned_type = '\Illuminate\Support\Collection'
                if query_type == 'select':
                    query_type = 'get'
                if query_type == 'count':
                    returned_type = 'int'
                if query_type == 'update' or query_type == 'delete':
                    returned_type = 'bool|null'
                description_conditions = ' '.join(fields)
                camel_conditions = ''.join(fields)
                unique_conditions = '_'.join(fields)
                unique_values = '""'
                condition_params = ''
                variable_names = []
                if query_type == 'update':
                    fields = ['data'] + fields
                    type_mapping['data'] = 'array'
                constants_with_values = []
                for field_name in fields:
                    variable_name = '$' + field_name[0].lower() + field_name[1:]
                    variable_type = type_mapping[field_name]
                    variable_names.append(variable_name)
                    unique_values += ' . "_". ' + variable_name
                    constant_name = Helper.camel_case_to_snake_case(field_name).upper()
                    condition_params += '     * @param ' + variable_type + ' ' + variable_name + '\n'
                    if not (query_type == 'update' and field_name == 'data'):
                        constants_with_values.append(
                            '            ' + model_name + '::' + constant_name + ' => ' + variable_name)
                filter_arguments = ''
                if query_type == 'update':
                    filter_arguments = '$data'
                condition_params += '     *'
                condition_arguments = ', '.join(variable_names)
                constants_with_values_array = ',\n'.join(constants_with_values)
                repository_implementation_content += Helper.bind(template, {
                    'returned_type': returned_type,
                    'filter_name': query_type,
                    'filter_name_label': query_type[0].upper() + query_type[1:],
                    'description_conditions': description_conditions,
                    'unique_conditions': unique_conditions,
                    'unique_values': unique_values,
                    'camel_conditions': camel_conditions,
                    'condition_params': condition_params,
                    'filter_arguments': filter_arguments,
                    'condition_arguments': condition_arguments,
                    'constants_with_values': constants_with_values_array,
                    'model_name': model_name,
                    'model_name_plural': model_name_plural,
                    'repository_name': repository_name,
                    'repository_name_with_space': repository_name_with_space
                }) + '\n\n    '
        return repository_implementation_content

    def generate_repository(
            self,
            template_builtin,
            template_filter,
            repository_folder_path,
            repository_name,
            model_name):
        """
        Generate repository builtin method for implementation and interface

        :param template_builtin:
        :param template_filter:
        :param repository_folder_path:
        :param repository_name:
        :param model_name:
        :return:
        """
        repository_file_path = Helper.get_absolute_path(repository_folder_path + '/' + repository_name + '.php')
        with open(repository_file_path, 'r') as stream:
            lines = stream.read().strip()
            repository_components = lines.split(self._identifier)
            if len(repository_components) != 2:
                print 'Identifier not found in repository implementation : ', repository_name
                exit(1)
            else:
                # Concat existing repository source code with builtin methods
                repository_content = repository_components[0]
                repository_builtin = self.get_repository_builtin_content(
                    template_builtin,
                    repository_name,
                    model_name
                )
                repository_filter = self.get_repository_filter_content(
                    template_filter,
                    repository_name,
                    model_name
                )
                repository_content += self._identifier + "\n    "
                repository_content += repository_filter
                repository_content += repository_builtin + "\n}\n"
                # Save new content to repository
                repository_file = open(repository_file_path, 'w')
                repository_file.write(repository_content)
                repository_file.close()
                print 'Generated repository:', repository_name

    def update_dependencies_to_bind(self, dependencies):
        with open(self._bind_path, 'r') as stream:
            lines = stream.read().strip()
            bind_components = lines.split(self._identifier)
            if len(bind_components) != 2:
                print 'Identifier not found in dependency list'
                exit(1)
            else:
                dependency_classes = ''
                for repository_class in dependencies:
                    dependency_classes += '    ' + repository_class + ',\n'
                bind_content = bind_components[0]
                bind_content += self._identifier + '\n' + dependency_classes + '\n];'
                bind = open(self._bind_path, 'w')
                bind.write(bind_content)
                bind.close()

    def generate_repositories(self):
        """
        Generate repositories
        To make flexible repository in controller level without break the architecture
        This method will generate same method in service layer as an alias
        to implement 3 layer Controller -> Service -> Repository
        if controller needs repository then they already had built-in service
        """
        repositories = []
        services = []
        for model in self._models:
            table_name = Helper.camel_case_to_snake_case(model)
            if table_name not in self._tables:
                print 'Table ', table_name, ' in database does not exist !'
                exit(1)
            else:
                repository_folder_path = self._repository_path
                service_folder_path = self._service_path
                repository_name = model + 'Repository'
                service_name = model + 'Service'
                repositories.append('\App\Repository\\' + repository_name + '\\' + repository_name + '::class')
                services.append('\App\Service\\' + service_name + '\\' + service_name + '::class')
                repository_folder_path_each_model = Helper.get_absolute_path(
                    repository_folder_path + '/' + repository_name)
                service_folder_path_each_model = Helper.get_absolute_path(
                    service_folder_path + '/' + service_name)
                if not os.path.exists(repository_folder_path_each_model):
                    os.mkdir(repository_folder_path_each_model)
                if not os.path.exists(service_folder_path_each_model):
                    os.mkdir(service_folder_path_each_model)
                repository_file_path = Helper.get_absolute_path(
                    repository_folder_path_each_model + '/' + repository_name + '.php')
                service_file_path = Helper.get_absolute_path(
                    service_folder_path_each_model + '/' + service_name + '.php')
                if not os.path.exists(repository_file_path):
                    self.create_repository_files(repository_folder_path_each_model, repository_name, model_name=model)
                    print 'Generated repository: ', repository_name
                if not os.path.exists(service_file_path):
                    self.create_service_files(service_folder_path_each_model, service_name, model_name=model)
                    print 'Generated service: ', service_name
                # Generate repository interfaces
                self.generate_repository(
                    REPOSITORY_INTERFACE_BUILTIN_TEMPLATE,
                    REPOSITORY_INTERFACE_FILTER_TEMPLATE,
                    repository_folder_path_each_model,
                    repository_name,
                    model_name=model
                )
                # Generate repository implementations
                self.generate_repository(
                    REPOSITORY_IMPLEMENTATION_BUILTIN_TEMPLATE,
                    REPOSITORY_IMPLEMENTATION_FILTER_TEMPLATE,
                    repository_folder_path_each_model,
                    repository_name + 'Impl',
                    model_name=model
                )

                # alias_methods = self.scan_repository_interface(repository_file_path)                #
                #
                # # Generate repository interfaces
                # self.generate_service(
                #     SERVICE_INTERFACE_BUILTIN_TEMPLATE,
                #     repository_folder_path_each_model,
                #     repository_name,
                #     model_name=model
                # )
                # # Generate repository implementations
                # self.generate_service(
                #     REPOSITORY_IMPLEMENTATION_BUILTIN_TEMPLATE,
                #     REPOSITORY_IMPLEMENTATION_FILTER_TEMPLATE,
                #     repository_folder_path_each_model,
                #     repository_name + 'Impl',
                #     model_name=model
                # )
        self.update_dependencies_to_bind(repositories + services)
