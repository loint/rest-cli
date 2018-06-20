# Command line supports for PHP Micro Services

### Prerequisite
- [x] Python for Rest
- [x] PHP 7.2
- [x] Laravel Lumen 5.6
- [x] Doctrine Migrations
- [x] PHPUnit 7.2

### Installation
```
make && sudo make install
```

### Road map
- [x] Reverse database to model - repository
- [ ] Compile routes and generate controller with test cases
- [ ] Generate swagger documentation base on routes
- [ ] Generate micro-service interfaces for inter-communication

### Usages (in proposals)
1. Create micro-service application
```
rest create user
```
2. Enter user service and write some migrations and up them with
```
rest migrate
```
3. Synchronous model - repository and service base on schema
```
rest sync
```
4. Create some endpoints in /api then controller and integration test will be ready
```
rest api
```
5. Generate Swagger documentation base
```
rest doc
```
6. Serve your application to test in browser with
```
rest serve
```