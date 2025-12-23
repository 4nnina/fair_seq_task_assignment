import random
import copy
import numpy as np
import sys
import os
sys.path.append(os.path.abspath(".."))
from local_sol.data_classes_local import  TimelineProfessors, TimelineStudents, TimelineGuides, TimelineTours, TimelineTourism, TimelineUniversity
from global_sol.data_classes_global import GlobalUniversity, GlobalTourism
from utils import *

print_ = False

#swap two random elements of the timeline
def swap_local(timeline_g, idx_timeline_choose, mode):
    possible_swap = False
    if isinstance(timeline_g, GlobalUniversity):
        timeline_choose = timeline_g.list_degree[idx_timeline_choose] if mode == 'cohort' else timeline_g.list_prof[idx_timeline_choose]
    elif isinstance(timeline_g, GlobalTourism):
        timeline_choose = timeline_g.list_tour[idx_timeline_choose] if mode == 'cohort' else timeline_g.list_guide[idx_timeline_choose]
    timeout = timeline_choose.days * timeline_choose.hours * 10

    item_in_timeline = set()
    for day in range(timeline_choose.days):
        for hour in range(timeline_choose.hours):
            if timeline_choose.timeline[day][hour] is not None:
                item_in_timeline.add(timeline_choose.timeline[day][hour])

    if len(item_in_timeline) < 3:
        return
    
    while not possible_swap and timeout > 0:
        item_1, day_1, hour_1, lenght_slot_1 = find_random_item(timeline_choose)
        item_2, day_2, hour_2, lenght_slot_2 = find_random_item(timeline_choose)

        if item_1 == item_2:
            continue
        else:
            if lenght_slot_1 == lenght_slot_2:
                possible_swap = True
            elif lenght_slot_1 + hour_2 < timeline_choose.hours and lenght_slot_2 + hour_1 < timeline_choose.hours:
                possible_swap = True
            else:
                timeout -= 1
                continue

    if mode == 'cohort':
        if isinstance(timeline_choose, TimelineUniversity):
            prof1 = timeline_choose.get_prof(item_1, day_1, hour_1)
            prof2 = timeline_choose.get_prof(item_2, day_2, hour_2)
        elif isinstance(timeline_choose, TimelineTourism):
            prof1 = timeline_choose.get_guide(item_1, day_1, hour_1)
            prof2 = timeline_choose.get_guide(item_2, day_2, hour_2)

        if print_:
            print("Swapping items:", item_1, "and", item_2)
            print("At positions:", (day_1, hour_1), "and", (day_2, hour_2))
            print("From timeline:", timeline_choose.degree, timeline_choose.year)
            print("Professors:", prof1, "and", prof2)

        #For students

        #remove item1
        timeline_choose.remove_item(item_1, day_1, hour_1, lenght_slot_1) 
        #remove item2
        timeline_choose.remove_item(item_2, day_2, hour_2, lenght_slot_2)

        #add item1 in the new position (ex item2)
        timeline_choose.add_item(item_1, day_2, hour_2, lenght_slot_1)
        #add item2 in the new position (ex item1)
        timeline_choose.add_item(item_2, day_1, hour_1, lenght_slot_2)

        if isinstance(timeline_choose, TimelineUniversity):
            #For professors
            for prof in timeline_g.list_prof:
                if prof.name == prof1:
                    #timeline_prof1 = prof
                    if print_:
                        print("Timeline professor 1:", prof)
                    prof.remove_item(item_1, day_1, hour_1, lenght_slot_1)
                    prof.add_item(item_1, day_2, hour_2, lenght_slot_1)
                    if print_:
                        print("MODIFIED Timeline professor 1:", prof)
                if prof.name == prof2:
                    #timeline_prof2 = prof
                    if print_:
                        print("Timeline professor 2:", prof)
                    prof.remove_item(item_2, day_2, hour_2, lenght_slot_2)
                    prof.add_item(item_2, day_1, hour_1, lenght_slot_2)
                    if print_:
                        print("MODIFIED Timeline professor 2:", prof)
        elif isinstance(timeline_choose, TimelineTourism):
            #For guides
            for guide in timeline_g.list_guide:
                if guide.guide == prof1:
                    #timeline_prof1 = prof
                    if print_:
                        print("Timeline guide 1:", guide)
                    guide.remove_item(item_1, day_1, hour_1, lenght_slot_1)
                    guide.add_item(item_1, day_2, hour_2, lenght_slot_1)
                    if print_:
                        print("MODIFIED Timeline guide 1:", guide)
                if guide.guide == prof2:
                    #timeline_prof2 = prof
                    if print_:
                        print("Timeline guide 2:", guide)
                    guide.remove_item(item_2, day_2, hour_2, lenght_slot_2)
                    guide.add_item(item_2, day_1, hour_1, lenght_slot_2)
                    if print_:
                        print("MODIFIED Timeline guide 2:", guide)


    elif mode == 'single':
        #For professors
        #remove item1
        timeline_choose.remove_item(item_1, day_1, hour_1, lenght_slot_1) 
        #remove item2
        timeline_choose.remove_item(item_2, day_2, hour_2, lenght_slot_2)

        #add item1 in the new position (ex item2)
        timeline_choose.add_item(item_1, day_2, hour_2, lenght_slot_1)
        #add item2 in the new position (ex item1)
        timeline_choose.add_item(item_2, day_1, hour_1, lenght_slot_2)

        if isinstance(timeline_choose, TimelineUniversity):
            #For students
            for degree in timeline_g.list_degree:
                if item_1 in degree.get_all_items():
                    timeline_stud1 = degree
                if item_2 in degree.get_all_items():
                    timeline_stud2 = degree
        elif isinstance(timeline_choose, TimelineTourism):
            #For tours
            for tour in timeline_g.list_tour:
                if item_1 in tour.get_all_items():
                    timeline_stud1 = tour
                if item_2 in tour.get_all_items():
                    timeline_stud2 = tour

        #remove item1
        timeline_stud1.remove_item(item_1, day_1, hour_1, lenght_slot_1)
        #remove item2
        timeline_stud2.remove_item(item_2, day_2, hour_2, lenght_slot_2)

        #add item1 in the new position
        timeline_stud1.add_item(item_1, day_2, hour_2, lenght_slot_1)
        #add item2 in the new position
        timeline_stud2.add_item(item_2, day_1, hour_1, lenght_slot_2)
    else:
        raise Exception("Invalid mode")

#move an item in a random (or not) position
def move_local(timeline_g, idx_timeline_choose, mode, random_slot = True, day_choose = None, hour_choose = None):
    if isinstance(timeline_g, GlobalUniversity):
        timeline_choose = timeline_g.list_degree[idx_timeline_choose] if mode == 'cohort' else timeline_g.list_prof[idx_timeline_choose]
    elif isinstance(timeline_g, GlobalTourism):
        timeline_choose = timeline_g.list_tour[idx_timeline_choose] if mode == 'cohort' else timeline_g.list_guide[idx_timeline_choose]

    if random_slot:
        item_choose, day_choose, hour_choose, lenght_slot = find_random_item(timeline_choose)
    else:
        item_choose, day_choose, hour_choose, lenght_slot = find_random_item(timeline_choose, random_slot, day_choose, hour_choose)

    #move to a new time slot, if there is no empty slot the lecture is moved in the last valid random slot
    empty_slot = False
    explored_slots = np.array([[False for _ in range(timeline_choose.hours)] for _ in range(timeline_choose.days)]) 
    while not empty_slot and not np.all(explored_slots):

        day_new = random.randrange(timeline_choose.days)
        hour_new = random.randrange(timeline_choose.hours)
        explored_slots[day_new][hour_new] = True

        #check if the lecture can be moved in the selected slot (has enough "space")
        if hour_new + lenght_slot >= timeline_choose.hours:
            hour = hour_new
            while hour < timeline_choose.hours:
                explored_slots[day_new][hour] = True
                hour += 1
            continue

        #check if the lecture can be moved in the selected slot (has no overlap)
        overlap = False
        for hour in range(hour_new, hour_new + lenght_slot):
            if timeline_choose.timeline[day_new][hour] is not None:
                overlap = True
                break

        if not overlap:
            empty_slot = True

    if mode == 'cohort':
        if isinstance(timeline_choose, TimelineUniversity):
            prof = timeline_choose.get_prof(item_choose, day_choose, hour_choose)
        elif isinstance(timeline_choose, TimelineTourism):
            prof = timeline_choose.get_guide(item_choose, day_choose, hour_choose)

        #For student
        #remove the item from the old position
        timeline_choose.remove_item(item_choose, day_choose, hour_choose, lenght_slot)
        #add the item in the new position
        timeline_choose.add_item(item_choose, day_new, hour_new, lenght_slot)

        if isinstance(timeline_choose, TimelineUniversity):
            #For professors
            for p in timeline_g.list_prof:
                if p.name == prof:
                    timeline_prof = p
        elif isinstance(timeline_choose, TimelineTourism):
            #For guides
            for g in timeline_g.list_guide:
                if g.guide == prof:
                    timeline_prof = g

        #remove the item from the old position
        timeline_prof.remove_item(item_choose, day_choose, hour_choose, lenght_slot)
        #add the item in the new position
        timeline_prof.add_item(item_choose, day_new, hour_new, lenght_slot)

    elif mode == 'single':

        #For professors
        #remove the item from the old position
        timeline_choose.remove_item(item_choose, day_choose, hour_choose, lenght_slot)
        #add the item in the new position
        timeline_choose.add_item(item_choose, day_new, hour_new, lenght_slot)

        if isinstance(timeline_choose, TimelineUniversity):
            #For students
            for degree in timeline_g.list_degree:
                if item_choose in degree.get_all_items():
                    timeline_stud = degree
        elif isinstance(timeline_choose, TimelineTourism):
            #For tours
            for tour in timeline_g.list_tour:
                if item_choose in tour.get_all_items():
                    timeline_stud = tour
        
        if timeline_stud:
            timeline_stud.remove_item(item_choose, day_choose, hour_choose, lenght_slot)
            timeline_stud.add_item(item_choose, day_new, hour_new, lenght_slot)
        


#switch two days of the timeline
def switch_days(timeline_g, idx_timeline_choose, day_1, day_2, mode):


    if isinstance(timeline_g, GlobalUniversity):
        timeline_choose = timeline_g.list_degree[idx_timeline_choose] if mode == 'cohort' else timeline_g.list_prof[idx_timeline_choose]
    elif isinstance(timeline_g, GlobalTourism):
        timeline_choose = timeline_g.list_tour[idx_timeline_choose] if mode == 'cohort' else timeline_g.list_guide[idx_timeline_choose]

    # for students
    timeline_d1 = copy.deepcopy(timeline_choose.timeline[day_1])
    timeline_d2 = copy.deepcopy(timeline_choose.timeline[day_2])
    timeline_choose.timeline[day_1] = timeline_d2
    timeline_choose.timeline[day_2] = timeline_d1

    if print_:
        print("Swapping days:", day_1, "and", day_2, "in timeline:", timeline_choose)
        print(timeline_choose.timeline[day_1])

    # for professors
    prev1 = -1
    prev2 = -1
    for hour in range(len(timeline_d1)):
        item_d1 = timeline_d1[hour]
        if item_d1 is not None and item_d1 != prev1:
            prev1 = item_d1
            if print_:
                print("Hour:", hour)
                print(f"Item day {day_1}:", item_d1)
            _, _, _, lenght_slot = find_random_item(timeline_choose, False, day_2, hour)

            if isinstance(timeline_choose, TimelineUniversity):
                prof = timeline_choose.get_prof(item_d1, day_2, hour)
                for p in timeline_g.list_prof:
                    if p.name == prof:
                        if print_:
                            print("Timeline professor 1:", p)
                        p.remove_item(item_d1, day_1, hour, lenght_slot)
                        p.add_item(item_d1, day_2, hour, lenght_slot)
                        if print_:
                            print("MODIFIED Timeline professor 1:", p)
                        break
            elif isinstance(timeline_choose, TimelineTourism):
                prof = timeline_choose.get_guide(item_d1, day_2, hour)
                for p in timeline_g.list_guide:
                    if p.guide == prof:
                        if print_:
                            print("Timeline guide 1:", p)
                        p.remove_item(item_d1, day_1, hour, lenght_slot)
                        p.add_item(item_d1, day_2, hour, lenght_slot)
                        if print_:
                            print("MODIFIED Timeline guide 1:", p)
                        break

        item_d2 = timeline_d2[hour]
        if item_d2 is not None and item_d2 != prev2:
            prev2 = item_d2
            if print_:
                print("Hour:", hour)
                print(f"Item day {day_2}:", item_d2)
            _, _, _, lenght_slot = find_random_item(timeline_choose, False, day_1, hour)


            if isinstance(timeline_choose, TimelineUniversity):
                prof = timeline_choose.get_prof(item_d2, day_1, hour)
                for p in timeline_g.list_prof:
                    if p.name == prof:
                        if print_:
                            print("Timeline professor 2:", p)
                        p.remove_item(item_d2, day_2, hour, lenght_slot)
                        p.add_item(item_d2, day_1, hour, lenght_slot)
                        if print_:
                            print("MODIFIED Timeline professor 2:", p)
                        break
            elif isinstance(timeline_choose, TimelineTourism):
                prof = timeline_choose.get_guide(item_d2, day_1, hour)
                for p in timeline_g.list_guide:
                    if p.guide == prof:
                        if print_:
                            print("Timeline guide 2:", p)
                        p.remove_item(item_d2, day_2, hour, lenght_slot)
                        p.add_item(item_d2, day_1, hour, lenght_slot)
                        if print_:
                            print("MODIFIED Timeline guide 2:", p)
                        break


#solution_obj: object of the class Timeline
#
#return a new perturbated solution object of the class Timeline
def perturbate(solution_g, mode, idx_timeline_choose = None):
    if print_:
        print("index timeline chosen PERTURBATE:", idx_timeline_choose)
    perturbated_solution_g = copy.deepcopy(solution_g)
    
    if idx_timeline_choose is None:
        if mode == 'cohort':
            if isinstance(perturbated_solution_g, GlobalUniversity):
                idx_timeline_choose = random.randrange(len(perturbated_solution_g.list_degree))
            elif isinstance(perturbated_solution_g, GlobalTourism):
                idx_timeline_choose = random.randrange(len(perturbated_solution_g.list_tour))
        elif mode == 'single':
            if isinstance(perturbated_solution_g, GlobalUniversity):
                idx_timeline_choose = random.randrange(len(perturbated_solution_g.list_prof))
            elif isinstance(perturbated_solution_g, GlobalTourism):
                idx_timeline_choose = random.randrange(len(perturbated_solution_g.list_guide))
        else:
            raise Exception("Invalid mode")
    
    # if isinstance(perturbated_solution_g, TimelineTourism):
    #     perturbated_solution_g.clear_distance()

    operation = random.randrange(2)

    if operation == 0:
        swap_local(perturbated_solution_g, idx_timeline_choose, mode)
    elif operation == 1:
        move_local(perturbated_solution_g, idx_timeline_choose, mode)
    else:
        raise Exception("Invalid operation number")
    

    # if isinstance(perturbated_solution_g, TimelineTourism):
    #     perturbated_solution_g.compute_distance()

    if print_:
        print("***"*10)
        print("Perturbated solution generated with operation:", operation)
        print(perturbated_solution_g)
        print("***"*10)
    return perturbated_solution_g


#solution_obj: object of the class Timeline
#
#return a new perturbated solution object of the class Timeline
def perturbate_with_heu(solution_g, mode):

    if isinstance(solution_g, GlobalUniversity):
        if mode == 'cohort':
            scores = solution_g.get_fairness_scores_dict_degree()

            min_score = min(scores.values())

            for idx_timeline_choose, timeline_choose in enumerate(solution_g.list_degree):
                if scores[(timeline_choose.degree, timeline_choose.year)] == min_score:
                    break

        elif mode == 'single':
            scores = solution_g.get_fairness_scores_dict_prof()

            min_score = min(scores.values())

            for idx_timeline_choose, timeline_choose in enumerate(solution_g.list_prof):
                if scores[timeline_choose.name] == min_score:
                    break
    elif isinstance(solution_g, GlobalTourism):
        if mode == 'cohort':
            scores = solution_g.get_fairness_scores_dict_tour()

            min_score = min(scores.values())

            for idx_timeline_choose, timeline_choose in enumerate(solution_g.list_tour):
                if scores[timeline_choose.tour_id] == min_score:
                    break

        elif mode == 'single':
            scores = solution_g.get_fairness_scores_dict_guide()

            min_score = min(scores.values())

            for idx_timeline_choose, timeline_choose in enumerate(solution_g.list_guide):
                if scores[timeline_choose.guide] == min_score:
                    break
    
    if print_:
        print("index timeline chosen PERTURBATE HEU:", idx_timeline_choose)
        print("Timeline chosen PERTURBATE HEU:", timeline_choose)
    
    #are we fair? 
    if timeline_choose.fairness_score() == 0:
        #YES, search other fair solutions
        return perturbate(solution_g, mode, idx_timeline_choose)
    else:
        #NO, try to make it fair
        perturbated_solution_g = copy.deepcopy(solution_g)
        # if isinstance(perturbated_solution_g, TimelineTourism):
        #     perturbated_solution_g.clear_distance()

        #PROFESSORS
        if isinstance(timeline_choose, TimelineProfessors):
            #FIRST: check if mandatory are satisfied
            if not timeline_choose.satisfied_mandatory():
                #NO
                list_unsatisfied_constraints = timeline_choose.find_overlaps()
                
            else:
                #YES
                list_unsatisfied_constraints = timeline_choose.get_unsatisfied_constraints()
                if len(list_unsatisfied_constraints) == 0:
                    #the only unsatisfied is two consecutive days
                    move_local(perturbated_solution_g,idx_timeline_choose, mode) #move randomly
                    return perturbated_solution_g
                
            
            #SECOND: choose randomly an unsatisfied constraint
            day, hour = list_unsatisfied_constraints[random.randrange(len(list_unsatisfied_constraints))]
            move_local(perturbated_solution_g,idx_timeline_choose, mode, False, day, hour)
            
            return perturbated_solution_g

        #STUDENTS
        elif isinstance(timeline_choose, TimelineStudents):
            #FIRST: check if mandatory are satisfied
            if not timeline_choose.satisfied_mandatory():
                #NO
                list_unsatisfied_constraints = timeline_choose.find_overlaps()
                day, hour = list_unsatisfied_constraints[random.randrange(len(list_unsatisfied_constraints))]
                move_local(perturbated_solution_g,idx_timeline_choose, mode, False, day, hour)

                return perturbated_solution_g
            else:
                #YES
                #check if there is a day without lunch break
                if not timeline_choose.has_lunch_break():
                    #YES
                    list_days = timeline_choose.find_day_without_lunch_break()
                    day = list_days[random.randrange(len(list_days))]
                    hour = 4 #lunch break span on 3 hours, minimun lesson lenght of 2 hours, so we can take the "middle" slot
                    move_local(perturbated_solution_g,idx_timeline_choose, mode, False, day, hour)
                    #return perturbated_solution DECOMMENT TO SOLVE IN ORDER AND ONE AT TIME
                else:
                    #NO
                    #solo lesson in a day
                    num_one_lesson_per_day = timeline_choose.alone_lecture()

                    #check if there are gap during the day
                    list_gaps_in_day = timeline_choose.num_gaps_in_days()
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
                                hour = random.randrange(timeline_choose.hours)
                                if timeline_choose.timeline[day][hour] is not None:
                                    empty_slot = False
                        move_local(perturbated_solution_g,idx_timeline_choose, mode, False, day, hour)
                        #return perturbated_solution DECOMMENT TO SOLVE IN ORDER AND ONE AT TIME
                    
                    #check if there are gap during the week
                    num_gaps_in_week, day_lecture = timeline_choose.num_gaps_in_week()
                    if num_gaps_in_week > 0:
                        day = day_lecture[random.randrange(len(day_lecture))]
                        list_free_days = [x for x in range(timeline_choose.days) if x not in day_lecture]
                        day_free = list_free_days[random.randrange(len(list_free_days))]

                        #switch_days(perturbated_solution_g,idx_timeline_choose, day, day_free, mode)#TODO:decomment
                        #return perturbated_solution DECOMMENT TO SOLVE IN ORDER AND ONE AT TIME

                return perturbated_solution_g
                
        #GUIDES
        elif isinstance(timeline_choose, TimelineGuides):
            #FIRST: check if mandatory are satisfied
            if not timeline_choose.satisfied_mandatory():
                #NO
                list_unsatisfied_constraints = timeline_choose.find_overlaps()
            else:
                #YES
                list_unsatisfied_constraints = timeline_choose.get_unsatisfied_constraints()

            if len(list_unsatisfied_constraints) == 0:
                #unstatified during the path between two pois
                return perturbate(solution_g, mode, idx_timeline_choose)

            #SECOND: choose randomly an unsatisfied constraint
            day, hour = list_unsatisfied_constraints[random.randrange(len(list_unsatisfied_constraints))]
            move_local(perturbated_solution_g,idx_timeline_choose, mode, False, day, hour)
            

            #perturbated_solution.compute_distance()
            return perturbated_solution_g

        #TOURS
        elif isinstance(timeline_choose, TimelineTours):
            #FIRST: check if mandatory are satisfied
            if not timeline_choose.satisfied_mandatory():
                #NO
                list_unsatisfied_constraints = timeline_choose.find_overlaps()
                day, hour = list_unsatisfied_constraints[random.randrange(len(list_unsatisfied_constraints))]
                move_local(perturbated_solution_g,idx_timeline_choose, mode, False, day, hour)
            else:
                #YES
                #move "solo" visit to populated days
                modified = False

                #check if there are gap during the day
                list_gaps_in_day = timeline_choose.num_gaps_in_days()
                if len(list_gaps_in_day) > 0:
                    #solve first day with more gaps
                    list_gaps_in_day.sort(key = lambda x: x[1], reverse = True)
                    day = list_gaps_in_day[0][0]
                    empty_slot = True
                    while empty_slot:
                        hour = random.randrange(timeline_choose.hours)
                        if timeline_choose.timeline[day][hour] is not None:
                            empty_slot = False
                    move_local(perturbated_solution_g, idx_timeline_choose, mode, False, day, hour)
                    modified = True
                    #perturbated_solution.compute_distance()
                    #return perturbated_solution DECOMMENT TO SOLVE IN ORDER AND ONE AT TIME
                
                #check if there are gap during the week
                num_gaps_in_week, day_lecture = timeline_choose.num_gaps_in_week()
                if num_gaps_in_week > 0:
                    choose_rand = random.randrange(2)
                    if choose_rand == 0:
                        index = 0
                    else:
                        index = -1
                    day = day_lecture[index]
                    list_free_days = [x for x in range(timeline_choose.days) if x not in day_lecture]
                    day_free = list_free_days[random.randrange(len(list_free_days))]
                    
                    switch_days(perturbated_solution_g,idx_timeline_choose, day, day_free, mode)#TODO:decomment
                    modified = True
                    #perturbated_solution.compute_distance()
                    #return perturbated_solution DECOMMENT TO SOLVE IN ORDER AND ONE AT TIME
                
                if not modified:
                    return perturbate(solution_g, mode, idx_timeline_choose)

            #perturbated_solution.compute_distance()
            return perturbated_solution_g
        
    
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
def performSa(curr_sol, paretoSet, paretoFront, initialTemp, finalTemp, alpha, maxPerturbation, mode, heuristic = False):
    temperature = initialTemp
    c = 0
    while temperature > finalTemp:
        for _ in range(maxPerturbation):
            if heuristic:
                perturb_sol = perturbate_with_heu(curr_sol, mode)
            else:
                perturb_sol = perturbate(curr_sol, mode)
        
            if perturb_sol == curr_sol:
                continue

            if print_:
                print("Pareto Front size: ", len(paretoFront))
                print("Pareto Set size: ", len(paretoSet))
                print("Current Temperature: ", temperature, "   Temp step: ", c)

            p = acceptanceProbability(curr_sol, perturb_sol, temperature, paretoFront)

            if random.uniform(0, 1) < p :
                updateParetoSet(perturb_sol, paretoSet)
                curr_sol = perturb_sol

        c += 1
        temperature = initialTemp - alpha * c
        

    return paretoSet


def getBestSolLocal(curr_sol, initialTemp, finalTemp, alpha, maxPerturbation, mode, heuristic = False):
    sol = copy.deepcopy(curr_sol)
    paretoSet = set()
    paretoSet.add(sol)
    paretoFront = computeParetoFront(paretoSet)

    paretoSet = performSa(sol, paretoSet, paretoFront, initialTemp, finalTemp, alpha, maxPerturbation, mode, heuristic)

    best_sol = max(paretoSet, key = lambda x: x.fairness_score())

    return best_sol