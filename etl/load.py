import pandas as pd
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database.connection import db

def load_all_data():
    try:
        # First, recreate the database schema
        from database.schema import db_schema
        db_schema()
        
        # Then load the data
        candidates_df = pd.read_csv('data/cleaned/basic_info_cleaned.csv')
        db.load_dataframe_to_table(candidates_df, 'candidates')
        skills_df = pd.read_csv('data/cleaned/skills_cleaned.csv')
        db.load_dataframe_to_table(skills_df, 'skills')
        experience_df = pd.read_csv('data/cleaned/experience_cleaned.csv')
        db.load_dataframe_to_table(experience_df, 'experience')
        education_df = pd.read_csv('data/cleaned/education_cleaned.csv')
        db.load_dataframe_to_table(education_df, 'education')
        
        print("\nAll data loaded successfully!")
        
        # 5. Display summary
        print("\n Database Summary:")
        print(f"Candidates: {db.get_table_count('candidates')}")
        print(f"Skills: {db.get_table_count('skills')}")
        print(f"Experience: {db.get_table_count('experience')}")
        print(f"Education: {db.get_table_count('education')}")
        
    except Exception as e:
        print(f"Error loading data: {e}")

def test_queries():
    print("\nTesting db queries")
    
    try:
        candidates = db.execute_query("SELECT candidate_id, full_name, total_skills FROM candidates LIMIT 5")
        print("\nSample Candidates:")
        print(candidates)
        
        skills = db.execute_query("""
            SELECT skill_name, category, proficiency 
            FROM skills 
            WHERE candidate_id = 1 
            LIMIT 5
        """)
        print("\nSample Skills for Candidate 1:")
        print(skills)
        
        experience_count = db.execute_query("SELECT COUNT(*) as total_experience FROM experience")
        print("\nTotal Experience Records:")
        print(experience_count)
        
    except Exception as e:
        print(f"Error testing queries: {e}")

if __name__ == "__main__":
    load_all_data()
    test_queries()
