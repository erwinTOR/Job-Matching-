import streamlit as st
import pandas as pd

# ---------- Page title ----------
st.title("Job Matcher (Phase 2 MVP)")

st.write(
    "Upload/paste your resume text, then view jobs and filter them by location. "
    "This is a simple prototype running entirely in the cloud."
)

# ---------- 1. Profile input ----------
st.header("Step 1: Paste your resume text")

resume_text = st.text_area(
    "Paste your resume or LinkedIn 'About'/Experience here:",
    height=200,
    placeholder="Paste your resume text..."
)

# NOTE: For now, resume_text is not used for scoring.
# Later, you'll use it to compute a 'fit_score' for each job.

# ---------- 2. Load job data ----------
@st.cache_data
def load_jobs():
    df = pd.read_csv("jobs.csv")
    # Dummy fit_score for now
    df["fit_score"] = 50
    return df

jobs_df = load_jobs()

# ---------- 3. Sidebar filters (including location) ----------
st.sidebar.header("Filters")

all_locations = sorted(jobs_df["location"].dropna().unique().tolist())

selected_locations = st.sidebar.multiselect(
    "Filter by location:",
    options=all_locations,
    default=all_locations
)

if selected_locations:
    filtered_jobs = jobs_df[jobs_df["location"].isin(selected_locations)]
else:
    filtered_jobs = jobs_df

# ---------- 4. Show results ----------
st.header("Step 2: Matched jobs")

st.write(
    "Below is a list of jobs filtered by location. "
    "Later, we'll sort these by how well they match your resume."
)

filtered_jobs = filtered_jobs.sort_values(by="fit_score", ascending=False)

st.dataframe(
    filtered_jobs[["title", "company", "location", "fit_score", "url"]],
    use_container_width=True
)
