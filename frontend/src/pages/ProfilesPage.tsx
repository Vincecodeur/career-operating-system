import { useEffect, useState } from "react";

import { CreateProfileModal } from "../components/CreateProfileModal";
import type { CreateProfileFormValues } from "../components/CreateProfileModal";
import { DeleteProfileDialog } from "../components/DeleteProfileDialog";
import { EditProfileModal } from "../components/EditProfileModal";
import type { ProfileFormValues } from "../components/EditProfileModal";
import { ProfileDetail } from "../components/ProfileDetail";
import { ProfileList } from "../components/ProfileList";
import { PageHeader } from "../components/ui/PageHeader";
import {
  createProfile,
  deleteProfile,
  getCertifications,
  getLanguages,
  getProfileCertifications,
  getProfileLanguages,
  getProfileSkills,
  getProfileWorkExperiences,
  getProfiles,
  getSkills,
  updateProfile,
} from "../services/api";

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

export function ProfilesPage() {
  const [profiles, setProfiles] = useState<Profile[]>([]);
  const [selectedProfile, setSelectedProfile] = useState<Profile | null>(null);

  const [profileSkills, setProfileSkills] = useState<ProfileSkill[]>([]);
  const [skills, setSkills] = useState<Skill[]>([]);
  const [workExperiences, setWorkExperiences] = useState<WorkExperience[]>([]);
  const [profileLanguages, setProfileLanguages] = useState<ProfileLanguage[]>(
    [],
  );
  const [languages, setLanguages] = useState<Language[]>([]);
  const [profileCertifications, setProfileCertifications] = useState<
    ProfileCertification[]
  >([]);
  const [certifications, setCertifications] = useState<Certification[]>([]);

  const [loadingProfiles, setLoadingProfiles] = useState(true);
  const [loadingDetails, setLoadingDetails] = useState(false);

  const [error, setError] = useState<string | null>(null);

  const [isCreateModalOpen, setIsCreateModalOpen] = useState(false);
  const [isEditModalOpen, setIsEditModalOpen] = useState(false);
  const [isDeleteDialogOpen, setIsDeleteDialogOpen] = useState(false);

  const [isCreatingProfile, setIsCreatingProfile] = useState(false);
  const [isSavingProfile, setIsSavingProfile] = useState(false);
  const [isDeletingProfile, setIsDeletingProfile] = useState(false);

  const [profileMutationError, setProfileMutationError] = useState<
    string | null
  >(null);

  useEffect(() => {
    async function loadProfiles() {
      try {
        const data = await getProfiles();

        const activeProfiles = data.filter(
          (profile: Profile) => profile.is_active,
        );

        setProfiles(activeProfiles);

        if (activeProfiles.length > 0) {
          setSelectedProfile(activeProfiles[0]);
        }
      } catch {
        setError("Unable to load profiles.");
      } finally {
        setLoadingProfiles(false);
      }
    }

    loadProfiles();
  }, []);

  useEffect(() => {
    async function loadDetails() {
      if (!selectedProfile) {
        return;
      }

      setLoadingDetails(true);

      try {
        const [
          profileSkillsData,
          skillsData,
          workExperiencesData,
          profileLanguagesData,
          languagesData,
          profileCertificationsData,
          certificationsData,
        ] = await Promise.all([
          getProfileSkills(selectedProfile.id),
          getSkills(),
          getProfileWorkExperiences(selectedProfile.id),
          getProfileLanguages(selectedProfile.id),
          getLanguages(),
          getProfileCertifications(selectedProfile.id),
          getCertifications(),
        ]);

        setProfileSkills(profileSkillsData);
        setSkills(skillsData);
        setWorkExperiences(workExperiencesData);
        setProfileLanguages(profileLanguagesData);
        setLanguages(languagesData);
        setProfileCertifications(profileCertificationsData);
        setCertifications(certificationsData);
      } catch {
        setError("Unable to load profile details.");
      } finally {
        setLoadingDetails(false);
      }
    }

    loadDetails();
  }, [selectedProfile]);

  async function handleCreateProfile(values: CreateProfileFormValues) {
    setIsCreatingProfile(true);
    setProfileMutationError(null);

    try {
      const createdProfile = await createProfile(values);

      setProfiles((profiles) => [
        createdProfile,
        ...profiles.filter((profile) => profile.id !== createdProfile.id),
      ]);

      setSelectedProfile(createdProfile);
      setIsCreateModalOpen(false);
    } catch {
      setProfileMutationError("Unable to create profile.");
    } finally {
      setIsCreatingProfile(false);
    }
  }

  async function handleUpdateProfile(values: ProfileFormValues) {
    if (!selectedProfile) {
      return;
    }

    setIsSavingProfile(true);
    setProfileMutationError(null);

    try {
      const updatedProfile = await updateProfile(selectedProfile.id, values);

      setProfiles((profiles) =>
        profiles.map((profile) =>
          profile.id === updatedProfile.id ? updatedProfile : profile,
        ),
      );

      setSelectedProfile(updatedProfile);
      setIsEditModalOpen(false);
    } catch {
      setProfileMutationError("Unable to update profile.");
    } finally {
      setIsSavingProfile(false);
    }
  }

  async function handleArchiveProfile() {
    if (!selectedProfile) {
      return;
    }

    setIsDeletingProfile(true);
    setProfileMutationError(null);

    try {
      const archivedProfile = await deleteProfile(selectedProfile.id);

      const remainingProfiles = profiles.filter(
        (profile) => profile.id !== archivedProfile.id,
      );

      setProfiles(remainingProfiles);
      setSelectedProfile(remainingProfiles[0] ?? null);
      setIsDeleteDialogOpen(false);
    } catch {
      setProfileMutationError("Unable to archive profile.");
    } finally {
      setIsDeletingProfile(false);
    }
  }

  return (
    <>
      <div className="flex flex-col gap-4 md:flex-row md:items-start md:justify-between">
        <PageHeader title="Profiles" description="Manage candidate profiles." />

        <button
          type="button"
          onClick={() => {
            setProfileMutationError(null);
            setIsCreateModalOpen(true);
          }}
          className="rounded-md bg-blue-600 px-4 py-2 text-sm font-semibold text-white hover:bg-blue-500">
          New Profile
        </button>
      </div>

      {loadingProfiles && <p className="text-slate-400">Loading profiles...</p>}

      {error && <p className="text-red-500">{error}</p>}

      {!loadingProfiles && !error && (
        <div className="grid gap-6 lg:grid-cols-3">
          <div className="max-h-[calc(100vh-220px)] overflow-y-auto pr-2">
            <ProfileList
              profiles={profiles}
              selectedProfileId={selectedProfile?.id}
              onSelectProfile={(profile) => setSelectedProfile(profile)}
            />
          </div>

          <div className="sticky top-6 self-start lg:col-span-2">
            {selectedProfile ? (
              <ProfileDetail
                profile={selectedProfile}
                profileSkills={profileSkills}
                skills={skills}
                workExperiences={workExperiences}
                profileLanguages={profileLanguages}
                languages={languages}
                profileCertifications={profileCertifications}
                certifications={certifications}
                loading={loadingDetails}
                onEditProfile={() => {
                  setProfileMutationError(null);
                  setIsEditModalOpen(true);
                }}
                onArchiveProfile={() => {
                  setProfileMutationError(null);
                  setIsDeleteDialogOpen(true);
                }}
              />
            ) : (
              <p className="text-slate-400">
                Select a profile to view details.
              </p>
            )}
          </div>
        </div>
      )}

      <CreateProfileModal
        isOpen={isCreateModalOpen}
        isSaving={isCreatingProfile}
        error={profileMutationError}
        onClose={() => setIsCreateModalOpen(false)}
        onCreate={handleCreateProfile}
      />

      <EditProfileModal
        profile={selectedProfile}
        isOpen={isEditModalOpen}
        isSaving={isSavingProfile}
        error={profileMutationError}
        onClose={() => setIsEditModalOpen(false)}
        onSave={handleUpdateProfile}
      />

      <DeleteProfileDialog
        profile={selectedProfile}
        isOpen={isDeleteDialogOpen}
        isDeleting={isDeletingProfile}
        error={profileMutationError}
        onClose={() => setIsDeleteDialogOpen(false)}
        onConfirm={handleArchiveProfile}
      />
    </>
  );
}
