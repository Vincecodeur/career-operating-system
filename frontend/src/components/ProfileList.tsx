type Profile = {
  id: number;
  full_name: string;
};

type Props = {
  profiles: Profile[];
};

export function ProfileList({ profiles }: Props) {
  return (
    <section>
      <h2>Profiles</h2>

      <ul>
        {profiles.map((profile) => (
          <li key={profile.id}>{profile.full_name}</li>
        ))}
      </ul>
    </section>
  );
}
