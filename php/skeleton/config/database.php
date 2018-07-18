<?php
return [
    'default' => 'mysql',
    'migrations' => '_migrations',
    'connections' => [
        'mysql' => [
            'read' => [
                'host' => ['127.0.0.1'],
            ],
            'write' => [
                'host' => ['127.0.0.1'],
            ],
            'sticky' => true,
            'driver' => 'mysql',
            'database' => 'database',
            'username' => 'root',
            'password' => 'password',
            'charset' => 'utf8mb4',
            'collation' => 'utf8mb4_unicode_ci',
            'prefix' => '',
        ],
    ]
];
