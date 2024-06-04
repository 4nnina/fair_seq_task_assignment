from data_classes import TimelineProfessors, TimelineStudents, TimelineGuides, TimelineTours
from utils import *


random.seed(20)

#Students
print('Creating timeline students...')
degree = 'Laurea in Informatica [420] Corsi di laurea - UNICO'
year = 1
timeline = TimelineStudents(degree=degree, year=year)
print('Randomic timeline created:\n', timeline)
print('Fairness score: ', timeline.fairness_score())

print('\nExecution of simulated annealing...')
pareto_set = performSa(timeline, set(), 50, 5, 0.5, 10)
best_sol = max(pareto_set, key=lambda x: x.fairness_score())
print('Best solution found:\n', best_sol)
print('Fairness score: ', best_sol.fairness_score(True))

print('\nExecution of simulated annealing with heuristic...')
pareto_set = performSa(timeline, set(), 50, 5, 0.5, 10, heuristic=True)
best_sol = max(pareto_set, key=lambda x: x.fairness_score())
print('Best solution found:\n', best_sol)
print('Fairness score: ', best_sol.fairness_score(True))

#Professors
print('\n', '*'*100, '\n')
print('Creating timeline Professor...')
prof_id = 5
timeline = TimelineProfessors(prof_id=prof_id)
print('Randomic timeline created:\n', timeline)
print('Fairness score: ', timeline.fairness_score())

print('\nExecution of simulated annealing...')
pareto_set = performSa(timeline, set(), 50, 5, 0.5, 10)
best_sol = max(pareto_set, key=lambda x: x.fairness_score())
print('Best solution found:\n', best_sol)
print('Fairness score: ', best_sol.fairness_score())

print('\nExecution of simulated annealing with heuristic...')
pareto_set = performSa(timeline, set(), 50, 5, 0.5, 10, heuristic=True)
best_sol = max(pareto_set, key=lambda x: x.fairness_score())
print('Best solution found:\n', best_sol)
print('Fairness score: ', best_sol.fairness_score())

#Tourists
print('\n', '*'*100, '\n')
print('Creating timeline Tourists...')
tour_id = 2
timeline = TimelineTours(tour_id=tour_id)
print('Randomic timeline created:\n', timeline)
print('Fairness score: ', timeline.fairness_score())

print('\nExecution of simulated annealing...')
pareto_set = performSa(timeline, set(), 50, 5, 0.5, 10)
best_sol = max(pareto_set, key=lambda x: x.fairness_score())
print('Best solution found:\n', best_sol)
print('Fairness score: ', best_sol.fairness_score(True))

print('\nExecution of simulated annealing with heuristic...')
pareto_set = performSa(timeline, set(), 50, 5, 0.5, 10, heuristic=True)
best_sol = max(pareto_set, key=lambda x: x.fairness_score())
print('Best solution found:\n', best_sol)
print('Fairness score: ', best_sol.fairness_score(True))

#Guides
print('\n', '*'*100, '\n')
print('Creating timeline Guides...')
guide_id = 2
timeline = TimelineGuides(guide_id=guide_id)
print('Randomic timeline created:\n', timeline)
print('Fairness score: ', timeline.fairness_score())

print('\nExecution of simulated annealing...')
pareto_set = performSa(timeline, set(), 10, 5, 0.5, 10)
best_sol = max(pareto_set, key=lambda x: x.fairness_score())
print('Best solution found:\n', best_sol)
print('Fairness score: ', best_sol.fairness_score())

print('\nExecution of simulated annealing with heuristic...')
pareto_set = performSa(timeline, set(), 10, 5, 0.5, 10, heuristic=True)
best_sol = max(pareto_set, key=lambda x: x.fairness_score())
print('Best solution found:\n', best_sol)
print('Fairness score: ', best_sol.fairness_score())

