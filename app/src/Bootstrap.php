<?php
require_once __DIR__.'/../vendor/autoload.php';

$app = new Laravel\Lumen\Application(
    realpath(__DIR__.'/../')
);

$app->withFacades();
$app->withEloquent();

$app->router->group([
    'namespace' => '\App\Controller',
], function () {
    require __DIR__.'/../src/Routes.php';
});

return $app;