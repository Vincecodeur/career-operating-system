type RankedJobOffer = {
  job_offer_id: number;
  title: string;
  matching_score: number;
  matching_skills: string[];
  missing_skills: string[];
};

type Props = {
  rankedJobOffers: RankedJobOffer[];
};

export function OpportunityRanking({ rankedJobOffers }: Props) {
  return (
    <div className="space-y-4">
      {rankedJobOffers.map((offer, index) => (
        <div
          key={offer.job_offer_id}
          className="rounded-lg border border-slate-700 bg-slate-950 p-4">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-xs uppercase tracking-wide text-slate-400">
                Rank #{index + 1}
              </p>

              <h3 className="mt-1 text-lg font-semibold text-white">
                {offer.title}
              </h3>
            </div>

            <div className="text-right">
              <p className="text-xs text-slate-400">Matching Score</p>

              <p className="text-2xl font-bold text-green-400">
                {offer.matching_score}%
              </p>
            </div>
          </div>
        </div>
      ))}
    </div>
  );
}
