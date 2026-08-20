import { useEffect, useState, type KeyboardEvent } from "react";

import { Card } from "../components/ui/Card";
import { PageHeader } from "../components/ui/PageHeader";

import {
  AVAILABLE_CONNECTORS,
  getConnectorLabel,
} from "../constants/connectors";

import {
  getCountries,
  getJobDiscoverySettings,
  getSearchCriteriaSettings,
  getWorkModes,
  updateJobDiscoverySettings,
  updateSearchCriteriaSettings,
  getDiscoveryPreferencesSettings,
  updateDiscoveryPreferencesSettings,
  type DiscoveryPreferencesSettings,
  type JobDiscoverySettings,
  type ReferenceDataItem,
  type SearchCriteriaSettings,
} from "../services/api";

type TagEditorProps = {
  label: string;
  values: string[];
  inputValue: string;
  placeholder: string;
  onInputChange: (value: string) => void;
  onAdd: () => void;
  onRemove: (value: string) => void;
};

function TagEditor({
  label,
  values,
  inputValue,
  placeholder,
  onInputChange,
  onAdd,
  onRemove,
}: TagEditorProps) {
  function handleKeyDown(event: KeyboardEvent<HTMLInputElement>) {
    if (event.key === "Enter") {
      event.preventDefault();
      onAdd();
    }
  }

  return (
    <div>
      <label className="mb-2 block text-sm text-slate-300">{label}</label>

      <div className="mb-3 flex flex-wrap gap-2">
        {values.map((value) => (
          <span
            key={value}
            className="inline-flex items-center gap-2 rounded-full border border-slate-600 bg-slate-800 px-3 py-1 text-sm text-white">
            {value}

            <button
              type="button"
              onClick={() => onRemove(value)}
              className="text-slate-400 hover:text-red-400"
              aria-label={`Remove ${value}`}>
              x
            </button>
          </span>
        ))}

        {values.length === 0 && (
          <span className="text-sm text-slate-500">No value configured.</span>
        )}
      </div>

      <div className="flex gap-2">
        <input
          type="text"
          value={inputValue}
          placeholder={placeholder}
          onChange={(event) => onInputChange(event.target.value)}
          onKeyDown={handleKeyDown}
          className="w-full rounded border border-slate-700 bg-slate-800 p-2 text-white"
        />

        <button
          type="button"
          onClick={onAdd}
          className="rounded bg-slate-700 px-4 py-2 text-white hover:bg-slate-600">
          Add
        </button>
      </div>
    </div>
  );
}

function normalizeValues(values: string[]): string[] {
  return values
    .flatMap((value) => value.split(",").map((item) => item.trim()))
    .filter(Boolean);
}

function getCountryLabel(
  countries: ReferenceDataItem[],
  countryCode: string,
): string {
  const country = countries.find((item) => item.code === countryCode);

  if (!country) {
    return countryCode;
  }

  return `${country.name} (${country.code})`;
}

export function SettingsPage() {
  const [settings, setSettings] = useState<JobDiscoverySettings | null>(null);

  const [searchCriteria, setSearchCriteria] =
    useState<SearchCriteriaSettings | null>(null);

  const [discoveryPreferences, setDiscoveryPreferences] =
    useState<DiscoveryPreferencesSettings | null>(null);

  const [countries, setCountries] = useState<ReferenceDataItem[]>([]);

  const [workModes, setWorkModes] = useState<ReferenceDataItem[]>([]);

  const [selectedCountryCode, setSelectedCountryCode] = useState("");

  const [selectedConnectorCode, setSelectedConnectorCode] = useState("");

  const [newTargetJobTitle, setNewTargetJobTitle] = useState("");

  const [newIncludedKeyword, setNewIncludedKeyword] = useState("");

  const [newExcludedKeyword, setNewExcludedKeyword] = useState("");

  const [saving, setSaving] = useState(false);

  const [message, setMessage] = useState("");

  useEffect(() => {
    loadSettings();
  }, []);

  async function loadSettings() {
    const [
      discoverySettings,
      criteriaSettings,
      discoveryPreferencesSettings,
      countryOptions,
      workModeOptions,
    ] = await Promise.all([
      getJobDiscoverySettings(),
      getSearchCriteriaSettings(),
      getDiscoveryPreferencesSettings(),
      getCountries(),
      getWorkModes(),
    ]);

    setDiscoveryPreferences(discoveryPreferencesSettings);

    setSettings(discoverySettings);

    setCountries(countryOptions);

    setWorkModes(workModeOptions);

    setSearchCriteria({
      target_job_titles: normalizeValues(criteriaSettings.target_job_titles),
      preferred_countries: normalizeValues(
        criteriaSettings.preferred_countries,
      ),
      work_modes: normalizeValues(criteriaSettings.work_modes),
      included_keywords: normalizeValues(criteriaSettings.included_keywords),
      excluded_keywords: normalizeValues(criteriaSettings.excluded_keywords),
    });
  }

  function addSearchCriteriaValue(
    field: keyof SearchCriteriaSettings,
    value: string,
    resetInput: () => void,
  ) {
    if (!searchCriteria) {
      return;
    }

    const cleanValue = value.trim();

    if (!cleanValue) {
      return;
    }

    const alreadyExists = searchCriteria[field].some(
      (existingValue) =>
        existingValue.toLowerCase() === cleanValue.toLowerCase(),
    );

    if (alreadyExists) {
      resetInput();
      return;
    }

    setSearchCriteria({
      ...searchCriteria,
      [field]: [...searchCriteria[field], cleanValue],
    });

    resetInput();
  }

  function removeSearchCriteriaValue(
    field: keyof SearchCriteriaSettings,
    value: string,
  ) {
    if (!searchCriteria) {
      return;
    }

    const updatedValues = searchCriteria[field].filter(
      (existingValue) => existingValue !== value,
    );

    setSearchCriteria({
      ...searchCriteria,
      [field]: updatedValues,
    });
  }

  function addPreferredCountry() {
    if (!searchCriteria || !selectedCountryCode) {
      return;
    }

    const alreadyExists =
      searchCriteria.preferred_countries.includes(selectedCountryCode);

    if (alreadyExists) {
      setSelectedCountryCode("");
      return;
    }

    setSearchCriteria({
      ...searchCriteria,
      preferred_countries: [
        ...searchCriteria.preferred_countries,
        selectedCountryCode,
      ],
    });

    setSelectedCountryCode("");
  }

  function addDiscoveryConnector() {
    if (!settings || !selectedConnectorCode) {
      return;
    }

    const alreadyExists = settings.discovery_connectors.includes(
      selectedConnectorCode,
    );

    if (alreadyExists) {
      setSelectedConnectorCode("");
      return;
    }

    setSettings({
      ...settings,
      discovery_connectors: [
        ...settings.discovery_connectors,
        selectedConnectorCode,
      ],
    });

    setSelectedConnectorCode("");
  }

  function removeDiscoveryConnector(connectorCode: string) {
    if (!settings) {
      return;
    }

    setSettings({
      ...settings,
      discovery_connectors: settings.discovery_connectors.filter(
        (existingConnector) => existingConnector !== connectorCode,
      ),
    });
  }

  function toggleWorkMode(workModeName: string) {
    if (!searchCriteria) {
      return;
    }

    const isSelected = searchCriteria.work_modes.includes(workModeName);

    setSearchCriteria({
      ...searchCriteria,
      work_modes: isSelected
        ? searchCriteria.work_modes.filter(
            (existingWorkMode) => existingWorkMode !== workModeName,
          )
        : [...searchCriteria.work_modes, workModeName],
    });
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

  async function saveSearchCriteria() {
    if (!searchCriteria) {
      return;
    }

    setSaving(true);

    try {
      const updated = await updateSearchCriteriaSettings(searchCriteria);

      setSearchCriteria({
        target_job_titles: normalizeValues(updated.target_job_titles),
        preferred_countries: normalizeValues(updated.preferred_countries),
        work_modes: normalizeValues(updated.work_modes),
        included_keywords: normalizeValues(updated.included_keywords),
        excluded_keywords: normalizeValues(updated.excluded_keywords),
      });

      setMessage("Search criteria saved successfully.");
    } finally {
      setSaving(false);
    }
  }

  async function saveDiscoveryPreferences() {
    if (!discoveryPreferences) {
      return;
    }

    setSaving(true);

    try {
      const updated =
        await updateDiscoveryPreferencesSettings(discoveryPreferences);

      setDiscoveryPreferences(updated);

      setMessage("Discovery preferences saved successfully.");
    } finally {
      setSaving(false);
    }
  }

  if (!settings || !searchCriteria || !discoveryPreferences) {
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

      <div className="space-y-6">
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
              <div>
                <label className="mb-2 block text-sm text-slate-300">
                  Connectors ({settings.discovery_connectors.length})
                </label>

                <div className="mb-3 flex flex-wrap gap-2">
                  {settings.discovery_connectors.map((connectorCode) => (
                    <span
                      key={connectorCode}
                      className="inline-flex items-center gap-2 rounded-full border border-slate-600 bg-slate-800 px-3 py-1 text-sm text-white">
                      {getConnectorLabel(connectorCode)}

                      <button
                        type="button"
                        onClick={() => removeDiscoveryConnector(connectorCode)}
                        className="text-slate-400 hover:text-red-400">
                        x
                      </button>
                    </span>
                  ))}

                  {settings.discovery_connectors.length === 0 && (
                    <span className="text-sm text-slate-500">
                      No connector configured.
                    </span>
                  )}
                </div>

                <div className="flex gap-2">
                  <select
                    value={selectedConnectorCode}
                    onChange={(event) =>
                      setSelectedConnectorCode(event.target.value)
                    }
                    className="w-full rounded border border-slate-700 bg-slate-800 p-2 text-white">
                    <option value="">Select a connector</option>

                    {AVAILABLE_CONNECTORS.filter(
                      (connector) =>
                        !settings.discovery_connectors.includes(connector.code),
                    ).map((connector) => (
                      <option key={connector.code} value={connector.code}>
                        {connector.name}
                      </option>
                    ))}
                  </select>

                  <button
                    type="button"
                    onClick={addDiscoveryConnector}
                    className="rounded bg-slate-700 px-4 py-2 text-white hover:bg-slate-600">
                    Add
                  </button>
                </div>
              </div>
            </div>

            <button
              onClick={saveSettings}
              disabled={saving}
              className="rounded bg-blue-600 px-4 py-2 text-white hover:bg-blue-500">
              {saving ? "Saving..." : "Save Settings"}
            </button>
          </div>
        </Card>

        <Card>
          <div className="space-y-6">
            <h2 className="text-xl font-semibold text-white">
              Search Criteria Settings
            </h2>

            <TagEditor
              label={`Target Job Titles (${searchCriteria.target_job_titles.length})`}
              values={searchCriteria.target_job_titles}
              inputValue={newTargetJobTitle}
              placeholder="Add a job title"
              onInputChange={setNewTargetJobTitle}
              onAdd={() =>
                addSearchCriteriaValue(
                  "target_job_titles",
                  newTargetJobTitle,
                  () => setNewTargetJobTitle(""),
                )
              }
              onRemove={(value) =>
                removeSearchCriteriaValue("target_job_titles", value)
              }
            />

            <div>
              <label className="mb-2 block text-sm text-slate-300">
                Preferred Countries ({searchCriteria.preferred_countries.length}
                )
              </label>

              <div className="mb-3 flex flex-wrap gap-2">
                {searchCriteria.preferred_countries.map((countryCode) => (
                  <span
                    key={countryCode}
                    className="inline-flex items-center gap-2 rounded-full border border-slate-600 bg-slate-800 px-3 py-1 text-sm text-white">
                    {getCountryLabel(countries, countryCode)}

                    <button
                      type="button"
                      onClick={() =>
                        removeSearchCriteriaValue(
                          "preferred_countries",
                          countryCode,
                        )
                      }
                      className="text-slate-400 hover:text-red-400"
                      aria-label={`Remove ${countryCode}`}>
                      x
                    </button>
                  </span>
                ))}

                {searchCriteria.preferred_countries.length === 0 && (
                  <span className="text-sm text-slate-500">
                    No country configured.
                  </span>
                )}
              </div>

              <div className="flex gap-2">
                <select
                  value={selectedCountryCode}
                  onChange={(event) =>
                    setSelectedCountryCode(event.target.value)
                  }
                  className="w-full rounded border border-slate-700 bg-slate-800 p-2 text-white">
                  <option value="">Select a country</option>

                  {countries.map((country) => (
                    <option key={country.code} value={country.code}>
                      {country.name} ({country.code})
                    </option>
                  ))}
                </select>

                <button
                  type="button"
                  onClick={addPreferredCountry}
                  className="rounded bg-slate-700 px-4 py-2 text-white hover:bg-slate-600">
                  Add
                </button>
              </div>
            </div>

            <div>
              <label className="mb-2 block text-sm text-slate-300">
                Work Modes ({searchCriteria.work_modes.length})
              </label>

              <div className="flex flex-wrap gap-2">
                {workModes.map((workMode) => {
                  const isSelected = searchCriteria.work_modes.includes(
                    workMode.name,
                  );

                  return (
                    <button
                      key={workMode.code}
                      type="button"
                      onClick={() => toggleWorkMode(workMode.name)}
                      className={
                        isSelected
                          ? "rounded-full border border-blue-500 bg-blue-600/20 px-3 py-1 text-sm text-blue-200"
                          : "rounded-full border border-slate-600 bg-slate-800 px-3 py-1 text-sm text-slate-300 hover:bg-slate-700"
                      }>
                      {isSelected ? "✓ " : ""}
                      {workMode.name}
                    </button>
                  );
                })}

                {workModes.length === 0 && (
                  <span className="text-sm text-slate-500">
                    No work mode available.
                  </span>
                )}
              </div>
            </div>

            <TagEditor
              label={`Included Keywords (${searchCriteria.included_keywords.length})`}
              values={searchCriteria.included_keywords}
              inputValue={newIncludedKeyword}
              placeholder="Add an included keyword"
              onInputChange={setNewIncludedKeyword}
              onAdd={() =>
                addSearchCriteriaValue(
                  "included_keywords",
                  newIncludedKeyword,
                  () => setNewIncludedKeyword(""),
                )
              }
              onRemove={(value) =>
                removeSearchCriteriaValue("included_keywords", value)
              }
            />

            <TagEditor
              label={`Excluded Keywords (${searchCriteria.excluded_keywords.length})`}
              values={searchCriteria.excluded_keywords}
              inputValue={newExcludedKeyword}
              placeholder="Add an excluded keyword"
              onInputChange={setNewExcludedKeyword}
              onAdd={() =>
                addSearchCriteriaValue(
                  "excluded_keywords",
                  newExcludedKeyword,
                  () => setNewExcludedKeyword(""),
                )
              }
              onRemove={(value) =>
                removeSearchCriteriaValue("excluded_keywords", value)
              }
            />

            <button
              onClick={saveSearchCriteria}
              disabled={saving}
              className="rounded bg-blue-600 px-4 py-2 text-white hover:bg-blue-500">
              {saving ? "Saving..." : "Save Search Criteria"}
            </button>
          </div>
        </Card>

        <Card>
          <div className="space-y-6">
            <h2 className="text-xl font-semibold text-white">
              Opportunity Discovery Preferences
            </h2>

            <p className="text-sm text-slate-400">
              Configure how opportunities are displayed and prioritized
              throughout the Opportunities workspace.
            </p>

            <div>
              <label className="mb-2 block text-sm text-slate-300">
                Opportunity Age Window
              </label>

              <select
                value={discoveryPreferences.discovery_age_window}
                onChange={(event) =>
                  setDiscoveryPreferences({
                    ...discoveryPreferences,
                    discovery_age_window: event.target.value,
                  })
                }
                className="w-full rounded border border-slate-700 bg-slate-800 p-2 text-white">
                <option value="7_DAYS">Last 7 Days</option>
                <option value="14_DAYS">Last 14 Days</option>
                <option value="30_DAYS">Last 30 Days</option>
                <option value="90_DAYS">Last 90 Days</option>
                <option value="ALL">All Opportunities</option>
              </select>
            </div>

            <div>
              <label className="mb-2 block text-sm text-slate-300">
                Minimum Matching Score
              </label>

              <select
                value={discoveryPreferences.discovery_minimum_matching_score}
                onChange={(event) =>
                  setDiscoveryPreferences({
                    ...discoveryPreferences,
                    discovery_minimum_matching_score: Number(
                      event.target.value,
                    ),
                  })
                }
                className="w-full rounded border border-slate-700 bg-slate-800 p-2 text-white">
                <option value={0}>0%</option>
                <option value={25}>25%</option>
                <option value={50}>50%</option>
                <option value={75}>75%</option>
              </select>
            </div>

            <div>
              <label className="mb-2 block text-sm text-slate-300">
                Show Archived Opportunities
              </label>

              <input
                type="checkbox"
                checked={discoveryPreferences.discovery_show_archived}
                onChange={(event) =>
                  setDiscoveryPreferences({
                    ...discoveryPreferences,
                    discovery_show_archived: event.target.checked,
                  })
                }
              />
            </div>

            <div>
              <label className="mb-2 block text-sm text-slate-300">
                Default Opportunity Sort
              </label>

              <select
                value={discoveryPreferences.discovery_default_sort}
                onChange={(event) =>
                  setDiscoveryPreferences({
                    ...discoveryPreferences,
                    discovery_default_sort: event.target.value,
                  })
                }
                className="w-full rounded border border-slate-700 bg-slate-800 p-2 text-white">
                <option value="BEST_MATCH_FIRST">Best Match First</option>

                <option value="NEWEST_FIRST">Newest First</option>

                <option value="OLDEST_FIRST">Oldest First</option>
              </select>
            </div>

            <button
              onClick={saveDiscoveryPreferences}
              disabled={saving}
              className="rounded bg-blue-600 px-4 py-2 text-white hover:bg-blue-500">
              {saving ? "Saving..." : "Save Discovery Preferences"}
            </button>
          </div>
        </Card>

        <Card>
          <div className="space-y-6">
            <h2 className="text-xl font-semibold text-white">
              Application Workflow Strategy
            </h2>

            <p className="text-sm text-slate-400">
              These settings explain the current application workflow strategy
              and highlight future enhancements already planned in the roadmap.
            </p>

            <div className="space-y-4 rounded-lg border border-slate-700 bg-slate-900/50 p-4">
              <h3 className="text-lg font-medium text-white">Current MVP</h3>

              <div>
                <p className="font-medium text-white">
                  Application Profile Selection
                </p>
                <p className="text-sm text-slate-400">
                  Selected Profile Context
                </p>
              </div>

              <div>
                <p className="font-medium text-white">
                  Opportunity Context Initialization
                </p>
                <p className="text-sm text-slate-400">
                  First Available Profile
                </p>
              </div>

              <div>
                <p className="font-medium text-white">
                  Opportunity Profile Comparison
                </p>
                <p className="text-sm text-slate-400">All Profiles</p>
              </div>

              <div>
                <p className="font-medium text-white">
                  Multiple Active Profiles
                </p>
                <p className="text-sm text-slate-400">Disabled</p>
              </div>
            </div>

            <div className="space-y-4 rounded-lg border border-blue-900/50 bg-blue-950/20 p-4">
              <h3 className="text-lg font-medium text-white">
                Upcoming Enhancements
              </h3>

              <div>
                <span className="rounded-full border border-blue-500 px-2 py-1 text-xs text-blue-300">
                  APP-005
                </span>

                <p className="mt-2 text-sm text-slate-300">
                  □ Best Matching Profile Preselection
                </p>
              </div>

              <div>
                <span className="rounded-full border border-purple-500 px-2 py-1 text-xs text-purple-300">
                  7.1.22 Multi Profile Opportunity Context
                </span>

                <div className="mt-2 space-y-1 text-sm text-slate-300">
                  <p>□ Ask Every Time</p>
                  <p>□ Last Used Profile</p>
                  <p>□ Active Profile Only</p>
                  <p>□ Multiple Active Profiles</p>
                </div>
              </div>
            </div>
          </div>
        </Card>

        {message && <p className="text-green-400">{message}</p>}
      </div>
    </>
  );
}
