type Profile = {
  id: number;
  full_name: string;
};

type Props = {
  profiles: Profile[];
};

export function ProfileList({ profiles }: Props) {
  return (
    <div className="space-y-3">
      {profiles.map((profile) => (
        <div
          key={profile.id}
          className="rounded-lg border border-slate-700 bg-slate-950 p-4">
          <p className="text-xs uppercase text-slate-400">Profile</p>

          <h3 className="mt-1 text-lg font-semibold text-white">
            {profile.full_name}
          </h3>
        </div>
      ))}
    </div>
  );
}
