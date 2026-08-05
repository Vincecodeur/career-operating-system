type JobOffer = {
  id: number;
  title: string;
};

type Props = {
  jobOffers: JobOffer[];
};

export function JobOfferList({ jobOffers }: Props) {
  return (
    <section>
      <h2>Job Offers</h2>

      <ul>
        {jobOffers.map((offer) => (
          <li key={offer.id}>{offer.title}</li>
        ))}
      </ul>
    </section>
  );
}
