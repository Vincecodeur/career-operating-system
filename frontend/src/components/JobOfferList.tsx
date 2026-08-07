type JobOffer = {
  id: number;
  title: string;
};

type Props = {
  jobOffers: JobOffer[];
};

export function JobOfferList({ jobOffers }: Props) {
  return (
    <div className="space-y-3">
      {jobOffers.map((offer) => (
        <div
          key={offer.id}
          className="rounded-lg border border-slate-700 bg-slate-950 p-4">
          <p className="text-xs uppercase text-slate-400">Job Offer</p>

          <h3 className="mt-1 text-lg font-semibold text-white">
            {offer.title}
          </h3>
        </div>
      ))}
    </div>
  );
}
