import sqlite3
import os


def db_schema():
    os.makedirs('database',exist_ok=True)
    
    #connecting to db
    
    conn = sqlite3.connect('database/resume_warehouse.db')
    cursor = conn.cursor()
    
    print("Creating Database Schema..")
    
    #creating tables
    print("Creating candidates table")
    cursor.execute('''
                   create table if not exists candidates(
                       candidate_id INTEGER PRIMARY KEY,
                       filename TEXT,
                       full_name TEXT,
                       current_title TEXT,
                       email TEXT,
                       phone TEXT,
                       city TEXT,
                       country TEXT,
                       linkedin TEXT,
                       github TEXT,
                       summary TEXT,
                       total_skills INTEGER,
                       education_level TEXT,
                       created_date TEXT,
                       completeness_score INTEGER,
                       total_experience_years REAL,
                       highest_degree TEXT,
                       level INTEGER,
                       skill_diversity_score INTEGER
                   )
            ''')
    
    print("Creating Skills Table")
    cursor.execute('''
                   create table if not exists skills(
                       candidate_id INTEGER,
                       skill_name TEXT,
                       proficiency TEXT,
                       category TEXT,
                       years_of_experience REAL,
                       FOREIGN KEY (candidate_id) REFERENCES candidates(candidate_id)
                   )
            ''')
    
    print("Creating Experience Table")
    cursor.execute('''
                   create table if not exists experience(
                       candidate_id INTEGER,
                       job_title TEXT,
                       company TEXT,
                       start_date TEXT,
                       end_date TEXT,
                       employment_type TEXT,
                       location TEXT,
                       is_current_job BOOLEAN,
                       responsibilities_count INTEGER,
                       skills_used_count INTEGER,
                       duration_yrs REAL,
                       FOREIGN KEY (candidate_id) REFERENCES candidates(candidate_id)
                   )
            ''')
    print("Creating Education Table")
    cursor.execute('''
                   create table if not exists education(
                       candidate_id INTEGER,
                       degree TEXT,
                       field TEXT,
                       institution TEXT,
                       start_date TEXT,
                       end_date TEXT,
                       grade TEXT,
                       location TEXT,
                       courses_count INTEGER,
                       level INTEGER,
                       FOREIGN KEY (candidate_id) REFERENCES candidates(candidate_id)
                   )
            ''')
    
    print("Creating Job Match Table")
    cursor.execute('''
                   create table if not exists Jobs(
                       match_id INTEGER PRIMARY KEY,
                       candidate_id INTEGER,
                       job_id INTEGER,
                       skill_match_score REAL,
                       experience_match_score REAL,
                       education_match_score REAL,
                       overall_match_score REAL,
                       match_date TEXT,
                       FOREIGN KEY (candidate_id) REFERENCES candidates(candidate_id))
                   ''')
    
    
    conn.commit()
    conn.close()

    
    print("Database Schema Created Successfully")
    
db_schema()
    
