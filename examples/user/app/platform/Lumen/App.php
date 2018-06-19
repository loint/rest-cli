<?php
namespace App\Platform\Lumen;

use App\App as AppInterface;

class App implements AppInterface
{
    /**
     * @var \Laravel\Lumen\Application
     */
    private $app;

    public function  __construct()
    {
        $this->app = new \Laravel\Lumen\Application(
            realpath(__DIR__.'/../../')
        );
        $this->app->withEloquent();
    }

    public function bind($abstract, $concrete)
    {
        $this->app->bind($abstract, $concrete, true);
    }
}