import math
import random

def computeParetoFront(paretoSet):  #new
    paretoFront = set()
    for p in paretoSet:
        isDominated = False
        for q in paretoSet:
            if p.dominate(q):
                isDominated = True
                break
        if not isDominated:
            paretoFront.add(p)
        
        #paretoFront.add(p)

    return paretoFront


def energy_(perturbate_solution, paretoFront): #ok
    energy = 0

    for p in paretoFront:
        if p.dominate(perturbate_solution): 
            energy += 1
    return energy


def energy(perturbate_solution, paretoSet):  #new
    paretoFront = computeParetoFront(paretoSet)
    return energy_(perturbate_solution, paretoFront)


def energyDifference(current_solution, perturbated_solution, paretoFront):        #new
    pSet = set()
    pSet.add(current_solution)
    pSet.add(perturbated_solution)

    pFront_tmp = computeParetoFront(pSet)
    for p in pFront_tmp:
        paretoFront.add(p)
    
    currEnergy = energy_(current_solution, paretoFront)
    newEnergy = energy_(perturbated_solution, paretoFront)

    energyDiff = (newEnergy - currEnergy) / len(paretoFront)

    return energyDiff


def acceptanceProbability(current_solution, perturbated_solution, temperature, paretoFront): #new
    #TODO: forse aggiungere qualcosa qui
    energyDiff = energyDifference(current_solution, perturbated_solution, paretoFront)
    prob = math.exp(-energyDiff / temperature)
    return min(prob, 1)


# timeln: object of the class Timeline -> do not modify the object!
def find_random_item(timeline, random_slot = True, day_choose = None, hour_choose = None):

    if random_slot:
        empty_slot = True
        while empty_slot:
            day_choose = random.randrange(timeline.days)
            hour_choose = random.randrange(timeline.hours)
            if timeline.timeline[day_choose][hour_choose] is not None:
                empty_slot = False

    #find the lenght of the lecture, if there is more then one lecture in the selected slot the first one is taken
    item = timeline.timeline[day_choose][hour_choose].split('+')[0]

    #take the lenght (in hours) of the lessons
    length_slot = 1
    #check if there is the same item before the slot selected
    item_before = True
    hour = hour_choose - 1
    while hour >= 0 and item_before:
        if timeline.timeline[day_choose][hour] is None:
            item_before = False
        else:
            if item in timeline.timeline[day_choose][hour].split('+'):
                length_slot += 1
                hour -= 1
            else:
                item_before = False

    hour_start = hour_choose - length_slot + 1 #hour_star is the first hour in which the item is present

    #check if there is the same item after the slot selected
    item_after = True
    hour = hour_choose + 1
    while hour < timeline.hours and item_after:
        if timeline.timeline[day_choose][hour] is None:
            item_after = False
        else:
            if item in timeline.timeline[day_choose][hour].split('+'):
                length_slot += 1
                hour += 1
            else:
                item_after = False

    return item, day_choose, hour_start, length_slot


def updateParetoSet(perturbated_solution, paretoSet): #new
    isDominated = False
    dominatedSet = set()

    for p in paretoSet:
        if perturbated_solution.dominate(p):
            dominatedSet.add(p)
        if p.dominate(perturbated_solution):
            isDominated = True

    if len(dominatedSet) > 0:
        paretoSet.difference_update(dominatedSet)
    if not isDominated:
        paretoSet.add(perturbated_solution)