package api

import (
	"encoding/json"
	"net/http"

	"github.com/go-chi/chi/v5"
	chimw "github.com/go-chi/chi/v5/middleware"
	"github.com/go-chi/cors"
	"github.com/go-chi/httprate"
	"github.com/jackc/pgx/v5/pgxpool"

	"github.com/web-platform/backend/internal/api/handler"
	"github.com/web-platform/backend/internal/api/middleware"
	"github.com/web-platform/backend/internal/config"
	"github.com/web-platform/backend/internal/infra"
	"github.com/web-platform/backend/internal/repository/postgres"
)

func NewRouter(cfg *config.Config, pool *pgxpool.Pool, cache *infra.Cache, osrm *infra.OSRMClient) *chi.Mux {
	r := chi.NewRouter()

	r.Use(chimw.RequestID)
	r.Use(chimw.RealIP)
	r.Use(chimw.Logger)
	r.Use(chimw.Recoverer)
	r.Use(cors.Handler(middleware.CORS(cfg.CorsOrigin)))
	r.Use(httprate.LimitByIP(100, 60))

	userRepo := postgres.NewUserRepo(pool)
	productRepo := postgres.NewProductRepo(pool)
	orderRepo := postgres.NewOrderRepo(pool)
	courierRepo := postgres.NewCourierRepo(pool)
	rideRepo := postgres.NewRideRepo(pool)
	foodRepo := postgres.NewFoodRepo(pool)
	supportRepo := postgres.NewSupportRepo(pool)

	authH := handler.NewAuthHandler(userRepo, cfg.JWTSecret)
	productH := handler.NewProductHandler(productRepo)
	orderH := handler.NewOrderHandler(orderRepo)
	courierH := handler.NewCourierHandler(courierRepo)
	rideH := handler.NewRideHandler(rideRepo, osrm)
	foodH := handler.NewFoodHandler(foodRepo)
	supportH := handler.NewSupportHandler(supportRepo)

	r.Route("/api/v1", func(r chi.Router) {
		r.Post("/auth/register", authH.Register)
		r.Post("/auth/login", authH.Login)

		r.Get("/products", productH.List)
		r.Get("/products/{id}", productH.Get)

		r.Group(func(r chi.Router) {
			r.Use(middleware.JWTAuth(cfg.JWTSecret))

			r.Post("/orders", orderH.Create)
			r.Get("/orders", orderH.ListMy)
			r.Get("/orders/{id}", orderH.Get)

			r.Group(func(r chi.Router) {
				r.Use(middleware.RequireRole("seller", "admin"))
				r.Post("/products", productH.Create)
				r.Put("/products/{id}", productH.Update)
				r.Delete("/products/{id}", productH.Delete)
			})

			r.Get("/couriers/nearby", courierH.GetNearby)

			r.Post("/rides/estimate", rideH.Estimate)
			r.Post("/rides", rideH.Create)
			r.Get("/rides/{id}", rideH.Get)

			// Food / Restaurants
			r.Group(func(r chi.Router) {
				r.Use(middleware.RequireRole("seller", "admin"))
				r.Post("/food/restaurants", foodH.RegisterRestaurant)
				r.Put("/food/restaurants/{rest_id}", foodH.UpdateRestaurant)
				r.Put("/food/restaurants/{rest_id}/verify", foodH.VerifyRestaurant)
				r.Post("/food/menu", foodH.CreateMenuItem)
				r.Put("/food/menu/{item_id}", foodH.UpdateMenuItem)
				r.Delete("/food/menu/{item_id}", foodH.DeleteMenuItem)
				r.Post("/food/menu/{item_id}/modifiers", foodH.AddModifier)
				r.Delete("/food/menu/{item_id}/modifiers/{mod_id}", foodH.DeleteModifier)
				r.Post("/food/restaurants/{rest_id}/branches", foodH.AddBranch)
				r.Post("/food/restaurants/{rest_id}/zones", foodH.AddZone)
			})

			r.Get("/food/restaurants", foodH.ListRestaurants)
			r.Get("/food/menu/{rest_id}", foodH.GetMenu)
			r.Get("/food/restaurants/{rest_id}/branches", foodH.ListBranches)
			r.Get("/food/restaurants/{rest_id}/zones", foodH.ListZones)

			// Support / Tickets
			r.Post("/tickets", supportH.Create)
			r.Get("/tickets", supportH.ListMy)
			r.Get("/tickets/{ticket_id}", supportH.Get)
			r.Post("/tickets/{ticket_id}/messages", supportH.AddMessage)
			r.Put("/tickets/{ticket_id}/status", supportH.UpdateStatus)
		})
	})

	r.Get("/health", func(w http.ResponseWriter, r *http.Request) {
		writeJSON(w, http.StatusOK, map[string]string{"status": "ok"})
	})

	return r
}

func writeJSON(w http.ResponseWriter, status int, data interface{}) {
	w.Header().Set("Content-Type", "application/json")
	w.WriteHeader(status)
	json.NewEncoder(w).Encode(data)
}
