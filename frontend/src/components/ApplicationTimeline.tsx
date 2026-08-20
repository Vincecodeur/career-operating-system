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
  profileNames?: Record<number, string>;
};

function getProfileName(
  value: string | null,
  profileNames: Record<number, string>,
) {
  if (value === null) {
    return "Unknown profile";
  }

  const profileId = Number(value);

  if (!Number.isFinite(profileId)) {
    return value;
  }

  return profileNames[profileId] ?? `Profile ${profileId}`;
}

export function ApplicationTimeline({
  events,
  createdAt,
  profileNames = {},
}: Props) {
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
      {events.map((event) => {
        const isProfileChange = event.event_type === "PROFILE_CHANGED";

        const oldValue = isProfileChange
          ? getProfileName(event.old_value, profileNames)
          : (event.old_value ?? "Start");

        const newValue = isProfileChange
          ? getProfileName(event.new_value, profileNames)
          : event.new_value;

        return (
          <div
            key={event.id}
            className={`border-l-2 pl-4 ${
              isProfileChange ? "border-amber-500" : "border-slate-700"
            }`}>
            <p
              className={`text-xs uppercase ${
                isProfileChange ? "text-amber-400" : "text-slate-500"
              }`}>
              {event.event_type}
            </p>

            <p className="font-medium text-white">
              {isProfileChange
                ? "Application Profile Changed"
                : `${oldValue} → ${newValue}`}
            </p>

            {isProfileChange && (
              <p className="text-sm text-slate-300">
                {oldValue} → {newValue}
              </p>
            )}

            <p className="text-sm text-slate-400">
              {new Date(event.event_date).toLocaleString()}
            </p>
          </div>
        );
      })}
    </div>
  );
}
