# Rest CLI
[![Build Status](https://travis-ci.org/loint/rest-cli.svg?branch=master)](https://travis-ci.org/loint/rest-cli)

If you love ?
- Beautiful restful web service with standard architecture
- The fastest way to get things done with less human manipulation
- Easy way to scale to hundred units as micro-services ?

Then this powerful tool is the right choice for you.

### Features:
- [x] Skeleton application is powered by Laravel Lumen
- [x] You provide schema and route then "Rest" will do the "rest"

### Prerequisite
- [x] Python 2.7 with pip
- [x] PHP 7.2 with composer

### Installation
```
make && make install
```

### Road map
- [x] Create web service base on skeleton application
- [x] Database schema migration
- [ ] Reverse schema to model - repository - service and DI
- [x] Support annotation query
- [ ] Compile routes and generate controller with test cases
- [x] Serve and test application
- [ ] Generate swagger documentation base on routes
- [ ] Generate micro-service interfaces for inter-communication

### Usages (Proposal)
1. Create web service application
```
$ rest create user
```
2. Enter user service and write some migrations and up them with
```
$ rest migrate
```
3. Synchronous model - repository and service base on schema
```
$ rest sync
```
4. Create some endpoints in /api then controller and integration test will be ready
```
$ rest api
```
5. Generate Swagger documentation base
```
$ rest doc
```
6. Serve your application to test in browser with
```
$ rest serve
```
7. Check current version
```
$ rest version
```
8. Automatically updates
```
$ rest upgrade
```
9. Need more help ?
```
$ rest --help
```