# University Hostel Facility Recommendation System

## Overview
This is an expert system for recommending hostel facility accommodation for university students based on various factors including family income, distance from university, scholarships, and special circumstances.

## Features
- **Comprehensive Evaluation**: Considers 20+ rules for recommendation
- **Multiple Factors**: Distance, family income (father's & mother's salary), scholarships (Mahapola, Samurdhi), special categories
- **Smart Prioritization**: Emergency, high, medium, and low priority categories
- **User-Friendly Interface**: Streamlit-based web interface
- **Real-time Analysis**: Instant recommendations with detailed reasoning
- **Capacity Management**: Shows current hostel availability

## System Components
1. **knowledge_base.pl**: Prolog knowledge base with facts and 22 inference rules
2. **main.py**: Streamlit web application interface
3. **Expert System Logic**: 20+ rules covering various scenarios

## Prerequisites
- Python 3.7+
- SWI-Prolog installed on your system
- Required Python packages (see Installation)

## Installation

### 1. Install SWI-Prolog
- **Windows**: Download from https://www.swi-prolog.org/download/stable
- **macOS**: `brew install swi-prolog`
- **Ubuntu/Debian**: `sudo apt-get install swi-prolog`

### 2. Install Python Dependencies
```bash
pip install streamlit pyswip
```

### 3. Clone/Download the Project
Ensure you have these files in the same directory:
- `knowledge_base.pl`
- `main.py`
- `README.md`

## Usage

### Running the Application
```bash
streamlit run main.py
```

The application will open in your default web browser at `http://localhost:8501`

### Input Parameters
The system requires the following information:

#### Personal Information
- **Gender**: Male/Female (affects hostel assignment)
- **Current GPA**: Minimum 2.5 required
- **Study Year**: 1-4 (undergraduate) or 5 (postgraduate)
- **Home District**: Select from Sri Lankan districts
- **Distance**: Distance from home to university (km)

#### Family Information
- **Father's Monthly Salary**: In LKR
- **Mother's Monthly Salary**: In LKR
- **Family Size**: Total family members

#### Support & Benefits
- **Mahapola Scholarship**: Available/Not Available
- **Samurdhi Benefit**: Available/Not Available
- **Special Category**: Disabled, Orphan, Single Parent, Chronic Illness, Financial Hardship, or None

## Recommendation Categories

### 1. HIGHLY RECOMMENDED - Emergency Priority
- Students with severe financial hardship
- Special circumstances (disabled, orphan, single parent)
- Long distance with very low income

### 2. RECOMMENDED - High Priority
- Low family income with moderate to long distance
- Rural students with financial constraints
- First-year students with qualifying factors

### 3. CONDITIONALLY RECOMMENDED - Medium Priority
- Moderate income levels
- Some supporting factors present
- Available hostel capacity permitting

### 4. LOW PRIORITY
- High family income
- Short distance from university
- Minimal financial need

### 5. NOT RECOMMENDED
- Below minimum GPA (2.5)
- No available hostel capacity
- High income with short distance

## Expert System Rules (20+ Rules)

The system implements over 20 rules including:

1. **Income-based qualification**
2. **Distance-based need assessment**
3. **Scholarship advantage evaluation**
4. **Special category priority**
5. **Combined priority calculation**
6. **Hostel availability check**
7. **Academic eligibility verification**
8. **Rural student preference**
9. **Large family consideration**
10. **First-year student priority**
11. **Financial hardship assessment**
12. **Transportation difficulty evaluation**
13. **Single parent support**
14. **Unemployment hardship**
15. **Merit-based consideration**
16. **Gender-specific hostel matching**
17. **Medical accommodation needs**
18. **Development level consideration**
19. **Age-based priority**
20. **Combined scholarship assessment**
21. **Final recommendation logic**
22. **Rejection criteria**

## Example Usage Scenarios

### Scenario 1: High Priority Student
- Father's Salary: LKR 15,000
- Mother's Salary: LKR 8,000
- Distance: 45 km
- GPA: 3.2
- Mahapola: Available
- Special Category: Orphan
- **Result**: HIGHLY RECOMMENDED - Emergency Priority

### Scenario 2: Low Priority Student
- Father's Salary: LKR 80,000
- Mother's Salary: LKR 60,000
- Distance: 10 km
- GPA: 3.5
- **Result**: LOW PRIORITY - Consider alternatives

### Scenario 3: Rejected Application
- GPA: 2.0 (below minimum)
- **Result**: NOT RECOMMENDED - Academic performance below minimum requirement

## File Structure
```
project/
├── knowledge_base.pl      # Prolog knowledge base with facts and rules
├── main.py               # Streamlit web application
└── README.md            # This documentation file
```

## Technical Details

### Knowledge Base Structure
- **Facts**: District categories, income thresholds, hostel capacity, special categories
- **Rules**: 22 inference rules for comprehensive evaluation
- **Predicates**: Helper functions for calculations and validations

### Web Interface Features
- Responsive design with custom CSS
- Form validation
- Real-time capacity display
- Detailed recommendation explanations
- Application summary
- Alternative suggestions

## Troubleshooting

### Common Issues
1. **"Knowledge base file not found"**: Ensure `knowledge_base.pl` is in the same directory as `main.py`
2. **PySwip import error**: Make sure SWI-Prolog is properly installed and in PATH
3. **Prolog query errors**: Check that all input values are valid numbers

### Dependencies
```bash
pip install streamlit==1.28.0
pip install pyswip==0.2.11
```

## Contributing
This system can be extended by:
- Adding more rules to the knowledge base
- Including additional student factors
- Enhancing the user interface
- Adding database integration
- Implementing user authentication

## Assignment Requirements Met
✅ Knowledge Base Development (20 Marks)
- Comprehensive Prolog knowledge base
- 20+ inference rules implemented
- Covers all required input parameters

✅ Expert System Application (20 Marks)
- Functional Streamlit web interface
- Integration with Prolog backend
- User-friendly recommendation system
- Complete with reasoning explanations

## Demo
Run the system and test with different input combinations to see how the expert system evaluates various student scenarios for hostel facility recommendations.
