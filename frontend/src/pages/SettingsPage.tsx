import { useEffect, useState, type KeyboardEvent } from "react";

import { Card } from "../components/ui/Card";
import { PageHeader } from "../components/ui/PageHeader";

import {
  getCountries,
  getJobDiscoverySettings,
  getSearchCriteriaSettings,
  getWorkModes,
  updateJobDiscoverySettings,
  updateSearchCriteriaSettings,
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

  const [countries, setCountries] = useState<ReferenceDataItem[]>([]);

  const [workModes, setWorkModes] = useState<ReferenceDataItem[]>([]);

  const [selectedCountryCode, setSelectedCountryCode] = useState("");

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
      countryOptions,
      workModeOptions,
    ] = await Promise.all([
      getJobDiscoverySettings(),
      getSearchCriteriaSettings(),
      getCountries(),
      getWorkModes(),
    ]);

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

  if (!settings || !searchCriteria) {
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

        {message && <p className="text-green-400">{message}</p>}
      </div>
    </>
  );
}
