<?php
namespace RestTest;

use Laravel\Lumen\Testing\TestCase;

abstract class Test extends TestCase
{
    public function createApplication()
    {
        return require realpath(__DIR__ . '/../../../../src/Bootstrap.php');
    }

    public function setUp()
    {
        parent::setUp();
    }

    public function tearDown()
    {
        parent::tearDown();
    }

    public function bind($template, $variables = [], $start = '{', $end = '}')
    {
        $content = $template;
        foreach ($variables as $variableName => $variableValue) {
            $content = \str_replace($start . $variableName . $end, $variableValue, $content);
        }
        return $content;
    }
}
