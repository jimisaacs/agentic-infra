package main

import (
	"context"
	"encoding/json"
	"flag"
	"fmt"
	"log"
	"math/rand/v2"
	"net/http"
	"os"
	"os/signal"
	"path/filepath"
	"syscall"
	"time"

	"pulse/shared/pulse"
)

func main() {
	staticDir := flag.String("static", "", "directory of static files to serve")
	addr := flag.String("addr", ":8080", "listen address")
	flag.Parse()

	mux := http.NewServeMux()

	mux.HandleFunc("GET /api/check", func(w http.ResponseWriter, r *http.Request) {
		target := r.URL.Query().Get("target")
		if target == "" {
			w.Header().Set("Content-Type", "application/json")
			w.WriteHeader(http.StatusBadRequest)
			fmt.Fprint(w, `{"error":"missing ?target= parameter"}`)
			return
		}

		result := pulse.Check(target)
		log.Printf("check %s → %s (%dms)", result.Target, result.Status, result.LatencyMs)

		w.Header().Set("Content-Type", "application/json")
		w.Header().Set("Access-Control-Allow-Origin", "*")
		json.NewEncoder(w).Encode(result)
	})

	mux.HandleFunc("GET /api/coin", func(w http.ResponseWriter, r *http.Request) {
		status := pulse.StatusUp
		latency := rand.IntN(200) + 50
		if rand.IntN(2) == 0 {
			status = pulse.StatusDown
		}
		result := pulse.CheckResult{
			Target:    "coin-flip",
			Status:    status,
			LatencyMs: int64(latency),
			CheckedAt: time.Now(),
		}
		if status == pulse.StatusDown {
			result.Error = "coin landed tails"
		}
		log.Printf("coin  → %s (%dms)", result.Status, result.LatencyMs)
		w.Header().Set("Content-Type", "application/json")
		w.Header().Set("Access-Control-Allow-Origin", "*")
		json.NewEncoder(w).Encode(result)
	})

	mux.HandleFunc("GET /api/health", func(w http.ResponseWriter, r *http.Request) {
		w.Header().Set("Content-Type", "application/json")
		fmt.Fprint(w, `{"status":"ok"}`)
	})

	if *staticDir != "" {
		abs, err := filepath.Abs(*staticDir)
		if err != nil {
			log.Fatalf("invalid static dir: %v", err)
		}
		log.Printf("serving static files from %s", abs)
		mux.Handle("/", spaHandler(abs))
	}

	srv := &http.Server{Addr: *addr, Handler: mux}

	ctx, stop := signal.NotifyContext(context.Background(), os.Interrupt, syscall.SIGTERM)
	defer stop()

	go func() {
		log.Printf("pulse listening on %s", *addr)
		if err := srv.ListenAndServe(); err != nil && err != http.ErrServerClosed {
			log.Fatal(err)
		}
	}()

	<-ctx.Done()
	log.Println("shutting down...")

	shutdownCtx, cancel := context.WithTimeout(context.Background(), 3*time.Second)
	defer cancel()
	if err := srv.Shutdown(shutdownCtx); err != nil {
		log.Fatal(err)
	}
}

// spaHandler serves static files and falls back to index.html for client-side routes.
func spaHandler(root string) http.Handler {
	fs := http.FileServer(http.Dir(root))
	return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		p := filepath.Join(root, filepath.Clean("/"+r.URL.Path))
		if info, err := os.Stat(p); err != nil || info.IsDir() {
			http.ServeFile(w, r, filepath.Join(root, "index.html"))
			return
		}
		fs.ServeHTTP(w, r)
	})
}
