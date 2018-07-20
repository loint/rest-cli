package src

import "github.com/kataras/iris"

func Routes(app *iris.Application) {
	app.Get("/", func(ctx iris.Context) {
		type Response struct {
			Draw            int `json:"draw"`
			RecordsTotal    int `json:"records_total"`
			RecordsFiltered int `json:"records_filtered"`
		}
		response := Response {
			Draw: 1,
			RecordsTotal: 3,
			RecordsFiltered: 3,
		}
		ctx.JSON(response)
	})
}
