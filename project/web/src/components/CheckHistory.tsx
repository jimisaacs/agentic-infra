interface CheckHistoryProps {
  counts: Record<string, number>;
  total: number;
}

export function CheckHistory({ counts, total }: CheckHistoryProps) {
  return (
    <div className="status-summary">
      <div className="summary-badge" data-status="total">
        <span className="summary-count">{total}</span>
        <span className="summary-label">Monitored</span>
      </div>
      {(counts.up ?? 0) > 0 && (
        <div className="summary-badge" data-status="up">
          <span className="summary-count">{counts.up}</span>
          <span className="summary-label">Up</span>
        </div>
      )}
      {(counts.degraded ?? 0) > 0 && (
        <div className="summary-badge" data-status="degraded">
          <span className="summary-count">{counts.degraded}</span>
          <span className="summary-label">Degraded</span>
        </div>
      )}
      {(counts.down ?? 0) > 0 && (
        <div className="summary-badge" data-status="down">
          <span className="summary-count">{counts.down}</span>
          <span className="summary-label">Down</span>
        </div>
      )}
    </div>
  );
}
