from pydantic import BaseModel


class ParsedCVExperience(BaseModel):
    title: str | None = None
    company: str | None = None
    start_date: str | None = None
    end_date: str | None = None
    description: str | None = None


class ParsedCVData(BaseModel):
    full_name: str | None = None
    professional_title: str | None = None
    summary: str | None = None
    skills: list[str] = []
    languages: list[str] = []
    certifications: list[str] = []
    experiences: list[ParsedCVExperience] = []


class ParsedCVResponse(BaseModel):
    cv_id: int
    parsing_status: str
    raw_text_length: int
    extracted_text_preview: str
    parsed_data: ParsedCVData