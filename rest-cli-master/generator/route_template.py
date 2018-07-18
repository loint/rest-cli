ROUTE_TEMPLATE = """
Route::group(['middleware' => 'auth:api,throttle'], function () {
{routes}
});
"""

CONTROLLER_TEMPLATE = """
<?php
declare(strict_types=1);
namespace App\Controller;

use Illuminate\Http\Response;
use Illuminate\Http\Request;
use Illuminate\Http\JsonResponse;
use Rest\Controller;
{actionNamespaces}

class {className} extends Controller
{
	/**
	 * {className} constructor
	*/
	public function __construct()
	{
		parent::__construct();
	}

{classContent}
}
"""

CONTROLLER_TEST_TEMPLATE = """
<?php
declare(strict_types=1);

namespace Tests\Controllers;

use Tests\IntegrationTest;
use Illuminate\Http\Response;
{actionNamespaces}

class {className}Test extends IntegrationTest
{
{classContent}
}
"""

ACTION_TEMPLATE = """
    /**
     * {description}
     *
     * @author {author}
     * @see HTTP/1.1 {method} {route}
{parameters}
     *
     * @return JsonResponse
     */
    public function {actionName}({actionArguments})
    {
{comments}
{declarations}
        try {
            // TODO - Your implementation here
            
        } catch (\Throwable $throwable) {
            SystemLogsHelper::catchThrowable($throwable);
            return $this->errorResponse($throwable);
        }
        return $this->successResponse(Response::HTTP_OK, $output);
    }
"""

ACTION_TEST_TEMPLATE = """
    /**
     * Test {description}
     *
     * @given Send {method} request to {route}
     * @expect Response is success
     */
    public function test{actionName}()
    {
        $this->withoutMiddleware();
        {inputDeclaration}
        $response = $this->{methodLowerCase}($this->bind('api{route}', [{parameters}]){inputVariable});
        $response->assertStatus(Response::HTTP_OK);
        
        $responseJson = $response->decodeResponseJson();
        $this->assertNotNull($responseJson['data']);
        
        /** @var {outputClassName} $output */
        $output = JsonHelper::cast($responseJson['data'], {outputClassName}::class);
        $this->assertNotNull($output);
    }
"""