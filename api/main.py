from fastapi import FastAPI
import uvicorn 
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database.connection import db

app = FastAPI(
    title = "Resume Data Warehouse API",
    description = "API for Resume Data Warehouse",
    version = "1.0.0"
)

@app.get("/")
async def root():
    return{"message":"Hello World"}

@app.get("/api/candidates")
async def get_candidates():
    try:
        query = "SELECT * FROM candidates"
        candidates = db.execute_query(query)
        candidates_clean = candidates.fillna("")
        return{
            "Success":True,
            "data":candidates_clean.to_dict(orient="records"),
            "total": db.get_table_count("candidates")
        }
    except Exception as e:
        return{
            "Success":False,
            "error":str(e)
        }

@app.get("/api/education/{candidate_id}")
async def get_education(candidate_id: int):
    try:
        query = f'SELECT e.candidate_id, c.full_name, e.degree, e.field, e.institution, e.grade FROM education e, candidates c WHERE e.candidate_id = c.candidate_id AND e.candidate_id = {candidate_id}'
        education = db.execute_query(query)
        education_clean = education.fillna("")
        return{
            "Success":True,
            "data":education_clean.to_dict(orient="records"),
            "total":db.get_table_count("education")
        }
    except Exception as e:
        return{
            "Success":False,
            "error":str(e)
        }

@app.get("/api/skills/{candidate_id}")
async def get_candidate_skills(candidate_id: int):
    try:
        query = f'SELECT s.skill_name,s.category,s.proficiency FROM skills s WHERE s.candidate_id = {candidate_id}'
        skills = db.execute_query(query)
        skills_clean = skills.fillna("")
        return{
            "Success": True,
            "data": skills_clean.to_dict(orient="records"),
            "total": len(skills_clean)
        }
    except Exception as e:
        return{
            "Success": False,
            "error": str(e)
        }

@app.get("/api/experience/{candidate_id}")
async def get_candidate_experience(candidate_id: int):
    try:
        query = f'SELECT e.job_title, e.company, e.start_date, e.end_date, e.employment_type, e.location, e.duration_yrs FROM experience e WHERE e.candidate_id = {candidate_id}'
        experience = db.execute_query(query)
        experience_clean = experience.fillna("")
        return{
            "Success": True,
            "data": experience_clean.to_dict(orient="records"),
            "total": len(experience_clean)
        }
    except Exception as e:
        return{
            "Success": False,
            "error": str(e)
        }

@app.get("/api/candidates/{candidate_id}")
async def get_candidate_details(candidate_id: int):
    try:
        basic_query = f'SELECT * FROM candidates WHERE candidate_id = {candidate_id}'
        basic_info = db.execute_query(basic_query)
        
        if basic_info.empty:
            return{
                "Success": False,
                "error": "Candidate not found"
            }
        
        skills_query = f'SELECT skill_name,category,proficiency FROM skills WHERE candidate_id = {candidate_id}'
        skills = db.execute_query(skills_query)
        exp_query = f'SELECT job_title,company,duration_yrs FROM experience WHERE candidate_id = {candidate_id}'
        experience = db.execute_query(exp_query)
        edu_query = f'SELECT degree,field,institution FROM education WHERE candidate_id = {candidate_id}'
        education = db.execute_query(edu_query)
        
        return{
            "Success": True,
            "data": {
                "basic_info": basic_info.fillna("").to_dict(orient="records")[0],
                "skills": skills.fillna("").to_dict(orient="records"),
                "experience": experience.fillna("").to_dict(orient="records"),
                "education": education.fillna("").to_dict(orient="records")
            }
        }
    except Exception as e:
        return{
            "Success": False,
            "error": str(e)
        }

@app.get("/api/analytics/summary")
async def get_analytics_summary():
    try:
        candidate_count = db.get_table_count("candidates")
        skills_count = db.get_table_count("skills")
        experience_count = db.get_table_count("experience")
        education_count = db.get_table_count("education")
        top_skills_query = """
            SELECT skill_name, COUNT(*) as count 
            FROM skills 
            GROUP BY skill_name 
            ORDER BY count DESC 
            LIMIT 10
        """
        top_skills = db.execute_query(top_skills_query)
        
        return{
            "Success": True,
            "data": {
                "summary": {
                    "total_candidates": candidate_count,
                    "total_skills": skills_count,
                    "total_experience": experience_count,
                    "total_education": education_count
                },
                "top_skills": top_skills.fillna("").to_dict(orient="records"),
            }
        }
    except Exception as e:
        return{
            "Success": False,
            "error": str(e)
        }

@app.get("/api/skills")
async def get_all_skills(category: str = None):
    try:
        if category:
            query = f"""
                SELECT skill_name, category, COUNT(*) as count
                FROM skills 
                WHERE category = '{category}'
                GROUP BY skill_name, category, proficiency
                ORDER BY count DESC
            """
        else:
            query = """
                SELECT skill_name, category COUNT(*) as count
                FROM skills 
                GROUP BY skill_name, category, proficiency
                ORDER BY count DESC
                LIMIT 50
            """
        
        skills = db.execute_query(query)
        return{
            "Success": True,
            "data": skills.fillna("").to_dict(orient="records"),
            "total": len(skills)
        }
    except Exception as e:
        return{
            "Success": False,
            "error": str(e)
        }
        
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)