import random
import copy
import numpy as np
import sys
import os
sys.path.append(os.path.abspath(".."))
from local_sol.data_classes_local import  TimelineProfessors, TimelineStudents, TimelineGuides, TimelineTours, TimelineTourism
from utils import *

print_ = False

#swap two random elements of the timeline
def swap(timeline):
    possible_swap = False
    timeout = timeline.days * timeline.hours * 10

    item_in_timeline = set()
    for day in range(timeline.days):
        for hour in range(timeline.hours):
            if timeline.timeline[day][hour] is not None:
                item_in_timeline.add(timeline.timeline[day][hour])

    if len(item_in_timeline) < 3:
        return
    
    while not possible_swap and timeout > 0:
        item_1, day_1, hour_1, lenght_slot_1 = find_random_item(timeline)
        item_2, day_2, hour_2, lenght_slot_2 = find_random_item(timeline)

        if item_1 == item_2:
            continue
        else:
            if lenght_slot_1 == lenght_slot_2:
                possible_swap = True
            elif lenght_slot_1 + hour_2 < timeline.hours and lenght_slot_2 + hour_1 < timeline.hours:
                possible_swap = True
            else:
                timeout -= 1
                continue

    #remove item1
    timeline.remove_item(item_1, day_1, hour_1, lenght_slot_1) 
    #remove item2
    timeline.remove_item(item_2, day_2, hour_2, lenght_slot_2)

    #add item1 in the new position (ex item2)
    timeline.add_item(item_1, day_2, hour_2, lenght_slot_1)
    #add item2 in the new position (ex item1)
    timeline.add_item(item_2, day_1, hour_1, lenght_slot_2)

#move an item in a random (or not) position
def move(timeline, random_slot = True, day_choose = None, hour_choose = None):
    if random_slot:
        item_choose, day_choose, hour_choose, lenght_slot = find_random_item(timeline)
    else:
        item_choose, day_choose, hour_choose, lenght_slot = find_random_item(timeline, random_slot, day_choose, hour_choose)

    #move to a new time slot, if there is no empty slot the lecture is moved in the last valid random slot
    empty_slot = False
    explored_slots = np.array([[False for _ in range(timeline.hours)] for _ in range(timeline.days)]) 
    while not empty_slot and not np.all(explored_slots):

        day_new = random.randrange(timeline.days)
        hour_new = random.randrange(timeline.hours)
        explored_slots[day_new][hour_new] = True

        #check if the lecture can be moved in the selected slot (has enough "space")
        if hour_new + lenght_slot >= timeline.hours:
            hour = hour_new
            while hour < timeline.hours:
                explored_slots[day_new][hour] = True
                hour += 1
            continue

        #check if the lecture can be moved in the selected slot (has no overlap)
        overlap = False
        for hour in range(hour_new, hour_new + lenght_slot):
            if timeline.timeline[day_new][hour] is not None:
                overlap = True
                break

        if not overlap:
            empty_slot = True

    #remove the item from the old position
    timeline.remove_item(item_choose, day_choose, hour_choose, lenght_slot)
    #add the item in the new position
    timeline.add_item(item_choose, day_new, hour_new, lenght_slot)

#switch two days of the timeline
def switch_days(timeline, day_1, day_2):
    tmp = copy.deepcopy(timeline.timeline[day_1])
    timeline.timeline[day_1] = copy.deepcopy(timeline.timeline[day_2])
    timeline.timeline[day_2] = tmp

#move an item from a day to another, valid only for TimelineTourism
def move_to(timeline, day, hour, day_to, hour_busy):
    item = timeline.timeline[day][hour].split('+')[0]
    lenght_slot = int(item.split('*')[1].split('by')[0])
    lenght_slot = int(np.ceil(lenght_slot/60))

    timeline.remove_item(item, day, hour, lenght_slot)
    empty_slot = False
    explored_slots = np.array([False for _ in range(timeline.hours)])
    for h in hour_busy:
        explored_slots[h] = True

    while not empty_slot and not np.all(explored_slots):

        hour_new = random.randrange(timeline.hours)
        if explored_slots[hour_new]:
            continue
        explored_slots[hour_new] = True

        if hour_new + lenght_slot >= timeline.hours:
            h = hour_new
            while h < timeline.hours:
                explored_slots[h] = True
                h += 1
            continue

        overlap = False
        for h in range(hour_new, hour_new + lenght_slot):
            if timeline.timeline[day_to][h] is not None:
                overlap = True
                break

        if not overlap:
            empty_slot = True

    if empty_slot:
        timeline.add_item(item, day_to, hour_new, lenght_slot)
    else:
        timeline.add_item(item, day, hour, lenght_slot)


#solution_obj: object of the class Timeline
#
#return a new perturbated solution object of the class Timeline
def perturbate(solution_obj):
    perturbated_solution = copy.deepcopy(solution_obj)
    
    if isinstance(perturbated_solution, TimelineTourism):
        perturbated_solution.clear_distance()

    operation = random.randrange(2)

    if operation == 0:
        swap(perturbated_solution)
    elif operation == 1:
        move(perturbated_solution)
    else:
        raise Exception("Invalid operation number")
    

    if isinstance(perturbated_solution, TimelineTourism):
        perturbated_solution.compute_distance()

    return perturbated_solution

#solution_obj: object of the class Timeline
#
#return a new perturbated solution object of the class Timeline
def perturbate_with_heu(solution_obj):
    
    #are we fair? 
    if solution_obj.fairness_score() == 0:
        #YES, search other fair solutions
        return perturbate(solution_obj)
    else:
        #NO, try to make it fair
        perturbated_solution = copy.deepcopy(solution_obj)
        if isinstance(perturbated_solution, TimelineTourism):
            perturbated_solution.clear_distance()

        #PROFESSORS
        if isinstance(perturbated_solution, TimelineProfessors):
            #FIRST: check if mandatory are satisfied
            if not perturbated_solution.satisfied_mandatory():
                #NO
                list_unsatisfied_constraints = perturbated_solution.find_overlaps()

                if len(list_unsatisfied_constraints) == 0:
                    #NO OVERLAP, get other unsatisfied constraints
                    list_unsatisfied_constraints = perturbated_solution.get_unsatisfied_impossible_constraints()
                
            else:
                #YES
                list_unsatisfied_constraints = perturbated_solution.get_unsatisfied_constraints()
                if len(list_unsatisfied_constraints) == 0:
                    #the only unsatisfied is two consecutive days
                    move(perturbated_solution) #move randomly
                    return perturbated_solution
            
            #SECOND: choose randomly an unsatisfied constraint
            day, hour = list_unsatisfied_constraints[random.randrange(len(list_unsatisfied_constraints))]
            move(perturbated_solution, False, day, hour)
            
            return perturbated_solution

        #STUDENTS
        elif isinstance(perturbated_solution, TimelineStudents):
            #FIRST: check if mandatory are satisfied
            if not perturbated_solution.satisfied_mandatory():
                #NO
                list_unsatisfied_constraints = perturbated_solution.find_overlaps()
                day, hour = list_unsatisfied_constraints[random.randrange(len(list_unsatisfied_constraints))]
                move(perturbated_solution, False, day, hour)

                return perturbated_solution
            else:
                #YES
                #check if there is a day without lunch break
                if not perturbated_solution.has_lunch_break():
                    #YES
                    list_days = perturbated_solution.find_day_without_lunch_break()
                    day = list_days[random.randrange(len(list_days))]
                    hour = 4 #lunch break span on 3 hours, minimun lesson lenght of 2 hours, so we can take the "middle" slot
                    move(perturbated_solution, False, day, hour)
                    #return perturbated_solution DECOMMENT TO SOLVE IN ORDER AND ONE AT TIME
                else:
                    #NO
                    #solo lesson in a day
                    num_one_lesson_per_day = perturbated_solution.alone_lecture()

                    #check if there are gap during the day
                    list_gaps_in_day = perturbated_solution.num_gaps_in_days()
                    if len(list_gaps_in_day) > 0:
                        if len(num_one_lesson_per_day) > 0:
                            day = num_one_lesson_per_day[0][0]
                            hour = num_one_lesson_per_day[0][1]
                        else:
                            #solve first day with more gaps
                            list_gaps_in_day.sort(key = lambda x: x[1], reverse = True)
                            day = list_gaps_in_day[0][0]
                            empty_slot = True
                            while empty_slot:
                                hour = random.randrange(perturbated_solution.hours)
                                if perturbated_solution.timeline[day][hour] is not None:
                                    empty_slot = False
                        move(perturbated_solution, False, day, hour)
                        #return perturbated_solution DECOMMENT TO SOLVE IN ORDER AND ONE AT TIME
                    
                    #check if there are gap during the week
                    num_gaps_in_week, day_lecture = perturbated_solution.num_gaps_in_week()
                    if num_gaps_in_week > 0:
                        day = day_lecture[random.randrange(len(day_lecture))]
                        list_free_days = [x for x in range(perturbated_solution.days) if x not in day_lecture]
                        day_free = list_free_days[random.randrange(len(list_free_days))]

                        switch_days(perturbated_solution, day, day_free)
                        #return perturbated_solution DECOMMENT TO SOLVE IN ORDER AND ONE AT TIME

                return perturbated_solution

        #GUIDES
        elif isinstance(perturbated_solution, TimelineGuides):
            #FIRST: check if mandatory are satisfied
            if not perturbated_solution.satisfied_mandatory():
                #NO
                list_unsatisfied_constraints = perturbated_solution.find_overlaps()

                if len(list_unsatisfied_constraints) == 0:
                    #NO OVERLAP, get other unsatisfied constraints
                    list_unsatisfied_constraints = perturbated_solution.get_unsatisfied_impossible_constraints()
                
            else:
                #YES
                list_unsatisfied_constraints = perturbated_solution.get_unsatisfied_constraints()

            if len(list_unsatisfied_constraints) == 0:
                #unstatified during the path between two pois
                return perturbate(solution_obj)

            #SECOND: choose randomly an unsatisfied constraint
            day, hour = list_unsatisfied_constraints[random.randrange(len(list_unsatisfied_constraints))]
            move(perturbated_solution, False, day, hour)

            perturbated_solution.compute_distance()
            return perturbated_solution

        #TOURS
        elif isinstance(perturbated_solution, TimelineTours):
            #FIRST: check if mandatory are satisfied
            if not perturbated_solution.satisfied_mandatory():
                #NO
                list_unsatisfied_constraints = perturbated_solution.find_overlaps()
                day, hour = list_unsatisfied_constraints[random.randrange(len(list_unsatisfied_constraints))]
                move(perturbated_solution, False, day, hour)
            else:
                #YES
                #move "solo" visit to populated days
                modified = False
                number_visit_per_day = perturbated_solution.num_visit_per_day()
                number_visit_per_day.sort(key = lambda x: x[1], reverse = False)
                if len(number_visit_per_day) > 1:
                    day = number_visit_per_day[0][0]
                    hour = number_visit_per_day[0][2][0]

                    day_to = number_visit_per_day[-1][0]
                    hour_busy = number_visit_per_day[-1][2]
                    move_to(perturbated_solution, day, hour, day_to, hour_busy)

                    modified = True
                    #perturbated_solution.compute_distance()
                    #return perturbated_solution DECOMMENT TO SOLVE IN ORDER AND ONE AT TIME

                #check if there are gap during the day
                list_gaps_in_day = perturbated_solution.num_gaps_in_days()
                if len(list_gaps_in_day) > 0:
                    #solve first day with more gaps
                    list_gaps_in_day.sort(key = lambda x: x[1], reverse = True)
                    day = list_gaps_in_day[0][0]
                    empty_slot = True
                    while empty_slot:
                        hour = random.randrange(perturbated_solution.hours)
                        if perturbated_solution.timeline[day][hour] is not None:
                            empty_slot = False
                    move(perturbated_solution, False, day, hour)
                    modified = True
                    #perturbated_solution.compute_distance()
                    #return perturbated_solution DECOMMENT TO SOLVE IN ORDER AND ONE AT TIME
                
                #check if there are gap during the week
                num_gaps_in_week, day_lecture = perturbated_solution.num_gaps_in_week()
                if num_gaps_in_week > 0:
                    choose_rand = random.randrange(2)
                    if choose_rand == 0:
                        index = 0
                    else:
                        index = -1
                    day = day_lecture[index]
                    list_free_days = [x for x in range(perturbated_solution.days) if x not in day_lecture]
                    day_free = list_free_days[random.randrange(len(list_free_days))]
                    
                    switch_days(perturbated_solution, day, day_free)
                    modified = True
                    #perturbated_solution.compute_distance()
                    #return perturbated_solution DECOMMENT TO SOLVE IN ORDER AND ONE AT TIME
                
                if not modified:
                    return perturbate(solution_obj)

            perturbated_solution.compute_distance()
            return perturbated_solution
        else:
            raise Exception("Invalid solution object")


#
# curr_sol: current solution object of the class Timeline
# paretoSet: empty pareto set, is a set() object
# initialTemp: initial temperature, int
# finalTemp: final temperature, int
# alpha: alpha, float  
# maxPerturbation: max perturbation, int
# heuristic: boolean, True if you want to use the heuristic (fairness), False if not
def performSa(curr_sol, paretoSet, paretoFront, initialTemp, finalTemp, alpha, maxPerturbation, heuristic = False):
    temperature = initialTemp
    c = 0
    while temperature > finalTemp:
        for _ in range(maxPerturbation):
            if heuristic:
                perturb_sol = perturbate_with_heu(curr_sol)
            else:
                perturb_sol = perturbate(curr_sol)
        
            if perturb_sol == curr_sol:
                continue

            if print_:
                print("Pareto Front size: ", len(paretoFront))
                print("Pareto Set size: ", len(paretoSet))

            p = acceptanceProbability(curr_sol, perturb_sol, temperature, paretoFront)

            if random.uniform(0, 1) < p :
                updateParetoSet(perturb_sol, paretoSet)
                curr_sol = perturb_sol

        c += 1
        temperature = initialTemp - alpha * c
        

    return paretoSet


def getBestSolLocal(curr_sol, initialTemp, finalTemp, alpha, maxPerturbation, heuristic = False):
    sol = copy.deepcopy(curr_sol)
    paretoSet = set()
    paretoSet.add(sol)
    paretoFront = computeParetoFront(paretoSet)

    paretoSet = performSa(sol, paretoSet, paretoFront, initialTemp, finalTemp, alpha, maxPerturbation, heuristic)

    best_sol = max(paretoSet, key = lambda x: x.fairness_score())

    return best_sol