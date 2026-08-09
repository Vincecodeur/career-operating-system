import { useEffect, useState } from "react";

import { Card } from "../components/ui/Card";
import { PageHeader } from "../components/ui/PageHeader";
import { getJobOffers } from "../services/api";

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

export function OpportunitiesPage() {
  const [offers, setOffers] = useState<JobOffer[]>([]);
  const [selectedOffer, setSelectedOffer] = useState<JobOffer | null>(null);

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

  return (
    <>
      <PageHeader
        title="Opportunities"
        description="Explore and analyze opportunities."
      />

      {loading && <p className="text-slate-400">Loading opportunities...</p>}

      {error && <p className="text-red-500">{error}</p>}

      {!loading && !error && (
        <div className="grid gap-6 lg:grid-cols-3">
          <div className="max-h-[calc(100vh-220px)] overflow-y-auto space-y-3 pr-2">
            {offers.map((offer) => (
              <button
                key={offer.id}
                onClick={() => setSelectedOffer(offer)}
                className="block w-full text-left">
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

          <div className="lg:col-span-2 sticky top-6 self-start">
            {selectedOffer ? (
              <Card>
                <h2 className="mb-2 text-2xl font-bold text-white">
                  {selectedOffer.title}
                </h2>

                <div className="mb-6 space-y-1 text-sm text-slate-400">
                  <p>Company: {selectedOffer.company_name ?? "Unknown"}</p>

                  <p>Location: {selectedOffer.location}</p>

                  <p>Source: {selectedOffer.source}</p>

                  <p>
                    Imported:{" "}
                    {new Date(selectedOffer.created_at).toLocaleString()}
                  </p>
                </div>

                <div className="mb-6">
                  <h3 className="mb-2 text-lg font-semibold text-white">
                    Description
                  </h3>

                  <p className="whitespace-pre-wrap text-slate-300">
                    {selectedOffer.description}
                  </p>
                </div>

                {selectedOffer.source_url && (
                  <a
                    href={selectedOffer.source_url}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="text-blue-400 hover:text-blue-300">
                    Open Source Offer
                  </a>
                )}
              </Card>
            ) : (
              <Card>
                <p className="text-slate-400">Select an opportunity.</p>
              </Card>
            )}
          </div>
        </div>
      )}
    </>
  );
}
