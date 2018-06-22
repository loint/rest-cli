# Rest CLI
[![Build Status](https://travis-ci.org/loint/rest-cli.svg?branch=master)](https://travis-ci.org/loint/rest-cli)

### Prerequisite
- [x] Python 2.7
- [x] Pip
- [x] PHP 7.2
- [x] Composer

### Installation
```
make && sudo make install
```

### Road map
- [x] Create new service with skeleton
- [x] Serve and test application
- [ ] Schema migration
- [ ] Reverse schema to model - repository
- [ ] Compile routes and generate controller with test cases
- [ ] Generate swagger documentation base on routes
- [ ] Generate micro-service interfaces for inter-communication

### Usages (in proposals)
1. Create micro-service application
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