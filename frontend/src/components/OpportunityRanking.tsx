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
    <section>
      <h2>Top Opportunities</h2>

      <ol>
        {rankedJobOffers.map((offer) => (
          <li key={offer.job_offer_id}>
            <strong>{offer.title}</strong>
            <br />
            Score : {offer.matching_score}%
          </li>
        ))}
      </ol>
    </section>
  );
}
