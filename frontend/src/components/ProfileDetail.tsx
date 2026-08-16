import { Card } from "./ui/Card";
import type { Cv, ProfileSoftSkill } from "../services/api";
import { getCvDownloadUrl } from "../services/api";

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
  profileSoftSkills: ProfileSoftSkill[];
  workExperiences: WorkExperience[];
  profileLanguages: ProfileLanguage[];
  languages: Language[];
  profileCertifications: ProfileCertification[];
  certifications: Certification[];
  cvs: Cv[];
  loading?: boolean;

  onEditProfile: () => void;
  onArchiveProfile: () => void;

  onAddProfileSkill: () => void;
  onEditProfileSkill: (profileSkill: ProfileSkill) => void;
  onDeleteProfileSkill: (profileSkill: ProfileSkill) => void;

  onAddProfileSoftSkill: () => void;
  onDeleteProfileSoftSkill: (softSkill: ProfileSoftSkill) => void;

  onAddWorkExperience: () => void;
  onEditWorkExperience: (workExperience: WorkExperience) => void;
  onDeleteWorkExperience: (workExperience: WorkExperience) => void;

  onAddProfileLanguage: () => void;
  onEditProfileLanguage: (profileLanguage: ProfileLanguage) => void;
  onDeleteProfileLanguage: (profileLanguage: ProfileLanguage) => void;

  onAddProfileCertification: () => void;
  onEditProfileCertification: (
    profileCertification: ProfileCertification,
  ) => void;
  onDeleteProfileCertification: (
    profileCertification: ProfileCertification,
  ) => void;
  onUploadCv: () => void;
  onDeleteCv: (cv: Cv) => void;
  onSetDefaultCv: (cv: Cv) => void | Promise<void>;
};

function formatDate(value: string | null) {
  if (!value) {
    return "Present";
  }

  return new Date(value).toLocaleDateString();
}

function formatFileSize(fileSizeBytes: number) {
  if (fileSizeBytes < 1024) {
    return `${fileSizeBytes} B`;
  }

  if (fileSizeBytes < 1024 * 1024) {
    return `${Math.round(fileSizeBytes / 1024)} KB`;
  }

  return `${(fileSizeBytes / (1024 * 1024)).toFixed(1)} MB`;
}

export function ProfileDetail({
  profile,
  profileSkills,
  profileSoftSkills,
  skills,
  workExperiences,
  profileLanguages,
  languages,
  profileCertifications,
  certifications,
  cvs,
  loading = false,
  onEditProfile,
  onArchiveProfile,
  onAddProfileSkill,
  onEditProfileSkill,
  onDeleteProfileSkill,
  onAddProfileSoftSkill,
  onDeleteProfileSoftSkill,
  onAddWorkExperience,
  onEditWorkExperience,
  onDeleteWorkExperience,
  onAddProfileLanguage,
  onEditProfileLanguage,
  onDeleteProfileLanguage,
  onAddProfileCertification,
  onEditProfileCertification,
  onDeleteProfileCertification,
  onUploadCv,
  onDeleteCv,
  onSetDefaultCv,
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
      <div className="mb-8 flex flex-col gap-4 md:flex-row md:items-start md:justify-between">
        <div>
          <p className="text-sm uppercase text-slate-400">Candidate Profile</p>

          <h2 className="mt-2 text-3xl font-bold text-white">
            {profile.full_name}
          </h2>

          <p className="mt-2 text-slate-300">
            {profile.current_title ?? "No current title"}
          </p>
        </div>

        <div className="flex gap-3">
          <button
            type="button"
            onClick={onEditProfile}
            className="rounded-md bg-blue-600 px-4 py-2 text-sm font-semibold text-white hover:bg-blue-500">
            Edit Profile
          </button>

          <button
            type="button"
            onClick={onArchiveProfile}
            className="rounded-md border border-red-700 px-4 py-2 text-sm font-semibold text-red-300 hover:bg-red-950">
            Archive Profile
          </button>
        </div>
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
        <div className="mb-4 flex items-center justify-between gap-3">
          <h3 className="text-lg font-semibold text-white">CVs</h3>

          <button
            type="button"
            onClick={onUploadCv}
            className="rounded-md bg-blue-600 px-3 py-2 text-sm font-semibold text-white hover:bg-blue-500">
            Upload CV
          </button>
        </div>

        {cvs.length === 0 ? (
          <p className="text-slate-400">No CV uploaded.</p>
        ) : (
          <div className="space-y-3">
            {cvs.map((cv) => (
              <div
                key={cv.id}
                className="rounded-md border border-slate-800 bg-slate-900 p-4">
                <div className="flex flex-col gap-3 md:flex-row md:items-start md:justify-between">
                  <div>
                    <p className="font-semibold text-white">
                      {cv.original_file_name}
                    </p>

                    <p className="mt-1 text-sm text-slate-400">
                      {cv.version_label ?? "No version"}
                    </p>

                    <p className="mt-1 text-sm text-slate-400">
                      Language: {cv.language ?? "Unknown"}
                    </p>

                    <p className="mt-1 text-sm text-slate-400">
                      Size: {formatFileSize(cv.file_size_bytes)}
                    </p>

                    <p className="mt-1 text-sm text-slate-400">
                      Status: {cv.parsing_status}
                    </p>

                    {cv.is_default && (
                      <p className="mt-2 text-sm font-medium text-blue-300">
                        Default CV
                      </p>
                    )}
                  </div>

                  <div className="flex gap-2">
                    <a
                      href={getCvDownloadUrl(cv.id)}
                      target="_blank"
                      rel="noreferrer"
                      className="rounded-md border border-green-700 px-3 py-1 text-sm text-green-300 hover:bg-green-950">
                      Download
                    </a>

                    {!cv.is_default && (
                      <button
                        type="button"
                        onClick={() => onSetDefaultCv(cv)}
                        className="rounded-md border border-blue-700 px-3 py-1 text-sm text-blue-300 hover:bg-blue-950">
                        Set Default
                      </button>
                    )}

                    <button
                      type="button"
                      onClick={() => onDeleteCv(cv)}
                      className="rounded-md border border-red-700 px-3 py-1 text-sm text-red-300 hover:bg-red-950">
                      Delete
                    </button>
                  </div>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
      <div className="mb-8 rounded-lg border border-slate-700 bg-slate-950 p-4">
        <h3 className="mb-6 text-lg font-semibold text-white">Skills</h3>

        <div className="mb-8">
          <div className="mb-4 flex items-center justify-between gap-3">
            <div>
              <h4 className="text-base font-semibold text-white">
                Hard Skills
              </h4>

              <p className="mt-1 text-sm text-slate-400">
                Technical skills used for matching and profile enrichment.
              </p>
            </div>

            <button
              type="button"
              onClick={onAddProfileSkill}
              className="rounded-md bg-blue-600 px-3 py-2 text-sm font-semibold text-white hover:bg-blue-500">
              Add Hard Skill
            </button>
          </div>

          {profileSkills.length === 0 ? (
            <p className="text-slate-400">No hard skills available.</p>
          ) : (
            <div className="space-y-3">
              {profileSkills.map((profileSkill) => {
                const skill = skillById.get(profileSkill.skill_id);

                return (
                  <div
                    key={profileSkill.skill_id}
                    className="rounded-md border border-slate-800 bg-slate-900 p-4">
                    <div className="flex flex-col gap-3 md:flex-row md:items-start md:justify-between">
                      <div>
                        <p className="font-semibold text-white">
                          {skill?.name ?? `Skill ${profileSkill.skill_id}`}
                        </p>

                        <p className="mt-1 text-sm text-slate-400">
                          {skill?.category ?? "No category"}
                        </p>

                        <p className="mt-2 text-sm text-slate-300">
                          {profileSkill.years_of_experience ?? 0} years -{" "}
                          {profileSkill.self_assessment_level ?? "No level"}
                        </p>
                      </div>

                      <div className="flex gap-2">
                        <button
                          type="button"
                          onClick={() => onEditProfileSkill(profileSkill)}
                          className="rounded-md border border-slate-600 px-3 py-1 text-sm text-slate-300 hover:bg-slate-800">
                          Edit
                        </button>

                        <button
                          type="button"
                          onClick={() => onDeleteProfileSkill(profileSkill)}
                          className="rounded-md border border-red-700 px-3 py-1 text-sm text-red-300 hover:bg-red-950">
                          Remove
                        </button>
                      </div>
                    </div>
                  </div>
                );
              })}
            </div>
          )}
        </div>

        <div className="border-t border-slate-800 pt-6">
          <div className="mb-4 flex items-center justify-between gap-3">
            <div>
              <h4 className="text-base font-semibold text-white">
                Soft Skills
              </h4>

              <p className="mt-1 text-sm text-slate-400">
                Manual behavioral skills. Not used for matching in the MVP.
              </p>
            </div>

            <button
              type="button"
              onClick={onAddProfileSoftSkill}
              className="rounded-md bg-blue-600 px-3 py-2 text-sm font-semibold text-white hover:bg-blue-500">
              Add Soft Skill
            </button>
          </div>

          {profileSoftSkills.length === 0 ? (
            <p className="text-slate-400">No soft skills available.</p>
          ) : (
            <div className="flex flex-wrap gap-2">
              {profileSoftSkills.map((softSkill) => (
                <div
                  key={softSkill.id}
                  className="flex items-center gap-2 rounded-full border border-slate-700 bg-slate-900 px-3 py-2 text-sm text-slate-200">
                  <span>{softSkill.name}</span>

                  <button
                    type="button"
                    onClick={() => onDeleteProfileSoftSkill(softSkill)}
                    className="text-red-300 hover:text-red-200"
                    aria-label={`Remove ${softSkill.name}`}>
                    ×
                  </button>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>

      <div className="mb-8 rounded-lg border border-slate-700 bg-slate-950 p-4">
        <div className="mb-4 flex items-center justify-between gap-3">
          <h3 className="text-lg font-semibold text-white">Work Experience</h3>

          <button
            type="button"
            onClick={onAddWorkExperience}
            className="rounded-md bg-blue-600 px-3 py-2 text-sm font-semibold text-white hover:bg-blue-500">
            Add Experience
          </button>
        </div>

        {workExperiences.length === 0 ? (
          <p className="text-slate-400">No work experience available.</p>
        ) : (
          <div className="space-y-4">
            {workExperiences.map((experience) => (
              <div
                key={experience.id}
                className="rounded-md border border-slate-800 bg-slate-900 p-4">
                <div className="flex flex-col gap-3 md:flex-row md:items-start md:justify-between">
                  <div>
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
                  </div>

                  <div className="flex gap-2">
                    <button
                      type="button"
                      onClick={() => onEditWorkExperience(experience)}
                      className="rounded-md border border-slate-600 px-3 py-1 text-sm text-slate-300 hover:bg-slate-800">
                      Edit
                    </button>

                    <button
                      type="button"
                      onClick={() => onDeleteWorkExperience(experience)}
                      className="rounded-md border border-red-700 px-3 py-1 text-sm text-red-300 hover:bg-red-950">
                      Remove
                    </button>
                  </div>
                </div>

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
        <div className="mb-4 flex items-center justify-between gap-3">
          <h3 className="text-lg font-semibold text-white">Languages</h3>

          <button
            type="button"
            onClick={onAddProfileLanguage}
            className="rounded-md bg-blue-600 px-3 py-2 text-sm font-semibold text-white hover:bg-blue-500">
            Add Language
          </button>
        </div>

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
                  <div className="flex flex-col gap-3 md:flex-row md:items-start md:justify-between">
                    <div>
                      <p className="font-medium text-white">
                        {language?.name ??
                          `Language ${profileLanguage.language_id}`}
                      </p>

                      <p className="mt-1 text-sm text-slate-400">
                        {profileLanguage.proficiency_level}
                      </p>
                    </div>

                    <div className="flex gap-2">
                      <button
                        type="button"
                        onClick={() => onEditProfileLanguage(profileLanguage)}
                        className="rounded-md border border-slate-600 px-3 py-1 text-sm text-slate-300 hover:bg-slate-800">
                        Edit
                      </button>

                      <button
                        type="button"
                        onClick={() => onDeleteProfileLanguage(profileLanguage)}
                        className="rounded-md border border-red-700 px-3 py-1 text-sm text-red-300 hover:bg-red-950">
                        Remove
                      </button>
                    </div>
                  </div>
                </div>
              );
            })}
          </div>
        )}
      </div>

      <div className="rounded-lg border border-slate-700 bg-slate-950 p-4">
        <div className="mb-4 flex items-center justify-between gap-3">
          <h3 className="text-lg font-semibold text-white">Certifications</h3>

          <button
            type="button"
            onClick={onAddProfileCertification}
            className="rounded-md bg-blue-600 px-3 py-2 text-sm font-semibold text-white hover:bg-blue-500">
            Add Certification
          </button>
        </div>

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
                  <div className="flex flex-col gap-3 md:flex-row md:items-start md:justify-between">
                    <div>
                      <p className="font-medium text-white">
                        {certification?.name ??
                          `Certification ${profileCertification.certification_id}`}
                      </p>

                      <p className="mt-1 text-sm text-slate-400">
                        {certification?.issuing_organization ??
                          "Unknown issuer"}
                      </p>

                      {profileCertification.obtained_date && (
                        <p className="mt-1 text-xs text-slate-500">
                          Obtained: {profileCertification.obtained_date}
                        </p>
                      )}

                      {profileCertification.expiration_date && (
                        <p className="mt-1 text-xs text-slate-500">
                          Expires: {profileCertification.expiration_date}
                        </p>
                      )}

                      {profileCertification.credential_id && (
                        <p className="mt-1 text-xs text-slate-500">
                          Credential: {profileCertification.credential_id}
                        </p>
                      )}
                    </div>

                    <div className="flex gap-2">
                      <button
                        type="button"
                        onClick={() =>
                          onEditProfileCertification(profileCertification)
                        }
                        className="rounded-md border border-slate-600 px-3 py-1 text-sm text-slate-300 hover:bg-slate-800">
                        Edit
                      </button>

                      <button
                        type="button"
                        onClick={() =>
                          onDeleteProfileCertification(profileCertification)
                        }
                        className="rounded-md border border-red-700 px-3 py-1 text-sm text-red-300 hover:bg-red-950">
                        Remove
                      </button>
                    </div>
                  </div>
                </div>
              );
            })}
          </div>
        )}
      </div>
    </Card>
  );
}
