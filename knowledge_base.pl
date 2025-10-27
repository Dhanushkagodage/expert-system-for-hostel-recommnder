% ============================================
% UNIVERSITY HOSTEL FACILITY RECOMMENDER SYSTEM
% Knowledge Base for Student Hostel Eligibility
% ============================================

% --- Distance Categories (in km) ---
% Distance ranges: 0-50 (25), 50-100 (75), 100-150 (125), 150-200 (175), above 200 (225)
distance_category(very_far, Distance) :- Distance > 150.
distance_category(far, Distance) :- Distance > 75, Distance =< 150.
distance_category(moderate, Distance) :- Distance > 25, Distance =< 75.
distance_category(near, Distance) :- Distance > 10, Distance =< 25.
distance_category(very_near, Distance) :- Distance =< 10.

% --- Income Categories (monthly family income in LKR) ---
combined_income(FatherSalary, MotherSalary, Total) :-
    Total is FatherSalary + MotherSalary.

income_category(very_low, Income) :- Income < 25000.
income_category(low, Income) :- Income >= 25000, Income < 50000.
income_category(middle, Income) :- Income >= 50000, Income < 100000.
income_category(high, Income) :- Income >= 100000, Income < 200000.
income_category(very_high, Income) :- Income >= 200000.

% --- Financial Support Status ---
has_financial_support(mahapola, samurdhi) :- !.
has_financial_support(mahapola, none) :- !.
has_financial_support(none, samurdhi) :- !.
has_no_support(none, none).

% --- Sibling Education Status ---
siblings_in_university(Count) :- Count > 0.
no_siblings_in_university(0).

% --- Special Circumstances ---
special_circumstance(orphan).
special_circumstance(single_parent).
special_circumstance(disabled_parent).
special_circumstance(chronic_illness_family).
special_circumstance(natural_disaster_affected).
special_circumstance(none).

% --- Student Status ---
student_year(first_year).
student_year(second_year).
student_year(third_year).
student_year(fourth_year).
student_year(postgraduate).

% ============================================
% ELIGIBILITY RULES (20 RULES)
% ============================================

% Rule 1: High Priority - Very far distance with low income
high_priority_distance_income(Distance, FatherSalary, MotherSalary) :-
    distance_category(very_far, Distance),
    combined_income(FatherSalary, MotherSalary, Total),
    income_category(very_low, Total).

% Rule 2: High Priority - Far distance with financial support
high_priority_distance_support(Distance, Mahapola, Samurdhi) :-
    (distance_category(very_far, Distance); distance_category(far, Distance)),
    has_financial_support(Mahapola, Samurdhi).

% Rule 3: High Priority - Special circumstances
high_priority_special(SpecialCase) :-
    special_circumstance(SpecialCase),
    SpecialCase \= none.

% Rule 4: High Priority - Orphan or single parent with low income
high_priority_vulnerable(SpecialCase, FatherSalary, MotherSalary) :-
    (SpecialCase = orphan; SpecialCase = single_parent),
    combined_income(FatherSalary, MotherSalary, Total),
    (income_category(very_low, Total); income_category(low, Total)).

% Rule 5: Medium Priority - Moderate distance with low income
medium_priority_distance_income(Distance, FatherSalary, MotherSalary) :-
    distance_category(moderate, Distance),
    combined_income(FatherSalary, MotherSalary, Total),
    (income_category(very_low, Total); income_category(low, Total)).

% Rule 6: Medium Priority - Far distance with middle income and siblings
medium_priority_family_burden(Distance, FatherSalary, MotherSalary, Siblings) :-
    distance_category(far, Distance),
    combined_income(FatherSalary, MotherSalary, Total),
    income_category(middle, Total),
    siblings_in_university(Siblings).

% Rule 7: Medium Priority - Financial support with moderate distance
medium_priority_support_distance(Distance, Mahapola, Samurdhi) :-
    distance_category(moderate, Distance),
    has_financial_support(Mahapola, Samurdhi).

% Rule 8: Medium Priority - Natural disaster affected
medium_priority_disaster(SpecialCase, Distance) :-
    SpecialCase = natural_disaster_affected,
    (distance_category(moderate, Distance); 
     distance_category(far, Distance); 
     distance_category(very_far, Distance)).

% Rule 9: Low Priority - Near distance with high income
low_priority_near_wealthy(Distance, FatherSalary, MotherSalary) :-
    (distance_category(near, Distance); distance_category(very_near, Distance)),
    combined_income(FatherSalary, MotherSalary, Total),
    (income_category(high, Total); income_category(very_high, Total)).

% Rule 10: Not Eligible - Very near distance with very high income
not_eligible_wealthy_near(Distance, FatherSalary, MotherSalary) :-
    distance_category(very_near, Distance),
    combined_income(FatherSalary, MotherSalary, Total),
    income_category(very_high, Total),
    SpecialCase = none.

% Rule 11: Priority boost for multiple financial supports
priority_boost_dual_support(Mahapola, Samurdhi) :-
    Mahapola = mahapola,
    Samurdhi = samurdhi.

% Rule 12: First year students with distance priority
first_year_priority(Year, Distance) :-
    Year = first_year,
    (distance_category(very_far, Distance); distance_category(far, Distance)).

% Rule 13: Postgraduate priority with financial need
postgraduate_priority(Year, FatherSalary, MotherSalary) :-
    Year = postgraduate,
    combined_income(FatherSalary, MotherSalary, Total),
    Total < 100000.

% Rule 14: Income threshold check
meets_income_threshold(FatherSalary, MotherSalary) :-
    combined_income(FatherSalary, MotherSalary, Total),
    Total < 150000.

% Rule 15: Distance threshold check
meets_distance_threshold(Distance) :-
    Distance > 25.

% Rule 16: Multiple siblings burden
significant_family_burden(Siblings, FatherSalary, MotherSalary) :-
    Siblings >= 2,
    combined_income(FatherSalary, MotherSalary, Total),
    income_category(middle, Total).

% Rule 17: Chronic illness with low income
health_related_priority(SpecialCase, FatherSalary, MotherSalary) :-
    SpecialCase = chronic_illness_family,
    combined_income(FatherSalary, MotherSalary, Total),
    (income_category(very_low, Total); income_category(low, Total)).

% Rule 18: Disabled parent with distance
disability_distance_priority(SpecialCase, Distance) :-
    SpecialCase = disabled_parent,
    (distance_category(moderate, Distance); 
     distance_category(far, Distance); 
     distance_category(very_far, Distance)).

% Rule 19: High financial need
high_financial_need(FatherSalary, MotherSalary, Siblings) :-
    combined_income(FatherSalary, MotherSalary, Total),
    (income_category(very_low, Total); income_category(low, Total)),
    Siblings >= 1.

% Rule 20: Comprehensive eligibility check
comprehensive_eligibility(Distance, FatherSalary, MotherSalary, Mahapola, Samurdhi) :-
    meets_distance_threshold(Distance),
    meets_income_threshold(FatherSalary, MotherSalary),
    has_financial_support(Mahapola, Samurdhi).

% ============================================
% MAIN ELIGIBILITY DETERMINATION
% ============================================

% Calculate eligibility score
calculate_score(Distance, FatherSalary, MotherSalary, Mahapola, Samurdhi, 
                Siblings, SpecialCase, Year, Score) :-
    combined_income(FatherSalary, MotherSalary, TotalIncome),
    
    % Distance points (0-30)
    (distance_category(very_far, Distance) -> DistPoints = 30;
     distance_category(far, Distance) -> DistPoints = 25;
     distance_category(moderate, Distance) -> DistPoints = 15;
     distance_category(near, Distance) -> DistPoints = 5;
     DistPoints = 0),
    
    % Income points (0-25)
    (income_category(very_low, TotalIncome) -> IncomePoints = 25;
     income_category(low, TotalIncome) -> IncomePoints = 20;
     income_category(middle, TotalIncome) -> IncomePoints = 10;
     income_category(high, TotalIncome) -> IncomePoints = 5;
     IncomePoints = 0),
    
    % Financial support points (0-15)
    (Mahapola = mahapola, Samurdhi = samurdhi -> SupportPoints = 15;
     Mahapola = mahapola -> SupportPoints = 10;
     Samurdhi = samurdhi -> SupportPoints = 10;
     SupportPoints = 0),
    
    % Siblings points (0-10)
    (Siblings >= 3 -> SiblingPoints = 10;
     Siblings = 2 -> SiblingPoints = 7;
     Siblings = 1 -> SiblingPoints = 4;
     SiblingPoints = 0),
    
    % Special circumstance points (0-20)
    (SpecialCase = orphan -> SpecialPoints = 20;
     SpecialCase = single_parent -> SpecialPoints = 15;
     SpecialCase = disabled_parent -> SpecialPoints = 15;
     SpecialCase = chronic_illness_family -> SpecialPoints = 12;
     SpecialCase = natural_disaster_affected -> SpecialPoints = 12;
     SpecialPoints = 0),
    
    % Year bonus (0-5)
    (Year = first_year -> YearPoints = 5;
     Year = postgraduate -> YearPoints = 3;
     YearPoints = 0),
    
    Score is DistPoints + IncomePoints + SupportPoints + 
             SiblingPoints + SpecialPoints + YearPoints.

% Determine eligibility based on score
determine_eligibility(Score, Status, Priority) :-
    (Score >= 80 -> Status = eligible, Priority = high;
     Score >= 60 -> Status = eligible, Priority = medium;
     Score >= 40 -> Status = eligible, Priority = low;
     Status = not_eligible, Priority = none).

% Generate reasons for decision
generate_reasons(Distance, FatherSalary, MotherSalary, Mahapola, Samurdhi,
                Siblings, SpecialCase, Year, Reasons) :-
    findall(Reason, (
        (high_priority_distance_income(Distance, FatherSalary, MotherSalary) ->
            Reason = 'Very far distance with low family income';
        fail),
        (high_priority_distance_support(Distance, Mahapola, Samurdhi) ->
            Reason = 'Long distance with government financial support';
        fail),
        (high_priority_special(SpecialCase) ->
            atom_string(SpecialCase, SpecialStr),
            atomic_list_concat(['Special circumstance: ', SpecialStr], Reason);
        fail),
        (medium_priority_distance_income(Distance, FatherSalary, MotherSalary) ->
            Reason = 'Moderate distance with low income';
        fail),
        (medium_priority_family_burden(Distance, FatherSalary, MotherSalary, Siblings) ->
            Reason = 'Multiple siblings in university creating financial burden';
        fail),
        (high_financial_need(FatherSalary, MotherSalary, Siblings) ->
            Reason = 'High financial need with siblings in university';
        fail),
        (first_year_priority(Year, Distance) ->
            Reason = 'First year student from far distance';
        fail),
        (low_priority_near_wealthy(Distance, FatherSalary, MotherSalary) ->
            Reason = 'Close proximity to university with high family income';
        fail)
    ), Reasons).

% Main evaluation predicate
evaluate_hostel_eligibility(Distance, FatherSalary, MotherSalary, Mahapola, 
                           Samurdhi, Siblings, SpecialCase, Year,
                           Status, Priority, Score, Reasons) :-
    calculate_score(Distance, FatherSalary, MotherSalary, Mahapola, Samurdhi,
                   Siblings, SpecialCase, Year, Score),
    determine_eligibility(Score, Status, Priority),
    generate_reasons(Distance, FatherSalary, MotherSalary, Mahapola, Samurdhi,
                    Siblings, SpecialCase, Year, Reasons).

% ============================================
% QUERY EXAMPLES
% ============================================
% ?- evaluate_hostel_eligibility(60, 20000, 15000, mahapola, samurdhi, 2, orphan, first_year, Status, Priority, Score, Reasons).
% ?- high_priority_distance_income(55, 18000, 12000).
% ?- calculate_score(45, 30000, 20000, mahapola, none, 1, single_parent, second_year, Score).
% ============================================