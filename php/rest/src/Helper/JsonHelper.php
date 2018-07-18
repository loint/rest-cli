<?php

namespace Rest\Helper;

use Rest\Helper\LogHelper;

/**
 *  Json to model helper
 *  Class object use for convert json to 1 object input or output in model
 * @category   App\Helper
 * @version    1.0
 * @since     File available since Release 1.0
 */
class JsonHelper
{
    /**
     * Map request data with model
     *
     * @param $className
     * @param $request
     *
     * @return mixed
     */
    public static function map($request, $className)
    {
        if (empty($request->input())) {
            return new $className();
        }
        return self::cast($request->input(), $className);
    }

    /**
     * Function use for convert json to object input or output
     *
     * @param $data
     * @param $className
     *
     * @return mixed
     */
    public static function cast($data, $className)
    {
        $data = \json_decode(\json_encode($data), true);
        $newObject = new $className();
        if (!is_array($data)) {
            return $newObject;
        }
        try {
            // Convert json to array
            foreach ($data as $key => $value) {
                if (!isset($data[$key]) || !method_exists($newObject, "set" . ucfirst($key))) {
                    continue;
                }
                $newObject->{"set" . ucfirst($key)}($data[$key]);
            }
        } catch (\Throwable $throwable) {
            LogHelper::catchThrowable($throwable);
        }
        return $newObject;
    }
}
