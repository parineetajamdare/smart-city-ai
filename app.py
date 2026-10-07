import streamlit as st
from groq import Groq
from dotenv import load_dotenv
from datetime import datetime
from database import (
    register_user,
    login_user,
    save_issue,
    get_user_issues,
    get_dashboard_stats
)
import os

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

# ---------------- SESSION STATE ----------------

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "user_name" not in st.session_state:
    st.session_state.user_name = ""

if "user_id" not in st.session_state:
    st.session_state.user_id = None

# ---------------- SIDEBAR ----------------

if st.session_state.logged_in:
    page = st.sidebar.selectbox(
        "Choose Page",
        ["Report Issue", "My Reports", "Logout"]
    )
else:
    page = st.sidebar.selectbox(
        "Choose Page",
        ["Register", "Login"]
    )

# ---------------- REGISTER ----------------

if page == "Register":

    st.header("Citizen Registration")

    name = st.text_input("Full Name")
    email = st.text_input("Email")
    phone = st.text_input("Phone Number")

    password = st.text_input(
        "Password",
        type="password"
    )

    confirm_password = st.text_input(
        "Confirm Password",
        type="password"
    )

    if st.button("Register"):

        if password != confirm_password:
            st.error("Passwords do not match")

        else:
            try:
                register_user(
                    name,
                    email,
                    phone,
                    password
                )

                st.success(
                    "Registration Successful!"
                )

            except Exception:
                st.error(
                    "Email already exists"
                )

# ---------------- LOGIN ----------------

if page == "Login":

    st.header("Citizen Login")

    email = st.text_input("Email")

    password = st.text_input(
        "Password",
        type="password"
    )

    if st.button("Login"):

        user = login_user(
            email,
            password
        )

        if user:

            st.session_state.logged_in = True
            st.session_state.user_id = user[0]
            st.session_state.user_name = user[1]

            st.success("Login Successful!")

            st.rerun()

        else:
            st.error(
                "Invalid Email or Password"
            )

# ---------------- LOGOUT ----------------

if page == "Logout":

    st.session_state.logged_in = False
    st.session_state.user_name = ""
    st.session_state.user_id = None

    st.success(
        "Logged out successfully"
    )

    st.rerun()

# ---------------- REPORT ISSUE ----------------

# ---------------- REPORT ISSUE ----------------

if page == "Report Issue":

    st.title("🏙️ Smart City Civic Issue Reporter")

    st.write(
        f"Welcome, {st.session_state.user_name}"
    )

    title = st.text_input("Issue Title")

    description = st.text_area(
        "Issue Description"
    )

    city = st.text_input("City")

    address = st.text_input("Address")

    photo = st.file_uploader(
        "Upload Issue Photo (Optional)",
        type=["jpg", "jpeg", "png"]
    )

    if photo:
        st.image(photo, width=300)

    if st.button("Analyze Issue"):

        if not title or not description or not city or not address:
            st.error("Please fill all fields")

        else:

            prompt = f"""
You are an AI assistant for a Smart City Civic Issue Reporting System.

Analyze the civic complaint below.

Title: {title}

Description: {description}

Return EXACTLY in this format:

Category:
Severity:
Responsible Department:
Professional Complaint:

The Professional Complaint should be a formal paragraph that can be submitted to the municipal authority.
"""

            response = client.chat.completions.create(
                model="openai/gpt-oss-20b",
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            )

            ai_response = response.choices[0].message.content

            complaint_id = f"CMP{datetime.now().strftime('%H%M%S')}"

            status = "Pending"

            created_at = datetime.now().strftime(
                "%d-%b-%Y %I:%M %p"
            )

            save_issue(
                complaint_id,
                st.session_state.user_id,
                title,
                description,
                city,
                address,
                status,
                created_at,
                ai_response
            )

            st.success("AI Analysis Complete!")

            st.write("### AI Analysis")
            st.write(ai_response)

# ---------------- MY REPORTS ----------------

if page == "My Reports":

    st.header("📋 My Reports")
    total, pending, resolved = get_dashboard_stats(
        st.session_state.user_id
    )

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Total Complaints",
            total
        )

    with col2:
        st.metric(
            "Pending",
            pending
        )

    with col3:
        st.metric(
            "Resolved",
            resolved
        )

    st.divider()

    reports = get_user_issues(
        st.session_state.user_id
    )

    if not reports:

        st.info(
            "No reports submitted yet."
        )

    else:

        for report in reports:

            st.subheader(
                f"📌 {report[0]}"
            )

            st.write(
                f"Title: {report[1]}"
            )

            st.write(
                f"Description: {report[2]}"
            )

            st.write(
                f"City: {report[3]}"
            )

            st.write(
                f"Address: {report[4]}"
            )

            st.write(
                f"Status: {report[5]}"
            )

            st.write(
                f"Date: {report[6]}"
            )

            st.write("### AI Analysis")

            st.write(
                report[7]
            )

            st.divider()