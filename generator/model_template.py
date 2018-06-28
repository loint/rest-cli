
__author__ = "Loi Nguyen <loinguyentrung@gmail.com>"

REST_TEMPLATE = """{
  "rest": "{app_name}",
  "name": "app",
  "config" : "api",
  "document": "public/docs/api.json",
  "source": "src",
  "test": "test",
  "interface": "../interface/src",
  "mysql": {
    "host": "{host}",
    "username": "{username}",
    "password": "{password}",
    "database": "{database}"
  }
}
"""

DATABASE_TEMPLATE = """<?php
return [
    'default' => 'mysql',
    'migrations' => '_migrations',
    'connections' => [
        'mysql' => [
            'read' => [
                'host' => ['{host}'],
            ],
            'write' => [
                'host' => ['{host}'],
            ],
            'sticky' => true,
            'driver' => 'mysql',
            'database' => '{database}',
            'username' => '{username}',
            'password' => '{password}',
            'charset' => 'utf8mb4',
            'collation' => 'utf8mb4_unicode_ci',
            'prefix' => '',
        ],
    ]
];
"""

MODEL_TEMPLATE = """
<?php
namespace App\Model;

use Illuminate\Database\Eloquent\Model;

/**
 * {model_name_with_space}
 *
 * @category   \App
 * @package    \App\Model
 * @version    1.0
 * @since      File available since Release 1.0
 */
class {model_name} extends Model
{
    /**
     * The table associated with the model.
     *
     * @var string
     */
    protected $table = '{table_name}';

    /**
     * {model_name} Model constructor
     */
    public function {model_name}()
    {
    }

    // TODO - Model relationships here

    // AUTO GENERATED - DO NOT MODIFY FROM HERE
}
"""

MODEL_CONSTRUCTOR_TEMPLATE = """
    use \Illuminate\Database\Eloquent\SoftDeletes;

    /**
     * Override default primary key
     */
    protected $primaryKey = 'Id';

    /**
     * Model generated constructor.
     */
    public function __construct()
    {
        parent::__construct();
        // Constructor interceptor
        $this->{model_name}();
        // Default values for model instance
{default_setters}
    }
"""

REPOSITORY_INTERFACE_TEMPLATE = """
<?php
namespace App\Repository\{repository_name};

use App\Model\{model_name};

/**
 *  {repository_name_with_space} Interface.
 *
 * @category  \App\Repository
 * @package   \App\Repository\{repository_name}
 * @version    1.0
 * @see       \App\Repository\{repository_name}\{repository_name}
 * @since     File available since Release 1.0
 */
interface {repository_name}
{
    // TODO - Your interfaces here

    // AUTO GENERATED - DO NOT MODIFY FROM HERE
}

"""

REPOSITORY_IMPLEMENTATION_TEMPLATE = """
<?php
namespace App\Repository\{repository_name};

use App\Model\{model_name};

/**
 *  {repository_name_with_space} Implementation.
 *
 * @category  \App\Repository
 * @package   \App\Repository\{repository_name}
 * @version    1.0
 * @see       \App\Repository\{repository_name}\{repository_name}
 * @since     File available since Release 1.0
 */
class {repository_name}Impl implements {repository_name}
{
    // TODO - Your implementations here

    // AUTO GENERATED - DO NOT MODIFY FROM HERE
}
"""

REPOSITORY_INTERFACE_BUILTIN_TEMPLATE = """
    /**
     * Get last record id of {model_name}.
     *
     * @return {model_name} || null
     */
    public function getLastRecordIdOf{model_name}();

    /**
     * Get all records.
     *
     * @return \Illuminate\Database\Eloquent\Collection
     */
    public function getAll{model_name_plural}();

    /**
     * Get record by id.
     *
     * @param int $id
     *
     * @return {model_name} || null
     */
    public function get{model_name}ById($id);

    /**
     * Get record by conditions.
     *
     * @param array $conditions
     *
     * @return \Illuminate\Database\Eloquent\Collection
     */
    public function get{model_name_plural}ByConditions($conditions);

    /**
     * Insert one record.
     *
     * @param {model_name} $record
     *
     * @return int
     */
    public function save{model_name}($record);

    /**
     * Insert multiple records.
     *
     * @param array $records
     *
     * @return bool
     */
    public function bulkInsert{model_name_plural}($records);

    /**
     * Update records by id.
     *
     * @param int   $id
     * @param array $data
     *
     * @return bool
     */
    public function update{model_name}ById($id, $data);

    /**
     * Update records by conditions.
     *
     * @param array $conditions
     * @param array $data
     *
     * @return bool
     */
    public function update{model_name_plural}ByConditions($conditions, $data);

    /**
     * Delete record by id.
     *
     * @param int $id
     *
     * @throws \Exception
     *
     * @return bool
     */
    public function delete{model_name}ById($id);

    /**
     * Force delete record by id.
     *
     * @param int $id
     *
     * @throws \Exception
     *
     * @return bool
     */
    public function forceDelete{model_name}ById($id);

    /**
     * Delete records by conditions.
     *
     * @param array $conditions
     *
     * @return bool
     */
    public function delete{model_name_plural}ByConditions($conditions);

    /**
     * Delete all records.
     *
     * @return bool
     */
    public function deleteAll{model_name_plural}();

    /**
     * Count number of records.
     *
     * @return int
     */
    public function count{model_name}();
"""

REPOSITORY_IMPLEMENTATION_BUILTIN_TEMPLATE = """
    /**
     * Get last record id of {model_name}.
     *
     * @return {model_name} || null
     */
    public function getLastRecordIdOf{model_name}()
    {
        return {model_name}::max('id');
    }
    
    /**
     * Find all records.
     *
     * @return \Illuminate\Database\Eloquent\Collection
     */
    public function getAll{model_name_plural}()
    {
        return {model_name}::all();
    }

    /**
     * Find record by id.
     *
     * @param $id
     *
     * @return {model_name} || null
     */
    public function get{model_name}ById($id)
    {
        return {model_name}::find($id);
    }

    /**
     * Get record by conditions.
     *
     * @param array $conditions
     *
     * @return \Illuminate\Database\Eloquent\Collection
     */
    public function get{model_name_plural}ByConditions($conditions)
    {
        return {model_name}::where($conditions)->get();
    }

    /**
     * Save one record.
     *
     * @param {model_name} $record
     *
     * @return int | bool
     */
    public function save{model_name}($record)
    {
        $status = $record->save();
        if (false === $status) {
            return false;
        }
        return $record->getId();
    }

    /**
     * Insert multiple records.
     *
     * @param array $records
     *
     * @return bool
     */
    public function bulkInsert{model_name_plural}($records)
    {
        $data = [];
        /** @var \Illuminate\Database\Eloquent\Model $record */
        foreach ($records as $record) {
            $data[] = $record->getAttributes();
        }

        return {model_name}::insert($data);
    }

    /**
     * Update records by id.
     *
     * @param int   $id
     * @param array $data
     *
     * @return bool
     */
    public function update{model_name}ById($id, $data)
    {
        $condition = [
            {model_name}::ID => $id,
        ];
        return {model_name}::where($condition)->update($data);
    }

    /**
     * Update records by conditions.
     *
     * @param array $conditions
     * @param array $data
     *
     * @return bool
     */
    public function update{model_name_plural}ByConditions($conditions, $data)
    {
        return {model_name}::where($conditions)->update($data);
    }

    /**
     * Delete record by id.
     *
     * @param $id
     *
     * @throws \Exception
     *
     * @return bool
     */
    public function delete{model_name}ById($id)
    {
        $object = $this->get{model_name}ById($id);
        if (null === $object) {
            // Can not delete undefined object
            return false;
        }

        return $object->delete();
    }

    /**
     * Force delete record by id.
     *
     * @param $id
     *
     * @throws \Exception
     *
     * @return bool
     */
    public function forceDelete{model_name}ById($id)
    {
        $object = $this->get{model_name}ById($id);
        if (null === $object) {
            // Can not delete undefined object
            return false;
        }

        return $object->forceDelete();
    }

    /**
     * Delete records by conditions.
     *
     * @param array $conditions
     *
     * @return bool
     */
    public function delete{model_name_plural}ByConditions($conditions)
    {
        return {model_name}::where($conditions)->delete();
    }

    /**
     * Delete all records.
     *
     * @return void
     */
    public function deleteAll{model_name_plural}()
    {
        return  {model_name}::truncate();
    }

    /**
     * Count number of records.
     *
     * @return int
     */
    public function count{model_name}()
    {
        return {model_name}::count();
    }
"""

REPOSITORY_INTERFACE_FILTER_TEMPLATE = """
    /**
     * {filter_name_label} records by {description_conditions}.
     *
{condition_params}
     *
     * @return {returned_type}
     *
     * @throws \Exception
     */
    public function {filter_name}{model_name_plural}By{camel_conditions}({condition_arguments});"""

REPOSITORY_IMPLEMENTATION_FILTER_TEMPLATE = """
    /**
     * {filter_name_label} records by {description_conditions}
     *
{condition_params}
     *
     * @return {returned_type}
     *
     * @throws \Exception
     */
    public function {filter_name}{model_name_plural}By{camel_conditions}({condition_arguments})
    {
        $condition = [
{constants_with_values},
        ];
        $queryBuilder = {model_name}::where($condition);

        return $queryBuilder->{filter_name}({filter_arguments});
    }"""


SERVICE_INTERFACE_TEMPLATE = """
<?php
namespace App\Service\{service_name};

/**
 * {service_name_with_space} Interface.
 *
 * @category  \App\Service
 * @package   \App\Service\{service_name}
 * @version    1.0
 * @since     File available since Release 1.0
 */
interface {service_name}
{
    // TODO - Your interfaces here

    // AUTO GENERATED - DO NOT MODIFY FROM HERE
}

"""

SERVICE_IMPLEMENTATION_TEMPLATE = """
<?php
namespace App\Service\{service_name};

use App\Repository\{model_name}Repository\{model_name}Repository;

/**
 * {service_name_with_space} Implementation.
 *
 * @category  \App\Service
 * @package   \App\Service\{service_name}
 * @version   1.0
 * @see       \App\Service\{service_name}\{service_name}
 * @since     File available since Release 1.0
 */
class {service_name}Impl implements {service_name}
{
    /**
     * @var {model_name}Repository ${model_name_variable}Repository
     */
    private ${model_name_variable}Repository;
    
    public function __constructor({model_name}Repository ${model_name_variable}Repository)
    {
        $this->{model_name_variable}Repository = ${model_name_variable}Repository;
    }   
    
    // TODO - Your implementations here

    // AUTO GENERATED - DO NOT MODIFY FROM HERE
}
"""

SETTER_GETTER_TEMPLATE = """
    /**
     * Constant for field `{field_name}`.
     */
    const {constant_field_name} = '{field_name}';

    /**
     * Set {method_name}
     * This setter will set value for field `{field_name}`.
     *
     * @param {field_type} ${camel_variable_name}
     *
     * @return \App\Model\{table_name}
     */
    public function {setter_name}(${camel_variable_name})
    {
        {intercept_filter_set}

        return $this;
    }

    /**
     * Get {method_name}
     * This getter will get value from field `{field_name}`.
     *
     * @return {field_type} || null
     */
    public function {getter_name}()
    {
        {intercept_filter_get}
    }
"""