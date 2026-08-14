import { useEffect, useState } from "react";

import { AddProfileSkillModal } from "../components/AddProfileSkillModal";
import type { AddProfileSkillFormValues } from "../components/AddProfileSkillModal";
import { AddWorkExperienceModal } from "../components/AddWorkExperienceModal";
import type { AddWorkExperienceFormValues } from "../components/AddWorkExperienceModal";
import { CreateProfileModal } from "../components/CreateProfileModal";
import type { CreateProfileFormValues } from "../components/CreateProfileModal";
import { DeleteProfileDialog } from "../components/DeleteProfileDialog";
import { DeleteProfileSkillDialog } from "../components/DeleteProfileSkillDialog";
import { DeleteWorkExperienceDialog } from "../components/DeleteWorkExperienceDialog";
import { EditProfileModal } from "../components/EditProfileModal";
import type { ProfileFormValues } from "../components/EditProfileModal";
import { EditProfileSkillModal } from "../components/EditProfileSkillModal";
import type { EditProfileSkillFormValues } from "../components/EditProfileSkillModal";
import { EditWorkExperienceModal } from "../components/EditWorkExperienceModal";
import type { EditWorkExperienceFormValues } from "../components/EditWorkExperienceModal";

import { AddProfileLanguageModal } from "../components/AddProfileLanguageModal";
import type { AddProfileLanguageFormValues } from "../components/AddProfileLanguageModal";
import { DeleteProfileLanguageDialog } from "../components/DeleteProfileLanguageDialog";
import { EditProfileLanguageModal } from "../components/EditProfileLanguageModal";
import type { EditProfileLanguageFormValues } from "../components/EditProfileLanguageModal";

import { AddProfileCertificationModal } from "../components/AddProfileCertificationModal";
import type { AddProfileCertificationFormValues } from "../components/AddProfileCertificationModal";
import { EditProfileCertificationModal } from "../components/EditProfileCertificationModal";
import type { EditProfileCertificationFormValues } from "../components/EditProfileCertificationModal";
import { DeleteProfileCertificationDialog } from "../components/DeleteProfileCertificationDialog";

import { UploadCvModal } from "../components/UploadCvModal";
import type { UploadCvFormValues } from "../components/UploadCvModal";
import { DeleteCvDialog } from "../components/DeleteCvDialog";

import type { Cv } from "../services/api";

import { ProfileDetail } from "../components/ProfileDetail";
import { ProfileList } from "../components/ProfileList";
import { PageHeader } from "../components/ui/PageHeader";
import {
  createProfile,
  createProfileSkill,
  deleteProfile,
  deleteProfileSkill,
  getCertifications,
  getLanguages,
  getProfileCertifications,
  getProfileLanguages,
  getProfileSkills,
  getProfileWorkExperiences,
  getProfiles,
  getSkills,
  updateProfile,
  updateProfileSkill,
  createWorkExperience,
  updateWorkExperience,
  deleteWorkExperience,
  createProfileLanguage,
  updateProfileLanguage,
  deleteProfileLanguage,
  createProfileCertification,
  updateProfileCertification,
  deleteProfileCertification,
  getProfileCvs,
  uploadCv,
  deleteCv,
  setDefaultCv,
  getWorkModes,
  getCountries,
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

type ReferenceDataItem = {
  id: number;
  code: string;
  name: string;
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
  const [workModes, setWorkModes] = useState<ReferenceDataItem[]>([]);
  const [countries, setCountries] = useState<ReferenceDataItem[]>([]);
  const [loadingProfiles, setLoadingProfiles] = useState(true);
  const [loadingDetails, setLoadingDetails] = useState(false);

  const [error, setError] = useState<string | null>(null);

  const [isCreateModalOpen, setIsCreateModalOpen] = useState(false);
  const [isEditModalOpen, setIsEditModalOpen] = useState(false);
  const [isDeleteDialogOpen, setIsDeleteDialogOpen] = useState(false);

  const [isAddProfileSkillModalOpen, setIsAddProfileSkillModalOpen] =
    useState(false);
  const [isEditProfileSkillModalOpen, setIsEditProfileSkillModalOpen] =
    useState(false);
  const [isDeleteProfileSkillDialogOpen, setIsDeleteProfileSkillDialogOpen] =
    useState(false);
  const [isAddWorkExperienceModalOpen, setIsAddWorkExperienceModalOpen] =
    useState(false);

  const [isEditWorkExperienceModalOpen, setIsEditWorkExperienceModalOpen] =
    useState(false);

  const [
    isDeleteWorkExperienceDialogOpen,
    setIsDeleteWorkExperienceDialogOpen,
  ] = useState(false);
  const [selectedProfileSkill, setSelectedProfileSkill] =
    useState<ProfileSkill | null>(null);
  const [selectedWorkExperience, setSelectedWorkExperience] =
    useState<WorkExperience | null>(null);
  const [isCreatingProfile, setIsCreatingProfile] = useState(false);
  const [isSavingProfile, setIsSavingProfile] = useState(false);
  const [isDeletingProfile, setIsDeletingProfile] = useState(false);

  const [isSavingProfileSkill, setIsSavingProfileSkill] = useState(false);
  const [isDeletingProfileSkill, setIsDeletingProfileSkill] = useState(false);
  const [isSavingWorkExperience, setIsSavingWorkExperience] = useState(false);

  const [isDeletingWorkExperience, setIsDeletingWorkExperience] =
    useState(false);
  const [profileMutationError, setProfileMutationError] = useState<
    string | null
  >(null);

  const [profileSkillMutationError, setProfileSkillMutationError] = useState<
    string | null
  >(null);

  const [workExperienceMutationError, setWorkExperienceMutationError] =
    useState<string | null>(null);

  const [selectedProfileLanguage, setSelectedProfileLanguage] =
    useState<ProfileLanguage | null>(null);

  const selectedSkill =
    selectedProfileSkill === null
      ? null
      : (skills.find((skill) => skill.id === selectedProfileSkill.skill_id) ??
        null);

  const selectedLanguage =
    selectedProfileLanguage === null
      ? null
      : (languages.find(
          (language) => language.id === selectedProfileLanguage.language_id,
        ) ?? null);

  const [selectedProfileCertification, setSelectedProfileCertification] =
    useState<ProfileCertification | null>(null);

  const selectedCertification =
    selectedProfileCertification === null
      ? null
      : (certifications.find(
          (certification) =>
            certification.id === selectedProfileCertification.certification_id,
        ) ?? null);

  const [isAddProfileLanguageModalOpen, setIsAddProfileLanguageModalOpen] =
    useState(false);

  const [isEditProfileLanguageModalOpen, setIsEditProfileLanguageModalOpen] =
    useState(false);

  const [
    isDeleteProfileLanguageDialogOpen,
    setIsDeleteProfileLanguageDialogOpen,
  ] = useState(false);

  const [isSavingProfileLanguage, setIsSavingProfileLanguage] = useState(false);

  const [isDeletingProfileLanguage, setIsDeletingProfileLanguage] =
    useState(false);

  const [profileLanguageMutationError, setProfileLanguageMutationError] =
    useState<string | null>(null);

  const [
    isAddProfileCertificationModalOpen,
    setIsAddProfileCertificationModalOpen,
  ] = useState(false);

  const [
    isEditProfileCertificationModalOpen,
    setIsEditProfileCertificationModalOpen,
  ] = useState(false);

  const [
    isDeleteProfileCertificationDialogOpen,
    setIsDeleteProfileCertificationDialogOpen,
  ] = useState(false);

  const [isSavingProfileCertification, setIsSavingProfileCertification] =
    useState(false);

  const [isDeletingProfileCertification, setIsDeletingProfileCertification] =
    useState(false);

  const [
    profileCertificationMutationError,
    setProfileCertificationMutationError,
  ] = useState<string | null>(null);

  const [cvs, setCvs] = useState<Cv[]>([]);

  const [selectedCv, setSelectedCv] = useState<Cv | null>(null);

  const [isUploadCvModalOpen, setIsUploadCvModalOpen] = useState(false);

  const [isDeleteCvDialogOpen, setIsDeleteCvDialogOpen] = useState(false);

  const [isSavingCv, setIsSavingCv] = useState(false);

  const [isDeletingCv, setIsDeletingCv] = useState(false);

  const [cvMutationError, setCvMutationError] = useState<string | null>(null);

  async function reloadSelectedProfileDetails(profileId: number) {
    const [
      profileSkillsData,
      skillsData,
      workExperiencesData,
      profileLanguagesData,
      languagesData,
      profileCertificationsData,
      certificationsData,
      cvsData,
      workModesData,
      countriesData,
    ] = await Promise.all([
      getProfileSkills(profileId),
      getSkills(),
      getProfileWorkExperiences(profileId),
      getProfileLanguages(profileId),
      getLanguages(),
      getProfileCertifications(profileId),
      getCertifications(),
      getProfileCvs(profileId),
      getWorkModes(),
      getCountries(),
    ]);

    setProfileSkills(profileSkillsData);
    setSkills(skillsData);
    setWorkExperiences(workExperiencesData);
    setProfileLanguages(profileLanguagesData);
    setLanguages(languagesData);
    setProfileCertifications(profileCertificationsData);
    setCertifications(certificationsData);
    setWorkModes(workModesData);
    setCountries(countriesData);
    setCvs(cvsData);
  }

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
        await reloadSelectedProfileDetails(selectedProfile.id);
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

  async function handleAddProfileSkill(values: AddProfileSkillFormValues) {
    if (!selectedProfile) {
      return;
    }

    setIsSavingProfileSkill(true);
    setProfileSkillMutationError(null);

    try {
      await createProfileSkill({
        profile_id: selectedProfile.id,
        skill_id: values.skill_id,
        years_of_experience: values.years_of_experience,
        self_assessment_level: values.self_assessment_level,
      });

      await reloadSelectedProfileDetails(selectedProfile.id);

      setIsAddProfileSkillModalOpen(false);
    } catch {
      setProfileSkillMutationError("Unable to add skill.");
    } finally {
      setIsSavingProfileSkill(false);
    }
  }

  async function handleUpdateProfileSkill(values: EditProfileSkillFormValues) {
    if (!selectedProfileSkill) {
      return;
    }

    setIsSavingProfileSkill(true);
    setProfileSkillMutationError(null);

    try {
      await updateProfileSkill(
        selectedProfileSkill.profile_id,
        selectedProfileSkill.skill_id,
        {
          years_of_experience: values.years_of_experience,
          self_assessment_level: values.self_assessment_level,
        },
      );

      await reloadSelectedProfileDetails(selectedProfileSkill.profile_id);

      setSelectedProfileSkill(null);
      setIsEditProfileSkillModalOpen(false);
    } catch {
      setProfileSkillMutationError("Unable to update skill.");
    } finally {
      setIsSavingProfileSkill(false);
    }
  }

  async function handleDeleteProfileSkill() {
    if (!selectedProfileSkill) {
      return;
    }

    setIsDeletingProfileSkill(true);
    setProfileSkillMutationError(null);

    try {
      await deleteProfileSkill(
        selectedProfileSkill.profile_id,
        selectedProfileSkill.skill_id,
      );

      await reloadSelectedProfileDetails(selectedProfileSkill.profile_id);

      setSelectedProfileSkill(null);
      setIsDeleteProfileSkillDialogOpen(false);
    } catch {
      setProfileSkillMutationError("Unable to remove skill.");
    } finally {
      setIsDeletingProfileSkill(false);
    }
  }

  function normalizeOptionalDate(value: string | undefined) {
    return value && value.length > 0 ? value : null;
  }

  async function handleAddWorkExperience(values: AddWorkExperienceFormValues) {
    if (!selectedProfile) {
      return;
    }

    setIsSavingWorkExperience(true);
    setWorkExperienceMutationError(null);

    try {
      await createWorkExperience({
        profile_id: selectedProfile.id,
        company_name: values.company_name,
        job_title: values.job_title,
        start_date: values.start_date,
        end_date: normalizeOptionalDate(values.end_date),
        is_current_position: values.is_current_position,
        description: values.description,
      });

      await reloadSelectedProfileDetails(selectedProfile.id);

      setIsAddWorkExperienceModalOpen(false);
    } catch {
      setWorkExperienceMutationError("Unable to add work experience.");
    } finally {
      setIsSavingWorkExperience(false);
    }
  }

  async function handleUpdateWorkExperience(
    values: EditWorkExperienceFormValues,
  ) {
    if (!selectedWorkExperience) {
      return;
    }

    setIsSavingWorkExperience(true);
    setWorkExperienceMutationError(null);

    try {
      await updateWorkExperience(selectedWorkExperience.id, {
        company_name: values.company_name,
        job_title: values.job_title,
        start_date: values.start_date,
        end_date: normalizeOptionalDate(values.end_date),
        is_current_position: values.is_current_position,
        description: values.description,
      });

      await reloadSelectedProfileDetails(selectedWorkExperience.profile_id);

      setSelectedWorkExperience(null);
      setIsEditWorkExperienceModalOpen(false);
    } catch {
      setWorkExperienceMutationError("Unable to update work experience.");
    } finally {
      setIsSavingWorkExperience(false);
    }
  }

  async function handleDeleteWorkExperience() {
    if (!selectedWorkExperience) {
      return;
    }

    setIsDeletingWorkExperience(true);
    setWorkExperienceMutationError(null);

    try {
      await deleteWorkExperience(selectedWorkExperience.id);

      await reloadSelectedProfileDetails(selectedWorkExperience.profile_id);

      setSelectedWorkExperience(null);
      setIsDeleteWorkExperienceDialogOpen(false);
    } catch {
      setWorkExperienceMutationError("Unable to remove work experience.");
    } finally {
      setIsDeletingWorkExperience(false);
    }
  }

  async function handleAddProfileLanguage(
    values: AddProfileLanguageFormValues,
  ) {
    if (!selectedProfile) {
      return;
    }

    setIsSavingProfileLanguage(true);
    setProfileLanguageMutationError(null);

    try {
      await createProfileLanguage({
        profile_id: selectedProfile.id,
        language_id: values.language_id,
        proficiency_level: values.proficiency_level,
      });

      await reloadSelectedProfileDetails(selectedProfile.id);

      setIsAddProfileLanguageModalOpen(false);
    } catch {
      setProfileLanguageMutationError("Unable to add language.");
    } finally {
      setIsSavingProfileLanguage(false);
    }
  }

  async function handleUpdateProfileLanguage(
    values: EditProfileLanguageFormValues,
  ) {
    if (!selectedProfileLanguage) {
      return;
    }

    setIsSavingProfileLanguage(true);
    setProfileLanguageMutationError(null);

    try {
      await updateProfileLanguage(
        selectedProfileLanguage.profile_id,
        selectedProfileLanguage.language_id,
        {
          proficiency_level: values.proficiency_level,
        },
      );

      await reloadSelectedProfileDetails(selectedProfileLanguage.profile_id);

      setSelectedProfileLanguage(null);
      setIsEditProfileLanguageModalOpen(false);
    } catch {
      setProfileLanguageMutationError("Unable to update language.");
    } finally {
      setIsSavingProfileLanguage(false);
    }
  }

  async function handleDeleteProfileLanguage() {
    if (!selectedProfileLanguage) {
      return;
    }

    setIsDeletingProfileLanguage(true);
    setProfileLanguageMutationError(null);

    try {
      await deleteProfileLanguage(
        selectedProfileLanguage.profile_id,
        selectedProfileLanguage.language_id,
      );

      await reloadSelectedProfileDetails(selectedProfileLanguage.profile_id);

      setSelectedProfileLanguage(null);
      setIsDeleteProfileLanguageDialogOpen(false);
    } catch {
      setProfileLanguageMutationError("Unable to remove language.");
    } finally {
      setIsDeletingProfileLanguage(false);
    }
  }

  async function handleAddProfileCertification(
    values: AddProfileCertificationFormValues,
  ) {
    if (!selectedProfile) {
      return;
    }

    setIsSavingProfileCertification(true);
    setProfileCertificationMutationError(null);

    try {
      await createProfileCertification({
        profile_id: selectedProfile.id,
        certification_id: values.certification_id,
        obtained_date:
          values.obtained_date && values.obtained_date.length > 0
            ? values.obtained_date
            : null,
        expiration_date:
          values.expiration_date && values.expiration_date.length > 0
            ? values.expiration_date
            : null,
        credential_id:
          values.credential_id && values.credential_id.length > 0
            ? values.credential_id
            : null,
      });

      await reloadSelectedProfileDetails(selectedProfile.id);

      setIsAddProfileCertificationModalOpen(false);
    } catch {
      setProfileCertificationMutationError("Unable to add certification.");
    } finally {
      setIsSavingProfileCertification(false);
    }
  }

  async function handleUpdateProfileCertification(
    values: EditProfileCertificationFormValues,
  ) {
    if (!selectedProfileCertification) {
      return;
    }

    setIsSavingProfileCertification(true);
    setProfileCertificationMutationError(null);

    try {
      await updateProfileCertification(
        selectedProfileCertification.profile_id,
        selectedProfileCertification.certification_id,
        {
          obtained_date:
            values.obtained_date && values.obtained_date.length > 0
              ? values.obtained_date
              : null,
          expiration_date:
            values.expiration_date && values.expiration_date.length > 0
              ? values.expiration_date
              : null,
          credential_id:
            values.credential_id && values.credential_id.length > 0
              ? values.credential_id
              : null,
        },
      );

      await reloadSelectedProfileDetails(
        selectedProfileCertification.profile_id,
      );

      setSelectedProfileCertification(null);
      setIsEditProfileCertificationModalOpen(false);
    } catch {
      setProfileCertificationMutationError("Unable to update certification.");
    } finally {
      setIsSavingProfileCertification(false);
    }
  }

  async function handleDeleteProfileCertification() {
    if (!selectedProfileCertification) {
      return;
    }

    setIsDeletingProfileCertification(true);
    setProfileCertificationMutationError(null);

    try {
      await deleteProfileCertification(
        selectedProfileCertification.profile_id,
        selectedProfileCertification.certification_id,
      );

      await reloadSelectedProfileDetails(
        selectedProfileCertification.profile_id,
      );

      setSelectedProfileCertification(null);
      setIsDeleteProfileCertificationDialogOpen(false);
    } catch {
      setProfileCertificationMutationError("Unable to remove certification.");
    } finally {
      setIsDeletingProfileCertification(false);
    }
  }

  async function handleCvEnrichmentApplied() {
    if (!selectedProfile) {
      return;
    }

    await reloadSelectedProfileDetails(selectedProfile.id);

    setIsUploadCvModalOpen(false);
  }

  async function handleUploadCv(values: UploadCvFormValues): Promise<Cv> {
    if (!selectedProfile) {
      throw new Error("No profile selected.");
    }

    setIsSavingCv(true);
    setCvMutationError(null);

    try {
      const cv = await uploadCv(
        selectedProfile.id,
        values.file,
        values.language,
        values.versionLabel,
        values.isDefault,
      );

      await reloadSelectedProfileDetails(selectedProfile.id);

      return cv;
    } catch {
      setCvMutationError("Unable to upload CV.");

      throw new Error("Unable to upload CV.");
    } finally {
      setIsSavingCv(false);
    }
  }

  async function handleDeleteCv() {
    if (!selectedCv) {
      return;
    }

    setIsDeletingCv(true);
    setCvMutationError(null);

    try {
      await deleteCv(selectedCv.id);

      await reloadSelectedProfileDetails(selectedCv.profile_id);

      setSelectedCv(null);
      setIsDeleteCvDialogOpen(false);
    } catch {
      setCvMutationError("Unable to delete CV.");
    } finally {
      setIsDeletingCv(false);
    }
  }

  async function handleSetDefaultCv(cv: Cv) {
    try {
      await setDefaultCv(cv.id);

      await reloadSelectedProfileDetails(cv.profile_id);
    } catch {
      setCvMutationError("Unable to set default CV.");
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
                onAddProfileSkill={() => {
                  setProfileSkillMutationError(null);
                  setIsAddProfileSkillModalOpen(true);
                }}
                onEditProfileSkill={(profileSkill) => {
                  setSelectedProfileSkill(profileSkill);
                  setProfileSkillMutationError(null);
                  setIsEditProfileSkillModalOpen(true);
                }}
                onDeleteProfileSkill={(profileSkill) => {
                  setSelectedProfileSkill(profileSkill);
                  setProfileSkillMutationError(null);
                  setIsDeleteProfileSkillDialogOpen(true);
                }}
                onAddWorkExperience={() => {
                  setWorkExperienceMutationError(null);
                  setIsAddWorkExperienceModalOpen(true);
                }}
                onEditWorkExperience={(workExperience) => {
                  setSelectedWorkExperience(workExperience);
                  setWorkExperienceMutationError(null);
                  setIsEditWorkExperienceModalOpen(true);
                }}
                onDeleteWorkExperience={(workExperience) => {
                  setSelectedWorkExperience(workExperience);
                  setWorkExperienceMutationError(null);
                  setIsDeleteWorkExperienceDialogOpen(true);
                }}
                onAddProfileLanguage={() => {
                  setProfileLanguageMutationError(null);
                  setIsAddProfileLanguageModalOpen(true);
                }}
                onEditProfileLanguage={(profileLanguage) => {
                  setSelectedProfileLanguage(profileLanguage);
                  setProfileLanguageMutationError(null);
                  setIsEditProfileLanguageModalOpen(true);
                }}
                onDeleteProfileLanguage={(profileLanguage) => {
                  setSelectedProfileLanguage(profileLanguage);
                  setProfileLanguageMutationError(null);
                  setIsDeleteProfileLanguageDialogOpen(true);
                }}
                onAddProfileCertification={() => {
                  setProfileCertificationMutationError(null);
                  setIsAddProfileCertificationModalOpen(true);
                }}
                onEditProfileCertification={(profileCertification) => {
                  setSelectedProfileCertification(profileCertification);
                  setProfileCertificationMutationError(null);
                  setIsEditProfileCertificationModalOpen(true);
                }}
                onDeleteProfileCertification={(profileCertification) => {
                  setSelectedProfileCertification(profileCertification);
                  setProfileCertificationMutationError(null);
                  setIsDeleteProfileCertificationDialogOpen(true);
                }}
                cvs={cvs}
                onUploadCv={() => {
                  setCvMutationError(null);
                  setIsUploadCvModalOpen(true);
                }}
                onDeleteCv={(cv: Cv) => {
                  setSelectedCv(cv);
                  setCvMutationError(null);
                  setIsDeleteCvDialogOpen(true);
                }}
                onSetDefaultCv={handleSetDefaultCv}
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
        workModes={workModes}
        countries={countries}
      />

      <EditProfileModal
        profile={selectedProfile}
        isOpen={isEditModalOpen}
        isSaving={isSavingProfile}
        error={profileMutationError}
        onClose={() => setIsEditModalOpen(false)}
        onSave={handleUpdateProfile}
        workModes={workModes}
        countries={countries}
      />

      <DeleteProfileDialog
        profile={selectedProfile}
        isOpen={isDeleteDialogOpen}
        isDeleting={isDeletingProfile}
        error={profileMutationError}
        onClose={() => setIsDeleteDialogOpen(false)}
        onConfirm={handleArchiveProfile}
      />

      <AddProfileSkillModal
        skills={skills}
        profileSkills={profileSkills}
        isOpen={isAddProfileSkillModalOpen}
        isSaving={isSavingProfileSkill}
        error={profileSkillMutationError}
        onClose={() => {
          setProfileSkillMutationError(null);
          setIsAddProfileSkillModalOpen(false);
        }}
        onAdd={handleAddProfileSkill}
      />

      <EditProfileSkillModal
        profileSkill={selectedProfileSkill}
        skill={selectedSkill}
        isOpen={isEditProfileSkillModalOpen}
        isSaving={isSavingProfileSkill}
        error={profileSkillMutationError}
        onClose={() => {
          setSelectedProfileSkill(null);
          setProfileSkillMutationError(null);
          setIsEditProfileSkillModalOpen(false);
        }}
        onSave={handleUpdateProfileSkill}
      />

      <DeleteProfileSkillDialog
        profileSkill={selectedProfileSkill}
        skill={selectedSkill}
        isOpen={isDeleteProfileSkillDialogOpen}
        isDeleting={isDeletingProfileSkill}
        error={profileSkillMutationError}
        onClose={() => {
          setSelectedProfileSkill(null);
          setProfileSkillMutationError(null);
          setIsDeleteProfileSkillDialogOpen(false);
        }}
        onConfirm={handleDeleteProfileSkill}
      />
      <AddWorkExperienceModal
        isOpen={isAddWorkExperienceModalOpen}
        isSaving={isSavingWorkExperience}
        error={workExperienceMutationError}
        onClose={() => {
          setWorkExperienceMutationError(null);
          setIsAddWorkExperienceModalOpen(false);
        }}
        onAdd={handleAddWorkExperience}
      />

      <EditWorkExperienceModal
        workExperience={selectedWorkExperience}
        isOpen={isEditWorkExperienceModalOpen}
        isSaving={isSavingWorkExperience}
        error={workExperienceMutationError}
        onClose={() => {
          setSelectedWorkExperience(null);
          setWorkExperienceMutationError(null);
          setIsEditWorkExperienceModalOpen(false);
        }}
        onSave={handleUpdateWorkExperience}
      />

      <DeleteWorkExperienceDialog
        workExperience={selectedWorkExperience}
        isOpen={isDeleteWorkExperienceDialogOpen}
        isDeleting={isDeletingWorkExperience}
        error={workExperienceMutationError}
        onClose={() => {
          setSelectedWorkExperience(null);
          setWorkExperienceMutationError(null);
          setIsDeleteWorkExperienceDialogOpen(false);
        }}
        onConfirm={handleDeleteWorkExperience}
      />
      <AddProfileLanguageModal
        languages={languages}
        profileLanguages={profileLanguages}
        isOpen={isAddProfileLanguageModalOpen}
        isSaving={isSavingProfileLanguage}
        error={profileLanguageMutationError}
        onClose={() => {
          setProfileLanguageMutationError(null);
          setIsAddProfileLanguageModalOpen(false);
        }}
        onAdd={handleAddProfileLanguage}
      />

      <EditProfileLanguageModal
        profileLanguage={selectedProfileLanguage}
        language={selectedLanguage}
        isOpen={isEditProfileLanguageModalOpen}
        isSaving={isSavingProfileLanguage}
        error={profileLanguageMutationError}
        onClose={() => {
          setSelectedProfileLanguage(null);
          setProfileLanguageMutationError(null);
          setIsEditProfileLanguageModalOpen(false);
        }}
        onSave={handleUpdateProfileLanguage}
      />

      <DeleteProfileLanguageDialog
        profileLanguage={selectedProfileLanguage}
        language={selectedLanguage}
        isOpen={isDeleteProfileLanguageDialogOpen}
        isDeleting={isDeletingProfileLanguage}
        error={profileLanguageMutationError}
        onClose={() => {
          setSelectedProfileLanguage(null);
          setProfileLanguageMutationError(null);
          setIsDeleteProfileLanguageDialogOpen(false);
        }}
        onConfirm={handleDeleteProfileLanguage}
      />

      <AddProfileCertificationModal
        certifications={certifications}
        profileCertifications={profileCertifications}
        isOpen={isAddProfileCertificationModalOpen}
        isSaving={isSavingProfileCertification}
        error={profileCertificationMutationError}
        onClose={() => {
          setProfileCertificationMutationError(null);
          setIsAddProfileCertificationModalOpen(false);
        }}
        onAdd={handleAddProfileCertification}
      />

      <EditProfileCertificationModal
        profileCertification={selectedProfileCertification}
        certification={selectedCertification}
        isOpen={isEditProfileCertificationModalOpen}
        isSaving={isSavingProfileCertification}
        error={profileCertificationMutationError}
        onClose={() => {
          setSelectedProfileCertification(null);
          setProfileCertificationMutationError(null);
          setIsEditProfileCertificationModalOpen(false);
        }}
        onSave={handleUpdateProfileCertification}
      />

      <DeleteProfileCertificationDialog
        profileCertification={selectedProfileCertification}
        certification={selectedCertification}
        isOpen={isDeleteProfileCertificationDialogOpen}
        isDeleting={isDeletingProfileCertification}
        error={profileCertificationMutationError}
        onClose={() => {
          setSelectedProfileCertification(null);
          setProfileCertificationMutationError(null);
          setIsDeleteProfileCertificationDialogOpen(false);
        }}
        onConfirm={handleDeleteProfileCertification}
      />
      <UploadCvModal
        isOpen={isUploadCvModalOpen}
        isSaving={isSavingCv}
        error={cvMutationError}
        onClose={() => {
          setCvMutationError(null);
          setIsUploadCvModalOpen(false);
        }}
        onApplied={handleCvEnrichmentApplied}
        onUpload={handleUploadCv}
      />
      <DeleteCvDialog
        cv={selectedCv}
        isOpen={isDeleteCvDialogOpen}
        isDeleting={isDeletingCv}
        error={cvMutationError}
        onClose={() => {
          setSelectedCv(null);
          setCvMutationError(null);
          setIsDeleteCvDialogOpen(false);
        }}
        onConfirm={handleDeleteCv}
      />
    </>
  );
}
