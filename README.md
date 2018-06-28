# Rest CLI
[![Build Status](https://travis-ci.org/loint/rest-cli.svg?branch=master)](https://travis-ci.org/loint/rest-cli) [![PyPI version](https://badge.fury.io/py/rest-cli.svg)](https://badge.fury.io/py/rest-cli) [![Documentation](https://img.shields.io/badge/documentation-rest-ff69b4.svg)](https://loint.github.io/rest-cli/index.md)

If you love ?
- Beautiful restful web service with standard architecture
- The fastest way to get things done with less human manipulation
- Easy way to initialize hundred units in minutes
- Well tested structure with maintainable like Java with the flexible from PHP

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
- [x] Create web service base on a lightweight skeleton
- [x] Database schema migration
- [x] Reverse schema to model - repository - service and dependency injectors
- [x] Support built-in query annotations
- [x] Compile api routes and generate controller with integration tests
- [x] Serve and test application
- [ ] Generate swagger documentation base on api routes
- [ ] Export micro-service interfaces for inter-communication in SOA
- [ ] Support RPC exception via response verification

### Usages
1. Create web service application
- [x] --quite : Quite mode without asking anything about configuration
- [x] --force : Force creating application without complaining about existing project
- [x] --mysql : Start a mysql container with default information
```
$ rest create <awesome-service>
```
2. Change directory to service and write some migrations at `src/Shared/Migration`
```
$ rest migrate
```
3. Synchronize model - repository - service - controller - test cases
- To create some awesome apis, modify your routes at `config/api`
```
$ rest sync
```
4. View route list
- To see which routes are configured and manage apis
```
$ rest route
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