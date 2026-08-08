from sqlalchemy.orm import Session

from app.jobs.job_offer_source_models import JobOfferSource
from app.jobs.job_source_models import JobSource
from app.jobs.models import JobOffer
from app.jobs.normalized_job_offer_schema import NormalizedJobOffer


class JobOfferRepository:
    """
    Repository responsable de la persistance des offres normalisées.
    """

    def __init__(self, db: Session):
        self.db = db

    def get_or_create_source(
        self,
        source_name: str,
        source_type: str = "MANUAL",
    ) -> JobSource:
        existing_source = self.db.query(JobSource).filter(
            JobSource.name == source_name
        ).first()

        if existing_source is not None:
            return existing_source

        new_source = JobSource(
            name=source_name,
            source_type=source_type,
            is_active=True,
        )

        self.db.add(new_source)
        self.db.flush()

        return new_source

    def find_duplicate(
        self,
        normalized_offer: NormalizedJobOffer,
    ) -> JobOffer | None:
        return self.db.query(JobOffer).filter(
            JobOffer.title == normalized_offer.title,
            JobOffer.company_name == normalized_offer.company,
            JobOffer.city == normalized_offer.city,
        ).first()

    def create_job_offer(
        self,
        normalized_offer: NormalizedJobOffer,
        source_name: str,
        source_type: str = "MANUAL",
        source_job_id: str | None = None,
        source_url: str | None = None,
    ) -> JobOffer:
        job_source = self.get_or_create_source(
            source_name=source_name,
            source_type=source_type,
        )

        job_offer = JobOffer(
            title=normalized_offer.title,
            company_name=normalized_offer.company,
            location=self._build_location(
                normalized_offer.city,
                normalized_offer.country,
            ),
            city=normalized_offer.city,
            region=normalized_offer.region,
            country=normalized_offer.country,
            source=source_name,
            source_url=source_url or normalized_offer.url_primary,
            url_primary=normalized_offer.url_primary,
            description=normalized_offer.description_raw,
            description_raw=normalized_offer.description_raw,
            description_normalized=normalized_offer.description_normalized,
            language=normalized_offer.language,
            work_mode=normalized_offer.work_mode,
            contract_type=normalized_offer.contract_type,
            seniority=normalized_offer.seniority,
            salary_min=normalized_offer.salary_min,
            salary_max=normalized_offer.salary_max,
            salary_currency=normalized_offer.salary_currency,
            salary_original_text=normalized_offer.salary_original_text,
            skills_extracted=normalized_offer.skills_extracted,
            skills_normalized=normalized_offer.skills_normalized,
            quality_level=normalized_offer.quality_level,
            status=normalized_offer.status,
        )

        self.db.add(job_offer)
        self.db.flush()

        self.attach_source(
            job_offer=job_offer,
            job_source=job_source,
            source_job_id=source_job_id,
            source_url=source_url or normalized_offer.url_primary,
        )

        return job_offer

    def update_job_offer(
        self,
        job_offer: JobOffer,
        normalized_offer: NormalizedJobOffer,
    ) -> JobOffer:
        job_offer.company_name = normalized_offer.company
        job_offer.location = self._build_location(
            normalized_offer.city,
            normalized_offer.country,
        )
        job_offer.city = normalized_offer.city
        job_offer.region = normalized_offer.region
        job_offer.country = normalized_offer.country
        job_offer.url_primary = normalized_offer.url_primary
        job_offer.description = normalized_offer.description_raw
        job_offer.description_raw = normalized_offer.description_raw
        job_offer.description_normalized = normalized_offer.description_normalized
        job_offer.language = normalized_offer.language
        job_offer.work_mode = normalized_offer.work_mode
        job_offer.contract_type = normalized_offer.contract_type
        job_offer.seniority = normalized_offer.seniority
        job_offer.salary_min = normalized_offer.salary_min
        job_offer.salary_max = normalized_offer.salary_max
        job_offer.salary_currency = normalized_offer.salary_currency
        job_offer.salary_original_text = normalized_offer.salary_original_text
        job_offer.skills_extracted = normalized_offer.skills_extracted
        job_offer.skills_normalized = normalized_offer.skills_normalized
        job_offer.quality_level = normalized_offer.quality_level
        job_offer.status = normalized_offer.status

        self.db.flush()

        return job_offer

    def upsert_job_offer(
        self,
        normalized_offer: NormalizedJobOffer,
        source_name: str,
        source_type: str = "MANUAL",
        source_job_id: str | None = None,
        source_url: str | None = None,
    ) -> JobOffer:
        duplicate = self.find_duplicate(normalized_offer)

        job_source = self.get_or_create_source(
            source_name=source_name,
            source_type=source_type,
        )

        if duplicate is not None:
            updated_offer = self.update_job_offer(
                duplicate,
                normalized_offer,
            )

            self.attach_source(
                job_offer=updated_offer,
                job_source=job_source,
                source_job_id=source_job_id,
                source_url=source_url or normalized_offer.url_primary,
            )

            return updated_offer

        return self.create_job_offer(
            normalized_offer=normalized_offer,
            source_name=source_name,
            source_type=source_type,
            source_job_id=source_job_id,
            source_url=source_url,
        )

    def attach_source(
        self,
        job_offer: JobOffer,
        job_source: JobSource,
        source_job_id: str | None,
        source_url: str,
    ) -> JobOfferSource:
        existing_link = self.db.query(JobOfferSource).filter(
            JobOfferSource.job_offer_id == job_offer.id,
            JobOfferSource.job_source_id == job_source.id,
            JobOfferSource.source_url == source_url,
        ).first()

        if existing_link is not None:
            return existing_link

        job_offer_source = JobOfferSource(
            job_offer_id=job_offer.id,
            job_source_id=job_source.id,
            source_job_id=source_job_id,
            source_url=source_url,
        )

        self.db.add(job_offer_source)
        self.db.flush()

        return job_offer_source

    @staticmethod
    def _build_location(
        city: str | None,
        country: str | None,
    ) -> str | None:
        if city and country:
            return f"{city}, {country}"

        if city:
            return city

        if country:
            return country

        return None