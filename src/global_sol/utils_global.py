import random
import copy
import numpy as np
import time
import sys
import os
sys.path.append(os.path.abspath(".."))
from utils import *


print_ = False
print_stats = False

#swap two random elements of the timeline and the professors
def swap(timeline_g):
    #first delect timeline

    idx_timeline = random.randrange(len(timeline_g.list_degree))

    timeline_chosen = timeline_g.list_degree[idx_timeline]

    if print_: print("TIMELINE CHOSEN:\n", timeline_chosen)

    possible_swap = False
    timeout = timeline_chosen.days * timeline_chosen.hours * 10

    item_in_timeline = set()
    for day in range(timeline_chosen.days):
        for hour in range(timeline_chosen.hours):
            if timeline_chosen.timeline[day][hour] is not None:
                item_in_timeline.add(timeline_chosen.timeline[day][hour])

    if len(item_in_timeline) < 3:
        return
    
    while not possible_swap and timeout > 0:
        item_1, day_1, hour_1, lenght_slot_1 = find_random_item(timeline_chosen)
        item_2, day_2, hour_2, lenght_slot_2 = find_random_item(timeline_chosen)

        if item_1 == item_2:
            continue
        else:
            if lenght_slot_1 == lenght_slot_2:
                possible_swap = True
            elif lenght_slot_1 + hour_2 < timeline_chosen.hours and lenght_slot_2 + hour_1 < timeline_chosen.hours:
                possible_swap = True
            else:
                timeout -= 1
                continue

    if print_: print("ITEMS SELECTED: ", item_1, item_2)

    #retrive the professor
    prof1 = timeline_chosen.get_prof(item_1, day_1, hour_1)
    prof2 = timeline_chosen.get_prof(item_2, day_2, hour_2)
    
    #For students

    #remove item1
    timeline_chosen.remove_item(item_1, day_1, hour_1, lenght_slot_1) 
    #remove item2
    timeline_chosen.remove_item(item_2, day_2, hour_2, lenght_slot_2)

    #add item1 in the new position (ex item2)
    timeline_chosen.add_item(item_1, day_2, hour_2, lenght_slot_1)
    #add item2 in the new position (ex item1)
    timeline_chosen.add_item(item_2, day_1, hour_1, lenght_slot_2)


    #For professors
    if print_: print("PROFESSORS SELECTED: ", prof1, prof2)

    for prof in timeline_g.list_prof:
        if prof.name == prof1:
            timeline_prof1 = prof
        if prof.name == prof2:
            timeline_prof2 = prof

    #remove item1
    timeline_prof1.remove_item(item_1, day_1, hour_1, lenght_slot_1)
    #remove item2
    timeline_prof2.remove_item(item_2, day_2, hour_2, lenght_slot_2)

    #add item1 in the new position
    timeline_prof1.add_item(item_1, day_2, hour_2, lenght_slot_1)
    #add item2 in the new position
    timeline_prof2.add_item(item_2, day_1, hour_1, lenght_slot_2)


    if print_: print("TIMELINE AFTER SWAP:\n", timeline_chosen)
    if print_: print("PROFESSORS AFTER SWAP:\n", timeline_prof1, timeline_prof2)


#move an item in a random (or not) position
def move(timeline_g, random_slot = True, day_choose = None, hour_choose = None):

    idx_timeline = random.randrange(len(timeline_g.list_degree))

    timeline_chosen = timeline_g.list_degree[idx_timeline]

    if print_: print("TIMELINE CHOSEN:\n", timeline_chosen)

    if random_slot:
        item_choose, day_choose, hour_choose, lenght_slot = find_random_item(timeline_chosen)
    else:
        item_choose, day_choose, hour_choose, lenght_slot = find_random_item(timeline_chosen, random_slot, day_choose, hour_choose)

    #move to a new time slot, if there is no empty slot the lecture is moved in the last valid random slot
    empty_slot = False
    explored_slots = np.array([[False for _ in range(timeline_chosen.hours)] for _ in range(timeline_chosen.days)])
    while not empty_slot and not np.all(explored_slots):

        day_new = random.randrange(timeline_chosen.days)
        hour_new = random.randrange(timeline_chosen.hours)
        explored_slots[day_new][hour_new] = True

        #check if the lecture can be moved in the selected slot (has enough "space")
        if hour_new + lenght_slot >= timeline_chosen.hours:
            hour = hour_new
            while hour < timeline_chosen.hours:
                explored_slots[day_new][hour] = True
                hour += 1
            continue

        #check if the lecture can be moved in the selected slot (has no overlap)
        overlap = False
        for hour in range(hour_new, hour_new + lenght_slot):
            if timeline_chosen.timeline[day_new][hour] is not None:
                overlap = True
                break

        if not overlap:
            empty_slot = True

    prof_item = timeline_chosen.get_prof(item_choose, day_choose, hour_choose)

    if print_: print("ITEM SELECTED: ", item_choose, "\nPROFESSOR: ", prof_item)

    #For students

    #remove the item from the old position
    timeline_chosen.remove_item(item_choose, day_choose, hour_choose, lenght_slot)
    #add the item in the new position
    timeline_chosen.add_item(item_choose, day_new, hour_new, lenght_slot)

    #For professors
    for prof in timeline_g.list_prof:
        if prof.name == prof_item:
            timeline_prof = prof

    #remove the item from the old position
    timeline_prof.remove_item(item_choose, day_choose, hour_choose, lenght_slot)
    #add the item in the new position
    timeline_prof.add_item(item_choose, day_new, hour_new, lenght_slot)

    if print_: print("TIMELINE AFTER MOVE:\n", timeline_chosen)
    if print_: print("PROFESSORS AFTER MOVE:\n", timeline_prof)

#return a new perturbated solution object 
def perturbate(solution_obj):
    perturbated_solution = copy.deepcopy(solution_obj)

    operation = random.randrange(2)#3)

    if operation == 0:
        if print_: print("\n##################\tSWAP\t##################")
        swap(perturbated_solution)
    elif operation == 1:
        if print_: print("\n##################\tMOVE\t##################")
        move(perturbated_solution)
    else:
        raise Exception("Invalid operation number")


    return perturbated_solution

#
# curr_sol: current solution object of the class Timeline
# paretoSet: empty pareto set, is a set() object
# initialTemp: initial temperature, int
# finalTemp: final temperature, int
# alpha: alpha, float  
# maxPerturbation: max perturbation, int
# heuristic: boolean, True if you want to use the heuristic (fairness), False if not
def performSa(curr_sol, paretoSet, paretoFront, initialTemp, finalTemp, alpha, maxPerturbation, seed, heuristic = False):
    temperature = initialTemp
    c = 0
    if print_stats:
        time_init = time.time()
        fd = open(f"stats_{seed}.csv", "w")
        fd.write("Temperature,Time,Fairness\n")
    
    while temperature > finalTemp:
        for _ in range(maxPerturbation):
            perturbSol = perturbate(curr_sol)
            
            if perturbSol == curr_sol:
                continue

            if print_:
                print("Pareto Front size: ", len(paretoFront))
                print("Pareto Set size: ", len(paretoSet))

            prob = acceptanceProbability(curr_sol, perturbSol, temperature, paretoFront)

            if random.uniform(0, 1) < prob:
                updateParetoSet(perturbSol, paretoSet)
                #paretoFront = computeParetoFront(paretoSet)
                curr_sol = copy.deepcopy(perturbSol)
        
        c += 1
        if print_stats:
            best_sol = max(paretoSet, key = lambda x: x.fairness_score())
            print("Temperature: ", temperature)
            print(best_sol.getSingleFairnessScore())
            print(best_sol.fairness_score())
            fd.write(str(temperature) + ", " + str(time.time() - time_init) + ", " + str(best_sol.fairness_score()) + "\n")

        temperature = initialTemp - alpha * c

        
    if print_stats:
        fd.close()

    return paretoSet



def getBestSol(curr_sol, initialTemp, finalTemp, alpha, maxPerturbation, seed='', heuristic = False):
    sol = copy.deepcopy(curr_sol)
    paretoSet = set()
    paretoSet.add(sol)
    paretoFront = computeParetoFront(paretoSet)

    paretoSet = performSa(sol, paretoSet, paretoFront, initialTemp, finalTemp, alpha, maxPerturbation, seed, heuristic)

    best_sol = max(paretoSet, key = lambda x: x.fairness_score())
    
    return best_sol