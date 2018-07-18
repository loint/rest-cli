<?php
// AUTO GENERATED - DO NOT MODIFY FROM HERE
$router->post('/user', [
	'as' => 'user.createUser',
	'uses' => 'UserController@createUser'
]);
$router->get('/user', [
	'as' => 'user.getUsers',
	'uses' => 'UserController@getUsers'
]);
$router->get('/user/{id}', [
	'as' => 'user.getUser',
	'uses' => 'UserController@getUser'
]);
$router->put('/user/{id}', [
	'as' => 'user.updateUser',
	'uses' => 'UserController@updateUser'
]);
$router->delete('/user/{id}', [
	'as' => 'user.deleteUser',
	'uses' => 'UserController@deleteUser'
]);

