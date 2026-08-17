export type ApplicationEvent = {
  id: number;
  event_type: string;
  old_value: string | null;
  new_value: string | null;
  event_date: string;
};

type Props = {
  events: ApplicationEvent[];
  createdAt?: string;
};

export function ApplicationTimeline({ events, createdAt }: Props) {
  if (events.length === 0) {
    return (
      <div className="border-l-2 border-green-600 pl-4">
        <p className="text-xs uppercase text-green-400">APPLICATION_CREATED</p>

        <p className="font-medium text-white">Application Created</p>

        <p className="text-sm text-slate-400">
          {createdAt
            ? new Date(createdAt).toLocaleString()
            : "Creation date unavailable"}
        </p>
      </div>
    );
  }

  return (
    <div className="space-y-4">
      {events.map((event) => (
        <div key={event.id} className="border-l-2 border-slate-700 pl-4">
          <p className="text-xs uppercase text-slate-500">{event.event_type}</p>

          <p className="font-medium text-white">
            {event.old_value ?? "Start"} → {event.new_value}
          </p>

          <p className="text-sm text-slate-400">
            {new Date(event.event_date).toLocaleString()}
          </p>
        </div>
      ))}
    </div>
  );
}
