% Members and Coaches
member(john).
member(sarah).
member(mike).
member(emily).
member(david).
member(lucy).

coach(alex).
coach(nina).

% Activities
activity(yoga).
activity(meditation).
activity(fitness_training).
activity(stress_management).
activity(nutrition_guidance).

% Participation Facts
participates(john, yoga).
participates(john, meditation).
participates(sarah, fitness_training).
participates(mike, stress_management).
participates(emily, nutrition_guidance).
participates(david, yoga).
participates(lucy, stress_management).

% Coaching Facts
coaches(alex, yoga).
coaches(alex, meditation).
coaches(nina, fitness_training).
coaches(nina, stress_management).
coaches(nina, nutrition_guidance).

% Rules
coach_of(Coach, Activity) :- coaches(Coach, Activity).
participants_of(Member, Activity) :- participates(Member, Activity).