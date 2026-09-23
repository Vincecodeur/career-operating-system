from pydantic import BaseModel
from pydantic import ConfigDict
from pydantic import Field


class ExtractedJobOfferMetadata(BaseModel):
    """
    Métadonnées structurées extraites de la description d'une offre
    par Gemini (DEC-093). matched_skills est restreint au catalogue
    Skill existant (aucune création à la volée) ; toute compétence
    mentionnée dans l'offre mais absente du catalogue est reportée
    dans unmatched_skill_mentions, à titre informatif uniquement.
    """

    matched_skills: list[str] = Field(default_factory=list)
    unmatched_skill_mentions: list[str] = Field(default_factory=list)
    seniority: str = "UNKNOWN"
    work_mode: str = "UNKNOWN"

    model_config = ConfigDict(
        extra="forbid",
    )