import { useEffect, useState } from "react";

import { Card } from "../components/ui/Card";
import { PageHeader } from "../components/ui/PageHeader";

import {
  getJobDiscoverySettings,
  updateJobDiscoverySettings,
  type JobDiscoverySettings,
} from "../services/api";

export function SettingsPage() {
  const [settings, setSettings] = useState<JobDiscoverySettings | null>(null);

  const [saving, setSaving] = useState(false);

  const [message, setMessage] = useState("");

  useEffect(() => {
    loadSettings();
  }, []);

  async function loadSettings() {
    const data = await getJobDiscoverySettings();

    setSettings(data);
  }

  async function saveSettings() {
    if (!settings) {
      return;
    }

    setSaving(true);

    try {
      const updated = await updateJobDiscoverySettings(settings);

      setSettings(updated);

      setMessage("Settings saved successfully.");
    } finally {
      setSaving(false);
    }
  }

  if (!settings) {
    return (
      <>
        <PageHeader
          title="Settings"
          description="Manage application settings."
        />

        <p className="text-slate-400">Loading...</p>
      </>
    );
  }

  return (
    <>
      <PageHeader title="Settings" description="Manage application settings." />

      <Card>
        <div className="space-y-6">
          <h2 className="text-xl font-semibold text-white">
            Job Discovery Settings
          </h2>

          <div>
            <label className="mb-2 block text-sm text-slate-300">
              Discovery Enabled
            </label>

            <input
              type="checkbox"
              checked={settings.discovery_enabled}
              onChange={(event) =>
                setSettings({
                  ...settings,
                  discovery_enabled: event.target.checked,
                })
              }
            />
          </div>

          <div>
            <label className="mb-2 block text-sm text-slate-300">
              Discovery Interval (minutes)
            </label>

            <input
              type="number"
              value={settings.discovery_interval_minutes}
              onChange={(event) =>
                setSettings({
                  ...settings,
                  discovery_interval_minutes: Number(event.target.value),
                })
              }
              className="w-full rounded border border-slate-700 bg-slate-800 p-2 text-white"
            />
          </div>

          <div>
            <label className="mb-2 block text-sm text-slate-300">
              Connectors
            </label>

            <input
              type="text"
              value={settings.discovery_connectors.join(", ")}
              onChange={(event) =>
                setSettings({
                  ...settings,
                  discovery_connectors: event.target.value
                    .split(",")
                    .map((item) => item.trim())
                    .filter(Boolean),
                })
              }
              className="w-full rounded border border-slate-700 bg-slate-800 p-2 text-white"
            />
          </div>

          <button
            onClick={saveSettings}
            disabled={saving}
            className="rounded bg-blue-600 px-4 py-2 text-white hover:bg-blue-500">
            {saving ? "Saving..." : "Save Settings"}
          </button>

          {message && <p className="text-green-400">{message}</p>}
        </div>
      </Card>
    </>
  );
}
