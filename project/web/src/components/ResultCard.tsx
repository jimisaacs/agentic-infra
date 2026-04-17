import type { MonitoredTarget } from "../types";

interface ResultCardProps {
  target: MonitoredTarget;
  onRemove: () => void;
  onTogglePolling: () => void;
  onRecheck: () => void;
}

function formatUrl(url: string): string {
  try {
    const u = new URL(url);
    return u.hostname + (u.pathname !== "/" ? u.pathname : "");
  } catch {
    return url;
  }
}

export function ResultCard({
  target,
  onRemove,
  onTogglePolling,
  onRecheck,
}: ResultCardProps) {
  const latest = target.checks[0];
  const status = latest?.status ?? "pending";
  const maxLatency = Math.max(
    ...target.checks.map((c) => c.latency_ms),
    1,
  );

  return (
    <div className="target-card" data-status={status}>
      <div className="target-header">
        <div className="target-status">
          <span
            className={`status-dot${latest ? " status-dot--pulse" : ""}`}
            data-status={status}
          />
          <span className="target-url" title={target.url}>
            {formatUrl(target.url)}
          </span>
        </div>
        <div className="target-actions">
          <button
            className={`action-btn${target.loading ? " action-btn--spin" : ""}`}
            onClick={onRecheck}
            title="Check now"
            disabled={target.loading}
          >
            ↻
          </button>
          <button
            className={`action-btn${target.polling ? " action-btn--active" : ""}`}
            onClick={onTogglePolling}
            title={target.polling ? "Pause polling" : "Resume polling"}
          >
            {target.polling ? "⏸" : "▶"}
          </button>
          <button
            className="action-btn action-btn--danger"
            onClick={onRemove}
            title="Remove"
          >
            ×
          </button>
        </div>
      </div>

      {(target.error || latest?.error) && (
        <div className="target-error">
          {target.error || latest?.error}
        </div>
      )}

      {latest && (
        <div className="target-stats">
          <div className="stat">
            <span className="stat-value" data-status={status}>
              {status}
            </span>
            <span className="stat-label">Status</span>
          </div>
          <div className="stat">
            <span className="stat-value">
              {latest.latency_ms}
              <span className="stat-unit">ms</span>
            </span>
            <span className="stat-label">Latency</span>
          </div>
          <div className="stat">
            <span className="stat-value">{target.checks.length}</span>
            <span className="stat-label">Checks</span>
          </div>
        </div>
      )}

      {target.checks.length > 1 && (
        <div className="sparkline">
          {target.checks
            .slice(0, 60)
            .reverse()
            .map((c, i) => (
              <div
                key={i}
                className="sparkline-bar"
                data-status={c.status}
                style={{
                  height: `${Math.max(8, (c.latency_ms / maxLatency) * 100)}%`,
                }}
                title={`${c.latency_ms}ms \u2013 ${c.status}`}
              />
            ))}
        </div>
      )}

      {target.loading && <div className="target-loading" />}
    </div>
  );
}
