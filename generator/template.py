MODEL_TEMPLATE = """
<?php
namespace App\Model;

use Illuminate\Database\Eloquent\Model;
use Illuminate\Support\Facades\DB;

/**
 *  {model_name_with_space}
 *
 * @category   \App
 * @package    \App\Model
 * @version    1.0
 * @see        \Illuminate\Foundation\Auth\User
 * @since      File available since Release 1.0
 */
class {model_name} extends Model
{
    /**
     * Table name
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
    //*************************************************
}
"""

MODEL_CONSTRUCTOR_TEMPLATE = """
    use \App\Common\Traits\ModelObservable;
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

use App\Common\Interfaces\Repository;
use App\Models\{model_name};

/**
 *  {repository_name_with_space} Interface.
 *
 * @category  \App\Repository
 * @package   \App\Repository\{repository_name}
 * @version    1.0
 * @see       \App\Repository\{repository_name}\{repository_name}
 * @since     File available since Release 1.0
 */
interface {repository_name} extends Repository
{
    // TODO - Your interfaces here

    // AUTO GENERATED - DO NOT MODIFY FROM HERE
    //*************************************************
}

"""

REPOSITORY_IMPLEMENTATION_TEMPLATE = """
<?php
namespace App\Repository\{repository_name};

use App\Models\{model_name};
use Illuminate\Support\Facades\Cache;

/**
 *  {repository_name_with_space} Implementation.
 *
 * @category  \App\Repository
 * @package   \App\Repository\{repository_name}
 * @version    1.0
 * @see         \App\Repository\{repository_name}\{repository_name}
 * @since     File available since Release 1.0
 */
class {repository_name}Impl implements {repository_name}
{
    // TODO - Your implementations here

    // AUTO GENERATED - DO NOT MODIFY FROM HERE
    //*************************************************
}
"""

REPOSITORY_INTERFACE_BUILTIN_TEMPLATE = """
    /**
     * Store all records in memory
     *
     * @param array | bool $records
     * @return void
     */
    public function storeInMemory($records = false);

    /**
     * Flush all records in memory
     *
     * @return void
     */
    public function flushMemory();

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
     * @return void
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
     * Insert one record.
     *
     * @param {model_name} $record
     *
     * @return int | bool
     */
    public function save{model_name}($record)
    {
        $status = $record->save();
        if ($status === false) {
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
        if ($object === null) {
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
        if ($object === null) {
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