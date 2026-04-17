import { useState, type FormEvent } from "react";

const PRESETS = [
  { label: "Netflix", url: "https://netflix.com" },
  { label: "GitHub", url: "https://github.com" },
  { label: "Google", url: "https://google.com" },
  { label: "Cloudflare", url: "https://cloudflare.com" },
  { label: "httpbin", url: "https://httpbin.org/" },
  { label: "httpbin 503", url: "https://httpbin.org/status/503" },
  { label: "Coin Flip", url: "pulse://coin" },
];

interface CheckFormProps {
  onAdd: (url: string) => void;
  monitoredUrls: string[];
}

export function CheckForm({ onAdd, monitoredUrls }: CheckFormProps) {
  const [value, setValue] = useState("");

  function handleSubmit(e: FormEvent) {
    e.preventDefault();
    const url = value.trim();
    if (!url) return;
    onAdd(url);
    setValue("");
  }

  const allPresetsAdded = PRESETS.every((p) =>
    monitoredUrls.includes(p.url),
  );

  function addAllPresets() {
    PRESETS.forEach((p, i) => {
      setTimeout(() => onAdd(p.url), i * 300);
    });
  }

  return (
    <div className="add-section">
      <form className="add-form" onSubmit={handleSubmit}>
        <input
          className="add-input"
          type="text"
          value={value}
          onChange={(e) => setValue(e.target.value)}
          placeholder="https://example.com"
          required
        />
        <button className="add-button" type="submit">
          Monitor
        </button>
      </form>
      <div className="presets">
        {PRESETS.map((p) => (
          <button
            key={p.url}
            className="preset-button"
            onClick={() => onAdd(p.url)}
            type="button"
            disabled={monitoredUrls.includes(p.url)}
          >
            {p.label}
          </button>
        ))}
        {!allPresetsAdded && (
          <button
            className="preset-button preset-button--all"
            onClick={addAllPresets}
            type="button"
          >
            Add all
          </button>
        )}
      </div>
    </div>
  );
}
