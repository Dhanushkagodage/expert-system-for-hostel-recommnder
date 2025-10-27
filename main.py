"""
University Hostel Facility Recommendation System - Streamlit Interface with Prolog Backend
Requirements: pip install streamlit pyswip
"""

import streamlit as st
from pyswip import Prolog
import os

# Initialize Prolog
@st.cache_resource
def init_prolog():
    """Initialize Prolog engine and load knowledge base"""
    prolog = Prolog()
    
    # Load the knowledge base file
    kb_path = "knowledge_base.pl"
    
    if os.path.exists(kb_path):
        prolog.consult(kb_path)
        return prolog, True
    else:
        return prolog, False

# Query helper functions
def query_prolog(prolog, query_string):
    """Execute a Prolog query and return results"""
    try:
        results = list(prolog.query(query_string))
        return results
    except Exception as e:
        st.error(f"Query error: {str(e)}")
        return []

def get_districts(prolog):
    """Get list of all districts"""
    results = query_prolog(prolog, "district_category(District, _)")
    districts = sorted(list(set([r['District'] for r in results])))
    return districts

def get_hostel_recommendation(prolog, father_salary, mother_salary, distance, gender, gpa, 
                            mahapola_status, samurdhi_status, special_category, district, 
                            family_size, year):
    """Get hostel recommendation based on student information"""
    
    # First check for rejection cases
    reject_query = f"""reject_hostel({father_salary}, {mother_salary}, {distance}, {gender}, 
                      {gpa}, Rejection, Reasons)"""
    
    reject_results = query_prolog(prolog, reject_query)
    
    if reject_results:
        return reject_results[0]['Rejection'], reject_results[0]['Reasons']
    
    # If not rejected, get recommendation
    recommend_query = f"""recommend_hostel({father_salary}, {mother_salary}, {distance}, {gender}, 
                         {gpa}, {mahapola_status}, {samurdhi_status}, {special_category}, {district}, 
                         {family_size}, {year}, Recommendation, Reasons)"""
    
    recommend_results = query_prolog(prolog, recommend_query)
    
    if recommend_results:
        return recommend_results[0]['Recommendation'], recommend_results[0]['Reasons']
    else:
        return "EVALUATION NEEDED", "Unable to determine recommendation - please review manually"

def check_hostel_capacity(prolog, gender):
    """Check available hostel capacity"""
    hostel_type = "boys_hostel" if gender == "male" else "girls_hostel"
    query = f"hostel_capacity({hostel_type}, Total, Current)"
    results = query_prolog(prolog, query)
    
    if results:
        total = results[0]['Total']
        current = results[0]['Current']
        available = total - current
        return total, current, available
    return None, None, None

# Streamlit UI
def main():
    st.set_page_config(
        page_title="University Hostel Recommendation System",
        page_icon="🏠",
        layout="wide"
    )
    
    # Custom CSS
    st.markdown("""
    <style>
    .main-header {
        background: linear-gradient(90deg, #1f77b4, #ff7f0e);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
    }
    .recommendation-card {
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
        border-left: 5px solid;
    }
    .recommended {
        background-color: #d4edda;
        border-left-color: #28a745;
    }
    .not-recommended {
        background-color: #f8d7da;
        border-left-color: #dc3545;
    }
    .conditional {
        background-color: #fff3cd;
        border-left-color: #ffc107;
    }
    .info-box {
        background-color: #e9ecef;
        padding: 1rem;
        border-radius: 5px;
        margin: 1rem 0;
    }
    </style>
    """, unsafe_allow_html=True)
    
    st.markdown('<div class="main-header"><h1>🏠 University Hostel Facility Recommendation System</h1></div>', 
                unsafe_allow_html=True)
    
    # Initialize Prolog
    prolog, loaded = init_prolog()
    
    if not loaded:
        st.error("❌ Knowledge base file 'knowledge_base.pl' not found!")
        st.info("Please ensure the Prolog file is in the same directory as this script.")
        return
    
    st.success("✅ Knowledge base loaded successfully!")
    
    # Sidebar for system information
    with st.sidebar:
        st.header("📊 System Information")
        
        # Display hostel capacity
        st.subheader("Hostel Capacity")
        for gender in ["male", "female"]:
            total, current, available = check_hostel_capacity(prolog, gender)
            if total is not None:
                hostel_name = "Boys Hostel" if gender == "male" else "Girls Hostel"
                st.metric(
                    label=f"{hostel_name}",
                    value=f"{available} available",
                    delta=f"{current}/{total} occupied"
                )
        
        st.markdown("---")
        st.subheader("💡 Tips")
        st.info("""
        **Required for Recommendation:**
        - Minimum 2.5 GPA
        - Available hostel capacity
        - Complete information
        
        **Priority Factors:**
        - Family income level
        - Distance from university
        - Special circumstances
        - Scholarship availability
        """)
    
    # Main application form
    st.header("📝 Student Information Form")
    
    with st.form("student_info_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Personal Information")
            
            gender = st.selectbox(
                "Gender *",
                ["male", "female"],
                format_func=lambda x: x.title()
            )
            
            gpa = st.number_input(
                "Current GPA *",
                min_value=0.0,
                max_value=4.0,
                value=3.0,
                step=0.1,
                help="Minimum 2.5 GPA required"
            )
            
            year = st.selectbox(
                "Study Year *",
                [1, 2, 3, 4, 5],
                format_func=lambda x: f"Year {x}" if x <= 4 else "Postgraduate"
            )
            
            districts = get_districts(prolog)
            district = st.selectbox(
                "Home District *",
                districts,
        format_func=lambda x: x.title()
    )
    
            distance = st.number_input(
                "Distance from University (km) *",
                min_value=0,
                max_value=200,
                value=25,
                help="Distance from your home to the university"
            )
        
        with col2:
            st.subheader("Family Information")
            
            father_salary = st.number_input(
                "Father's Monthly Salary (LKR) *",
                min_value=0,
                max_value=500000,
                value=25000,
                step=1000
            )
            
            mother_salary = st.number_input(
                "Mother's Monthly Salary (LKR) *",
                min_value=0,
                max_value=500000,
                value=15000,
                step=1000
            )
            
            family_size = st.number_input(
                "Family Size *",
                min_value=1,
                max_value=15,
                value=4,
                help="Total number of family members including parents and siblings"
            )
            
            st.subheader("Scholarships & Special Circumstances")
            
            mahapola_status = st.selectbox(
                "Mahapola Scholarship",
                ["available", "not_available"],
                format_func=lambda x: "Available" if x == "available" else "Not Available"
            )
            
            samurdhi_status = st.selectbox(
                "Samurdhi Benefit",
                ["available", "not_available"],
                format_func=lambda x: "Available" if x == "available" else "Not Available"
            )
            
            special_category = st.selectbox(
                "Special Category",
                ["none", "disabled", "orphan", "single_parent", "chronic_illness", "financial_hardship"],
                format_func=lambda x: x.replace("_", " ").title() if x != "none" else "None"
            )
        
        # Submit button
        submitted = st.form_submit_button("🔍 Get Hostel Recommendation", type="primary")
    
    if submitted:
        # Validate inputs
        if gpa < 0 or father_salary < 0 or mother_salary < 0 or distance < 0:
            st.error("❌ Please enter valid positive values for all fields.")
            return
        
        # Show input summary
        st.header("📋 Application Summary")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown('<div class="info-box">', unsafe_allow_html=True)
            st.write("**Personal Details**")
            st.write(f"Gender: {gender.title()}")
            st.write(f"GPA: {gpa}")
            st.write(f"Study Year: {year}")
            st.write(f"District: {district.title()}")
            st.write(f"Distance: {distance} km")
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col2:
            st.markdown('<div class="info-box">', unsafe_allow_html=True)
            st.write("**Family Information**")
            st.write(f"Father's Salary: LKR {father_salary:,}")
            st.write(f"Mother's Salary: LKR {mother_salary:,}")
            total_income = father_salary + mother_salary
            st.write(f"**Total Income: LKR {total_income:,}**")
            st.write(f"Family Size: {family_size}")
            per_capita = total_income / family_size
            st.write(f"Per Capita Income: LKR {per_capita:,.0f}")
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col3:
            st.markdown('<div class="info-box">', unsafe_allow_html=True)
            st.write("**Support & Benefits**")
            st.write(f"Mahapola: {'✅ Available' if mahapola_status == 'available' else '❌ Not Available'}")
            st.write(f"Samurdhi: {'✅ Available' if samurdhi_status == 'available' else '❌ Not Available'}")
            if special_category != "none":
                st.write(f"Special Category: {special_category.replace('_', ' ').title()}")
            st.markdown('</div>', unsafe_allow_html=True)
        
        # Get recommendation
        st.header("🎯 Recommendation Result")
        
        with st.spinner("Analyzing your application..."):
            special_cat = special_category if special_category != "none" else "normal"
            recommendation, reasons = get_hostel_recommendation(
                prolog, father_salary, mother_salary, distance, gender, gpa,
                mahapola_status, samurdhi_status, special_cat, district, family_size, year
            )
        
        # Display recommendation with appropriate styling
        if "HIGHLY RECOMMENDED" in recommendation:
            st.markdown(f'<div class="recommendation-card recommended">', unsafe_allow_html=True)
            st.success(f"✅ {recommendation}")
        elif "RECOMMENDED" in recommendation and "NOT" not in recommendation:
            st.markdown(f'<div class="recommendation-card recommended">', unsafe_allow_html=True)
            st.success(f"✅ {recommendation}")
        elif "CONDITIONALLY" in recommendation:
            st.markdown(f'<div class="recommendation-card conditional">', unsafe_allow_html=True)
            st.warning(f"⚠️ {recommendation}")
        else:
            st.markdown(f'<div class="recommendation-card not-recommended">', unsafe_allow_html=True)
            st.error(f"❌ {recommendation}")
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Display reasons
        st.subheader("📝 Detailed Analysis")
        if reasons and reasons.strip():
            reason_list = [r.strip() for r in reasons.split(';') if r.strip()]
            for i, reason in enumerate(reason_list, 1):
                st.write(f"{i}. {reason}")
        else:
            st.write("No specific reasons provided.")
        
        # Additional recommendations
        st.subheader("💡 Additional Recommendations")
        
        if "NOT RECOMMENDED" in recommendation:
            st.info("""
            **Alternative Options:**
            - Consider private boarding houses near the university
            - Look into shared accommodation with other students
            - Explore transportation options if distance is the main issue
            - Improve academic performance if GPA is below requirements
            """)
        elif "LOW PRIORITY" in recommendation:
            st.info("""
            **Suggestions:**
            - Apply early as spaces may become available
            - Consider alternative accommodation options
            - Monitor for cancellations or additional capacity
            """)
        else:
            st.info("""
            **Next Steps:**
            - Submit your hostel application as soon as possible
            - Prepare required documentation
            - Contact the accommodation office for application procedures
            - Keep track of application status
            """)

if __name__ == "__main__":
    main()