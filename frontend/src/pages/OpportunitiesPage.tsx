import { useEffect, useState } from "react";

import { Card } from "../components/ui/Card";
import { PageHeader } from "../components/ui/PageHeader";
import { getJobOffers } from "../services/api";
import { getMatching } from "../services/api";
import { MatchingResult } from "../components/MatchingResult";

type JobOffer = {
  id: number;
  title: string;
  company_name: string | null;
  location: string | null;
  source: string | null;
  source_url: string | null;
  description: string | null;
  created_at: string;
};

type MatchingData = {
  matching_score: number;
  skills_score: number;
  experience_score: number;
  work_mode_score: number;
  location_score: number;
  matching_skills: string[];
  missing_skills: string[];
  strengths: string[];
  weaknesses: string[];
};

export function OpportunitiesPage() {
  const [offers, setOffers] = useState<JobOffer[]>([]);
  const [selectedOffer, setSelectedOffer] = useState<JobOffer | null>(null);
  const [matching, setMatching] = useState<MatchingData | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    async function loadOffers() {
      try {
        const data = await getJobOffers();

        setOffers(data);

        if (data.length > 0) {
          setSelectedOffer(data[0]);
        }
      } catch {
        setError("Unable to load opportunities.");
      } finally {
        setLoading(false);
      }
    }

    loadOffers();
  }, []);

  useEffect(() => {
    async function loadMatching() {
      if (!selectedOffer) {
        return;
      }

      try {
        const result = await getMatching(1, selectedOffer.id);

        setMatching(result);
      } catch {
        setMatching(null);
      }
    }

    loadMatching();
  }, [selectedOffer]);

  return (
    <>
      <PageHeader
        title="Opportunities"
        description="Explore and analyze opportunities."
      />

      <p className="mb-6 text-sm text-slate-400">
        {offers.length} opportunities found
      </p>

      {loading && <p className="text-slate-400">Loading opportunities...</p>}

      {error && <p className="text-red-500">{error}</p>}

      {!loading && !error && (
        <div className="grid gap-6 lg:grid-cols-3">
          <div className="max-h-[calc(100vh-220px)] overflow-y-auto space-y-3 pr-2">
            {offers.map((offer) => (
              <button
                key={offer.id}
                type="button"
                onClick={() => setSelectedOffer(offer)}
                className={`block w-full rounded-lg text-left transition-all ${
                  selectedOffer?.id === offer.id
                    ? "border-2 border-blue-500 bg-slate-800 shadow-lg shadow-blue-500/20"
                    : ""
                }`}>
                <Card>
                  <h3 className="font-medium text-white">{offer.title}</h3>

                  <p className="text-sm text-slate-300">
                    {offer.company_name ?? "Unknown company"}
                  </p>

                  <p className="text-xs text-slate-500">{offer.location}</p>
                </Card>
              </button>
            ))}
          </div>

          <div className="sticky top-6 self-start lg:col-span-2">
            {selectedOffer ? (
              <Card>
                <h2 className="mb-6 text-3xl font-bold text-white">
                  {selectedOffer.title}
                </h2>

                <div className="mb-8 grid grid-cols-2 gap-4 text-sm text-slate-400">
                  <div>
                    <p className="font-medium text-slate-300">Company</p>

                    <p>{selectedOffer.company_name ?? "Unknown"}</p>
                  </div>

                  <div>
                    <p className="font-medium text-slate-300">Source</p>

                    <p>{selectedOffer.source ?? "Unknown"}</p>
                  </div>

                  <div>
                    <p className="font-medium text-slate-300">Location</p>

                    <p>{selectedOffer.location ?? "Unknown"}</p>
                  </div>

                  <div>
                    <p className="font-medium text-slate-300">Imported</p>

                    <p>{new Date(selectedOffer.created_at).toLocaleString()}</p>
                  </div>
                </div>

                <div className="mb-8">
                  <h3 className="mb-3 text-lg font-semibold text-white">
                    Description
                  </h3>

                  <p className="whitespace-pre-wrap text-slate-300">
                    {selectedOffer.description ?? "No description available."}
                  </p>
                </div>

                <div className="border-t border-slate-700 pt-6">
                  <h3 className="mb-4 text-lg font-semibold text-white">
                    Matching Analysis
                  </h3>

                  {matching ? (
                    <MatchingResult
                      matchingScore={matching.matching_score}
                      skillsScore={matching.skills_score}
                      experienceScore={matching.experience_score}
                      workModeScore={matching.work_mode_score}
                      locationScore={matching.location_score}
                      matchingSkills={matching.matching_skills}
                      missingSkills={matching.missing_skills}
                      strengths={matching.strengths}
                      weaknesses={matching.weaknesses}
                    />
                  ) : (
                    <p className="text-slate-400">
                      Matching information unavailable.
                    </p>
                  )}
                </div>

                <div className="mt-8 border-t border-slate-700 pt-6">
                  <h3 className="mb-2 text-lg font-semibold text-white">
                    AI Recommendations
                  </h3>

                  <p className="text-slate-400">Available in Phase 7.</p>
                </div>

                {selectedOffer.source_url && (
                  <div className="mt-8 border-t border-slate-700 pt-6">
                    <a
                      href={selectedOffer.source_url}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="text-blue-400 hover:text-blue-300">
                      Open Source Offer
                    </a>
                  </div>
                )}
              </Card>
            ) : (
              <Card>
                <p className="text-slate-400">
                  Select an opportunity to view details.
                </p>
              </Card>
            )}
          </div>
        </div>
      )}
    </>
  );
}
