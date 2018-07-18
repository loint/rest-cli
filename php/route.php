<?php
class ApiGenerator
{
    const SERVER_ROUTE = <<< 'SERVER_ROUTE'
{routes}
SERVER_ROUTE;

    const CLASS_TEMPLATE = <<< 'CLASS_TEMPLATE'
<?php
namespace App\Controller;

use Illuminate\Http\Response;
use Illuminate\Http\Request;
use Illuminate\Http\JsonResponse;
use Rest\Helper\JsonHelper;
use Rest\Helper\LogHelper;
use Rest\Abstraction\Controller;
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

CLASS_TEMPLATE;

    const CLASS_TEST_TEMPLATE = <<< 'CLASS_TEST_TEMPLATE'
<?php
namespace Tests\Controller;

use Illuminate\Http\Response;
use RestTest\Test;
use Rest\Helper\JsonHelper;
{actionNamespaces}
class {className}Test extends Test
{	
{classContent}
}
CLASS_TEST_TEMPLATE;

    const METHOD_TEMPLATE = <<< 'METHOD_TEMPLATE'
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
            return $this->error($throwable);
        }
        return $this->response(Response::HTTP_OK, $output);
    }
METHOD_TEMPLATE;

    const METHOD_TEST_TEMPLATE = <<< 'METHOD_TEST_TEMPLATE'
    /**
     * Test {description}
     *
     * @given Send {method} request to {route}
     * @expect Response is success
     */
    public function test{actionName}()
    {{inputDeclaration}
		$content = $this
		    ->{methodLowerCase}($this->bind('{route}', [{parameters}]){inputVariable})
		    ->seeStatusCode(Response::HTTP_OK)
            ->seeJsonStructure(['code', 'data', 'message'])
            ->response->content();
 
//		$responseJson = $response->getResult();
//		$this->assertNotNull($responseJson['data']);
//		
//		/** @var {outputClassName} $output */
//		$output = JsonHelper::cast($responseJson['data'], {outputClassName}::class);
//		$this->assertNotNull($output);
    }
METHOD_TEST_TEMPLATE;

    const INPUT_OUTPUT_MODEL_TEMPLATE = <<< 'INPUT_OUTPUT_MODEL_TEMPLATE'
<?php
namespace App\Shared\IO\{namespace};

use Rest\Abstraction\Abstract{io};

class {interfaceName} extends Abstract{io}
{
	/**
	  * {interfaceName} constructor
	  */
	public function __construct() {
		parent::__construct();
{defaultValues}
	}
	
	/**
	 * Get IO schema for testing data structure
	 * @return array
	 */
	public static function schema() {
		return array(
{schemas}
		);
	}
	
{classContent}
}
INPUT_OUTPUT_MODEL_TEMPLATE;

    const PROPERTIES_MODEL = <<< 'PROPERTIES_MODEL'
    private ${propertiesName};
    
    /**
      * Set {propertiesName}
      * This setter will set value for field `{propertiesName}`.
      *
      * @param {type} ${propertiesName}
      *
      * @return {interfaceName}
      */
    public function set{name}(${propertiesName}) 
    {
        if (${propertiesName} === null) {
            $this->{propertiesName} = null;
        } else {
            $this->{propertiesName} = ({type}) ${propertiesName};
        }
        
        return $this;
    }  
    
    /**
    * Get {name}
    * This getter will get value from field `{name}`.
    *
    * @return {type} || null
    */    
    public function get{name}() 
    {
        ${propertiesName}Value = $this->{propertiesName};
        if (${propertiesName}Value === null) {
            return null;
        }
        return ({type}) ${propertiesName}Value;
    }    

PROPERTIES_MODEL;

    const SWAGGER_PATH_TEMPLATE = <<< 'SWAGGER_PATH'
      "{method}": {
        "summary": "{description}",
        "tags": ["{tag}"],
        "operationId": "{routeName}",
        "produces": ["application/json"],
        "parameters": [
          {
            "name": "tags",
            "in": "query",
            "description": "tags to filter by",
            "required": false,
            "type": "array",
            "items": {
              "type": "string"
            },
            "collectionFormat": "csv"
          },
          {
            "name": "limit",
            "in": "query",
            "required": false,
            "type": "integer",
            "format": "int32"
          }
        ],
        "responses": {
          "200": {
            "schema": {
              "type": "array",
              "items": {
              }
            }
          },
          "default": {
            "description": "unexpected error",
            "schema": {
            }
          }
        }
      }
SWAGGER_PATH;

    const SWAGGER_TEMPLATE = <<< 'SWAGGER'
{
  "swagger": "2.0",
  "info": {
    "version": "1.0.0",
    "title": "Rest API Documentation",
    "description": ""
  },
  "host": "localhost:8000",
  "basePath": "/",
  "tags": {tag},
  "schemes": ["http"],
  "consumes": ["application/json"],
  "produces": ["application/json"],
  "paths": {
{path}
  },
  "definitions": {}
}
SWAGGER;


    /**
     * Configuration directory
     * @var string
     */
    private $configurationDirectory;

    /**
     * Server root
     * @var string
     */
    private $serverRoot;

    /**
     * Server interfaces - define type casting for server
     * @var string
     */
    private $serverInterfaces;

    /**
     * Swagger UI
     * @var string
     */
    private $swaggerDist;

    /**
     * List routes - use to be a global variable to hold route
     * from recursive discovery
     * @var array
     */
    private $routes;

    /**
     * Auto generated identifier
     * @var string
     */
    private $identifier;

    public function base_path($path)
    {
        $path = getcwd() . "/$path";
        return $path;
    }

    public static function bind($template, $variables = [], $start = '{', $end = '}')
    {
        $content = $template;
        foreach ($variables as $variableName => $variableValue) {
            $content = \str_replace($start . $variableName . $end, $variableValue, $content);
        }

        return $content;
    }

    public static function endsWith($haystack, $needle)
    {
        // search forward starting from end minus needle length characters
        return $needle === '' || (($temp = \mb_strlen($haystack) - \mb_strlen($needle)) >= 0 && \mb_strpos($haystack, $needle, $temp) !== false);
    }

    /**
     * Set configuration directory
     *
     * @param $configurationDirectory
     *
     * @return $this
     */
    public function setConfigurationDirectory($configurationDirectory)
    {
        $this->configurationDirectory = self::base_path($configurationDirectory);
        return $this;
    }

    /**
     * Set server root directory
     *
     * @param $serverRoot
     *
     * @return $this
     */
    public function setServerRoot($serverRoot)
    {
        $this->serverRoot = self::base_path($serverRoot);
        return $this;
    }

    /**
     * Set server interfaces
     *
     * @param $serverInterfaces
     *
     * @return $this
     */
    public function setServerInterfaces($serverInterfaces)
    {
        $this->serverInterfaces = self::base_path($serverInterfaces);
        return $this;
    }

    /**
     * Set swagger dist
     *
     * @param $swaggerLocation
     *
     * @return $this
     */
    public function setSwaggerDist($swaggerLocation)
    {
        $this->swaggerDist = self::base_path($swaggerLocation);
        return $this;
    }

    /**
     * Set identifier
     *
     * @param $identifier
     *
     * @return $this
     */
    public function setIdentifier($identifier)
    {
        $this->identifier = $identifier;
        return $this;
    }

    /**
     * Get identifier
     * @return string
     */
    public function getIdentifier()
    {
        return $this->identifier;
    }

    /**
     * Read configuration
     *
     * @return array
     */
    public function readConfiguration()
    {
        $configFiles = scandir($this->configurationDirectory);
        $config = array();
        foreach ($configFiles as $configFile) {
            if (self::endsWith($configFile, '.json')) {
                $filePath = $this->configurationDirectory . "/" . $configFile;
                // We already detect only json file so first element should exist
                $fileName = explode('.json', $configFile)[0];
                $fileContent = '';
                try {
                    $fileContent = json_decode(file_get_contents($filePath));
                } catch (\Throwable $throwable) {
                    echo $throwable->getMessage();
                }
                if ($fileContent == null || $fileContent == '') {
                    echo "JSON syntax error in '$filePath'\n !";
                }
                if (is_object($fileContent)) {
                    $fileContent->controller = $this->convertSnackToCamel($fileName . '_controller');
                    $fileContent->fileName = $fileName;
                    if (isset($fileContent->route)) {
                        $routeComponent = explode("?", $fileContent->route);
                        if (count($routeComponent) > 0) {
                            $fileContent->path = $routeComponent[0];
                        }
                        if (count($routeComponent) > 1) {
                            $fileContent->query = "?" . $routeComponent[1];
                        }
                    }
                }
                $config[$configFile] = $fileContent;
            }
        }
        return $config;
    }

    /**
     * Validate parameters
     */
    public function validateParameters()
    {
        if ($this->configurationDirectory == null) {
            echo "Missing setting for configuration directory folder !";
            return false;
        }
        if ($this->serverInterfaces == null) {
            echo "Missing setting for server interfaces folder !";
            return false;
        }
        if ($this->serverRoot == null) {
            echo "Missing setting for server root folder !";
            return false;
        }
        return true;
    }

    /**
     * Validate route configuration
     *
     * @param $config
     *
     * @return bool
     */
    public function validateRoute($config)
    {
        // Prerequisite parameters
        if (!isset($config->route)
            || !isset($config->method)
        ) {
            return false;
        }
        // Property child can be optional
        return true;
    }

    /**
     * Generate file with new content
     *
     * @param $filePath
     * @param $newContent
     */
    public function generateFileWithContent($filePath, $newContent)
    {
        $fileContent = file_get_contents($filePath);
        $fileContentComponents = explode($this->getIdentifier(), $fileContent);
        if (count($fileContentComponents) != 2) {
            echo "Identifier not found in $filePath \n";
            exit(0);
        }

        // Only keep old content
        try {
            $oldContent = $fileContentComponents[0];
            $newFileContent = $oldContent . $this->getIdentifier() . "\n$newContent\n";
            file_put_contents($filePath, $newFileContent);
        } catch (\Throwable $throwable) {
            file_put_contents($filePath, $fileContent . "\n");
        }
    }

    /**
     * Generate Laravel routes
     *
     * @param $routes
     */
    public function generateRoute($routes)
    {
        // Collect controller with its actions
        $controllers = [];
        foreach ($routes as $route) {
            if (!isset($controllers[$route->controllerName])) {
                $controllers[$route->controllerName] = [];
            }
            if (!isset($controllers[$route->controllerName])) {
                $controllers[$route->controllerName][$route->actionName] = [];
            }
            $controllers[$route->controllerName][$route->actionName][] = $route->inputClassName;
            $controllers[$route->controllerName][$route->actionName][] = $route->outputClassName;
        }
        $routeContent = '';
        foreach ($routes as $route) {
            $this->generateFullController($route, $controllers[$route->controllerName]);
            $routeName = $route->routeName;
            $controllerName = $route->controllerName;
            $actionName = $route->actionName;
            $method = strtolower($route->method);
            $route = $route->route;
            $routeContent .= "\$router->$method('$route', [\n\t'as' => '$routeName.$actionName',\n\t'uses' => '$controllerName@$actionName'\n]);\n";
        }
        $this->generateFileWithContent(self::base_path("src/Routes.php"), self::bind(self::SERVER_ROUTE, array(
            'routes' => $routeContent
        )));
    }

    private function convertStringToUpperCase($stringValue)
    {
        $action = preg_split('/(?=[A-Z])/', $stringValue);
        $actionUpper = [];
        foreach ($action as $key => $value) {
            if(empty($value) || $value === null || $value === '') {
                continue;
            }
            $actionUpper[] = mb_strtoupper($value);
        }
        $fullActionName = implode("_", $actionUpper);
        return $fullActionName;
    }

    /**
     * Convert snack string to camel string
     *
     * @param $name
     *
     * @return string
     */
    public function convertSnackToCamel($name)
    {
        return implode('', array_map('ucfirst', explode('_', $name)));
    }

    /**
     * Check if target contains special characters
     *
     * @param $target
     *
     * @return bool
     */
    public function isContainSpecialCharacter($target)
    {
        $specialCharacters = array("?", "{", "}");
        foreach ($specialCharacters as $specialCharacter) {
            if (strpos($target, $specialCharacter) != false) {
                return true;
            }
        }
        return false;
    }

    /**
     * Extract route name from route
     *
     * @param $routePath
     * @param $actionName
     *
     * @return bool|string
     */
    public function extractRouteNameFromRoute($routePath, $actionName)
    {
        $routeComponents = explode("/", $routePath);
        $name = '';
        foreach ($routeComponents as $routeComponent) {
            if (strlen($routeComponent) == 0) {
                continue;
            }
            $continue = false;
            if ($this->isContainSpecialCharacter($routeComponent)) {
                $continue = true;
            }
            if ($continue) continue;
            $name .= '_' . $routeComponent;
        }

        $routeName =  substr($name, 1, strlen($name) - 1);

        // If end of route name is action name then remove action name
        if (($actionName != null) && self::endsWith($routeName, $actionName)) {
            return substr($routeName, 0, strlen($routeName) - strlen($actionName) - 1);
        }

        if (self::endsWith($routeName, '_')) {
            return substr($routeName, 0, strlen($routeName) - 1);
        }

        return $routeName;
    }

    /**
     * Build action name
     *
     * @param $action
     * @param $routeName
     * @param $output
     *
     * @return string
     */
    public function buildActionName($action, $routeName, $output)
    {
        $routeComponents = explode('/', $routeName);
        $mainAction = '';
        for ($routeIndex = count($routeComponents) - 1; $routeIndex > 0; $routeIndex--) {
            $routeComponent = $routeComponents[$routeIndex];
            if (strlen($routeComponent) == 0) {
                continue;
            }
            if ($this->isContainSpecialCharacter($routeComponent)) {
                continue;
            }
            $mainAction = $routeComponent . '_' . $mainAction;
        }

        // Remove first character  _
        $mainAction = substr($mainAction, 0, strlen($mainAction) - 1);
        $mainAction = $this->convertSnackToCamel($mainAction);

        $mainAction = "$action$mainAction";

        if (self::endsWith($mainAction, ucfirst($action))) {
            $mainAction = substr($mainAction, 0, strlen($mainAction) - strlen($action));
        }

        if (is_array($output)) {
            $mainAction .= 's';
        }

        return $mainAction;
    }

    /**
     * Make flat route
     *
     * @param $route
     */
    public function makeFlatRoute($route)
    {
        foreach ($route->method as $methodName => $routeDetail) {
            $newRoute = new \stdClass();
            $action = isset($routeDetail->action) ? $routeDetail->action : null;

            if ($action == null) {
                switch ($methodName) {
                    case "POST":
                        $action = "create";
                        break;
                    case "PUT":
                        $action = "update";
                        break;
                    case "DELETE":
                        $action = "delete";
                        break;
                    default:
                        $action = "get";
                }
            }

            $routeName = $this->extractRouteNameFromRoute($route->path, $action);
            $camelRouteName = $this->convertSnackToCamel($routeName);
            $newRoute->name = $camelRouteName;
            $newRoute->controllerName = $route->controller;
            $newRoute->routeBase = $route->path;
            $newRoute->routeName = str_replace('_', '.', $routeName);
            $newRoute->route = $route->path . $route->query;
            $newRoute->method = $methodName;
            $newRoute->fileName = $route->fileName;
            $newRoute->action = $action;
            if (!isset($routeDetail->input)) {
                $routeDetail->input = new \stdClass();
            }
            if (!isset($routeDetail->output)) {
                $routeDetail->output = new \stdClass();
            }
            if (!isset($routeDetail->author)) {
                $routeDetail->author = "";
            }
            if (!isset($routeDetail->description)) {
                $routeDetail->description = "";
            }

            $newRoute->author = $routeDetail->author;
            $newRoute->description = $routeDetail->description;

            $newRoute->actionName = $this->buildActionName(
                $newRoute->action,
                $newRoute->routeBase,
                $routeDetail->output
            );

            $newRoute->input = $routeDetail->input;
            $newRoute->inputClassName = $this->convertSnackToCamel($newRoute->actionName . "Input");
            $newRoute->output = $routeDetail->output;
            $newRoute->outputClassName = $this->convertSnackToCamel($newRoute->actionName . "Output");;

            $this->routes [] = $newRoute;
        }
    }

    /**
     * Recursive compile route
     *
     * @param      $config
     * @param null $fileName
     * @param null $controller
     * @param null $rootPath
     */
    public function recursiveDiscoveryRoute($config, $fileName = null, $controller = null, $rootPath = null)
    {
        if ($config == null) {
            return;
        }
        foreach ($config as $index => $route) {
            if ($this->validateRoute($route)) {
                if (isset($route->route)) {
                    if (isset($route->controller)) {
                        $controller = $route->controller;
                    }
                    $routeComponent = explode("?", $route->route);
                    $route->path = '';
                    $route->query = '';
                    $route->fileName = $fileName;
                    if (count($routeComponent) > 0) {
                        $route->path = $routeComponent[0];
                    }
                    if (count($routeComponent) > 1) {
                        $route->query = "?" . $routeComponent[1];
                    }
                }
                if ($rootPath != null) {
                    $route->path = $rootPath . $route->route;
                }
                $route->controller = $controller;
                $this->makeFlatRoute($route);
                // If this route has child route then
                // we need to make a recursion
                if (isset($route->path) && isset($route->child)) {
                    $this->recursiveDiscoveryRoute($route->child, $fileName, $controller, $route->path);
                }
            }
        }
    }

    /**
     * Compile flat routes
     * @return array|bool
     */
    public function compileFlatRoutes()
    {
        // Require parameter before generating
        if (!$this->validateParameters()) {
            return false;
        }
        try {
            $config = $this->readConfiguration();
            $this->routes = array();
            // Recursive discovery routes in configuration file
            if (count($config) > 0) {
                $fileName = null;
                if (isset($config[0]->fileName)) {
                    $fileName = $config[0]->fileName;
                }
                $this->recursiveDiscoveryRoute($config, $fileName);
            }
            return $this->routes;
        } catch (\Throwable $throwable) {
            echo $throwable->getMessage();
            echo $throwable->getTraceAsString();
        }
    }

    private function generateFullController($route, $actions)
    {
        $this->generateInputAndOutputModel($route);
        $this->generateController($route, $actions);
        $this->generateControllerTest($route, $actions);
    }

    private function generateInputAndOutputModel($route)
    {
        $controllerName = $route->controllerName;
        $actionName = ucfirst($route->actionName);
        $inputClassName = $route->inputClassName;
        $outputClassName = $route->outputClassName;
        $modelInput = $route->input;
        $modelOutput = is_array($route->output) ? $route->output[0] : $route->output;

        //Check file exists
        $actionInterfacePath = self::base_path(implode(DIRECTORY_SEPARATOR, ["src", "Shared", "IO", $controllerName]));
        $isExist = file_exists($actionInterfacePath);
        if ($isExist === false) {
            mkdir($actionInterfacePath, 0777, true);
        }

        //file of action input
        $fileInputModelPath = $actionInterfacePath . DIRECTORY_SEPARATOR . $inputClassName . '.php';
        $handle = fopen($fileInputModelPath, 'w+');
        //Foreach all properties of input model
        $content = '';
        $defaultValues = '';
        $schemas = '';
        foreach ($modelInput as $name => $type) {
            $content .= self::bind(self::PROPERTIES_MODEL, array(
                'namespace' => $controllerName,
                'propertiesName' => lcfirst($name),
                'type' => $type,
                'actionName' => $actionName,
                'name' => ucfirst($name),
                'interfaceName' => $inputClassName
            ));

            switch ($type) {
                case 'int':
                    $defaultValue = '0';
                    break;
                case 'float':
                    $defaultValue = '0.0';
                    break;
                case 'string':
                    $defaultValue = '""';
                    break;
                case 'boolean':
                    $defaultValue = 'true';
                    break;
                default:
                    $defaultValue = 'null';
            }
            $schemas .= "\t\t\t'" . lcfirst($name) . "',\n";
            $defaultValues .= "\t\t\$this->". lcfirst($name) . " = $defaultValue;\n";
        }
        $newContent = self::bind(self::INPUT_OUTPUT_MODEL_TEMPLATE, array(
            'namespace' => $controllerName,
            'actionName' => $actionName,
            'interfaceName' => $inputClassName,
            'classContent' => $content,
            'defaultValues' => $defaultValues,
            'schemas' => $schemas,
            'io' => 'Input'
        ));
        fwrite($handle, $newContent);
        fclose($handle);

        //File of action output
        $fileInputModelPath = $actionInterfacePath . DIRECTORY_SEPARATOR . $outputClassName . '.php';
        $handle = fopen($fileInputModelPath, 'w+');
        //Foreach all properties of input model
        $content = '';
        $defaultValues = '';
        $schemas = '';
        foreach ($modelOutput as $name => $type) {
            $content .= self::bind(self::PROPERTIES_MODEL, array(
                'namespace' => $controllerName,
                'propertiesName' => lcfirst($name),
                'type' => $type,
                'actionName' => $actionName,
                'name' => ucfirst($name),
                'interfaceName' => $outputClassName
            ));

            switch ($type) {
                case 'int':
                    $defaultValue = '0';
                    break;
                case 'float':
                    $defaultValue = '0.0';
                    break;
                case 'string':
                    $defaultValue = '""';
                    break;
                case 'boolean':
                    $defaultValue = 'true';
                    break;
                default:
                    $defaultValue = 'null';
            }
            $schemas .= "\t\t\t'" . lcfirst($name) . "',\n";
            $defaultValues .= "\t\t\$this->" . lcfirst($name) . " = $defaultValue;\n";
        }

        $newContent = self::bind(self::INPUT_OUTPUT_MODEL_TEMPLATE, array(
            'namespace' => $controllerName,
            'actionName' => $actionName,
            'interfaceName' => $outputClassName,
            'classContent' => $content,
            'defaultValues' => $defaultValues,
            'schemas' => $schemas,
            'io' => 'Output'
        ));
        fwrite($handle, $newContent);
        fclose($handle);
    }

    private function getActionNamespaces($controllerName, $routeName, $actions)
    {
        $actionNamespaces = '';
        foreach ($actions as $actionName => $actionIOs) {
            foreach ($actionIOs as $actionIO) {
                $actionNamespaces .= "use App\Shared\IO\\$controllerName". '\\' . "$actionIO" . ";\n";
            }
        }
        return $actionNamespaces;
    }

    private function generateController($route, $actions)
    {
        $controllerName = $route->controllerName;
        $actionName = $route->actionName;
        $authorName = $route->author;

        //Check file exists
        $controllerPath = self::base_path(implode(DIRECTORY_SEPARATOR, ["src", "Controller"]));
        $isExist = file_exists($controllerPath);
        if ($isExist === false) {
            mkdir($controllerPath, 0777, true);
        }
        $fileControllerPath = $controllerPath . DIRECTORY_SEPARATOR . $controllerName . '.php';
        $data = '';
        $isNew = false;
        if (file_exists($fileControllerPath)) {
            $handle = fopen($fileControllerPath, 'r');
            $data = fread($handle, filesize($fileControllerPath));
        } else {
            $handle = fopen($fileControllerPath, 'wr');
            $newAction = $this->appendToFile($handle, $route);
            $newClass = self::bind(self::CLASS_TEMPLATE, array(
                'classContent' => $newAction,
                'className' => $controllerName,
                'authorName' => $authorName,
                'actionNamespaces' => $this->getActionNamespaces($route->controllerName, $route->name, $actions)
            ));
            fwrite($handle, $newClass);
            $isNew = true;
        }
        //Check if action already exists
        $findAction = mb_strpos($data, $actionName . '(');
        if ($findAction === false && !$isNew) {
            $newAction = $this->appendToFile($handle, $route);
            $allContents = file($fileControllerPath);
            $last = sizeof($allContents) - 1;
            unset($allContents[$last]);
            $handle = fopen($fileControllerPath, 'w+');
            $newContent = implode('', $allContents) . $newAction . "\r\n}";
            fwrite($handle, $newContent);
        }

        fclose($handle);
    }

    private function generateControllerTest($route, $actions)
    {
        $routeName = $route->controllerName;
        $controllerName = $route->controllerName;
        $actionName = $route->actionName;
        $authorName = $route->author;

        //Check file exists
        $controllerPath = self::base_path(implode(DIRECTORY_SEPARATOR, ['test', 'Controller']));
        $isExist = file_exists($controllerPath);
        if ($isExist === false) {
            mkdir($controllerPath, 0777, true);
        }
        $fileControllerPath = $controllerPath . DIRECTORY_SEPARATOR . $controllerName . 'Test.php';
        $data = '';
        $isNew = false;
        if (file_exists($fileControllerPath)) {
            $handle = fopen($fileControllerPath, 'r');
            $data = fread($handle, filesize($fileControllerPath));
        } else {
            $handle = fopen($fileControllerPath, 'wr');
            $newAction = $this->appendToTestFile($handle, $route);
            $newClass = self::bind(self::CLASS_TEST_TEMPLATE, array(
                'namespace' => $routeName,
                'classContent' => $newAction,
                'className' => $routeName,
                'authorName' => $authorName,
                'actionNamespaces' => $this->getActionNamespaces($route->controllerName, $route->name, $actions)
            ));
            fwrite($handle, $newClass);
            $isNew = true;
        }

        //Check if action already exists
        $findAction = mb_strpos($data, 'test' . ucfirst($actionName) . '(');
        if ($findAction === false && !$isNew) {
            $newAction = $this->appendToTestFile($handle, $route);
            $allContents = file($fileControllerPath);
            $last = sizeof($allContents) - 1;
            unset($allContents[$last]);
            $handle = fopen($fileControllerPath, 'w+');
            $newContent = implode('', $allContents) . $newAction . "\r\n}";
            fwrite($handle, $newContent);
        }

        fclose($handle);
    }

    private function appendToFile($handle, $route)
    {
        $actionName = $route->actionName;
        $actionNameUpper = ucfirst($actionName);
        $description = $route->description;
        $author = $route->author;
        $routePath = $route->route;
        $controllerName = $route->controllerName;
        $inputClassName = $route->inputClassName;
        $outputClassName = $route->outputClassName;
        $method = $route->method;
        $modelOutput = is_array($route->output);
        // Request is a required argument for any action
        // Developer can use it to retrieve more things from request
        $actionArguments = 'Request $request, ';
        $parameters = "     * @param Request \$request\n";
        $comments = '';
        $declarations = '';
        if ($method !== 'GET') {
            $comments .= "\t\t/** @var $inputClassName" . ' $input */';
            $comments .= "\n";
            $declarations = "\t\t\$input = JSONHelper::map(\$request, $inputClassName::class);\n";
        }

        if ($modelOutput) {
            $comments .= "\t\t/** @var array " . '$output */';
            $declarations .= "\t\t\$outputItem = new $outputClassName();\n";
            $declarations .= "\t\t\$output = array();\n";
        } else {
            $comments .= "\t\t/** @var $outputClassName" . ' $output */';
            $declarations .= "\t\t\$output = new $outputClassName();\n";
        }

        preg_match_all("/(?<=\{)[a-zA-Z0-9]+(?=\})/", $route->route, $output_array);
        if (count($output_array) > 0) {
            foreach ($output_array[0] as $key => $match) {
                $actionArguments .= "\$$match, ";
                $parameters .= "     * @param string \$$match\n";
            }
        }

        // Has more arguments then cut off 2 last characters
        $actionArguments = substr($actionArguments, 0, strlen($actionArguments) - 2);

        $newAction = self::bind(self::METHOD_TEMPLATE, array(
            'description' => $description,
            'namespace' => $controllerName,
            'author' => $author,
            'route' => $routePath,
            'method' => $method,
            'comments' => $comments,
            'declarations' => $declarations,
            'parameters' => rtrim($parameters, "\n"),
            'inputClassName' => $inputClassName,
            'outputClassName' => $outputClassName,
            'actionName' => $actionName,
            'actionArguments' => $actionArguments,
            'actionNameUpper' => $actionNameUpper,
        ));

        $newAction .= "\n";

        return $newAction;
    }

    private function appendToTestFile($handle, $route)
    {
        $actionName = $route->actionName;
        $actionNameUpper = ucfirst($actionName);
        $description = $route->description;
        $author = $route->author;
        $routePath = $route->route;
        $routeName = $route->name;
        $controllerName = $route->controllerName;
        $inputClassName = $route->inputClassName;
        $outputClassName = $route->outputClassName;
        $method = $route->method;
        $methodLowerCase = strtolower($route->method);

        // Request is a required argument for any action
        // Developer can use it to retrieve more things from request
        $parameters = '';
        $comments = '';
        if ($method !== 'GET') {
            $comments .= "\t\t/** @var $inputClassName" . ' $input */';
            $comments .= "\n";
            $parameters = '';
        }

        preg_match_all("/(?<=\{)[a-zA-Z0-9]+(?=\})/", $route->route, $input_array);
        if (count($input_array) > 0) {
            foreach ($input_array[0] as $key => $match) {
                $parameters .= "'$match' => 'test', ";
            }
        }

        if (strlen($parameters) > 0) {
            $parameters = substr($parameters, 0, strlen($parameters) - 2);
        }

        $inputDeclaration = '';
        if ($method != 'GET') {
            $inputDeclaration ="\n\t\t/** @var $inputClassName \$input */\n\t\t\$input = new $inputClassName();";
        }

        $newAction = self::bind(self::METHOD_TEST_TEMPLATE, array(
            'description' => $description,
            'namespace' => $controllerName,
            'author' => $author,
            'route' => $routePath,
            'method' => $method,
            'methodLowerCase' => $methodLowerCase,
            'comments' => $comments,
            'parameters' => rtrim($parameters, "\n"),
            'inputClassName' => $inputClassName,
            'outputClassName' => $outputClassName,
            'actionName' => ucfirst($actionName),
            'actionNameUpper' => $actionNameUpper,
            'inputDeclaration' => $inputDeclaration,
            'inputVariable' => strlen($inputDeclaration) > 0 ? ', $input->toArray()' : ''
        ));

        $newAction .= "\n";

        return $newAction;
    }

    public function generateSwagger($flatRoutes)
    {
        $swaggerContent = self::SWAGGER_TEMPLATE;
        $swaggerPaths = '';
        $swaggerTags = [];
        $paths = [];
        $tags = [];
        foreach ($flatRoutes as $route) {
            if (!isset($paths[$route->route])) {
                $paths[$route->route] = array();
            }
            if (!isset($tags[$route->name])) {
                $tag = [
                    'name' => $route->name,
                ];
                $swaggerTags []= $tag;
                $tags[$route->name] = array();
            }

            $swaggerPathContent = self::bind(self::SWAGGER_PATH_TEMPLATE, [
                'route' => $route->route,
                'tag' => $route->name,
                'method' => strtolower($route->method),
                'routeName' => $route->actionName,
                'description' => $route->description
            ]);
            $paths[$route->route][] = $swaggerPathContent;
        }

        foreach ($paths as $route => $pathContents) {
            $swaggerPaths .= "\t\"$route\" : {\n";
            foreach ($pathContents as $pathContent) {
                $swaggerPaths .= $pathContent . ",\n";
            }
            $swaggerPaths = substr($swaggerPaths, 0, strlen($swaggerPaths) - 2);
            $swaggerPaths .= "\n\t},\n";
        }
        if (strlen($swaggerPaths) > 0) {
            $swaggerPaths = substr($swaggerPaths, 0, strlen($swaggerPaths) - 2);
        }
        $swaggerContent = self::bind($swaggerContent, [
            'tag' => json_encode($swaggerTags),
            'path' => $swaggerPaths
        ]);
        file_put_contents($this->swaggerDist, $swaggerContent);
    }
}

$apiGenerator = new ApiGenerator();
$apiGenerator
    ->setIdentifier("// AUTO GENERATED - DO NOT MODIFY FROM HERE")
    ->setConfigurationDirectory('./config/api')
    ->setServerRoot('.')
    ->setServerInterfaces('src/Shared/IO')
    ->setSwaggerDist('public/docs/api.json');
$flatRoutes = $apiGenerator->compileFlatRoutes();
$apiGenerator->generateRoute($flatRoutes);
$apiGenerator->generateSwagger($flatRoutes);
