from app.jobs.normalized_job_offer_schema import NormalizedJobOffer
from app.jobs.raw_offer_schema import RawOffer


class NormalizationService:
    """
    Transforme une RawOffer en NormalizedJobOffer.
    """

    DEFAULT_SENIORITY = "UNKNOWN"
    DEFAULT_QUALITY_LEVEL = "PARTIAL"

    def normalize(self, raw_offer: RawOffer) -> NormalizedJobOffer:
        return NormalizedJobOffer(
            title=raw_offer.title.strip(),
            company=self._clean_optional_text(raw_offer.company),
            description_raw=raw_offer.raw_description,
            description_normalized=raw_offer.raw_description.strip(),
            url_primary=raw_offer.source_url or "",
            language=raw_offer.language_raw or "UNKNOWN",
            city=self._clean_optional_text(raw_offer.city),
            region=self._clean_optional_text(raw_offer.region),
            country=raw_offer.country or "UNKNOWN",
            work_mode=raw_offer.work_mode_raw or "UNKNOWN",
            contract_type=raw_offer.contract_type_raw or "UNKNOWN",
            seniority=self.DEFAULT_SENIORITY,
            salary_min=None,
            salary_max=None,
            salary_currency=None,
            salary_original_text=raw_offer.salary_raw,
            skills_extracted=[],
            skills_normalized=[],
            quality_level=self.DEFAULT_QUALITY_LEVEL,
            status="ACTIVE",
        )

    @staticmethod
    def _clean_optional_text(value: str | None) -> str | None:
        if value is None:
            return None

        value = value.strip()

        return value or None