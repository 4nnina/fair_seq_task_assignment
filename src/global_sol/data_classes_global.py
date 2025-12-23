import copy
import sys
import os
import numpy as np
import math
sys.path.append(os.path.abspath(".."))
from local_sol.data_classes_local import TimelineProfessors, TimelineStudents, TimelineGuides, TimelineTours


verbose = False

###################################################################
#                                                                 #
#                           UNIVERSITY                            #
#                                                                 #
###################################################################

class GlobalUniversity():
    def __init__(self, list_prof, dict_degree):
        
        self.list_prof = []
        self.list_degree = []

        for degree in dict_degree:
            for year in dict_degree[degree]:
                if verbose: print("Degree: ", degree, " Year: ", year)
                timeline = TimelineStudents(degree, year)
                if verbose: print(timeline)
                self.list_degree.append(timeline)

        for prof in list_prof:
            if verbose: print("Professor: ", prof)
            timeline = TimelineProfessors(prof)
            self.list_prof.append(timeline)

        # convert the student one into professors
        #first step: clean prof timeline
        for prof in self.list_prof:
            prof.timeline = [[None for _ in range(prof.hours)] for _ in range(prof.days)]

        #second pupulate timeline
        for degree in self.list_degree:
            for day in range(degree.days):
                for hour in range(degree.hours):
                    items = degree.timeline[day][hour]
                    if items is not None:
                        if '+' in items:
                            item_list = items.split('+')
                        else:
                            item_list = [items]
                            
                        for i in item_list:
                            prof_slot = degree.get_prof(i,day,hour)
                        
                            for prof in self.list_prof:
                                if prof.name == prof_slot:
                                    if prof.timeline[day][hour] is not None:
                                        prof.timeline[day][hour] += '+' + i
                                    else:
                                        prof.timeline[day][hour] = i

    def fairness_score(self):
        prof_score = 0
        stud_score = 0

        for prof in self.list_prof:
            prof_score += prof.fairness_score()

        for degree in self.list_degree:
            stud_score += degree.fairness_score()


        return (prof_score/len(self.list_prof) + stud_score/len(self.list_degree))/2     

    def avg_fairness_degree(self):
        stud_score = []

        for degree in self.list_degree:
            stud_score.append(degree.fairness_score())
        
        return np.mean(np.array(stud_score))
    
    def avg_fairness_prof(self):
        prof_score = []

        for prof in self.list_prof:
            prof_score.append(prof.fairness_score())

        return np.mean(np.array(prof_score))
    
    def avg_fairness(self):
        return (self.avg_fairness_degree() + self.avg_fairness_prof())/2

    
    def get_fairness_scores_dict_prof(self):
        list_fairness = dict()
        for prof in self.list_prof:
            list_fairness[prof.name] = prof.fairness_score()
        return list_fairness
        
    def get_fairness_scores_dict_degree(self):
        list_fairness = dict()
        for degree in self.list_degree:
            list_fairness[(degree.degree, degree.year)] = degree.fairness_score()
        return list_fairness
    
    def std_fairness_degree(self):
        stud_score = []

        for degree in self.list_degree:
            stud_score.append(degree.fairness_score())
        
        return np.std(np.array(stud_score))
    
    def std_fairness_prof(self):
        prof_score = []

        for prof in self.list_prof:
            prof_score.append(prof.fairness_score())

        return np.std(np.array(prof_score))
    
    def std_fairness(self):
        avg_prof = self.avg_fairness_prof()
        avg_degree = self.avg_fairness_degree()

        prof_sq_mean = 0
        for prof in self.list_prof:
            prof_sq_mean += (prof.fairness_score()-avg_prof)**2

        degree_sq_mean = 0
        for degree in self.list_degree:
            degree_sq_mean += (degree.fairness_score()-avg_degree)**2

        return math.sqrt(prof_sq_mean/len(self.list_prof) + degree_sq_mean/len(self.list_degree))

    def get_list_obj(self):
        res = [self.avg_fairness_degree(), self.avg_fairness_degree(), self.avg_fairness()] #avgs
        res.append(self.std_fairness_degree())
        res.append(self.std_fairness_prof())
        res.append(self.std_fairness())

        return res


    
    def dominate(self, other):
        
        #if self.fairness_score() <= other.fairness_score():
        #    return False
        
        if self.avg_fairness() <= other.avg_fairness() or self.std_fairness() >= other.std_fairness():
            return False

        return True
        
        
    def __str__(self):
        out = ''
        for prof in self.list_prof:
            out += str(prof)+ f'\nFairness Score: {prof.fairness_score()}' + '\n'

        for degree in self.list_degree:
            out += str(degree)+ f'\nFairness Score: {degree.fairness_score()}' + '\n'
        
        return out
    
    def getSingleFairnessScore(self):
        out =  '^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n'
        out += '^                                            Detailed Fairness Score                                           ^\n'
        out += '^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n'

        for prof in self.list_prof:
            out +=  f'Prof Name: {str(prof.name)}\tFairness Score: {prof.fairness_score()}\t{int((1-prof.real_fairness_score()/prof.sum_contraints())*100)}%' + '\n'
        out += f'\tAverage Fairness Score: {self.avg_fairness_prof()}\n'
        out += f'\tStandard Deviation Fairness Score: {self.std_fairness_prof()}\n\n'

        for degree in self.list_degree:
            out += f'Degree Name: {str(degree.degree)}\tYear: {str(degree.year)}\tFairness Score: {degree.fairness_score()}' + '\n'
        out += f'\tAverage Fairness Score: {self.avg_fairness_degree()}\n'
        out += f'\tStandard Deviation Fairness Score: {self.std_fairness_degree()}\n'

        out += '\nAverage Fairness Score Overall: ' + str(self.avg_fairness()) + '\n'
        out += 'Standard Deviation Fairness Score Overall: ' + str(self.std_fairness()) + '\n'
        out += '^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n'

        return out

    def __eq__(self,other):
        if len(self.list_prof) != len(other.list_prof):
            return False
        if len(self.list_degree) != len(other.list_degree):
            return False

        for idx in range(len(self.list_prof)):
            if self.list_prof[idx] != other.list_prof[idx]:
                return False

        for idx in range(len(self.list_degree)):
            if self.list_degree[idx] != other.list_degree[idx]:
                return False
            
        return True
    
    def __hash__(self):
        return hash(str(self))
    
    def has_overlap(self):
        for degree in self.list_degree:
            if degree.has_overlap():
                return (True, 'stud')

        for prof in self.list_prof:
            if prof.has_overlap():
                return (True, 'prof')
            
        return (False,'')
    
    def find_overlaps(self):
        degree_overlap = dict()
        for degree in self.list_degree:
            if degree.has_overlaps():
                degree_overlap[(degree.degree, degree.year)] = degree.find_overlaps()

        prof_overlap = dict()
        for prof in self.list_prof:
            if prof.has_overlaps():
                prof_overlap[prof.name] = prof.find_overlaps()

        return degree_overlap, prof_overlap
    
    def get_degree_index(self, degree_name, year):
        for idx in range(len(self.list_degree)):
            if self.list_degree[idx].degree == degree_name and self.list_degree[idx].year == year:
                return idx
        return -1

    def is_valid(self) -> bool:
        for degree in self.list_degree:
            if not degree.is_valid():
                return False

        for prof in self.list_prof:
            if not prof.is_valid():
                return False
            
        return True    
 

###################################################################
#                                                                 #
#                             TOURISM                             #
#                                                                 #
###################################################################

   
class GlobalTourism():
    def __init__(self, list_guide, list_tour):
        
        self.list_guide = []
        self.list_tour = []

        for tour in list_tour:
            if verbose: print("tour: ", tour)
            timeline = TimelineTours(tour)
            if verbose: print(timeline)
            self.list_tour.append(timeline)

        for guide in list_guide:
            if verbose: print("guideessor: ", guide)
            timeline = TimelineGuides(guide)
            self.list_guide.append(timeline)

        # convert the tour one into guideessors
        #first step: clean guide timeline
        for guide in self.list_guide:
            guide.timeline = [[None for _ in range(guide.hours)] for _ in range(guide.days)]

        #second pupulate timeline
        for tour in self.list_tour:
            for day in range(tour.days):
                for hour in range(tour.hours):
                    items = tour.timeline[day][hour]
                    if items is not None:
                        if '+' in items:
                            item_list = items.split('+')
                        else:
                            item_list = [items]
                            
                        for i in item_list:
                            guide_slot = tour.get_guide(i,day,hour)
                        
                            for guide in self.list_guide:
                                if guide.guide == guide_slot:
                                    if guide.timeline[day][hour] is not None:
                                        guide.timeline[day][hour] += '+' + i
                                    else:
                                        guide.timeline[day][hour] = i

    def fairness_score(self):
        guide_score = 0
        tour_score = 0

        for guide in self.list_guide:
            guide_score += guide.fairness_score()

        for tour in self.list_tour:
            tour_score += tour.fairness_score()


        return (guide_score/len(self.list_guide) + tour_score/len(self.list_tour))/2   

    def avg_fairness_tour(self):
        stud_score = []

        for tour in self.list_tour:
            stud_score.append(tour.fairness_score())
        
        return np.mean(np.array(stud_score))
    
    def avg_fairness_guide(self):
        guide_score = []

        for guide in self.list_guide:
            guide_score.append(guide.fairness_score())

        return np.mean(np.array(guide_score))
    
    def avg_fairness(self):
        return (self.avg_fairness_tour() + self.avg_fairness_guide())/2

    
    def get_fairness_scores_dict_guide(self):
        list_fairness = dict()
        for guide in self.list_guide:
            list_fairness[guide.guide] = guide.fairness_score()
        return list_fairness
        
    def get_fairness_scores_dict_tour(self):
        list_fairness = dict()
        for tour in self.list_tour:
            list_fairness[(tour.tour_id)] = tour.fairness_score()
        return list_fairness
    
    def std_fairness_tour(self):
        stud_score = []

        for tour in self.list_tour:
            stud_score.append(tour.fairness_score())
        
        return np.std(np.array(stud_score))
    
    def std_fairness_guide(self):
        guide_score = []

        for guide in self.list_guide:
            guide_score.append(guide.fairness_score())

        return np.std(np.array(guide_score))
    
    def std_fairness(self):
        avg_guide = self.avg_fairness_guide()
        avg_tour = self.avg_fairness_tour()

        guide_sq_mean = 0
        for guide in self.list_guide:
            guide_sq_mean += (guide.fairness_score()-avg_guide)**2

        tour_sq_mean = 0
        for tour in self.list_tour:
            tour_sq_mean += (tour.fairness_score()-avg_tour)**2

        return math.sqrt(guide_sq_mean/len(self.list_guide) + tour_sq_mean/len(self.list_tour))

    def get_list_obj(self):
        res = [self.avg_fairness_tour(), self.avg_fairness_tour(), self.avg_fairness()] #avgs
        res.append(self.std_fairness_tour())
        res.append(self.std_fairness_guide())
        res.append(self.std_fairness())

        return res
     
    
    def dominate(self, other):
        if self.fairness_score() <= other.fairness_score():
            return False

        return True
        
        
    def __str__(self):
        out = ''
        for guide in self.list_guide:
            out += str(guide)+ f'\nFairness Score: {guide.fairness_score()}' + '\n'

        for tour in self.list_tour:
            out += str(tour)+ f'\nFairness Score: {tour.fairness_score()}' + '\n'
        
        return out
    
    def getSingleFairnessScore(self):
        out =  '^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n'
        out += '^                                            Detailed Fairness Score                                           ^\n'
        out += '^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n'

        for guide in self.list_guide:
            out +=  f'Guide name: {str(guide.guide)}\tFairness Score: {guide.fairness_score()}\n'
        out += f'\tAverage Fairness Score: {self.avg_fairness_guide()}\n'
        out += f'\tStandard Deviation Fairness Score: {self.std_fairness_guide()}\n\n'


        out += '\n'
        for tour in self.list_tour:
            out += f'Tour Name: {str(tour.tour_id)}\tFairness Score: {tour.fairness_score()}' + '\n'

        out += f'\tAverage Fairness Score: {self.avg_fairness_tour()}\n'
        out += f'\tStandard Deviation Fairness Score: {self.std_fairness_tour()}\n'

        out += '\nAverage Fairness Score Overall: ' + str(self.avg_fairness()) + '\n'
        out += 'Standard Deviation Fairness Score Overall: ' + str(self.std_fairness()) + '\n'
        out += '^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n'

        return out

    def __eq__(self,other):
        if len(self.list_guide) != len(other.list_guide):
            return False
        if len(self.list_tour) != len(other.list_tour):
            return False

        for idx in range(len(self.list_guide)):
            if self.list_guide[idx] != other.list_guide[idx]:
                return False

        for idx in range(len(self.list_tour)):
            if self.list_tour[idx] != other.list_tour[idx]:
                return False
            
        return True
    
    def __hash__(self):
        return hash(str(self)) 

    def has_overlap(self):
        for tour in self.list_tour:
            if tour.has_overlap():
                return (True, 'stud')

        for guide in self.list_guide:
            if guide.has_overlap():
                return (True, 'guide')
            
        return (False,'')
    
    def find_overlaps(self):
        tour_overlap = dict()
        for tour in self.list_tour:
            if tour.has_overlaps():
                tour_overlap[(tour.tour_id)] = tour.find_overlaps()

        guide_overlap = dict()
        for guide in self.list_guide:
            if guide.has_overlaps():
                guide_overlap[guide.guide] = guide.find_overlaps()

        return tour_overlap, guide_overlap
    
    def get_tour_index(self, tour_name, year):
        for idx in range(len(self.list_tour)):
            if self.list_tour[idx].tour == tour_name and self.list_tour[idx].year == year:
                return idx
        return -1  
    
    def is_valid(self) -> bool:
        for tour in self.list_tour:
            if not tour.is_valid():
                return False

        for guide in self.list_guide:
            if not guide.is_valid():
                return False
            
        return True
    
    def get_tour_index(self, tour_id):
        for idx in range(len(self.list_tour)):
            if self.list_tour[idx].tour_id == tour_id:
                return idx
        return -1
  