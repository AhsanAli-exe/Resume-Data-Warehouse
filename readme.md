# 📊 Resume ETL Pipeline into SQL Warehouse

A complete **ETL (Extract, Transform, Load)** pipeline that processes resume data using LLM parsing, stores it in a SQLite data warehouse, and provides a FastAPI backend with Streamlit dashboard for analytics.

## 🎯 Project Overview

This project demonstrates **data engineering fundamentals** by building a production-ready ETL pipeline that:
- **Extracts** resume data using Groq LLM
- **Transforms** raw data into structured format with cleaning and standardization
- **Loads** processed data into a SQLite data warehouse with star schema
- **Serves** data via FastAPI REST endpoints
- **Visualizes** insights through an interactive Streamlit dashboard

## 🏗️ Architecture

```
Raw Resumes (TXT) → LLM Parsing → JSON Files → Pandas Transformation → SQLite Warehouse → FastAPI → Streamlit Dashboard
```

## 📁 Project Structure

```
Resume Pipeline/
├── data/
│   ├── raw/                 # Original resume text files
│   ├── processed/           # LLM-parsed JSON files
│   └── cleaned/             # Transformed CSV files
├── etl/
│   ├── transform.ipynb      # Data transformation notebook
│   └── load.py             # Database loading script
├── database/
│   ├── schema.py           # SQLite schema definition
│   ├── connection.py       # Database connection utility
│   └── resume_warehouse.db # SQLite database
├── api/
│   └── main.py             # FastAPI application
├── dashboard/
│   └── streamlit_app.py    # Streamlit dashboard
└── requirements.txt        # Python dependencies
```

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Groq API key (for LLM parsing)

### Installation

1. **Clone the repository**
```bash
git clone <your-repo-url>
cd Resume-Pipeline
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Set up environment variables**
```bash
# Create .env file with your Groq API key
GROQ_API_KEY=your_api_key_here
```

4. **Run the ETL pipeline**
```bash
# From Resume Pipeline directory
python -m uvicorn api.main:app --reload  # Start FastAPI server
streamlit run dashboard/streamlit_app.py  # Start Streamlit dashboard
```

## 📊 Database Schema

### Star Schema Design
- **Dimension Tables**: `candidates`, `skills`, `experience`, `education`
- **Fact Table**: `Jobs` (for future job matching)
- **Relationships**: Foreign keys linking dimensions to facts

### Key Tables
```sql
candidates (candidate_id, full_name, email, total_skills, ...)
skills (candidate_id, skill_name, category, proficiency, ...)
experience (candidate_id, job_title, company, duration_yrs, ...)
education (candidate_id, degree, institution, level, ...)
```

## 🔌 API Endpoints

### Core Endpoints
- `GET /api/candidates` - List all candidates
- `GET /api/candidates/{id}` - Get candidate details
- `GET /api/skills/{id}` - Get candidate skills
- `GET /api/experience/{id}` - Get candidate experience
- `GET /api/education/{id}` - Get candidate education

### Analytics Endpoints
- `GET /api/analytics/summary` - Dashboard metrics
- `GET /api/skills?category={category}` - Skills by category

## 📈 Dashboard Features

### Multi-Page Interface
1. **Overview** - Key metrics and summary statistics
2. **Candidates** - Searchable candidate table
3. **Skill Analysis** - Interactive charts and skill breakdown
4. **Individual Profiles** - Detailed candidate profiles

### Interactive Elements
- Real-time search functionality
- Interactive charts (Plotly)
- Responsive data tables
- API integration

## 🔧 ETL Process Details

### Extract Phase
- **Source**: Text resume files
- **Method**: Groq LLM parsing with structured prompts
- **Output**: JSON files with standardized format

### Transform Phase
- **Data Cleaning**: Phone standardization, skill categorization
- **Derived Fields**: Experience calculations, completeness scores
- **Quality Checks**: Null handling, data validation

### Load Phase
- **Target**: SQLite data warehouse
- **Method**: Pandas to_sql with custom schema
- **Optimization**: Proper indexing and relationships

## 🛠️ Technologies Used

- **Data Processing**: Pandas, NumPy
- **Database**: SQLite
- **API Framework**: FastAPI
- **Dashboard**: Streamlit, Plotly
- **LLM**: Groq API
- **File Processing**: JSON, CSV

## 📊 Sample Data

The project includes **23 real resumes** from computer science and AI enthusiasts, providing realistic data for testing and demonstration.

## 🎯 Key Features

- ✅ **Complete ETL Pipeline**
- ✅ **LLM-Powered Data Extraction**
- ✅ **Professional Database Design**
- ✅ **RESTful API**
- ✅ **Interactive Dashboard**
- ✅ **Data Quality Assurance**
- ✅ **Scalable Architecture**

## 🚀 Deployment Notes

**Local Development**: The current setup uses localhost for API calls. For production deployment, you would need to:
1. Deploy FastAPI to a cloud service (Heroku, AWS, etc.)
2. Update API URLs in Streamlit app
3. Deploy Streamlit to Streamlit Cloud

## 👨‍💻 Developer

**Ahsan Ali** - Data Engineering Enthusiast

---

*This project demonstrates fundamental data engineering concepts and is perfect for learning ETL processes, API development, and data visualization.*
