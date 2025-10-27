% ============================================
% UNIVERSITY HOSTEL FACILITY RECOMMENDATION SYSTEM
% ============================================

% --- Student Financial Information ---
% family_income(father_salary, mother_salary, total_family_income)
family_income_threshold(very_low, 0, 30000).
family_income_threshold(low, 30001, 50000).
family_income_threshold(middle, 50001, 80000).
family_income_threshold(high, 80001, 120000).
family_income_threshold(very_high, 120001, 500000).

% --- Distance from University (in kilometers) ---
distance_category(very_near, 0, 5).
distance_category(near, 6, 15).
distance_category(moderate, 16, 30).
distance_category(far, 31, 50).
distance_category(very_far, 51, 100).

% --- Scholarship Information ---
scholarship_type(mahapola, available).
scholarship_type(mahapola, not_available).
scholarship_type(samurdhi, available).
scholarship_type(samurdhi, not_available).
scholarship_type(merit_based, available).
scholarship_type(merit_based, not_available).

% --- Academic Performance Categories ---
academic_performance(excellent, 85, 100).
academic_performance(good, 70, 84).
academic_performance(average, 55, 69).
academic_performance(poor, 0, 54).

% --- Priority Levels ---
priority_level(emergency, 1).
priority_level(high, 2).
priority_level(medium, 3).
priority_level(low, 4).
priority_level(very_low, 5).

% --- Hostel Capacity Information ---
hostel_capacity(boys_hostel, 200, 180).  % (hostel_name, total_capacity, current_occupancy)
hostel_capacity(girls_hostel, 150, 135).
hostel_capacity(mixed_hostel, 100, 85).

% --- Special Categories ---
special_category(disabled).
special_category(orphan).
special_category(single_parent).
special_category(chronic_illness).
special_category(financial_hardship).

% --- District Information ---
district_category(colombo, urban).
district_category(gampaha, urban).
district_category(kalutara, urban).
district_category(kandy, semi_urban).
district_category(galle, semi_urban).
district_category(matara, semi_urban).
district_category(hambantota, rural).
district_category(ratnapura, rural).
district_category(kegalle, rural).
district_category(kurunegala, rural).
district_category(puttalam, rural).
district_category(anuradhapura, rural).
district_category(polonnaruwa, rural).
district_category(badulla, rural).
district_category(monaragala, rural).
district_category(ampara, rural).
district_category(batticaloa, rural).
district_category(trincomalee, rural).
district_category(vavuniya, rural).
district_category(mannar, rural).
district_category(jaffna, rural).
district_category(kilinochchi, rural).
district_category(mullaitivu, rural).

% --- Family Size Categories ---
family_size_category(small, 1, 3).
family_size_category(medium, 4, 6).
family_size_category(large, 7, 15).

% --- Study Year Information ---
study_year(first_year, 1).
study_year(second_year, 2).
study_year(third_year, 3).
study_year(fourth_year, 4).
study_year(postgraduate, 5).

% --- Gender Categories ---
gender_category(male).
gender_category(female).

% --- Parent Employment Status ---
employment_status(employed).
employment_status(unemployed).
employment_status(retired).
employment_status(deceased).

% --- Transportation Availability ---
transport_availability(excellent).
transport_availability(good).
transport_availability(fair).
transport_availability(poor).
transport_availability(none).

% ============================================
% INFERENCE RULES (20+ RULES AS REQUIRED)
% ============================================

% Rule 1: Check if student qualifies based on family income alone
qualifies_by_income(FatherSalary, MotherSalary, Category) :-
    TotalIncome is FatherSalary + MotherSalary,
    family_income_threshold(Category, Min, Max),
    TotalIncome >= Min,
    TotalIncome =< Max,
    (Category = very_low; Category = low).

% Rule 2: Check if distance justifies hostel need
needs_hostel_by_distance(Distance, Justification) :-
    Distance > 30,
    Justification = 'Long distance from university requires hostel accommodation'.

needs_hostel_by_distance(Distance, Justification) :-
    Distance > 15,
    Distance =< 30,
    Justification = 'Moderate distance makes hostel accommodation beneficial'.

% Rule 3: Scholarship availability increases eligibility
scholarship_advantage(MahapolaStatus, SamurdhiStatus, Advantage) :-
    MahapolaStatus = available,
    SamurdhiStatus = available,
    Advantage = 'Both Mahapola and Samurdhi scholarships provide strong financial support'.

scholarship_advantage(MahapolaStatus, SamurdhiStatus, Advantage) :-
    (MahapolaStatus = available; SamurdhiStatus = available),
    Advantage = 'Scholarship availability provides financial assistance'.

% Rule 4: Special category students get priority
special_category_priority(Category, Priority) :-
    member(Category, [disabled, orphan, single_parent, chronic_illness]),
    Priority = emergency.

% Rule 5: Calculate priority based on multiple factors
calculate_priority(FatherSalary, MotherSalary, Distance, SpecialCategory, Priority) :-
    TotalIncome is FatherSalary + MotherSalary,
    TotalIncome < 30000,
    Distance > 30,
    member(SpecialCategory, [disabled, orphan, single_parent]),
    Priority = emergency.

calculate_priority(FatherSalary, MotherSalary, Distance, _, Priority) :-
    TotalIncome is FatherSalary + MotherSalary,
    TotalIncome < 30000,
    Distance > 15,
    Priority = high.

calculate_priority(FatherSalary, MotherSalary, Distance, _, Priority) :-
    TotalIncome is FatherSalary + MotherSalary,
    TotalIncome < 50000,
    Distance > 30,
    Priority = high.

calculate_priority(FatherSalary, MotherSalary, _, _, Priority) :-
    TotalIncome is FatherSalary + MotherSalary,
    TotalIncome >= 80000,
    Priority = low.

calculate_priority(_, _, _, _, Priority) :-
    Priority = medium.

% Rule 6: Check hostel availability
hostel_available(Gender, Available) :-
    (Gender = male -> HostelType = boys_hostel; HostelType = girls_hostel),
    hostel_capacity(HostelType, Total, Current),
    Available is Total - Current,
    Available > 0.

% Rule 7: Academic performance affects eligibility
academic_eligibility(GPA, Status) :-
    GPA >= 2.5,
    Status = eligible.

academic_eligibility(GPA, Status) :-
    GPA < 2.5,
    Status = 'Academic performance below minimum requirement (2.5 GPA)'.

% Rule 8: Rural students get preference
rural_student_preference(District, Preference) :-
    district_category(District, rural),
    Preference = 'Rural area student - gets preference for hostel accommodation'.

% Rule 9: Family size consideration
large_family_consideration(FamilySize, Consideration) :-
    FamilySize >= 7,
    Consideration = 'Large family size indicates additional financial burden'.

% Rule 10: First-year student priority
first_year_priority(Year, Priority) :-
    Year = 1,
    Priority = 'First-year students get higher priority for adjustment'.

% Rule 11: Combined financial hardship assessment
severe_financial_hardship(FatherSalary, MotherSalary, FamilySize, Hardship) :-
    TotalIncome is FatherSalary + MotherSalary,
    PerCapitaIncome is TotalIncome / FamilySize,
    PerCapitaIncome < 5000,
    Hardship = 'Severe financial hardship - per capita income below poverty line'.

% Rule 12: Transportation difficulty assessment
transport_difficulty(Distance, TransportAvailability, Difficulty) :-
    Distance > 25,
    member(TransportAvailability, [poor, none]),
    Difficulty = 'Poor transportation with long distance creates significant hardship'.

% Rule 13: Single parent family consideration
single_parent_support(FatherEmployment, MotherEmployment, Support) :-
    (FatherEmployment = deceased; MotherEmployment = deceased),
    Support = 'Single parent family requires additional support'.

% Rule 14: Unemployed parents consideration
unemployment_hardship(FatherEmployment, MotherEmployment, Hardship) :-
    FatherEmployment = unemployed,
    MotherEmployment = unemployed,
    Hardship = 'Both parents unemployed - extreme financial difficulty'.

% Rule 15: Merit-based consideration
merit_consideration(GPA, MeritStatus) :-
    GPA >= 3.5,
    MeritStatus = 'High academic performance demonstrates merit'.

% Rule 16: Gender-specific hostel availability
gender_hostel_match(Gender, HostelType) :-
    Gender = male,
    HostelType = boys_hostel.

gender_hostel_match(Gender, HostelType) :-
    Gender = female,
    HostelType = girls_hostel.

% Rule 17: Chronic illness accommodation need
medical_accommodation_need(MedicalCondition, Need) :-
    member(MedicalCondition, [chronic_illness, disability]),
    Need = 'Medical condition requires stable accommodation for treatment continuity'.

% Rule 18: District development level consideration
development_level_consideration(District, Consideration) :-
    district_category(District, rural),
    Consideration = 'Student from underdeveloped area needs educational opportunity support'.

% Rule 19: Age-based priority (for older students)
age_priority(Age, Priority) :-
    Age >= 25,
    Priority = 'Mature student with potentially different accommodation needs'.

% Rule 20: Combined scholarship and income assessment
scholarship_income_assessment(MahapolaStatus, SamurdhiStatus, FatherSalary, MotherSalary, Assessment) :-
    TotalIncome is FatherSalary + MotherSalary,
    MahapolaStatus = available,
    SamurdhiStatus = available,
    TotalIncome < 40000,
    Assessment = 'Multiple scholarships with low income - highly eligible'.

% Rule 21: Final hostel recommendation
recommend_hostel(FatherSalary, MotherSalary, Distance, Gender, GPA, MahapolaStatus, SamurdhiStatus, 
                SpecialCategory, District, FamilySize, Year, Recommendation, Reasons) :-
    
    % Check basic eligibility
    academic_eligibility(GPA, AcademicStatus),
    AcademicStatus = eligible,
    
    % Check hostel availability
    hostel_available(Gender, AvailableSpots),
    AvailableSpots > 0,
    
    % Calculate priority
    calculate_priority(FatherSalary, MotherSalary, Distance, SpecialCategory, Priority),
    
    % Collect all supporting reasons
    findall(Reason, (
        (qualifies_by_income(FatherSalary, MotherSalary, _), 
         Reason = 'Qualifies based on low family income');
        (needs_hostel_by_distance(Distance, Reason));
        (scholarship_advantage(MahapolaStatus, SamurdhiStatus, Reason));
        (rural_student_preference(District, Reason));
        (large_family_consideration(FamilySize, Reason));
        (first_year_priority(Year, Reason));
        (severe_financial_hardship(FatherSalary, MotherSalary, FamilySize, Reason))
    ), ReasonsList),
    
    % Determine recommendation based on priority
    (Priority = emergency -> 
        Recommendation = 'HIGHLY RECOMMENDED - Emergency Priority';
    Priority = high ->
        Recommendation = 'RECOMMENDED - High Priority';
    Priority = medium ->
        Recommendation = 'CONDITIONALLY RECOMMENDED - Medium Priority';
    Priority = low ->
        Recommendation = 'LOW PRIORITY - Consider alternatives'
    ),
    
    % Combine all reasons
    atomic_list_concat(ReasonsList, '; ', Reasons).

% Rule 22: Rejection cases
reject_hostel(FatherSalary, MotherSalary, Distance, Gender, GPA, Rejection, Reasons) :-
    (   
        % Academic performance insufficient
        academic_eligibility(GPA, AcademicStatus),
        AcademicStatus \= eligible,
        Rejection = 'NOT RECOMMENDED',
        Reasons = 'Academic performance below minimum requirement (2.5 GPA)'
    ;   
        % No hostel availability
        \+ hostel_available(Gender, _),
        Rejection = 'NOT RECOMMENDED',
        Reasons = 'No available hostel capacity for your gender category'
    ;   
        % High income and short distance
        TotalIncome is FatherSalary + MotherSalary,
        TotalIncome > 100000,
        Distance < 15,
        Rejection = 'NOT RECOMMENDED',
        Reasons = 'High family income and short distance from university - hostel not necessary'
    ).

% ============================================
% HELPER PREDICATES
% ============================================

% Check if student is from rural area
is_rural_student(District) :-
    district_category(District, rural).

% Check if student has any scholarship
has_scholarship(MahapolaStatus, SamurdhiStatus) :-
    (MahapolaStatus = available; SamurdhiStatus = available).

% Calculate total family income
total_family_income(FatherSalary, MotherSalary, Total) :-
    Total is FatherSalary + MotherSalary.

% Check if student is in special category
is_special_category(Category) :-
    member(Category, [disabled, orphan, single_parent, chronic_illness, financial_hardship]).

% ============================================
% QUERY EXAMPLES
% ============================================
% ?- recommend_hostel(15000, 8000, 45, male, 3.2, available, not_available, orphan, ratnapura, 6, 1, R, Reasons).
% ?- reject_hostel(80000, 60000, 10, female, 2.0, R, Reasons).
% ?- calculate_priority(20000, 12000, 35, disabled, P).
% ?- scholarship_advantage(available, available, A).
% ?- needs_hostel_by_distance(40, J).
% ============================================