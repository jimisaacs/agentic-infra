import { useReducer, useEffect, useRef, useCallback, useState } from "react";
import type { CheckResult, MonitoredTarget } from "./types";
import { CheckForm } from "./components/CheckForm";
import { ResultCard } from "./components/ResultCard";
import { CheckHistory } from "./components/CheckHistory";

type Action =
  | { type: "ADD_TARGET"; id: string; url: string }
  | { type: "REMOVE_TARGET"; id: string }
  | { type: "CHECK_START"; id: string }
  | { type: "CHECK_SUCCESS"; id: string; result: CheckResult }
  | { type: "CHECK_ERROR"; id: string; error: string }
  | { type: "TOGGLE_POLLING"; id: string };

function reducer(
  state: MonitoredTarget[],
  action: Action,
): MonitoredTarget[] {
  switch (action.type) {
    case "ADD_TARGET":
      return [
        ...state,
        {
          id: action.id,
          url: action.url,
          checks: [],
          polling: true,
          intervalMs: 30_000,
          loading: false,
          error: null,
        },
      ];
    case "REMOVE_TARGET":
      return state.filter((t) => t.id !== action.id);
    case "CHECK_START":
      return state.map((t) =>
        t.id === action.id ? { ...t, loading: true, error: null } : t,
      );
    case "CHECK_SUCCESS":
      return state.map((t) =>
        t.id === action.id
          ? {
              ...t,
              loading: false,
              checks: [action.result, ...t.checks].slice(0, 60),
              error: null,
            }
          : t,
      );
    case "CHECK_ERROR":
      return state.map((t) =>
        t.id === action.id
          ? { ...t, loading: false, error: action.error }
          : t,
      );
    case "TOGGLE_POLLING":
      return state.map((t) =>
        t.id === action.id ? { ...t, polling: !t.polling } : t,
      );
  }
}

let nextId = 0;

const STORAGE_KEY = "pulse";

function loadPersistedState(): MonitoredTarget[] {
  try {
    const raw = sessionStorage.getItem(STORAGE_KEY);
    if (!raw) return [];
    const targets: MonitoredTarget[] = JSON.parse(raw);
    for (const t of targets) {
      const n = parseInt(t.id, 10);
      if (n > nextId) nextId = n;
    }
    return targets.map((t) => ({ ...t, loading: false, error: null }));
  } catch {
    return [];
  }
}

function getNotifPermission(): NotificationPermission | "unsupported" {
  return "Notification" in window ? Notification.permission : "unsupported";
}

function notify(target: string, error?: string) {
  if (getNotifPermission() === "granted") {
    new Notification("Pulse: endpoint down", {
      body: error ? `${target}\n${error}` : target,
      tag: target,
    });
  }
}

export function App() {
  const [targets, dispatch] = useReducer(
    reducer,
    null,
    loadPersistedState,
  );
  const targetsRef = useRef(targets);
  targetsRef.current = targets;

  useEffect(() => {
    sessionStorage.setItem(STORAGE_KEY, JSON.stringify(targets));
  }, [targets]);

  const checkTarget = useCallback(async (id: string, url: string) => {
    dispatch({ type: "CHECK_START", id });
    const controller = new AbortController();
    const timer = setTimeout(() => controller.abort(), 15_000);
    try {
      const endpoint =
        url === "pulse://coin"
          ? "/api/coin"
          : `/api/check?target=${encodeURIComponent(url)}`;
      const res = await fetch(endpoint, { signal: controller.signal });
      if (!res.ok) throw new Error(`HTTP ${res.status}`);
      const result: CheckResult = await res.json();
      const prev = targetsRef.current.find((t) => t.id === id);
      const wasAlreadyDown = prev?.checks[0]?.status === "down";
      dispatch({ type: "CHECK_SUCCESS", id, result });
      if (result.status === "down" && !wasAlreadyDown && !notifMutedRef.current) {
        notify(result.target, result.error);
      }
    } catch (err) {
      const message =
        err instanceof Error ? err.message : "Unknown error";
      dispatch({ type: "CHECK_ERROR", id, error: message });
    } finally {
      clearTimeout(timer);
    }
  }, []);

  const [notifPerm, setNotifPerm] = useState(getNotifPermission);
  const [notifMuted, setNotifMuted] = useState(
    () => localStorage.getItem("pulse-muted") === "1",
  );
  const notifMutedRef = useRef(notifMuted);
  notifMutedRef.current = notifMuted;

  async function toggleNotifications() {
    if (!("Notification" in window)) return;
    if (notifPerm === "granted") {
      setNotifMuted((m) => {
        localStorage.setItem("pulse-muted", m ? "0" : "1");
        return !m;
      });
      return;
    }
    try {
      const perm = await Notification.requestPermission();
      setNotifPerm(perm);
    } catch {
      setNotifPerm(Notification.permission);
    }
  }

  function addTarget(url: string) {
    if (targetsRef.current.some((t) => t.url === url)) return;
    const id = String(++nextId);
    dispatch({ type: "ADD_TARGET", id, url });
    checkTarget(id, url);
  }

  useEffect(() => {
    const id = window.setInterval(() => {
      targetsRef.current.forEach((t) => {
        if (!t.polling || t.loading) return;
        if (t.checks.length === 0 && !t.error) return;
        const last =
          t.checks.length > 0
            ? new Date(t.checks[0].checked_at).getTime()
            : 0;
        if (Date.now() - last >= t.intervalMs) {
          checkTarget(t.id, t.url);
        }
      });
    }, 5_000);
    return () => clearInterval(id);
  }, [checkTarget]);

  const counts = targets.reduce(
    (acc, t) => {
      const status = t.checks[0]?.status;
      if (status) acc[status] = (acc[status] || 0) + 1;
      return acc;
    },
    {} as Record<string, number>,
  );

  return (
    <div className="app">
      <header className="header">
        <div className="logo">
          <span className="logo-dot" />
          <h1 className="logo-text">Pulse</h1>
        </div>
        <p className="tagline">Real-time endpoint monitoring</p>
        {notifPerm !== "unsupported" && (
          <button
            className="notif-toggle"
            onClick={toggleNotifications}
            title={
              notifPerm === "denied"
                ? "Notifications blocked in browser settings"
                : notifPerm === "granted" && notifMuted
                  ? "Notifications muted — click to unmute"
                  : notifPerm === "granted"
                    ? "Notifications on — click to mute"
                    : "Enable notifications for downtime alerts"
            }
          >
            <svg width="16" height="16" viewBox="0 0 16 16" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round">
              <path d="M6 13a2 2 0 0 0 4 0" />
              <path d="M8 1a4.5 4.5 0 0 0-4.5 4.5c0 2.5-1.5 4-1.5 4h12s-1.5-1.5-1.5-4A4.5 4.5 0 0 0 8 1z" />
              {notifPerm !== "granted" || notifMuted ? <line x1="1" y1="1" x2="15" y2="15" /> : null}
            </svg>
          </button>
        )}
      </header>

      {targets.length > 0 && (
        <CheckHistory counts={counts} total={targets.length} />
      )}

      <CheckForm
        onAdd={addTarget}
        monitoredUrls={targets.map((t) => t.url)}
      />

      {targets.length === 0 ? (
        <div className="empty-state">
          <div className="empty-icon">
            <span className="empty-ring" />
            <span className="empty-ring" />
            <span className="empty-ring" />
          </div>
          <p className="empty-text">Add a URL to start monitoring</p>
          <p className="empty-hint">Or try a preset above</p>
        </div>
      ) : (
        <div className="target-grid">
          {targets.map((t) => (
            <ResultCard
              key={t.id}
              target={t}
              onRemove={() =>
                dispatch({ type: "REMOVE_TARGET", id: t.id })
              }
              onTogglePolling={() =>
                dispatch({ type: "TOGGLE_POLLING", id: t.id })
              }
              onRecheck={() => {
                if (!t.loading) checkTarget(t.id, t.url);
              }}
            />
          ))}
        </div>
      )}
    </div>
  );
}
