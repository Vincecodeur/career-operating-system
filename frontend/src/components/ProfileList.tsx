import { Card } from "./ui/Card";

type Props = {
  profiles: any[];
  selectedProfileId?: number | null;
  onSelectProfile?: (profile: any) => void;
};

export function ProfileList({
  profiles,
  selectedProfileId = null,
  onSelectProfile,
}: Props) {
  if (profiles.length === 0) {
    return (
      <Card>
        <p className="text-slate-400">No profiles available.</p>
      </Card>
    );
  }

  return (
    <div className="space-y-3">
      {profiles.map((profile: any) => (
        <button
          key={profile.id}
          type="button"
          onClick={() => onSelectProfile?.(profile)}
          className={`block w-full rounded-lg text-left transition-all ${
            selectedProfileId === profile.id
              ? "border-2 border-blue-500 bg-slate-800 shadow-lg shadow-blue-500/20"
              : ""
          }`}>
          <Card>
            <p className="text-xs uppercase text-slate-400">Profile</p>

            <h3 className="mt-1 text-lg font-semibold text-white">
              {profile.full_name}
            </h3>

            {profile.current_title && (
              <p className="mt-1 text-sm text-slate-400">
                {profile.current_title}
              </p>
            )}
          </Card>
        </button>
      ))}
    </div>
  );
}
