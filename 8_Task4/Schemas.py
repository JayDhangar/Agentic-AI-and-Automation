from pydantic import BaseModel
from typing import List, Optional, TypedDict

class ResumeSchema(BaseModel):
    name: Optional[str]
    email: Optional[str]
    phone: Optional[str]
    skills: List[str]
    experience_years: Optional[int]
    education: Optional[str]

class SkillMatch(BaseModel):
    shortlisted: bool
    match_score: float
    matched_skills: List[str]
    missing_skills: List[str]
    reason: str

class HRState(TypedDict):
    resume_files: list[str]
    resume_text: str
    parsed_resume: dict
    skill_match: dict
    email_status: str