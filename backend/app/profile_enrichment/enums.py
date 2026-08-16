from enum import Enum


class ProfileEnrichmentProposalType(str, Enum):
    PROFILE_FIELD = "PROFILE_FIELD"
    SKILL = "SKILL"
    HARD_SKILL = "HARD_SKILL"
    SOFT_SKILL = "SOFT_SKILL"
    LANGUAGE = "LANGUAGE"
    CERTIFICATION = "CERTIFICATION"
    EXPERIENCE = "EXPERIENCE"


class ProfileEnrichmentProposalStatus(str, Enum):
    PENDING = "PENDING"
    ACCEPTED = "ACCEPTED"
    REJECTED = "REJECTED"