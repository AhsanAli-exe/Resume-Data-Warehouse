
import os
import json
import sys
import logging
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

def generate_resume_prompt(resume_text):
    schema = """
**Instructions:**
- Parse the provided resume text and return the parsed data strictly in the JSON format as outlined in the schema below.
- Do not add any commentary or explanations; just return the structured JSON.
- If any data or field is missing, infer it where possible. For instance, if years of experience are not explicitly provided, calculate it based on the start and end dates of experience or education.
- If something cannot be inferred, leave the field as `null` or an empty string as appropriate.
- If there are multiple entries for a section (e.g., multiple jobs, educational qualifications, certifications), ensure each is captured in the order they appear in the resume.
- Handle edge cases where data may be incomplete or ambiguous, such as missing contact information, skills, or publications.
- If specific sections like publications, volunteer experiences, or awards are not present in the resume, leave them as empty lists.
- Follow the exact structure and data types as shown in the provided schema.

**Important Notes:**
- In the event of unclear or missing data (e.g., job responsibilities or skills, projects description), attempt to infer or leave it as null. If found any description, just keep it intact (Don't even change the wordings)
- The **contact info** should be filled based on provided details; if some fields (like email or phone) are missing, mark them as empty strings or `null`.
- Ensure all sections are accounted for logically based on the content provided in the resume. For example, if no projects are mentioned, leave the **projects** array empty.
- The **dates** should be formatted as `"YYYY-MM-DD"`. If the exact date is unknown, try to estimate or mark it as `null`.
- If there is no **summary** or brief description in the resume, the **summary** field should be marked as `null` or an empty string. If found any summary, keep wordings intact.
- Donot change the sentences written for job responsibilites, keep them as it is, any senetence textual data should remain as it is, with sub-headings.

**Structured JSON Schema:**

"""
    
    json_schema = """
{
  "basic_info": {
    "full_name": "string",
    "current_title": "string",
    "gender": "string",
    "date_of_birth": "string",
    "nationality": "string"
  },
  "contact_info": {
    "email": "string",
    "phone": "string",
    "address": {
      "street": "string",
      "city": "string",
      "state": "string",
      "zip_code": "string",
      "country": "string"
    },
    "linkedin": "string",
    "github": "string",
    "portfolio": "string"
  },
  "summary": "string",
  "skills": [
    {
      "skill_name": "string",
      "proficiency": "string",
      "category": "string",
      "years_of_experience": "integer"
    }
  ],
  "education": [
    {
      "degree": "string",
      "field": "string",
      "institution": "string",
      "start_date": "string",
      "end_date": "string",
      "grade": "string",
      "location": "string",
      "courses": [
        "string"
      ]
    }
  ],
  "experience": [
    {
      "job_title": "string",
      "company": "string",
      "start_date": "string",
      "end_date": "string",
      "employment_type": "string",
      "location": "string",
      "responsibilities": [
        "string"
      ],
      "skills_used": [
        "string"
      ]
    }
  ],
  "projects": [
    {
      "title": "string",
      "description": "string",
      "technologies": [
        "string"
      ],
      "role": "string",
      "start_date": "string",
      "end_date": "string",
      "link": "string"
    }
  ],
  "certifications": [
    {
      "title": "string",
      "issuer": "string",
      "issue_date": "string",
      "expiration_date": "string",
      "credential_id": "string",
      "url": "string"
    }
  ],
  "publications": [
    {
      "title": "string",
      "journal": "string",
      "authors": [
        "string"
      ],
      "year": "integer",
      "doi": "string",
      "url": "string"
    }
  ],
  "languages": [
    {
      "language": "string",
      "proficiency": "string"
    }
  ],
  "interests": [
    "string"
  ],
  "volunteer_experience": [
    {
      "role": "string",
      "organization": "string",
      "start_date": "string",
      "end_date": "string",
      "description": "string"
    }
  ],
  "awards": [
    {
      "title": "string",
      "issuer": "string",
      "date": "string",
      "description": "string"
    }
  ],
  "links": [
    {
      "label": "string",
      "url": "string"
    }
  ]
}
"""

    return schema + f"\n\nResume Text: {resume_text}\n" + json_schema


def call_llm(resume_text: str) -> dict:
    try:
        client = Groq(api_key=os.getenv("GROQ_API_KEY"))
        prompt = generate_resume_prompt(resume_text)
        
        response = client.chat.completions.create(
            model = "llama-3.3-70b-versatile",
            messages = [
                {"role":"system","content":"You are a helpful resume parser."},
                {"role":"user","content":prompt}
            ],
            temperature = 0.3
        )
        
        content = response.choices[0].message.content
        tokens = response.usage.total_tokens
        
        return {
            "content": content,
            "tokens": tokens
        }
    except Exception as e:
        logging.error(e)
        return {
            "content": "",
            "tokens": 0
        }
        

