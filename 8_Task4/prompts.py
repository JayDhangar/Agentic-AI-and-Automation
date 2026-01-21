from langchain_core.prompts import ChatPromptTemplate

resume_prompt = ChatPromptTemplate.from_messages([
    ("system", "Extract resume information. Return ONLY valid JSON."),
    ("human", "Resume:\n{resume_text}\n{format_instructions}")
])

skill_prompt = ChatPromptTemplate.from_messages([
    ("system",
     """You are a Skill Matching Agent.

CRITICAL RULES:
- Output MUST be valid JSON
- Do NOT include code, markdown, or explanations
- Output must start with {{ and end with }}

JSON SCHEMA:
{{
  "shortlisted": boolean,
  "match_score": number,
  "matched_skills": string[],
  "missing_skills": string[],
  "reason": string
}}
"""),
    ("human",
     """Resume:
{resume}

Job Requirements:
{job_requirements}

{format_instructions}
""")
])
