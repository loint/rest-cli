<?php
require_once __DIR__.'/../vendor/autoload.php';

$app = new Laravel\Lumen\Application(
    realpath(__DIR__.'/../')
);

$app->singleton(
    Illuminate\Contracts\Debug\ExceptionHandler::class,
    Rest\Exception\Handler::class
);

$app->singleton(
    Illuminate\Contracts\Console\Kernel::class,
    Rest\Console\Kernel::class
);

$app->withFacades();
$app->withEloquent();

$app->configure('database');
$app->configure('cache');


$app->router->group([
    'namespace' => '\App\Controller',
], function ($router) {
    require __DIR__.'/../src/Routes.php';
});

$dependencies = require 'Dependencies.php';
if (!empty($dependencies)) {
    foreach ($dependencies as $dependency) {
        $app->bind($dependency, "$dependency" . "Impl");
    }
}

$app->register(Appzcoder\LumenRoutesList\RoutesCommandServiceProvider::class);

return $app;