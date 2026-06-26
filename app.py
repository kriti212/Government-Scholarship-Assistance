import streamlit as st

# Configure the page layout and title
st.set_page_config(
    page_title="Scholarship Eligibility Portal",
    page_icon="🎓",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Custom premium CSS styling for modern aesthetics
st.markdown(
    """
    <style>
        /* Import Outfit or Inter font */
        @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;700&display=swap');
        
        /* Apply font to elements */
        html, body, [class*="css"], .stText, .stMarkdown, .stButton {
            font-family: 'Outfit', sans-serif;
        }
        
        /* Main background and container styling */
        .main {
            background: linear-gradient(135deg, #0f172a 0%, #1e1b4b 100%);
            color: #f8fafc;
        }
        
        /* Form Card Layout styling */
        .form-card {
            background: rgba(30, 41, 59, 0.7);
            padding: 2.5rem;
            border-radius: 16px;
            border: 1px solid rgba(255, 255, 255, 0.1);
            backdrop-filter: blur(12px);
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
            margin-bottom: 2rem;
        }
        
        /* Gradient Header Text */
        .gradient-header {
            background: linear-gradient(90deg, #6366f1, #a855f7, #ec4899);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            font-weight: 700;
            font-size: 2.5rem;
            text-align: center;
            margin-bottom: 0.5rem;
        }
        
        .subheader {
            color: #94a3b8;
            font-size: 1.1rem;
            text-align: center;
            margin-bottom: 2rem;
        }

        /* Section Headings */
        .section-title {
            color: #c084fc;
            font-size: 1.25rem;
            font-weight: 600;
            margin-top: 1.5rem;
            margin-bottom: 0.75rem;
            border-bottom: 2px solid rgba(192, 132, 252, 0.2);
            padding-bottom: 0.25rem;
        }

        /* Customize Streamlit Input styles */
        div[data-baseweb="input"] {
            background-color: rgba(15, 23, 42, 0.6) !important;
            border: 1px solid rgba(255, 255, 255, 0.15) !important;
            border-radius: 8px !important;
        }
        div[data-baseweb="select"] {
            background-color: rgba(15, 23, 42, 0.6) !important;
            border: 1px solid rgba(255, 255, 255, 0.15) !important;
            border-radius: 8px !important;
        }
        
        /* Premium Submit Button styling */
        .stButton>button {
            background: linear-gradient(90deg, #6366f1, #a855f7) !important;
            color: white !important;
            font-weight: 600 !important;
            border: none !important;
            padding: 0.75rem 2.5rem !important;
            border-radius: 9999px !important;
            box-shadow: 0 4px 14px 0 rgba(99, 102, 241, 0.4) !important;
            transition: all 0.3s ease !important;
            width: 100% !important;
        }
        .stButton>button:hover {
            transform: translateY(-2px) !important;
            box-shadow: 0 6px 20px 0 rgba(168, 85, 247, 0.6) !important;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# Header Section
st.markdown('<div class="gradient-header">Candidate Registration Portal</div>', unsafe_allow_html=True)
st.markdown('<div class="subheader">Complete your profile details to discover eligible government scholarships</div>', unsafe_allow_html=True)

# Form container
with st.container():
    st.markdown('<div class="form-card">', unsafe_allow_html=True)
    
    with st.form("candidate_form", clear_on_submit=False):
        
        # Section 1: Personal Details
        st.markdown('<div class="section-title">👤 Personal Information</div>', unsafe_allow_html=True)
        col1, col2 = st.columns([2, 1])
        
        with col1:
            full_name = st.text_input("Full Name", placeholder="e.g. Rahul Sharma")
        with col2:
            age = st.number_input("Age", min_value=5, max_value=100, value=18, step=1)
            
        col3, col4 = st.columns(2)
        with col3:
            gender = st.selectbox(
                "Gender",
                options=["Select Gender", "Male", "Female", "Other", "Prefer not to say"]
            )
        with col4:
            caste = st.selectbox(
                "Category / Caste Group",
                options=["Select Category", "General", "OBC", "SC", "ST", "EWS"]
            )

        # Section 2: Academic & Financial Details
        st.markdown('<div class="section-title">📚 Academic & Financial Details</div>', unsafe_allow_html=True)
        
        col5, col6 = st.columns(2)
        with col5:
            education_level = st.selectbox(
                "Current Educational Level",
                options=[
                    "Select Education Level",
                    "Secondary School (Class 10)",
                    "Higher Secondary (Class 12)",
                    "Undergraduate Degree (UG)",
                    "Postgraduate Degree (PG)",
                    "Ph.D. / Research Fellowship",
                    "Diploma / Vocational Training"
                ]
            )
        with col6:
            income_range = st.selectbox(
                "Annual Family Income Range",
                options=[
                    "Select Income Range",
                    "Less than ₹1,00,000",
                    "₹1,00,000 - ₹2,50,000",
                    "₹2,50,000 - ₹5,00,000",
                    "₹5,00,000 - ₹8,00,000",
                    "More than ₹8,00,000"
                ]
            )

        # Section 3: Special Eligibility (Disability Status)
        st.markdown('<div class="section-title">♿ Special Eligibility</div>', unsafe_allow_html=True)
        
        is_disabled = st.radio(
            "Do you have a physical disability (Person with Disability - PwD)?",
            options=["No", "Yes"],
            horizontal=True
        )
        
        # Dynamic input based on disability option selection
        disability_details = ""
        if is_disabled == "Yes":
            col7, col8 = st.columns([2, 1])
            with col7:
                disability_type = st.selectbox(
                    "Type of Disability",
                    options=[
                        "Select Type",
                        "Locomotor Disability",
                        "Visual Impairment",
                        "Hearing Impairment",
                        "Speech and Language Disability",
                        "Intellectual Disability / Autism",
                        "Multiple Disabilities"
                    ]
                )
            with col8:
                disability_percentage = st.number_input(
                    "Disability Percentage (%)",
                    min_value=40,
                    max_value=100,
                    value=40,
                    step=5,
                    help="Normally, minimum 40% disability is required for PwD scholarships."
                )
                disability_details = f"{disability_type} ({disability_percentage}%)"

        # Spacer and Submit Button
        st.markdown("<br>", unsafe_allow_html=True)
        submit_btn = st.form_submit_button("Check Eligible Scholarships")

    st.markdown('</div>', unsafe_allow_html=True)

# Handle Form Submission
if submit_btn:
    # Basic Form Validation
    errors = []
    if not full_name.strip():
        errors.append("Please enter your Full Name.")
    if gender == "Select Gender":
        errors.append("Please select your Gender.")
    if caste == "Select Category":
        errors.append("Please select your Caste/Category.")
    if education_level == "Select Education Level":
        errors.append("Please select your current Educational Level.")
    if income_range == "Select Income Range":
        errors.append("Please select your Annual Family Income Range.")
    if is_disabled == "Yes" and disability_type == "Select Type":
        errors.append("Please specify your Type of Disability.")

    if errors:
        for error in errors:
            st.error(error)
    else:
        st.balloons()
        st.success("🎉 Profile registered successfully! Connecting with backend API...")
        
        # Display submitted data overview (simulated response)
        st.markdown("### Profile Summary")
        summary_cols = st.columns(2)
        with summary_cols[0]:
            st.write(f"**Name:** {full_name}")
            st.write(f"**Age / Gender:** {age} / {gender}")
            st.write(f"**Category:** {caste}")
        with summary_cols[1]:
            st.write(f"**Education Level:** {education_level}")
            st.write(f"**Annual Income:** {income_range}")
            st.write(f"**PwD Status:** {'Yes - ' + disability_details if is_disabled == 'Yes' else 'No'}")
