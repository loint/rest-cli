# Rest CLI
[![Build Status](https://travis-ci.org/loint/rest-cli.svg?branch=master)](https://travis-ci.org/loint/rest-cli) [![PyPI version](https://badge.fury.io/py/rest-cli.svg)](https://badge.fury.io/py/rest-cli)

If you love ?
- Beautiful restful web service with standard architecture
- The fastest way to get things done with less human manipulation
- Easy way to scale to hundred units as micro-services ?

Then this powerful tool is the right choice for you.

### Prerequisite
- [x] Docker
- [x] Python 2.7 with pip
- [x] PHP 7.2 with composer

### Installation
```
$ pip install rest-cli
```

### Road map
- [x] Create web service base on a skeleton application
- [x] Database schema migration
- [x] Reverse schema to model - repository - service and dependency injectors
- [x] Provides built-in query annotations
- [ ] Compile api routes and generate controller with test cases
- [x] Serve and test application
- [ ] Generate swagger documentation base on routes
- [ ] Generate micro-service interfaces for inter-communication

### Usages (proposal)
1. Create web service application
- [x] --quite : Quite mode - use default configuration without asking anything
- [x] --mysql : Run a default mysql container with default information
```
$ rest create <awesome-service>
```
2. Change directory to service and write some migrations at `src/Shared/Migration`
```
$ rest migrate
```
3. Synchronize model - repository - service - controller - test
To create some awesome apis, modify your routes at `config/api`
```
$ rest sync
```
4. Update Swagger API documentation base on api routes
```
$ rest doc
```
5. Serve your application to test in browser
```
$ rest serve
```
6. Test your application with PHPUnit
```
$ rest test
```
7. Check current version
```
$ rest version
```
8. Update new version of rest-cli ?
```
$ rest upgrade
```
9. Need more help ?
```
$ rest --help
```