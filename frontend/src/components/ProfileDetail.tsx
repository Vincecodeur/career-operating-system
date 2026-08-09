import { Card } from "./ui/Card";

type Profile = {
  id: number;
  profile_name: string;
  full_name: string;
  current_title: string | null;
  location: string | null;
  years_of_experience: number | null;
  target_role_short_term: string | null;
  target_role_long_term: string | null;
  remote_preference: string | null;
  preferred_countries: string | null;
  is_active: boolean;
  created_at: string;
  updated_at: string;
};

type ProfileSkill = {
  profile_id: number;
  skill_id: number;
  years_of_experience: number | null;
  self_assessment_level: string | null;
  created_at: string;
};

type Skill = {
  id: number;
  name: string;
  category: string | null;
  created_at: string;
};

type WorkExperience = {
  id: number;
  profile_id: number;
  company_name: string;
  job_title: string;
  start_date: string;
  end_date: string | null;
  is_current_position: boolean;
  description: string | null;
  created_at: string;
};

type ProfileLanguage = {
  profile_id: number;
  language_id: number;
  proficiency_level: string;
  created_at: string;
};

type Language = {
  id: number;
  name: string;
  created_at: string;
};

type ProfileCertification = {
  profile_id: number;
  certification_id: number;
  obtained_date: string | null;
  expiration_date: string | null;
  credential_id: string | null;
  created_at: string;
};

type Certification = {
  id: number;
  name: string;
  issuing_organization: string | null;
  created_at: string;
};

type Props = {
  profile: Profile;
  profileSkills: ProfileSkill[];
  skills: Skill[];
  workExperiences: WorkExperience[];
  profileLanguages: ProfileLanguage[];
  languages: Language[];
  profileCertifications: ProfileCertification[];
  certifications: Certification[];
  loading?: boolean;
};

function formatDate(value: string | null) {
  if (!value) {
    return "Present";
  }

  return new Date(value).toLocaleDateString();
}

export function ProfileDetail({
  profile,
  profileSkills,
  skills,
  workExperiences,
  profileLanguages,
  languages,
  profileCertifications,
  certifications,
  loading = false,
}: Props) {
  const skillById = new Map(skills.map((skill) => [skill.id, skill]));

  const languageById = new Map(
    languages.map((language) => [language.id, language]),
  );

  const certificationById = new Map(
    certifications.map((certification) => [certification.id, certification]),
  );

  if (loading) {
    return (
      <Card>
        <p className="text-slate-400">Loading profile details...</p>
      </Card>
    );
  }

  return (
    <Card>
      <div className="mb-8">
        <p className="text-sm uppercase text-slate-400">Candidate Profile</p>

        <h2 className="mt-2 text-3xl font-bold text-white">
          {profile.full_name}
        </h2>

        <p className="mt-2 text-slate-300">
          {profile.current_title ?? "No current title"}
        </p>
      </div>

      <div className="mb-8 grid grid-cols-2 gap-4 md:grid-cols-4">
        <div className="rounded-lg border border-slate-700 bg-slate-950 p-3">
          <p className="text-sm text-slate-400">Skills</p>

          <p className="mt-2 text-2xl font-bold text-white">
            {profileSkills.length}
          </p>
        </div>

        <div className="rounded-lg border border-slate-700 bg-slate-950 p-3">
          <p className="text-sm text-slate-400">Experiences</p>

          <p className="mt-2 text-2xl font-bold text-white">
            {workExperiences.length}
          </p>
        </div>

        <div className="rounded-lg border border-slate-700 bg-slate-950 p-3">
          <p className="text-sm text-slate-400">Languages</p>

          <p className="mt-2 text-2xl font-bold text-white">
            {profileLanguages.length}
          </p>
        </div>

        <div className="rounded-lg border border-slate-700 bg-slate-950 p-3">
          <p className="text-sm text-slate-400">Certifications</p>

          <p className="mt-2 text-2xl font-bold text-white">
            {profileCertifications.length}
          </p>
        </div>
      </div>

      <div className="mb-8 rounded-lg border border-slate-700 bg-slate-950 p-3">
        <h3 className="mb-4 text-lg font-semibold text-white">
          General Information
        </h3>

        <div className="grid gap-4 text-sm text-slate-400 md:grid-cols-2">
          <div>
            <p className="font-medium text-slate-300">Profile Name</p>
            <p>{profile.profile_name}</p>
          </div>

          <div>
            <p className="font-medium text-slate-300">Location</p>
            <p>{profile.location ?? "Unknown"}</p>
          </div>

          <div>
            <p className="font-medium text-slate-300">Years of Experience</p>
            <p>{profile.years_of_experience ?? 0}</p>
          </div>

          <div>
            <p className="font-medium text-slate-300">Remote Preference</p>
            <p>{profile.remote_preference ?? "Unknown"}</p>
          </div>

          <div>
            <p className="font-medium text-slate-300">Short-Term Target</p>
            <p>{profile.target_role_short_term ?? "Not specified"}</p>
          </div>

          <div>
            <p className="font-medium text-slate-300">Long-Term Target</p>
            <p>{profile.target_role_long_term ?? "Not specified"}</p>
          </div>

          <div>
            <p className="font-medium text-slate-300">Preferred Countries</p>
            <p>{profile.preferred_countries ?? "Not specified"}</p>
          </div>

          <div>
            <p className="font-medium text-slate-300">Status</p>
            <p>{profile.is_active ? "Active" : "Inactive"}</p>
          </div>
        </div>
      </div>

      <div className="mb-8 rounded-lg border border-slate-700 bg-slate-950 p-4">
        <h3 className="mb-4 text-lg font-semibold text-white">Skills</h3>

        {profileSkills.length === 0 ? (
          <p className="text-slate-400">No skills available.</p>
        ) : (
          <div className="flex flex-wrap gap-2">
            {profileSkills.map((profileSkill) => {
              const skill = skillById.get(profileSkill.skill_id);

              return (
                <span
                  key={profileSkill.skill_id}
                  className="rounded-md border border-blue-700 bg-blue-950 px-3 py-1 text-sm text-blue-300">
                  {skill?.name ?? `Skill ${profileSkill.skill_id}`}
                </span>
              );
            })}
          </div>
        )}
      </div>
      <div className="mb-8 rounded-lg border border-slate-700 bg-slate-950 p-4">
        <h3 className="mb-4 text-lg font-semibold text-white">
          Work Experience
        </h3>

        {workExperiences.length === 0 ? (
          <p className="text-slate-400">No work experience available.</p>
        ) : (
          <div className="space-y-4">
            {workExperiences.map((experience) => (
              <div
                key={experience.id}
                className="rounded-md border border-slate-800 bg-slate-900 p-4">
                <h4 className="font-semibold text-white">
                  {experience.job_title}
                </h4>

                <p className="mt-1 text-sm text-slate-300">
                  {experience.company_name}
                </p>

                <p className="mt-1 text-xs text-slate-500">
                  {formatDate(experience.start_date)} -{" "}
                  {formatDate(experience.end_date)}
                </p>

                {experience.description && (
                  <p className="mt-3 whitespace-pre-wrap text-sm text-slate-300">
                    {experience.description}
                  </p>
                )}
              </div>
            ))}
          </div>
        )}
      </div>

      <div className="mb-8 rounded-lg border border-slate-700 bg-slate-950 p-4">
        <h3 className="mb-4 text-lg font-semibold text-white">Languages</h3>

        {profileLanguages.length === 0 ? (
          <p className="text-slate-400">No languages available.</p>
        ) : (
          <div className="space-y-3">
            {profileLanguages.map((profileLanguage) => {
              const language = languageById.get(profileLanguage.language_id);

              return (
                <div
                  key={profileLanguage.language_id}
                  className="rounded-md border border-slate-800 bg-slate-900 p-3">
                  <p className="font-medium text-white">
                    {language?.name ??
                      `Language ${profileLanguage.language_id}`}
                  </p>

                  <p className="mt-1 text-sm text-slate-400">
                    {profileLanguage.proficiency_level}
                  </p>
                </div>
              );
            })}
          </div>
        )}
      </div>

      <div className="rounded-lg border border-slate-700 bg-slate-950 p-4">
        <h3 className="mb-4 text-lg font-semibold text-white">
          Certifications
        </h3>

        {profileCertifications.length === 0 ? (
          <p className="text-slate-400">No certifications available.</p>
        ) : (
          <div className="space-y-3">
            {profileCertifications.map((profileCertification) => {
              const certification = certificationById.get(
                profileCertification.certification_id,
              );

              return (
                <div
                  key={profileCertification.certification_id}
                  className="rounded-md border border-slate-800 bg-slate-900 p-3">
                  <p className="font-medium text-white">
                    {certification?.name ??
                      `Certification ${profileCertification.certification_id}`}
                  </p>

                  <p className="mt-1 text-sm text-slate-400">
                    {certification?.issuing_organization ?? "Unknown issuer"}
                  </p>

                  {profileCertification.credential_id && (
                    <p className="mt-1 text-xs text-slate-500">
                      Credential: {profileCertification.credential_id}
                    </p>
                  )}
                </div>
              );
            })}
          </div>
        )}
      </div>
    </Card>
  );
}
