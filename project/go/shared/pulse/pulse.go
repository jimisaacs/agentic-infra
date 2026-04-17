package pulse

import (
	"fmt"
	"net"
	"net/http"
	"net/url"
	"time"
)

type Status string

const (
	StatusUp       Status = "up"
	StatusDown     Status = "down"
	StatusDegraded Status = "degraded"
)

type CheckResult struct {
	Target    string    `json:"target"`
	Status    Status    `json:"status"`
	LatencyMs int64     `json:"latency_ms"`
	CheckedAt time.Time `json:"checked_at"`
	Error     string    `json:"error,omitempty"`
}

var client = &http.Client{Timeout: 5 * time.Second}

func Check(target string) CheckResult {
	start := time.Now()
	result := CheckResult{
		Target:    target,
		CheckedAt: start,
	}

	if err := validateTarget(target); err != nil {
		result.Status = StatusDown
		result.Error = err.Error()
		return result
	}

	resp, err := client.Get(target)
	result.LatencyMs = time.Since(start).Milliseconds()

	if err != nil {
		result.Status = StatusDown
		result.Error = err.Error()
		return result
	}
	defer resp.Body.Close()

	switch {
	case resp.StatusCode >= 200 && resp.StatusCode < 400:
		result.Status = StatusUp
	case resp.StatusCode >= 400 && resp.StatusCode < 500:
		result.Status = StatusDegraded
		result.Error = fmt.Sprintf("HTTP %d", resp.StatusCode)
	default:
		result.Status = StatusDown
		result.Error = fmt.Sprintf("HTTP %d", resp.StatusCode)
	}
	return result
}

func validateTarget(raw string) error {
	u, err := url.Parse(raw)
	if err != nil {
		return fmt.Errorf("invalid URL: %w", err)
	}
	if u.Scheme != "http" && u.Scheme != "https" {
		return fmt.Errorf("unsupported scheme %q: use http or https", u.Scheme)
	}
	host := u.Hostname()
	if host == "" {
		return fmt.Errorf("missing hostname")
	}
	ips, err := net.LookupIP(host)
	if err != nil {
		return fmt.Errorf("DNS lookup failed: %w", err)
	}
	for _, ip := range ips {
		if ip.IsLoopback() || ip.IsPrivate() || ip.IsLinkLocalUnicast() {
			return fmt.Errorf("target resolves to a private address")
		}
	}
	return nil
}
