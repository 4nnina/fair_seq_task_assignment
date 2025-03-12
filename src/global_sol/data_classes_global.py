import copy
import sys
import os
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
    
    def dominate(self, other):
        if self.fairness_score() <= other.fairness_score():
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

        for degree in self.list_degree:
            out += f'Degree Name: {str(degree.degree)}\tYear: {str(degree.year)}\tFairness Score: {degree.fairness_score()}' + '\n'

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
    
    def find_overlap(self):
        degree_overlap = dict()
        for degree in self.list_degree:
            if degree.has_overlap():
                degree_overlap[(degree.degree, degree.year)] = degree.find_overlap()

        prof_overlap = dict()
        for prof in self.list_prof:
            if prof.has_overlap():
                prof_overlap[prof.name] = prof.find_overlap()

        return degree_overlap, prof_overlap    


class GlobalUniveristyFromLocal(GlobalUniversity):
    def __init__(self, list_prof, list_degree, start_from = ''):
        self.list_prof = []
        self.list_degree = []

       
        for degree in list_degree:
            self.list_degree.append(copy.deepcopy(degree))

        for prof in list_prof:
            self.list_prof.append(copy.deepcopy(prof))

        if start_from == 'stud':
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
        elif start_from == 'prof':
            #first step: clean student timelins
            dict_lesson_degree = {}
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
                                dict_lesson_degree[i] = (degree.degree, degree.year)

                degree.timeline = [[None for _ in range(degree.hours)] for _ in range(degree.days)]

            #second pupulate timeline
            for prof in self.list_prof:
                for day in range(prof.days):
                    for hour in range(prof.hours):
                        items = prof.timeline[day][hour]
                        if items is not None:
                            if '+' in items:
                                item_list = items.split('+')
                            else:
                                item_list = [items]
                                
                            for i in item_list:
                                if i in dict_lesson_degree.keys():
                                    degree_slot = dict_lesson_degree[i]
                                else:
                                    continue
                            
                                for degree in self.list_degree:
                                    if degree.degree == degree_slot[0] and degree.year == degree_slot[1]:
                                        if degree.timeline[day][hour] is not None:
                                            degree.timeline[day][hour] += '+' + i
                                        else:
                                            degree.timeline[day][hour] = i
    

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

        out += '\n'
        for tour in self.list_tour:
            out += f'Tour Name: {str(tour.tour_id)}\tFairness Score: {tour.fairness_score()}' + '\n'

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


class GlobalTourismFromLocal(GlobalTourism):
    def __init__(self, list_guide, list_tour, start_from = ''):
        self.list_guide = []
        self.list_tour = []

       
        for tour in list_tour:
            self.list_tour.append(copy.deepcopy(tour))

        for guide in list_guide:
            self.list_guide.append(copy.deepcopy(guide))

        if start_from == 'tour':
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
        elif start_from == 'guide':
            #first step: clean tour timelines
            for tour in self.list_tour:
                tour.timeline = [[None for _ in range(tour.hours)] for _ in range(tour.days)]

            #second pupulate timeline
            for guide in self.list_guide:
                for day in range(guide.days):
                    for hour in range(guide.hours):
                        items = guide.timeline[day][hour]
                        if items is not None:
                            if '+' in items:
                                item_list = items.split('+')
                            else:
                                item_list = [items]
                                
                            for i in item_list:
                                tour_slot = int(i.split('-')[0])
                                
                                for tour in self.list_tour:
                                    if tour.tour_id == tour_slot:
                                        if tour.timeline[day][hour] is not None:
                                            tour.timeline[day][hour] += '+' + i
                                        else:
                                            tour.timeline[day][hour] = i
    