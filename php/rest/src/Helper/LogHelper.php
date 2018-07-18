<?php
namespace Rest\Helper;

use Illuminate\Support\Facades\Log;

class LogHelper
{
    /**
     * Catch a throwable instance
     * This helper will support write error and exception to system logs in database
     *
     * @param \Throwable $throwable
     */
    public static function catchThrowable(\Throwable $throwable)
    {
        if (strlen($throwable->getMessage()) > 0) {
            $logContext = [
                'fileName' => $throwable->getFile(),
                'lineNo' => $throwable->getLine(),
            ];
            Log::error($throwable->getMessage(), $logContext);
        }
    }
}