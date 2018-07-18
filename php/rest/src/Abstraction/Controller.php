<?php
namespace Rest\Abstraction;

use Illuminate\Http\Response;
use Rest\Helper\LogHelper;

abstract class Controller
{
    protected function __construct()
    {
    }

    /**
     * Response valid data
     *
     * @param $status int
     * @param $data AbstractOutput | array
     * @param $headers array
     *
     * @return \Illuminate\Http\JsonResponse
     */
    public function response($status, $data, $headers = array())
    {
        if (is_array($data)) {
            $dumpData = array();
            foreach ($data as $outputItem) {
                /** @var AbstractOutput $outputItem */
                if ($outputItem instanceof AbstractOutput) {
                    $dumpData [] = $outputItem->toArray();
                    continue;
                }
                $dumpData [] = $outputItem;
            }
            $dataContent = $dumpData;
        } else {
            $dataContent = $data->toArray();
        }

        $body = [
            'headers' => $headers,
            'status' => $status,
            'code' => Exception::NO_EXCEPTION,
            'message' => 'OK',
            'data' => $dataContent
        ];
        return response()->json($body, Response::HTTP_OK);
    }

    /**
     * Response error and exception
     *
     * @param \Throwable $throwable
     *
     * @return \Illuminate\Http\JsonResponse
     */
    public function error(\Throwable $throwable)
    {
        // Will be refactored to handle standard complex exception
        return response()->json([
            'status' => Response::HTTP_BAD_REQUEST,
            'code' => $throwable->getCode(),
            'message' => $throwable->getMessage(),
            'data' => []
        ], Response::HTTP_BAD_REQUEST);
    }

    /**
     * Response error and exception
     *
     * @param \Throwable $throwable
     *
     * @return \Illuminate\Http\JsonResponse
     */
    public function errorExceptionResponse(\Exception $exception, $data)
    {
        return response()->json([
            'status' => Response::HTTP_BAD_REQUEST,
            'code' => $data['code'],
            'message' => $exception->getMessage(),
            'data' => $data
        ], Response::HTTP_BAD_REQUEST);
    }
}