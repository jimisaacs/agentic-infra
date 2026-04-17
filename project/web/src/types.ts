export type Status = "up" | "down" | "degraded";

export interface CheckResult {
  target: string;
  status: Status;
  latency_ms: number;
  checked_at: string;
  error?: string;
}

export interface MonitoredTarget {
  id: string;
  url: string;
  checks: CheckResult[];
  polling: boolean;
  intervalMs: number;
  loading: boolean;
  error: string | null;
}
