"""
Expert System for University Hostel Allocation - Streamlit Interface with Prolog Backend
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
    
    kb_path = "knowledge_base.pl"
    
    if os.path.exists(kb_path):
        prolog.consult(kb_path)
        return prolog, True
    else:
        return prolog, False

def query_prolog(prolog, query_string):
    """Execute a Prolog query and return results"""
    try:
        results = list(prolog.query(query_string))
        return results
    except Exception as e:
        st.error(f"Query error: {str(e)}")
        return []

def evaluate_student(prolog, distance, father_salary, mother_salary, mahapola, 
                     samurdhi, siblings, special_case, year):
    """Evaluate student eligibility for hostel"""
    query = f"""evaluate_hostel_eligibility({distance}, {father_salary}, {mother_salary}, 
            {mahapola}, {samurdhi}, {siblings}, {special_case}, {year},
            Status, Priority, Score, Reasons)"""
    
    results = query_prolog(prolog, query)
    return results[0] if results else None

def get_priority_color(priority):
    """Return color based on priority level"""
    if priority == 'high':
        return '#28a745'  # Green
    elif priority == 'medium':
        return '#ffc107'  # Yellow
    elif priority == 'low':
        return '#17a2b8'  # Blue
    else:
        return '#dc3545'  # Red

def main():
    st.set_page_config(
        page_title="Hostel Facility Recommender",
        page_icon="🏠",
        layout="wide"
    )
    
    # Custom CSS
    st.markdown("""
        <style>
        .main-header {
            font-size: 2.5rem;
            font-weight: bold;
            text-align: center;
            padding: 1rem;
            background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
            color: white !important;
            border-radius: 10px;
            margin-bottom: 2rem;
        }
        .sub-header {
            font-size: 1.5rem;
            font-weight: bold;
            color: inherit;
            margin-top: 1.5rem;
            margin-bottom: 1rem;
        }
        .info-box {
            background: rgba(33, 150, 243, 0.1);
            padding: 1.5rem;
            border-radius: 12px;
            border-left: 5px solid #2196f3;
            border: 1px solid rgba(33, 150, 243, 0.2);
            margin-bottom: 1rem;
            color: inherit;
        }
        .success-box {
            background: rgba(76, 175, 80, 0.1);
            padding: 1.5rem;
            border-radius: 12px;
            border-left: 5px solid #4caf50;
            border: 1px solid rgba(76, 175, 80, 0.2);
            margin-bottom: 1rem;
            color: inherit;
        }
        .warning-box {
            background: rgba(255, 152, 0, 0.1);
            padding: 1.5rem;
            border-radius: 12px;
            border-left: 5px solid #ff9800;
            border: 1px solid rgba(255, 152, 0, 0.2);
            margin-bottom: 1rem;
            color: inherit;
        }
        .danger-box {
            background: rgba(244, 67, 54, 0.1);
            padding: 1.5rem;
            border-radius: 12px;
            border-left: 5px solid #f44336;
            border: 1px solid rgba(244, 67, 54, 0.2);
            margin-bottom: 1rem;
            color: inherit;
        }
        .metric-card {
            background: rgba(255, 255, 255, 0.05);
            padding: 1.2rem;
            border-radius: 12px;
            border: 1px solid rgba(255, 255, 255, 0.1);
            text-align: center;
            backdrop-filter: blur(10px);
            color: inherit;
        }
        .stButton>button {
            width: 100%;
            background-color: #28a745;
            color: white;
            font-weight: bold;
            padding: 0.75rem;
            border-radius: 8px;
            border: none;
            font-size: 1.1rem;
        }
        .stButton>button:hover {
            background-color: #218838;
        }
        /* Dark mode improvements */
        .info-box h3, .info-box h4, .info-box p,
        .success-box h3, .success-box h4, .success-box p,
        .warning-box h3, .warning-box h4, .warning-box p,
        .danger-box h3, .danger-box h4, .danger-box p {
            color: inherit !important;
        }
        .metric-card h3, .metric-card p {
            color: inherit !important;
        }
        </style>
    """, unsafe_allow_html=True)
    
    st.markdown('<div class="main-header">🏠 Expert System for University Hostel Allocation</div>', 
                unsafe_allow_html=True)
    
    # Initialize Prolog
    prolog, loaded = init_prolog()
    
    if not loaded:
        st.error("❌ Knowledge base file 'knowledge_base.pl' not found!")
        st.info("Please ensure the Prolog file is in the same directory as this script.")
        return
    
    
    # Main content
    st.markdown('<div class="sub-header">📝 Student Information Form</div>', 
                unsafe_allow_html=True)
    
    with st.form("student_form"):
        # Personal Information
        st.markdown("#### 👤 Personal Details")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            student_name = st.text_input("Student Name *", placeholder="Enter full name")
        
        with col2:
            year = st.selectbox(
                "Academic Year *",
                ["-- Select --", "first_year", "second_year", "third_year", "fourth_year", "postgraduate"],
                format_func=lambda x: "Select Academic Year" if x == "-- Select --" else x.replace('_', ' ').title(),
                index=0
            )
        
        with col3:
            faculty = st.selectbox(
                "Faculty *",
                ["-- Select --", "Engineering", "Science", "Medicine", "Arts", "Management", "Law"],
                format_func=lambda x: "Select Faculty" if x == "-- Select --" else x,
                index=0
            )
        
        st.markdown("---")
        
        # Location and Distance
        st.markdown("#### 📍 Location Information")
        col1, col2 = st.columns(2)
        
        with col1:
            home_district = st.selectbox(
                "Home District",
                ["-- Select --", "Colombo", "Gampaha", "Kalutara", "Kandy", "Matale", "Nuwara Eliya",
                 "Galle", "Matara", "Hambantota", "Jaffna", "Kilinochchi", "Mannar",
                 "Vavuniya", "Mullaitivu", "Batticaloa", "Ampara", "Trincomalee",
                 "Kurunegala", "Puttalam", "Anuradhapura", "Polonnaruwa", "Badulla",
                 "Monaragala", "Ratnapura", "Kegalle"],
                format_func=lambda x: "Select District" if x == "-- Select --" else x,
                index=0
            )
        
        with col2:
            distance_range = st.selectbox(
                "Distance from University (km) *",
                ["-- Select --", "0-50", "50-100", "100-150", "150-200", "above 200"],
                format_func=lambda x: "Select Distance Range" if x == "-- Select --" else x,
                help="Select the distance range from your home to the university",
                index=0
            )
        
        st.markdown("---")
        
        # Financial Information
        st.markdown("#### 💰 Financial Information *")
        st.info("ℹ️ At least one parent's income must be greater than 0")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            father_salary = st.number_input(
                "Father's Monthly Income (LKR)",
                min_value=0,
                max_value=1000000,
                value=0,
                step=5000,
                help="Enter father's monthly income. At least one parent's income is required."
            )
        
        with col2:
            mother_salary = st.number_input(
                "Mother's Monthly Income (LKR)",
                min_value=0,
                max_value=1000000,
                value=0,
                step=5000,
                help="Enter mother's monthly income. At least one parent's income is required."
            )
        
        with col3:
            total_income = father_salary + mother_salary
            st.metric("Total Family Income", f"LKR {total_income:,}")
            if total_income > 0:
                st.caption("✅ Valid")
        
        st.markdown("---")
        
        # Government Support
        st.markdown("#### 🎓 Government Support Schemes *")
        col1, col2 = st.columns(2)
        
        with col1:
            mahapola = st.selectbox(
                "Mahapola Scholarship *",
                ["-- Select --", "none", "mahapola"],
                format_func=lambda x: "Select Option" if x == "-- Select --" else ("Yes" if x == "mahapola" else "No"),
                index=0
            )
        
        with col2:
            samurdhi = st.selectbox(
                "Samurdhi Recipient *",
                ["-- Select --", "none", "samurdhi"],
                format_func=lambda x: "Select Option" if x == "-- Select --" else ("Yes" if x == "samurdhi" else "No"),
                index=0
            )
        
        st.markdown("---")
        
        # Family Information
        st.markdown("#### 👨‍👩‍👧‍👦 Family Information (Optional)")
        col1, col2 = st.columns(2)
        
        with col1:
            siblings = st.number_input(
                "Siblings in University",
                min_value=0,
                max_value=10,
                value=0,
                step=1,
                help="Number of siblings currently studying in university"
            )
        
        with col2:
            special_case = st.selectbox(
                "Special Circumstances",
                ["-- Select --", "none", "orphan", "single_parent", "disabled_parent", 
                 "chronic_illness_family", "natural_disaster_affected"],
                format_func=lambda x: "Select if applicable" if x == "-- Select --" else x.replace('_', ' ').title(),
                index=0
            )
        
        st.markdown("---")
        
        # Submit button
        submitted = st.form_submit_button("🔍 Evaluate Eligibility", use_container_width=True)
    
    # Process form submission
    if submitted:
        # Validate all required fields
        validation_errors = []
        
        if not student_name or student_name.strip() == "":
            validation_errors.append("Student Name")
        if year == "-- Select --":
            validation_errors.append("Academic Year")
        if faculty == "-- Select --":
            validation_errors.append("Faculty")
        if distance_range == "-- Select --":
            validation_errors.append("Distance from University")
        if mahapola == "-- Select --":
            validation_errors.append("Mahapola Scholarship")
        if samurdhi == "-- Select --":
            validation_errors.append("Samurdhi Recipient")
        
        # Validate financial information - at least one parent must have income
        if father_salary == 0 and mother_salary == 0:
            validation_errors.append("Financial Information: At least one parent must have income greater than 0")
        
        if validation_errors:
            st.error(f"⚠️ Please fill in all required fields: {', '.join(validation_errors)}")
        else:
            # Handle optional fields
            if special_case == "-- Select --":
                special_case = "none"
            if home_district == "-- Select --":
                home_district = "Not Specified"
            
            # Convert distance range to numeric value for processing
            distance_map = {
                "0-50": 25,
                "50-100": 75,
                "100-150": 125,
                "150-200": 175,
                "above 200": 225
            }
            distance = distance_map[distance_range]
            
            with st.spinner("Evaluating your eligibility..."):
                result = evaluate_student(
                    prolog, distance, father_salary, mother_salary,
                    mahapola, samurdhi, siblings, special_case, year
                )
                
                if result:
                    status = result['Status']
                    priority = result['Priority']
                    score = result['Score']
                    
                    st.markdown("---")
                    st.markdown('<div class="sub-header">📊 Evaluation Results</div>', 
                               unsafe_allow_html=True)
                    
                    # Results summary
                    col1, col2, col3, col4 = st.columns(4)
                    
                    with col1:
                        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
                        st.markdown("**Student Name**")
                        st.markdown(f"<h3>{student_name}</h3>", unsafe_allow_html=True)
                        st.markdown('</div>', unsafe_allow_html=True)
                    
                    with col2:
                        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
                        st.markdown("**Distance Range**")
                        st.markdown(f"<h3>{distance_range} km</h3>", unsafe_allow_html=True)
                        st.markdown('</div>', unsafe_allow_html=True)
                    
                    with col3:
                        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
                        st.markdown("**Eligibility Score**")
                        st.markdown(f"<h3 style='color: {get_priority_color(priority)}'>{score}</h3>", 
                                  unsafe_allow_html=True)
                        st.markdown('</div>', unsafe_allow_html=True)
                    
                    with col4:
                        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
                        st.markdown("**Priority Level**")
                        st.markdown(f"<h3 style='color: {get_priority_color(priority)}'>{priority.upper()}</h3>", 
                                  unsafe_allow_html=True)
                        st.markdown('</div>', unsafe_allow_html=True)
                    
                    st.markdown("<br>", unsafe_allow_html=True)
                    
                    # Eligibility status
                    if status == 'eligible':
                        if priority == 'high':
                            st.markdown("""
                            <div class="success-box">
                                <h3>✅ ELIGIBLE FOR HOSTEL FACILITY</h3>
                                <p style='font-size: 1.1rem;'><strong>Priority: HIGH</strong></p>
                                <p>Congratulations! You qualify for hostel accommodation with high priority. 
                                Please proceed with the application process at the Student Affairs Office.</p>
                            </div>
                            """, unsafe_allow_html=True)
                        elif priority == 'medium':
                            st.markdown("""
                            <div class="success-box">
                                <h3>✅ ELIGIBLE FOR HOSTEL FACILITY</h3>
                                <p style='font-size: 1.1rem;'><strong>Priority: MEDIUM</strong></p>
                                <p>You qualify for hostel accommodation with medium priority. 
                                Subject to availability, please apply at the Student Affairs Office.</p>
                            </div>
                            """, unsafe_allow_html=True)
                        else:
                            st.markdown("""
                            <div class="warning-box">
                                <h3>✅ ELIGIBLE FOR HOSTEL FACILITY</h3>
                                <p style='font-size: 1.1rem;'><strong>Priority: LOW</strong></p>
                                <p>You meet the minimum eligibility criteria for hostel accommodation. 
                                Allocation will be subject to availability after high and medium priority students.</p>
                            </div>
                            """, unsafe_allow_html=True)
                    else:
                        st.markdown("""
                        <div class="danger-box">
                            <h3>❌ NOT ELIGIBLE FOR HOSTEL FACILITY</h3>
                            <p style='font-size: 1.1rem;'><strong>Score below minimum threshold</strong></p>
                            <p>Based on the evaluation criteria, you do not currently meet the eligibility 
                            requirements for hostel accommodation. You may appeal or reapply if your 
                            circumstances change.</p>
                        </div>
                        """, unsafe_allow_html=True)
                    
                    # Detailed breakdown
                    st.markdown("<br>", unsafe_allow_html=True)
                    st.markdown("### 📈 Score Breakdown")
                    
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.markdown("#### Evaluation Factors")
                        
                        # Distance evaluation
                        if distance > 150:
                            dist_score, dist_msg = 30, "Very Far (30 points)"
                        elif distance > 75:
                            dist_score, dist_msg = 25, "Far (25 points)"
                        elif distance > 25:
                            dist_score, dist_msg = 15, "Moderate (15 points)"
                        elif distance > 10:
                            dist_score, dist_msg = 5, "Near (5 points)"
                        else:
                            dist_score, dist_msg = 0, "Very Near (0 points)"
                        
                        st.markdown(f"**Distance ({distance_range} km):** {dist_msg}")
                        st.progress(dist_score / 30)
                        
                        # Income evaluation
                        if total_income < 25000:
                            inc_score, inc_msg = 25, "Very Low Income (25 points)"
                        elif total_income < 50000:
                            inc_score, inc_msg = 20, "Low Income (20 points)"
                        elif total_income < 100000:
                            inc_score, inc_msg = 10, "Middle Income (10 points)"
                        elif total_income < 200000:
                            inc_score, inc_msg = 5, "High Income (5 points)"
                        else:
                            inc_score, inc_msg = 0, "Very High Income (0 points)"
                        
                        st.markdown(f"**Family Income (LKR {total_income:,}):** {inc_msg}")
                        st.progress(inc_score / 25)
                        
                        # Financial support
                        if mahapola == 'mahapola' and samurdhi == 'samurdhi':
                            sup_score, sup_msg = 15, "Both (15 points)"
                        elif mahapola == 'mahapola':
                            sup_score, sup_msg = 10, "Mahapola (10 points)"
                        elif samurdhi == 'samurdhi':
                            sup_score, sup_msg = 10, "Samurdhi (10 points)"
                        else:
                            sup_score, sup_msg = 0, "None (0 points)"
                        
                        st.markdown(f"**Government Support:** {sup_msg}")
                        st.progress(sup_score / 15)
                    
                    with col2:
                        # Siblings
                        if siblings >= 3:
                            sib_score, sib_msg = 10, "3+ Siblings (10 points)"
                        elif siblings == 2:
                            sib_score, sib_msg = 7, "2 Siblings (7 points)"
                        elif siblings == 1:
                            sib_score, sib_msg = 4, "1 Sibling (4 points)"
                        else:
                            sib_score, sib_msg = 0, "No Siblings (0 points)"
                        
                        st.markdown(f"**Siblings in University:** {sib_msg}")
                        st.progress(sib_score / 10)
                        
                        # Special circumstances
                        if special_case == 'orphan':
                            spec_score, spec_msg = 20, "Orphan (20 points)"
                        elif special_case == 'single_parent':
                            spec_score, spec_msg = 15, "Single Parent (15 points)"
                        elif special_case == 'disabled_parent':
                            spec_score, spec_msg = 15, "Disabled Parent (15 points)"
                        elif special_case == 'chronic_illness_family':
                            spec_score, spec_msg = 12, "Chronic Illness (12 points)"
                        elif special_case == 'natural_disaster_affected':
                            spec_score, spec_msg = 12, "Disaster Affected (12 points)"
                        else:
                            spec_score, spec_msg = 0, "None (0 points)"
                        
                        st.markdown(f"**Special Circumstances:** {spec_msg}")
                        st.progress(spec_score / 20)
                    
                    # Reasons for decision
                    st.markdown("<br>", unsafe_allow_html=True)
                    st.markdown("### 📋 Reasons for Decision")
                    
                    reasons_list = []
                    
                    # Generate reasons based on criteria
                    if distance > 150 and total_income < 50000:
                        reasons_list.append("✓ Very far distance from university combined with low family income")
                    
                    if (distance > 75) and (mahapola == 'mahapola' or samurdhi == 'samurdhi'):
                        reasons_list.append("✓ Long distance from university with government financial support")
                    
                    if special_case != 'none':
                        reasons_list.append(f"✓ Special circumstance: {special_case.replace('_', ' ').title()}")
                    
                    if distance > 25 and total_income < 50000:
                        reasons_list.append("✓ Moderate to long distance with low family income")
                    
                    if siblings >= 2 and total_income < 100000:
                        reasons_list.append("✓ Multiple siblings in university creating financial burden")
                    
                    if year == 'first_year' and distance > 75:
                        reasons_list.append("✓ First year student from far distance")
                    
                    if distance <= 10 and total_income >= 200000:
                        reasons_list.append("✗ Close proximity to university with high family income")
                    
                    if distance <= 25 and total_income >= 100000 and special_case == 'none':
                        reasons_list.append("✗ Relatively near to university with adequate family income")
                    
                    if status == 'not_eligible':
                        reasons_list.append("✗ Overall score below minimum eligibility threshold (40 points)")
                    
                    if reasons_list:
                        for reason in reasons_list:
                            if reason.startswith("✓"):
                                st.markdown(f'<div class="info-box">{reason}</div>', unsafe_allow_html=True)
                            else:
                                st.markdown(f'<div class="warning-box">{reason}</div>', unsafe_allow_html=True)
                    else:
                        st.info("Standard evaluation completed based on all criteria.")
                    
                    # Download report button
                    st.markdown("<br>", unsafe_allow_html=True)
                    report_text = f"""
UNIVERSITY HOSTEL FACILITY EVALUATION REPORT
{"="*50}

STUDENT INFORMATION:
Name: {student_name}
Faculty: {faculty}
Academic Year: {year.replace('_', ' ').title()}

LOCATION & FAMILY DETAILS:
Home District: {home_district}
Distance from University: {distance_range} km
Father's Monthly Income: LKR {father_salary:,}
Mother's Monthly Income: LKR {mother_salary:,}
Total Family Income: LKR {total_income:,}

SUPPORT & CIRCUMSTANCES:
Mahapola Scholarship: {'Yes' if mahapola == 'mahapola' else 'No'}
Samurdhi Recipient: {'Yes' if samurdhi == 'samurdhi' else 'No'}
Siblings in University: {siblings}
Special Circumstances: {special_case.replace('_', ' ').title()}

EVALUATION RESULTS:
{"="*50}
Eligibility Status: {status.upper()}
Priority Level: {priority.upper()}
Total Score: {score} / 105

SCORE BREAKDOWN:
- Distance: {dist_score} / 30 points
- Family Income: {inc_score} / 25 points
- Government Support: {sup_score} / 15 points
- Siblings: {sib_score} / 10 points
- Special Circumstances: {spec_score} / 20 points

DECISION FACTORS:
{chr(10).join('- ' + r for r in reasons_list) if reasons_list else '- Standard evaluation completed'}

RECOMMENDATION:
{f'Student is ELIGIBLE for hostel facility with {priority.upper()} priority.' if status == 'eligible' else 'Student does not meet current eligibility criteria.'}

Date Generated: {st.session_state.get('timestamp', 'N/A')}
{"="*50}
This is a computer-generated report.
For queries, contact: hostel@university.lk
                    """
                    
                    st.download_button(
                        label="📄 Download Evaluation Report",
                        data=report_text,
                        file_name=f"hostel_evaluation_{student_name.replace(' ', '_')}.txt",
                        mime="text/plain",
                        use_container_width=True
                    )
                    
                else:
                    st.error("❌ Error evaluating eligibility. Please check your inputs and try again.")
    
    # Footer
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown("---")
    st.markdown("""
        <div style='text-align: center; color: #7f8c8d; padding: 1rem;'>
            <p><strong>Expert System for University Hostel Allocation</strong></p>
        </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    # Set timestamp in session state
    import datetime
    if 'timestamp' not in st.session_state:
        st.session_state.timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    main()