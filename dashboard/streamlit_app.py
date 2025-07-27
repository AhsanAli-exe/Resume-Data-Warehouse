import streamlit as st 
import requests
import pandas as pd
import plotly.express as px

def fetch_data(endpoint):
    try:
        response = requests.get(f"http://127.0.0.1:8000/{endpoint}")
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"API Error: {response.status_code}")
            return None
    except Exception as e:
        st.error(f"Connection Error:{e}")
        return None
    
    

st.set_page_config(
    page_title = "Resume Data Warehouse",
    page_icon = "💼",
    layout = "wide"
)


st.title("_Resume_ _Data_ :blue[Warehouse] :sunglasses:")
st.header("Developed by: :blue[Ahsan Ali]")
st.markdown("---")

st.sidebar.title("Navigation")
page = st.sidebar.selectbox(
    "Choose a page",
    ['Overview',"Candidates","Skill Analysis","Individual Profiles"]
)

if page=="Overview":
    st.header("Dashboard Overview")
    summary_data = fetch_data("api/analytics/summary")
    if summary_data and summary_data.get("Success"):
        data = summary_data['data']
        col1,col2,col3,col4 = st.columns(4)
        with col1:
            st.metric("Total Candidates", data['summary']['total_candidates'])
        with col2:
            st.metric("Total Skills", data['summary']['total_skills'])
        with col3:
            st.metric("Total Experience", data['summary']['total_experience'])
        with col4:
            st.metric("Total Education", data['summary']['total_education'])
    else:
        st.error("Failed to fetch data")
        
    st.markdown("---")
    

elif page=="Candidates":
    st.header("All Candidates")
    candidates_data = fetch_data("api/candidates")
    if candidates_data and candidates_data.get("Success"):
        candidates = candidates_data['data']
        
        st.info(f"Total Candidates: {candidates_data['total']}")
        df = pd.DataFrame(candidates)
        display_cols = ['candidate_id','full_name','email','city','total_skills']
        df_display = df[display_cols].copy()
        df_display.columns = ['ID','Name','Email','City','Skills Count']
        st.dataframe(df_display,use_container_width=True)
        st.subheader("Search Candidates")
        search_name = st.text_input("Search by Name: ")
        if search_name:
            ans = df_display[df_display['Name'].str.contains(search_name,case=False,na=False)]
            st.dataframe(ans,use_container_width=True)
    else:
        st.error("Failed to fetch data")
        
elif page=="Skill Analysis":
    st.header("Skill Analysis")
    summary_data = fetch_data("api/analytics/summary")
    if summary_data and summary_data.get("Success"):
        top_skills = summary_data['data']['top_skills']
        
        if top_skills:
            df_skills = pd.DataFrame(top_skills)
            
            fig = px.bar(
                df_skills,
                x = "skill_name",
                y = 'count',
                title = "Top 10 Most Common Skills",
                labels = {'skill_name':'Skill','count':"Number of Candidates"},
                color = 'count',
                color_continuous_scale = 'Blues'
            )
            fig.update_layout(xaxis_tickangle = 45)
            st.plotly_chart(fig,use_container_width=True)
            
            st.subheader("Skills Breakdown")
            st.dataframe(df_skills,use_container_width=True)
            
elif page=="Individual Profiles":
    st.header("Individual Candidate Profiles")
    candidates_data = fetch_data("api/candidates")
    if candidates_data and candidates_data.get("Success"):
        candidates = candidates_data['data']
    candidate_options = {f"{c['full_name']} (ID: {c['candidate_id']})": c['candidate_id'] for c in candidates}
    selected_candidate = st.selectbox("Choose a candidate:", list(candidate_options.keys()))
    if selected_candidate:
        candidate_id = candidate_options[selected_candidate]
        profile_data = fetch_data(f"api/candidates/{candidate_id}")
        if profile_data and profile_data.get("Success"):
            profile = profile_data['data']
            basic = profile['basic_info']
            col1, col2 = st.columns(2)
            with col1:
                st.write(f"**Name:** {basic['full_name']}")
                st.write(f"**Current Title:** {basic['current_title']}")
                st.write(f"**Email:** {basic['email']}")
                st.write(f"**Phone:** {basic['phone']}")
            
            with col2:
                st.write(f"**City:** {basic['city']}")
                st.write(f"**Country:** {basic['country']}")
                st.write(f"**Total Skills:** {basic['total_skills']}")
            
            st.subheader("Skills")
            if profile["skills"]:
                skills_df = pd.DataFrame(profile["skills"])
                st.dataframe(skills_df,use_container_width=True)
            else:
                st.info("No skills data available")
            
            st.subheader("Experience")
            if profile["experience"]:
                exp_df = pd.DataFrame(profile["experience"])
                st.dataframe(exp_df,use_container_width=True)
            else:
                st.info("No experience data available")
            
            st.subheader("Education")
            if profile["education"]:
                    edu_df = pd.DataFrame(profile["education"])
                    st.dataframe(edu_df,use_container_width=True)
            else:
                st.info("No education data available")
                
        else:
            st.error("Failed to fetch candidate profile")
else:
    st.error("Failed to fetch candidates list")