package main

import (
	"github.com/kataras/iris"
	"github.com/loint/rest-cli/go/src"
)

func main() {
	app := iris.New()
	src.Dependencies(app)
	src.Routes(app)
	src.Bootstrap(app)
}