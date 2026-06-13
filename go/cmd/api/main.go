package main

import (
	"context"
	"fmt"
	"log"
	"net/http"
	"os"
	"os/signal"
	"syscall"
	"time"

	"github.com/jackc/pgx/v5/pgxpool"

	"github.com/web-platform/backend/internal/api"
	"github.com/web-platform/backend/internal/config"
	"github.com/web-platform/backend/internal/infra"
)

func main() {
	cfg := config.Load()
	ctx, cancel := context.WithTimeout(context.Background(), 30*time.Second)
	defer cancel()

	// PostgreSQL
	pool, err := pgxpool.New(ctx, cfg.DatabaseURL)
	if err != nil {
		log.Fatalf("postgres pool: %v", err)
	}
	defer pool.Close()

	if err := pool.Ping(ctx); err != nil {
		log.Fatalf("postgres ping: %v", err)
	}
	log.Println("postgres connected")

	// Redis (optional)
	var cache *infra.Cache
	if cfg.RedisURL != "" {
		c, err := infra.NewCache(ctx, cfg.RedisURL)
		if err != nil {
			log.Printf("redis unavailable (skipping): %v", err)
		} else {
			cache = c
			defer cache.Close()
			log.Println("redis connected")
		}
	}

	// NATS (optional)
	var eb *infra.EventBus
	if cfg.NATSURL != "" {
		e, err := infra.NewEventBus(cfg.NATSURL)
		if err != nil {
			log.Printf("nats unavailable (skipping): %v", err)
		} else {
			eb = e
			defer eb.Close()
			log.Println("nats connected")
		}
	}

	// OSRM (optional)
	osrm := infra.NewOSRM(cfg.OSRMURL)

	// Router
	router := api.NewRouter(cfg, pool, cache, osrm)

	srv := &http.Server{
		Addr:         cfg.Addr(),
		Handler:      router,
		ReadTimeout:  15 * time.Second,
		WriteTimeout: 30 * time.Second,
		IdleTimeout:  60 * time.Second,
	}

	// Graceful shutdown
	go func() {
		sigCh := make(chan os.Signal, 1)
		signal.Notify(sigCh, syscall.SIGINT, syscall.SIGTERM)
		<-sigCh
		log.Println("shutting down...")
		shutdownCtx, shutdownCancel := context.WithTimeout(context.Background(), 10*time.Second)
		defer shutdownCancel()
		srv.Shutdown(shutdownCtx)
	}()

	log.Printf("server starting on %s", cfg.Addr())
	if err := srv.ListenAndServe(); err != nil && err != http.ErrServerClosed {
		log.Fatalf("server: %v", err)
	}
	log.Println("server stopped")
}
