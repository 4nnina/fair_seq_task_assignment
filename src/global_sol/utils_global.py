import random
import copy
import numpy as np
import time
import sys
import os
sys.path.append(os.path.abspath(".."))
from utils import *
from global_sol.utils_local import perturbate_with_heu
from global_sol.data_classes_global import GlobalUniversity, GlobalTourism


print_ = False
print_stats = False

#swap two random elements of the timeline and the professors
def swap(timeline_g):
    #first delect timeline

    if isinstance(timeline_g, GlobalUniversity):

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

    elif isinstance(timeline_g, GlobalTourism):
        idx_timeline = random.randrange(len(timeline_g.list_tour))

        timeline_chosen = timeline_g.list_tour[idx_timeline]

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

        #retrive the guide
        prof1 = timeline_chosen.get_guide(item_1, day_1, hour_1)
        prof2 = timeline_chosen.get_guide(item_2, day_2, hour_2)
        
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

        for prof in timeline_g.list_guide:
            if prof.guide == prof1:
                timeline_prof1 = prof
            if prof.guide == prof2:
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

    if isinstance(timeline_g, GlobalUniversity):
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

    elif isinstance(timeline_g, GlobalTourism):
        idx_timeline = random.randrange(len(timeline_g.list_tour))

        timeline_chosen = timeline_g.list_tour[idx_timeline]

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

        prof_item = timeline_chosen.get_guide(item_choose, day_choose, hour_choose)

        if print_: print("ITEM SELECTED: ", item_choose, "\nPROFESSOR: ", prof_item)

        #For students

        #remove the item from the old position
        timeline_chosen.remove_item(item_choose, day_choose, hour_choose, lenght_slot)
        #add the item in the new position
        timeline_chosen.add_item(item_choose, day_new, hour_new, lenght_slot)

        #For professors
        for prof in timeline_g.list_guide:
            if prof.guide == prof_item:
                timeline_prof = prof

        #remove the item from the old position
        timeline_prof.remove_item(item_choose, day_choose, hour_choose, lenght_slot)
        #add the item in the new position
        timeline_prof.add_item(item_choose, day_new, hour_new, lenght_slot)

        if print_: print("TIMELINE AFTER MOVE:\n", timeline_chosen)
        if print_: print("PROFESSORS AFTER MOVE:\n", timeline_prof)

#move an item in a random (or not) position
def move_validity(timeline_g, idx_timeline = None, day_choose = None, hour_choose = None):

    #invalid timeline
    #idx_timeline = random.randrange(len(timeline_g.list_degree))
    if isinstance(timeline_g, GlobalUniversity):

        timeline_chosen = timeline_g.list_degree[idx_timeline]

        if print_: print("TIMELINE CHOSEN:\n", timeline_chosen)

        item_choose, day_choose, hour_choose, lenght_slot = find_random_item(timeline_chosen, False, day_choose, hour_choose)

        prof_item = timeline_chosen.get_prof(item_choose, day_choose, hour_choose)
        if print_: print("ITEM SELECTED: ", item_choose, "\nPROFESSOR: ", prof_item)

        #For professors
        for prof in timeline_g.list_prof:
            if prof.name == prof_item:
                timeline_prof = prof

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
            #student
            for hour in range(hour_new, hour_new + lenght_slot):
                if timeline_chosen.timeline[day_new][hour] is not None:
                    overlap = True
                    break

            #professor
            for hour in range(hour_new, hour_new + lenght_slot):
                if timeline_prof.timeline[day_new][hour] is not None:
                    overlap = True
                    break

            if not overlap:
                empty_slot = True
        

        #For students

        #remove the item from the old position
        timeline_chosen.remove_item(item_choose, day_choose, hour_choose, lenght_slot)
        #add the item in the new position
        timeline_chosen.add_item(item_choose, day_new, hour_new, lenght_slot)


        #remove the item from the old position
        timeline_prof.remove_item(item_choose, day_choose, hour_choose, lenght_slot)
        #add the item in the new position
        timeline_prof.add_item(item_choose, day_new, hour_new, lenght_slot)

        if print_: print("TIMELINE AFTER MOVE:\n", timeline_chosen)
        if print_: print("PROFESSORS AFTER MOVE:\n", timeline_prof)

    elif isinstance(timeline_g, GlobalTourism):
        timeline_chosen = timeline_g.list_tour[idx_timeline]

        if print_: print("TIMELINE CHOSEN:\n", timeline_chosen)

        item_choose, day_choose, hour_choose, lenght_slot = find_random_item(timeline_chosen, False, day_choose, hour_choose)

        prof_item = timeline_chosen.get_guide(item_choose, day_choose, hour_choose)
        if print_: print("ITEM SELECTED: ", item_choose, "\nPROFESSOR: ", prof_item)

        #For professors
        for prof in timeline_g.list_guide:
            if prof.guide == prof_item:
                timeline_prof = prof

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
            #student
            for hour in range(hour_new, hour_new + lenght_slot):
                if timeline_chosen.timeline[day_new][hour] is not None:
                    overlap = True
                    break

            #professor
            for hour in range(hour_new, hour_new + lenght_slot):
                if timeline_prof.timeline[day_new][hour] is not None:
                    overlap = True
                    break

            if not overlap:
                empty_slot = True
        

        #For students

        #remove the item from the old position
        timeline_chosen.remove_item(item_choose, day_choose, hour_choose, lenght_slot)
        #add the item in the new position
        timeline_chosen.add_item(item_choose, day_new, hour_new, lenght_slot)


        #remove the item from the old position
        timeline_prof.remove_item(item_choose, day_choose, hour_choose, lenght_slot)
        #add the item in the new position
        timeline_prof.add_item(item_choose, day_new, hour_new, lenght_slot)

        if print_: print("TIMELINE AFTER MOVE:\n", timeline_chosen)
        if print_: print("PROFESSORS AFTER MOVE:\n", timeline_prof)


def perturbate_validity(solution_obj):
    perturbated_solution = copy.deepcopy(solution_obj)

    if isinstance(solution_obj, GlobalUniversity):
        while not perturbated_solution.is_valid():

            if print_:
                print(" the solution is valid?", perturbated_solution.is_valid())

            degree_overlap, prof_overlap = perturbated_solution.find_overlaps()

            if print_:              
                print("Degree overlap: ", len(degree_overlap))
                print("Prof overlap: ", len(prof_overlap))

            if len(degree_overlap) > 0:
                #select a random degree with overlap
                key = random.choice(list(degree_overlap.keys()))
                degree, year = key
                day_choose, hour_choose = degree_overlap[key][0]
                move_validity(perturbated_solution, 
                            perturbated_solution.get_degree_index(degree, year), 
                            day_choose, hour_choose)
                
            if len(prof_overlap) > 0:
                #select a random professor with overlap
                prof_name = random.choice(list(prof_overlap.keys()))
                day_choose, hour_choose = prof_overlap[prof_name][0]

                #select the timeline where there is the overlap
                for degree in perturbated_solution.list_degree:
                    slot = degree.timeline[day_choose][hour_choose]
                    #get_prof(self, item, day, hour)
                    if slot is not None:
                        items = slot.split('+')
                        for i in items:
                            if degree.get_prof(i, day_choose, hour_choose) == prof_name:
                                degree_index = perturbated_solution.get_degree_index(degree.degree, degree.year)
                                break 
                        
                move_validity(perturbated_solution, 
                            degree_index, 
                            day_choose, hour_choose)
    
    elif isinstance(solution_obj, GlobalTourism):
        while not perturbated_solution.is_valid():
            if print_:
                print(" the solution is valid?", perturbated_solution.is_valid())

            tour_overlap, guide_overlap = perturbated_solution.find_overlaps()

            if print_:
                print("Tour overlap: ", len(tour_overlap))
            if print_:
                print("Guide overlap: ", len(guide_overlap))

            if len(tour_overlap) > 0:
                #select a random tour with overlap
                key = random.choice(list(tour_overlap.keys()))
                tour_id = key
                day_choose, hour_choose = tour_overlap[key][0]
                move_validity(perturbated_solution, 
                            perturbated_solution.get_tour_index(tour_id), 
                            day_choose, hour_choose)
                
            if len(guide_overlap) > 0:
                #select a random guide with overlap
                guide = random.choice(list(guide_overlap.keys()))
                day_choose, hour_choose = guide_overlap[guide][0]

                #select the timeline where there is the overlap
                for tour in perturbated_solution.list_tour:
                    slot = tour.timeline[day_choose][hour_choose]
                    #get_guide(self, item, day, hour)
                    if slot is not None:
                        items = slot.split('+')
                        for i in items:
                            if tour.get_guide(i, day_choose, hour_choose) == guide:
                                tour_index = perturbated_solution.get_tour_index(tour.tour_id)
                                break 
                        
                move_validity(perturbated_solution, 
                            tour_index, 
                            day_choose, hour_choose)
        
    return perturbated_solution

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

def perturbate_with_heu_g(solution_obj):
    perturbated_solution = copy.deepcopy(solution_obj)

    operation = random.randrange(2)#3)

    if operation == 0:
        perturbated_solution= perturbate_with_heu(perturbated_solution,'cohort')
    elif operation == 1:
        perturbated_solution = perturbate_with_heu(perturbated_solution,'single')
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
def performSa(curr_sol, paretoSet, paretoFront, initialTemp, finalTemp, alpha, maxPerturbation, seed, heuristic = False,file=''):
    temperature = initialTemp
    c = 0
    if print_stats:
        time_init = time.time()
        fd = open(f"{file}stats_{seed}.csv", "w")
        fd.write("Temperature,Time,avg_p,std_p,avg_d,std_d,avg,std\n")
    
    while temperature > finalTemp:
        for _ in range(maxPerturbation):
            if not heuristic:
                perturbSol = perturbate(curr_sol)
            else:
                perturbSol = perturbate_with_heu_g(curr_sol)
            #perturbSol = perturbate(curr_sol)
            
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
            avg_p=best_sol.avg_fairness_prof()
            std_p=best_sol.std_fairness_prof()
            avg_d=best_sol.avg_fairness_degree()
            std_d=best_sol.std_fairness_degree()
            avg=best_sol.avg_fairness()
            std=best_sol.std_fairness()
            fd.write(f'{temperature},{time.time() - time_init},{avg_p},{std_p},{avg_d},{std_d},{avg},{std}\n')

        temperature = initialTemp - alpha * c

        
    if print_stats:
        fd.close()

    return paretoSet



def getBestSol(curr_sol, initialTemp, finalTemp, alpha, maxPerturbation, seed='', heuristic = False,file=''):
    sol = copy.deepcopy(curr_sol)
    paretoSet = set()
    paretoSet.add(sol)
    paretoFront = computeParetoFront(paretoSet)

    paretoSet = performSa(sol, paretoSet, paretoFront, initialTemp, finalTemp, alpha, maxPerturbation, seed, heuristic, file=file)

    best_sol = max(paretoSet, key = lambda x: x.fairness_score())
    
    return best_sol



# ============================================================
# AMOSA UTILITIES
# ============================================================

def get_objectives(sol):
    """
    Restituisce il vettore degli obiettivi della soluzione.
    >>> ATTENZIONE: qui sto assumendo che esista sol.getObjectives()
    """
    return sol.get_list_obj()  # cambia se la tua API è diversa

def compute_objective_ranges(solutions):
    """
    Calcola min e max per ciascun obiettivo sull'insieme di soluzioni dato.
    Serve per normalizzare la Δdom come in AMOSA.
    """
    solutions = list(solutions)
    if not solutions:
        return [], []

    objs_list = [get_objectives(s) for s in solutions]
    m = len(objs_list[0])

    mins = [float('inf')] * m
    maxs = [float('-inf')] * m

    for vec in objs_list:
        for i, v in enumerate(vec):
            if v < mins[i]:
                mins[i] = v
            if v > maxs[i]:
                maxs[i] = v

    for i in range(m):
        if maxs[i] == mins[i]:
            maxs[i] = mins[i] + 1e-12

    return mins, maxs

def amount_of_domination(a, b, mins, maxs):
    if not a.dominate(b):
        return 0.0

    fa = get_objectives(a)
    fb = get_objectives(b)
    prod = 1.0
    m = len(fa)

    for i in range(m):
        diff = fa[i] - fb[i]
        if diff > 0:  
            R = maxs[i] - mins[i]
            prod *= (diff / R)

    return prod

def average_amount_of_domination(dominators, dominated, mins, maxs):
    if not dominators:
        return 0.0
    total = 0.0
    for p in dominators:
        total += amount_of_domination(p, dominated, mins, maxs)
    return total / len(dominators)

def min_domination_difference(new_pt, dominating_points, mins, maxs):
    if not dominating_points:
        return 0.0, None

    best_diff = float('inf')
    best_point = None

    for q in dominating_points:
        dom_q_new = amount_of_domination(q, new_pt, mins, maxs)
        dom_new_q = amount_of_domination(new_pt, q, mins, maxs)
        diff = abs(dom_q_new - dom_new_q)
        if diff < best_diff:
            best_diff = diff
            best_point = q

    return best_diff, best_point

def euclidean_distance(v1, v2):
    return math.sqrt(sum((a - b) ** 2 for a, b in zip(v1, v2)))


def cluster_archive(archive, HL):

    archive = list(archive)
    if len(archive) <= HL:
        return set(archive)

    while len(archive) > HL:
        mins, maxs = compute_objective_ranges(archive)
        
        best_i, best_j = None, None
        best_d = float('inf')
        for i in range(len(archive)):
            oi = get_objectives(archive[i])
            for j in range(i + 1, len(archive)):
                oj = get_objectives(archive[j])
                d = euclidean_distance(oi, oj)
                if d < best_d:
                    best_d = d
                    best_i, best_j = i, j

       
        i, j = best_i, best_j
        cand = [archive[i], archive[j]]
        avg_d = []
        for c in cand:
            oc = get_objectives(c)
            s = 0.0
            for other in archive:
                if other is c:
                    continue
                s += euclidean_distance(oc, get_objectives(other))
            avg_d.append(s / max(1, len(archive) - 1))

        if avg_d[0] <= avg_d[1]:
            del archive[i]
        else:
            del archive[j]

    return set(archive)



def performSa_AMOSA(curr_sol,archive,initialTemp,finalTemp,alpha,iters_per_temp,HL,SL,heuristic=False,seed=None,print_debug=False,file=''):
    if seed is not None:
        random.seed(seed)

    temp = initialTemp

    if print_stats:
        time_init = time.time()
        fd = open(f"{file}stats_{seed if seed is not None else 'run'}.csv", "w")
        fd.write("Temperature,Time,avg_p,std_p,avg_d,std_d,avg,std\n")
    

    if not archive:
        archive.add(copy.deepcopy(curr_sol))
    current_pt = random.choice(list(archive))

    while temp > finalTemp:
        for _ in range(iters_per_temp):
            if not heuristic:
                new_pt = perturbate(current_pt)
            else:
                new_pt = perturbate_with_heu_g(current_pt)

            if new_pt == current_pt:
                continue

            all_solutions = set(archive)
            all_solutions.add(current_pt)
            all_solutions.add(new_pt)
            mins, maxs = compute_objective_ranges(all_solutions)

            current_dominates_new = current_pt.dominate(new_pt)
            new_dominates_current = new_pt.dominate(current_pt)

            dominating_new = set()
            dominated_by_new = set()
            for p in archive:
                if p is new_pt or p is current_pt:
                    continue
                if p.dominate(new_pt):
                    dominating_new.add(p)
                elif new_pt.dominate(p):
                    dominated_by_new.add(p)

            k = len(dominating_new) # TODO

            if print_debug:
                print("Temp:", temp)
                print("Archive size:", len(archive))
                print("k dominating new:", k)

            
            #CASE 1: current dominates new
            if current_dominates_new:
               
                dominators = set(dominating_new)
                dominators.add(current_pt)
                delta_avg = average_amount_of_domination(dominators, new_pt, mins, maxs)

                prob = 1/(1+math.exp(delta_avg*temp))

                if random.random() < prob:
                    current_pt = new_pt  
                    

            #CASE 3: new domimates current
            elif new_dominates_current:
                
                if k > 0:
                    #Case 3(a): 
                    delta_min, best_arch = min_domination_difference(new_pt, dominating_new, mins, maxs)
                    prob = 1/(1+math.exp(-delta_min))

                    
                    if random.random() < prob and best_arch is not None:
                        current_pt = best_arch
                    else:
                        current_pt = new_pt
                else:
                    
                    if not dominated_by_new:
                        #Case 3(b)
                        current_pt = new_pt
                        archive.add(new_pt)
                        
                        if current_pt in archive:
                            archive.discard(current_pt)
                        elif len(archive)> SL:
                            archive = cluster_archive(archive, HL)
                        
                    else:
                        #Case 3(c)
                        current_pt = new_pt
                        archive.add(new_pt)
                        archive.difference_update(dominated_by_new)

            #CASE 2
            else:
                if k > 0:
                    #Case 2(a)
                    delta_avg = average_amount_of_domination(dominating_new, new_pt, mins, maxs)
                    prob = 1/(1+math.exp(-delta_avg *temp))
                    prob = min(1.0, max(0.0, prob))

                    if random.random() < prob:
                        current_pt = new_pt  
                else:
                    if not dominated_by_new:
                        #Case 2(b)
                        current_pt = new_pt
                        archive.add(new_pt)
                        if len(archive) > SL:
                            archive = cluster_archive(archive, HL)
                    else:
                        #Case 2(c)
                        current_pt = new_pt
                        archive.add(new_pt)
                        archive.difference_update(dominated_by_new)

            
            if len(archive) > SL:
                archive = cluster_archive(archive, HL)

        
        if print_stats:
            best_sol = max(archive, key=lambda x: x.fairness_score())  
            print("Temperature:", temp)
            print("Best fairness (scalar):", best_sol.fairness_score())
            avg_p=best_sol.avg_fairness_prof()
            std_p=best_sol.std_fairness_prof()
            avg_d=best_sol.avg_fairness_degree()
            std_d=best_sol.std_fairness_degree()
            avg=best_sol.avg_fairness()
            std=best_sol.std_fairness()
            fd.write(f'{temp},{time.time() - time_init},{avg_p},{std_p},{avg_d},{std_d},{avg},{std}\n')

        # raffreddamento geometrico
        temp *= alpha

    if len(archive)> SL:
        archive = cluster_archive(archive, HL)

    if print_stats:
        fd.close()

    return archive


def getBestSol_AMOSA(curr_sol,initialTemp,finalTemp,alpha,iters_per_temp, HL,SL,heuristic,seed=None,file=''):
    sol = copy.deepcopy(curr_sol)
    archive = set()
    archive.add(sol)

    archive = performSa_AMOSA(sol,archive,initialTemp,finalTemp,alpha,iters_per_temp,HL,SL,heuristic=heuristic,seed=seed,file=file )

    best_sol = max(archive, key=lambda x: x.fairness_score())

    return best_sol
