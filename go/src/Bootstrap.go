package src

import "github.com/kataras/iris"

func Bootstrap(app *iris.Application) {
	app.Run(iris.Addr(":3000"))
}