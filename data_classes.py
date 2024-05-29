#from dataclasses import dataclass, field
import pandas as pd
import numpy as np
import random
from tabulate import tabulate
import re

dataset_timeslot_file = './dataset/university/lecture_timeslots.csv'
data_prof_cons_file = './dataset/university/constraint_professors.csv'
dataset_guide_file = './dataset/tourism/guide.csv'
dataset_tour_file = './dataset/tourism/final_data/tours.csv'
dataset_cons_guide_file = './dataset/tourism/constraint_guide.csv'
dataset_poi_distance_file = './dataset/tourism/distance_poi.csv'
inf_dist = 10000

class Timeline():

    def __init__(self):
        self.hours = 11
        self.days = 7
        self.hour_lunch = [3,4,5]
        self.timeline = [[None for _ in range(self.hours)] for _ in range(self.days)]

    def __str__(self):
        days = ['mon', 'tue', 'wed', 'thu', 'fri', 'sat', 'sun']
        print_days = [[None for _ in range(self.hours)] for _ in range(self.days)]
        for day in range(self.days):
            for hour in range(self.hours):
                if self.timeline[day][hour] is not None:
                    #print_days[day][hour] = re.sub(r'by.*?-','-',self.timeline[day][hour])
                    print_days[day][hour] = self.timeline[day][hour]

        pretty_print = [[days[i]] + print_days[i] for i in range(self.days)]
        return tabulate(pretty_print, headers=['   '] + [str(i+8) + ' - ' + str(i+9) for i in range(self.hours)]) + '\n'
    
    def __eq__(self, other) -> bool:
        return type(self) == type(other) and self.timeline == other.timeline
    
    def __hash__(self) -> int:
        return hash(str(self.timeline))
    
    def fairness_score(self) -> float:
        return 0
    
    def dominate(self, other) -> bool:
        return self.fairness_score() > other.fairness_score()
    
    def has_overlaps(self) -> bool:
        for day in range(self.days):
            for hour in range(self.hours):
                if self.timeline[day][hour] is not None:
                    if '+' in self.timeline[day][hour]:
                        return True
        return False
    
    def find_overlaps(self) -> list:
        overlaps = []
        for day in range(self.days):
            for hour in range(self.hours):
                if self.timeline[day][hour] is not None:
                    if '+' in self.timeline[day][hour]:
                        overlaps.append((day, hour))
        return overlaps
    
    def satisfied_mandatory(self) -> bool:
        return not self.has_overlaps()
    
    def has_lunch_break(self) -> bool:
        for day in range(self.days):
            not_lunch = list()
            for hour in self.hour_lunch:
                if self.timeline[day][hour] is not None:
                    not_lunch.append(True)
                else:
                    not_lunch.append(False)
            if all(not_lunch):
                return False
        return True
    
    def find_day_without_lunch_break(self) -> list:
        days_without_lunch = []
        for day in range(self.days):
            not_lunch = list()
            for hour in self.hour_lunch:
                if self.timeline[day][hour] is not None:
                    not_lunch.append(True)
                else:
                    not_lunch.append(False)
            if all(not_lunch):
                days_without_lunch.append(day)
        return days_without_lunch
    
    #remove an item from a timeslot
    def remove_item(self, item, day, hour, lenght_slot):
        for slot in range(hour, hour + lenght_slot):
            list_item = self.timeline[day][slot].split('+')
            try:
                list_item.remove(item)
            except:
                print(f'Item {item} not found in slot {day} {slot}')
                print(self)

            if len(list_item) == 0:
                self.timeline[day][slot] = None
            else:
                self.timeline[day][slot] = '+'.join(list_item)

    #add an item in a timeslot
    def add_item(self, item, day, hour, lenght_slot):
        for slot in range(hour, hour + lenght_slot):
            if self.timeline[day][slot] is None:
                self.timeline[day][slot] = item
            else:
                self.timeline[day][slot] += '+' + item

    def get_filtered_timeline(self, list_lectures, prof):
        #TODO: serve?
        return 
    
    def get_filtered_timeline_real(self, prof):
        #TODO: serve?
        return 
    
    def filter_by_courses(self, list_courses):
        #TODO: serve?
        return 
    
    def get_set_modules(self):
        #TODO: serve?
        return 


class TimelineUniversity(Timeline):

    def __init__(self):
        super().__init__()
        self.days = 5
        self.timeline = [[None for _ in range(self.hours)] for _ in range(self.days)]



class TimelineProfessors(TimelineUniversity):
    def __init__(self, prof_id):
        super().__init__()
        self.name = prof_id
        self.constraints = [[None for _ in range(self.hours)] for _ in range(self.days)]
        self.comment = []

        df = pd.read_csv(dataset_timeslot_file)#pd.read_csv('../'+dataset_timeslot_file)
        df = df[df['prof_id'] == prof_id]
        df = df[['module_id','n_hours','prof_id']]
        df.drop_duplicates(inplace=True)
        df.reset_index(inplace=True)

        #initialize randomic slot: with no look at constraint, may be some overlap
        for lecture_idx in df.index:
            day = random.randrange(self.days)
            hour = random.randrange(self.hours)
            n_hours = df.iloc[lecture_idx]['n_hours']

            if hour+n_hours > 11:
                hour = 11 - n_hours
            
            for i in range(n_hours):
                if self.timeline[day][hour+i] is None:
                    self.timeline[day][hour+i] = str(df.iloc[lecture_idx]['module_id']) + 'by' + str(df.iloc[lecture_idx]['prof_id']) + '-' + str(df.iloc[lecture_idx]['n_hours'])
                else:
                    self.timeline[day][hour+i] = self.timeline[day][hour+i] + '+' \
                                                + str(df.iloc[lecture_idx]['module_id']) + 'by' + str(df.iloc[lecture_idx]['prof_id']) + '-' + str(df.iloc[lecture_idx]['n_hours'])
                    
        #initialize constraints
        impossible = -1
        undesired = -0.5
        preference = -0.25

        df_cons = pd.read_csv(data_prof_cons_file)#pd.read_csv('../'+data_prof_cons_file)
        df_cons = df_cons[df_cons['prof_id'] == prof_id]
        df_cons = df_cons[['constraint','level']]

        cons_defined = df_cons[(df_cons['level'].notnull())]
        map_week_days = {'Mon': 0, 'Tue': 1, 'Wed': 2, 'Thu': 3, 'Fri': 4, '*': [0,1,2,3,4]}
        #NOT (Thu, [18:30, 19:30])
        for _, row in cons_defined.iterrows():
            possibility = row['constraint'].split(' ')[0]
            if possibility == 'NOT':
                value = impossible
            elif possibility == 'not':
                value = undesired
            else:
                raise ValueError('Constraint defined not recognized')
            
            day = map_week_days[row['constraint'].split(' ')[1][1:4]]
            hour_start = int(row['constraint'].split(' ')[2].replace('[','').split(':')[0])
            hour_end = int(row['constraint'].split(' ')[3].split(':')[0])
            for hour in range(hour_start-8, hour_end-8):
                self.constraints[day][hour] = value

        cons_undefined = df_cons[(df_cons['level'].isnull()) & (df_cons['constraint'].notnull())]
        if len(cons_undefined) > 1:
            raise ValueError('More than one comment is defined')
        elif len(cons_undefined) == 1:
            self.comment = []
            cons_undefined = cons_undefined['constraint'].iloc[0].split(' & ')

            if 'other_venue' == cons_undefined[0]:
                value = impossible
                cons_undefined = cons_undefined[1:]
            else:
                value = preference

            for cons in cons_undefined:
                cons_part = cons.split(' ')
                if len(cons_part) == 2:
                    if cons_part[0] == 'NOT':
                        day = map_week_days[cons_part[1][:3]]
                        for hour in range(11):
                            if self.constraints[day][hour] is None or self.constraints[day][hour] > value:
                                self.constraints[day][hour] = value
                    elif cons_part[0] == 'OK':
                        continue        #TODO: if we want to add preference we MUST take in account
                    elif cons_part[1] == 'h':
                        self.comment.append(' '.join(cons_part))
                elif len(cons_part) == 4:
                    if cons_part[0] == 'NOT':
                        try:
                            day = map_week_days[cons_part[1][1:-1]]
                        except KeyError:
                            self.comment.append(' '.join(cons_part))
                            continue

                        hour_start = cons_part[2].replace('[','').replace(',','').split(':')
                        if hour_start[0] == '-inf':
                            hour_start = 8
                        else:
                            hour_start = int(hour_start[0])
                        
                        hour_end = cons_part[3].replace('])','').split(':')
                        if hour_end[0] == 'inf':
                            hour_end = 19
                        else:
                            hour_end = int(hour_end[0])

                        for hour in range(hour_start-8, hour_end-8):
                            if type(day) is list:
                                for d in day:
                                    if self.constraints[d][hour] is None or self.constraints[d][hour] > value:
                                        self.constraints[d][hour] = value
                            else:
                                if self.constraints[day][hour] is None or self.constraints[day][hour] > value:
                                    self.constraints[day][hour] = value
                        

                    elif cons_part[0] == 'OK':
                        continue        #TODO: if we want to add preference we MUST take in account
                elif cons_part[0] == 'Two_cons_days':
                    self.comment.append(' '.join(cons_part))
                elif cons_part[0] == 'Commuter' or cons_part[0] == 'online'  or cons_part[0] == '(OK':
                    continue            #TODO: actualy it doesn't make any difference
                else:
                    print(cons_part)
                    raise ValueError('Constraint undefined not recognized')
                
    def print_constraints(self):
        days = ['mon', 'tue', 'wed', 'thu', 'fri', 'sat', 'sun']
        pretty_print = [[days[i]] + self.constraints[i] for i in range(self.days)]
        out = '\nCONSTRAINTS:\n'
        out += tabulate(pretty_print, headers=['   '] + [str(i+8) + ' - ' + str(i+9) for i in range(self.hours)]) + '\n'
        
        if len(self.comment) > 0:
            out += '\nAdditional comments:'
            for c in self.comment:
                out += '\n' + str(c)
            out += '\n'
        return out

    def __str__(self):
        return f'PROFESSOR {self.name}\n' + super().__str__() + self.print_constraints()
        
    def satisfied_impossible_constraints(self) -> bool:
        for day in range(self.days):
            for hour in range(self.hours):
                if self.constraints[day][hour] == -1 and self.timeline[day][hour] is not None:
                    return False
        return True

    def satisfied_mandatory(self) -> bool:
        return super().satisfied_mandatory() and self.satisfied_impossible_constraints()
    
    def get_unsatisfied_impossible_constraints(self) -> list:
        unsatisfied = []
        for day in range(self.days):
            for hour in range(self.hours):
                if self.constraints[day][hour] == -1 and self.timeline[day][hour] is not None:
                    unsatisfied.append((day, hour))
        return unsatisfied
    
    #return only soft constraints
    def get_unsatisfied_constraints(self) -> list:
        unsatisfied = []
        for day in range(self.days):
            for hour in range(self.hours):
                if self.constraints[day][hour] is not None and self.timeline[day][hour] is not None:
                    if self.constraints[day][hour] != -1:
                        unsatisfied.append((day, hour))
        return unsatisfied

    def fairness_score(self) -> float:
        score = 0
        if not self.satisfied_mandatory():
            score += -1000 * len(super().find_overlaps())
            if not self.satisfied_impossible_constraints():
                score += -501 * len(self.get_unsatisfied_impossible_constraints())

        for day in range(self.days):
            for hour in range(self.hours):
                if self.constraints[day][hour] is not None and self.timeline[day][hour] is not None:
                    score += self.constraints[day][hour]

        if len(self.comment) > 0:
            for comment in self.comment:
                if comment == 'Two_cons_days':
                    lectures = []
                    for day in range(self.days):
                        if not all(slot is None for slot in self.timeline[day]):
                            lectures.append(day)
                    if len(lectures) > 2:
                        score += (-0.25)
                    elif len(lectures) == 2 and abs(lectures[0] - lectures[1]) > 1:
                        score += (-0.25)
                else:
                    raise Warning('Comment not recognized')

        return score
    
    def dominate(self, other) -> bool:
        if self.fairness_score() > other.fairness_score():
            return True
        else:
            return False
    

class TimelineStudents(TimelineUniversity):
    def __is_in_degree_year(self, year, degree_year):
        if str(year) in degree_year:
            return True
        else:
            return False

    def __init__(self, degree, year):
        super().__init__()
        self.degree = degree
        self.year = year

        df = pd.read_csv(dataset_timeslot_file)
        df['degree_year'] = df.degree_year.apply(lambda x: list(x)if len(x)==1 else x.replace('[','').replace(']','').split(','))     
        df = df[(df['degree'] == degree) & (df['degree_year'].apply(lambda x: self.__is_in_degree_year(year, x)))]
        df = df[['module_id','n_hours','prof_id']]
        df.reset_index(inplace=True)

        #initialize randomic slot: with no look at constraint, may be some overlap
        for lecture_idx in df.index:
            day = random.randrange(self.days)
            hour = random.randrange(self.hours)
            n_hours = df.iloc[lecture_idx]['n_hours']

            if hour+n_hours > 11:
                hour = 11 - n_hours
            
            for i in range(n_hours):
                if self.timeline[day][hour+i] is None:
                    self.timeline[day][hour+i] = str(df.iloc[lecture_idx]['module_id']) + 'by' + str(df.iloc[lecture_idx]['prof_id']) + '-' + str(df.iloc[lecture_idx]['n_hours'])
                else:
                    self.timeline[day][hour+i] = self.timeline[day][hour+i] + '+' \
                                                + str(df.iloc[lecture_idx]['module_id']) + 'by' + str(df.iloc[lecture_idx]['prof_id']) + '-' + str(df.iloc[lecture_idx]['n_hours'])

    def __str__(self):
        return f'DEGREE: {self.degree}\tYEAR: {self.year}\n' + super().__str__()

    def obj_fun_gap(self) -> float:
        gap_h = 0
        total_h = 0

        for day in range(self.days):
            tmp_gap_h = 0
            find_lecture = False

            first_lesson = -1
            last_lesson = -1
            for hour in range(self.hours):
                if self.timeline[day][hour] is not None:
                    if first_lesson == -1:
                        first_lesson = hour
                        last_lesson = hour
                    else:
                        last_lesson = hour

                    if tmp_gap_h > 0:   #end of gap
                        gap_h += tmp_gap_h
                        tmp_gap_h = 0
                    else:
                        find_lecture = True
                elif find_lecture:
                    tmp_gap_h += 1
            if first_lesson != -1:
                total_h += last_lesson - first_lesson + 1

        return gap_h/total_h

    def obj_fun_gaps_in_week(self) -> float:
        day_lecture = []
        for day in range(self.days):
            if not all(slot is None for slot in self.timeline[day]):
                day_lecture.append(day)

        if len(day_lecture) <= 1:
            return 0
        
        count = 0
        for day in range(1, len(day_lecture)):
            if day_lecture[day] - day_lecture[day-1] > 1:
                count += day_lecture[day] - day_lecture[day-1] -1
            
        return count/self.days

    def num_days_with_lectures(self) -> int:
        count = 0
        for day in range(self.days):
            if not all(slot is None for slot in self.timeline[day]):
                count += 1
        return count
    
    def obj_fun_num_days(self) -> float:
        return self.num_days_with_lectures()/self.days

    def obj_fun_lunch(self) -> float: #num lunch break / number of days with lesson : 0 if every day has lunch break, 1 if no day has lunch break
        not_lunch_break = len(self.find_day_without_lunch_break())
        days_with_lesson = self.num_days_with_lectures()
        
        return not_lunch_break/days_with_lesson

    def obj_fun_early(self) -> float:
        early_lectures = 0
        for day in range(self.days):
            if self.timeline[day][0] is not None:
                early_lectures += 1

        days_with_lesson = self.num_days_with_lectures()
        return early_lectures/days_with_lesson
    
    def obj_fun_late(self) -> float:
        late_lectures = 0
        for day in range(self.days):
            if self.timeline[day][-1] is not None:
                late_lectures += 1

        days_with_lesson = self.num_days_with_lectures()
        return late_lectures/days_with_lesson

    #def satisfied_mandatory(self) -> bool:
    #    return super().satisfied_mandatory()

    def fairness_score(self, print_stats = False) -> float:
        if not self.satisfied_mandatory():
            mand = 1000 * len(super().find_overlaps())
        else:
            mand = 0
        
        gap = self.obj_fun_gap()
        gaps_in_week = self.obj_fun_gaps_in_week()
        lunch = self.obj_fun_lunch()
        num_days = self.obj_fun_num_days()
        early = self.obj_fun_early()
        late = self.obj_fun_late()

        if print_stats:
            print(f'Overlaps: {mand}')
            print(f'gap:',gap)
            print(f'gaps_in_week:',gaps_in_week)
            print(f'lunch:',lunch)
            print(f'num_days:',num_days)
            print(f'early:',early)
            print(f'late:',late)
        
        return (mand + gap + gaps_in_week + lunch + num_days + early + late) * -1
    
    def dominate(self, other) -> bool:
        if self.obj_fun_gap() > other.obj_fun_gap():
            return False
        if self.obj_fun_gaps_in_week() > other.obj_fun_gaps_in_week():
            return False
        if self.obj_fun_lunch() > other.obj_fun_lunch():
            return False
        if self.obj_fun_num_days() > other.obj_fun_num_days():
            return False
        if self.obj_fun_early() > other.obj_fun_early():
            return False
        if self.obj_fun_late() > other.obj_fun_late():
            return False
        
        if self.fairness_score() < other.fairness_score():
            return False

        return True
    
    def num_gaps_in_days(self) -> int:   
        gaps = 0
        list_day_gaps = []
        for day in range(self.days):
            tmp_gaps = 0
            day_gaps = 0
            find_lecture = False
            for hour in range(self.hours):
                if self.timeline[day][hour] is not None:
                    if tmp_gaps > 0:    #end of gap
                        gaps += tmp_gaps
                        day_gaps += tmp_gaps
                        tmp_gaps = 0
                    else:
                        find_lecture = True
                elif find_lecture:
                        tmp_gaps += 1
            if day_gaps > 0:
                list_day_gaps.append([day, day_gaps])
        
        return list_day_gaps

    def num_gaps_in_week(self) -> tuple: 
        day_lecture = []
        for day in range(self.days):
            if not all(slot is None for slot in self.timeline[day]):
                day_lecture.append(day)
            
        if len(day_lecture) == 0:
            return 0, day_lecture
        
        count = 0
        for day in range(1, len(day_lecture)):
            if day_lecture[day] - day_lecture[day-1] > 1:
                count += day_lecture[day] - day_lecture[day-1] -1
        
        return count, day_lecture
    

class TimelineTourism(Timeline):
    def __init__(self):
        super().__init__()
        self.distance = 0

    def has_overlaps(self) -> bool:
        df_dist = pd.read_csv(dataset_poi_distance_file)
        df_tour = pd.read_csv(dataset_tour_file)
        for day in range(self.days):
            for hour in range(self.hours):
                if self.timeline[day][hour] is not None:
                    items = self.timeline[day][hour].split('+')
                    if len(items) > 2:
                        #More than two item in the same slot
                        return True
                    else:
                        #Two item in the same slot
                        if len(items) == 2:
                            if hour-1 >= 0 and self.timeline[day][hour-1] is not None:
                                #previous slot is not empty
                                if items[1] == self.timeline[day][hour-1]:
                                    #Initial random assignement overlap
                                    return True

                            pois = self.get_poi(day, hour)
                            if pois[0] == pois[1]:
                                #Same POI impossible
                                return True
                            distance_real = df_dist[(df_dist['poi_1'] == pois[0]) & (df_dist['poi_2'] == pois[1])]['distance_minutes'].values[0]
                            visit_duration_1 = df_tour[(df_tour['tour_id'] == int(items[0].split('-')[0])) & (df_tour['poi_id'] == pois[0])]['time_visit'].values[0]
                            d1 = int(items[0].split('*')[1].split('by')[0])
                            d2 = int(items[1].split('*')[1].split('by')[0])

                            if d1 != visit_duration_1 + distance_real:
                                #distance not already computed, it is a real overlap
                                return True
                            if d1 - 60 < 0:
                                #visit of the first is less than an hour, real overlap
                                return True
                            
        return False
    
    def satisfied_mandatory(self) -> bool:
        return not self.has_overlaps()
    
    def clear_distance(self):
        if not self.has_overlaps():
            df_tour = pd.read_csv(dataset_tour_file)
            df_tour['tour_id'] = df_tour['tour_id'].apply(lambda x: int(x))
            df_tour['poi_id'] = df_tour['poi_id'].apply(lambda x: int(x))
            df_tour['time_visit'] = df_tour['time_visit'].apply(lambda x: int(x))

            for day in range(self.days):
                for hour in range(self.hours):
                    if self.timeline[day][hour] is not None:
                        #TOUR_ID-POI_ID*TIME_VISITbyGUIDE_ID
                        tour_id, remains = self.timeline[day][hour].split('-')
                        poi_id, remains = remains.split('*')
                        time_visit, guide_id = remains.split('by')

                        tour_id = int(tour_id)
                        poi_id = int(poi_id)
                        time_visit = int(time_visit)
                        guide_id = int(guide_id)

                        real_time_visit = df_tour[(df_tour['tour_id'] == tour_id) & (df_tour['poi_id'] == poi_id)]['time_visit'].values[0]

                        if time_visit != real_time_visit:
                            if time_visit > 60:
                                self.remove_item(self.timeline[day][hour], day, hour, int(np.ceil(time_visit/60)))
                            else:   
                                self.remove_item(self.timeline[day][hour], day, hour, 1)

                            clear_item = f'{tour_id}-{poi_id}*{real_time_visit}by{guide_id}'
                            self.add_item(clear_item, day, hour, int(np.ceil(real_time_visit/60))) 


    def compute_distance(self):
        #The timeline has overlaps?
        if self.has_overlaps():
            #YES, the timeline is not valid
            self.distance = inf_dist
            #return
        else:
            #NO, we can compute
            self.distance = 0

            df_dist = pd.read_csv(dataset_poi_distance_file)
            df_tour = pd.read_csv(dataset_tour_file)

            df_dist['poi_1'] = df_dist['poi_1'].apply(lambda x: int(x))
            df_dist['poi_2'] = df_dist['poi_2'].apply(lambda x: int(x))
            df_tour['tour_id'] = df_tour['tour_id'].apply(lambda x: int(x))
            df_tour['poi_id'] = df_tour['poi_id'].apply(lambda x: int(x))
            df_tour['time_visit'] = df_tour['time_visit'].apply(lambda x: int(x))

            #FIRST: clean the timeline from the duration
            self.clear_distance()

            #SECOND: compute the distance between POIs
            for day in range(self.days):
                poi1 = None
                slot1 = None
                for hour in range(self.hours):
                    if self.timeline[day][hour] is not None:
                        p = self.get_poi(day,hour)
                        slot = self.timeline[day][hour]
                        if slot1 is not None and slot == slot1: #p[0] == poi1:    #there is a POI which time_visit is more than one slot (an hour)
                            continue
                        elif '+' in slot:
                            item_slot_before, slot1 = slot.split('+')
                            poi1 = p[1]
                            more_poi = True
                        else:
                            poi1 = p[0]
                            slot1 = slot
                            more_poi = False

                        next =  False
                        hour_second = hour+1
                        while not next and hour_second < self.hours:
                            if self.timeline[day][hour_second] is not None:
                                poi2 = self.get_poi(day,hour_second)
                                poi2 = poi2[0]
                                if poi1 != poi2:
                                    dist_pois = df_dist[(df_dist['poi_1'] == poi1) & (df_dist['poi_2'] == poi2)]['distance_minutes'].values[0]   
                                    next = True
                                else:
                                    hour_second += 1
                            else:
                                hour_second += 1
                            
                        if next:
                            tour_id = slot1.split('-')[0]
                            visit_duration = df_tour[(df_tour['tour_id'] == int(tour_id)) & (df_tour['poi_id'] == poi1)]['time_visit'].values[0]
                            visit_duration += dist_pois

                            self.distance += dist_pois
                            
                            first_part = slot1.split('*')[0]
                            second_part = slot1.split('by')[1]

                            new_slot = first_part + '*' + str(visit_duration) + 'by' + second_part
                            
                            #old_slot = self.timeline[day][hour].split('+')[-1]

                            if more_poi:
                                self.timeline[day][hour] = item_slot_before + '+' + new_slot
                            else:
                                self.timeline[day][hour] = new_slot
                            #self.timeline[day][hour] = first_part + '*' + str(visit_duration) + 'by' + second_part

                            if visit_duration > 60:
                                #more thant an hour
                                if self.timeline[day][hour+1] is not None:
                                    #the next slot is not empty
                                    if self.timeline[day][hour+1] == slot1:
                                        #the next slot is the same of the old slot (same item)
                                        self.timeline[day][hour+1] = new_slot
                                    else:
                                        #the next slot is different
                                        if hour-1 >= 0 and self.timeline[day][hour-1] is None:
                                            #the previous slot is empty
                                            self.timeline[day][hour-1] = new_slot
                                        else:
                                            self.timeline[day][hour+1] = new_slot + '+' + self.timeline[day][hour+1]
                                else:
                                    #the next slot is empty
                                    self.timeline[day][hour+1] = new_slot
                                slot1 = new_slot
                                

    def get_poi(self, day, hour):
        if self.timeline[day][hour] is None:
            return list()
        
        if '+' in self.timeline[day][hour]:
            items = self.timeline[day][hour].split('+')
            pois = []
            for item in items:
                poi = item.split('-')[1]
                poi = poi.split('*')[0]
                pois.append(int(poi))
        else:
            poi = self.timeline[day][hour].split('-')[1]
            poi = poi.split('*')[0]
            pois = [int(poi)]

        return pois


class TimelineGuides(TimelineTourism):
    def __add_new_constraint(self, row_cons, impossible, undesired, map_week_days, guide = False):
        possibility = row_cons['constraint'].split(' ')[0]
        if possibility == 'NOT':
            value = impossible
        elif possibility == 'not':
            value = undesired
        else:
            raise ValueError('Constraint defined not recognized')
        
        if guide:
            key = 'g'
        else:
            key = row_cons['poi_id']
        
        day = map_week_days[row_cons['constraint'].split(' ')[1].replace('(','').replace(',','')]
        if len(row_cons['constraint'].split(' ')) == 2:
            #CONSTRAINT TYPE: 'NOT Mon'
            for hour in range(self.hours):
                if self.constraints[day][hour] is None:
                    self.constraints[day][hour] = {key: value}
                else:
                    self.constraints[day][hour][key] = value
        else:
            #CONSTRAINT TYPE: 'NOT (Fri, [08:00, 10:00]'
            hour_start = int(row_cons['constraint'].split(' ')[2].replace('[','').split(':')[0])
            hour_end = int(row_cons['constraint'].split(' ')[3].split(':')[0])
            for hour in range(hour_start-8, hour_end-8):
                if self.constraints[day][hour] is None:
                    self.constraints[day][hour] = {key: value}
                else:
                    self.constraints[day][hour][key] = value

    def __init__(self, guide_id):
        super().__init__()
        self.guide = guide_id
        self.constraints = [[None for _ in range(self.hours)] for _ in range(self.days)]

        df_guide = pd.read_csv(dataset_guide_file)
        df_guide = df_guide[df_guide['guide_id'] == guide_id]
        df_guide.reset_index(inplace=True)
        list_pois = df_guide['poi_id'].tolist()
        df_tours = pd.read_csv(dataset_tour_file)
        df_tours = df_tours[df_tours['poi_id'].isin(list_pois)]
        df_tours.reset_index(inplace=True)

        #initialize randomic slot: with no look at constraint, may be some overlap
        for idx in df_tours.index:
            day = random.randrange(self.days)
            hour = random.randrange(self.hours)
            n_hours = int(np.ceil((df_tours.iloc[idx]['time_visit'])/60))

            if hour+n_hours > 11:
                hour = 11 - n_hours

            for i in range(n_hours):
                if self.timeline[day][hour+i] is None:
                    self.timeline[day][hour+i] = str(df_tours.iloc[idx]['tour_id']) + '-' + str(df_tours.iloc[idx]['poi_id']) + '*' + str(df_tours.iloc[idx]['time_visit']) + 'by' + str(guide_id)
                else:
                    self.timeline[day][hour+i] = self.timeline[day][hour+i] + '+' \
                                                + str(df_tours.iloc[idx]['tour_id']) + '-' + str(df_tours.iloc[idx]['poi_id']) + '*' + str(df_tours.iloc[idx]['time_visit']) + 'by' + str(guide_id)
        self.compute_distance()

        #initialize constraints
        impossible = -1
        undesired = -0.5

        df_constraints = pd.read_csv(dataset_cons_guide_file)
        df_constraints = df_constraints[df_constraints['guide_id'] == guide_id]
        df_constraints_poi = df_constraints[df_constraints['poi_id'].notnull()]
        df_constraints_guide = df_constraints[df_constraints['poi_id'].isnull()]
        map_week_days = {'Mon': 0, 'Tue': 1, 'Wed': 2, 'Thu': 3, 'Fri': 4, 'Sat': 5, 'Sun': 6}

        #FIRST: constraints on POIs (closure hours/days)
        for _, row in df_constraints_poi.iterrows():
            self.__add_new_constraint(row, impossible, undesired, map_week_days)

        #SECOND: constraints on guide
        for _, row in df_constraints_guide.iterrows():
            self.__add_new_constraint(row, impossible, undesired, map_week_days, guide = True)
            
    def print_constraints(self):
        days = ['mon', 'tue', 'wed', 'thu', 'fri', 'sat', 'sun']
        pretty_print = [[days[i]] + self.constraints[i] for i in range(self.days)]
        out = '\nCONSTRAINTS:\n'
        out += tabulate(pretty_print, headers=['   '] + [str(i+8) + ' - ' + str(i+9) for i in range(self.hours)]) + '\n'

        return out

    def __str__(self):
        return f'GUIDE {self.guide}\n' + super().__str__() + self.print_constraints()

    def satisfied_impossible_constraints(self) -> bool:
        for day in range(self.days):
            for hour in range(self.hours):
                if self.constraints[day][hour] is not None and self.timeline[day][hour] is not None:
                    constraints_keys = self.constraints[day][hour].keys()
                    if 'g' in constraints_keys and self.constraints[day][hour]['g'] == -1:
                        return False
                    else:
                        pois = self.get_poi(day,hour)
                        for poi in pois:
                            if poi in constraints_keys and self.constraints[day][hour][poi] == -1:
                                return False
        return True

    def satisfied_mandatory(self) -> bool:
        return super().satisfied_mandatory() and self.satisfied_impossible_constraints()

    def get_unsatisfied_impossible_constraints(self) -> list:
        unsatisfied = []
        for day in range(self.days):
            for hour in range(self.hours):
                if self.constraints[day][hour] is not None and self.timeline[day][hour] is not None:
                    constraints_keys = self.constraints[day][hour].keys()
                    if 'g' in constraints_keys and self.constraints[day][hour]['g'] == -1:
                        unsatisfied.append((day, hour))
                    else:
                        pois = self.get_poi(day,hour)
                        for poi in pois:
                            if poi in constraints_keys and self.constraints[day][hour][poi] == -1:
                                unsatisfied.append((day, hour))
                                break
        return unsatisfied
    
    #return only soft constraints
    def get_unsatisfied_constraints(self) -> list:
        unsatisfied = []
        for day in range(self.days):
            for hour in range(self.hours):
                if self.constraints[day][hour] is not None and self.timeline[day][hour] is not None:
                    constraints_keys = self.constraints[day][hour].keys()
                    if 'g' in constraints_keys and self.constraints[day][hour]['g'] != -1:
                        unsatisfied.append((day, hour))
                    else:
                        pois = self.get_poi(day,hour)
                        for poi in pois:
                            if poi in constraints_keys and self.constraints[day][hour][poi] != -1:
                                unsatisfied.append((day, hour))
                                break
        return unsatisfied
    
    def fairness_score(self) -> float:
        score = 0
        if not self.satisfied_mandatory():
            score += -1000 * len(super().find_overlaps())
            if not self.satisfied_impossible_constraints():
                score += -501 * len(self.get_unsatisfied_impossible_constraints())

        for day,hour in self.get_unsatisfied_constraints():
            constraints_keys = self.constraints[day][hour].keys()
            if 'g' in constraints_keys and self.constraints[day][hour]['g'] != -1:
                score += self.constraints[day][hour]['g']
            else:
                pois = self.get_poi(day,hour)
                for poi in pois:
                    if poi in constraints_keys and self.constraints[day][hour][poi] != -1:
                        score += self.constraints[day][hour][poi]

        return score
    
    def dominate(self, other) -> bool:
        if self.fairness_score() > other.fairness_score():
            return True
        else:
            return False

class TimelineTours(TimelineTourism):
    def __init__(self, tour_id):
        super().__init__()
        self.tour_id = tour_id

        df_tours = pd.read_csv(dataset_tour_file)
        df_tours = df_tours[df_tours['tour_id'] == tour_id]
        df_tours['poi_id'] = df_tours['poi_id'].apply(lambda x: int(x))
        list_pois = df_tours['poi_id'].tolist()
        df_guide = pd.read_csv(dataset_guide_file)
        df_guide['poi_id'] = df_guide['poi_id'].apply(lambda x: int(x))
        df_guide = df_guide[df_guide['poi_id'].isin(list_pois)]
        df_guide = df_guide[['guide_id','poi_id']]
        df_tours = df_tours.merge(df_guide, on='poi_id', how='left')
        df_tours.reset_index(inplace=True)

        for idx in df_tours.index:
            day = random.randrange(self.days)
            hour = random.randrange(self.hours)
            n_hours = int(np.ceil((df_tours.iloc[idx]['time_visit'])/60))

            if hour+n_hours > 11:
                hour = 11 - n_hours

            for i in range(n_hours):
                if self.timeline[day][hour+i] is None:
                    self.timeline[day][hour+i] = str(df_tours.iloc[idx]['tour_id']) + '-' + str(df_tours.iloc[idx]['poi_id']) + '*' + str(df_tours.iloc[idx]['time_visit']) + 'by' + str(df_tours.iloc[idx]['guide_id'])
                else:
                    self.timeline[day][hour+i] = self.timeline[day][hour+i] + '+' \
                                                + str(df_tours.iloc[idx]['tour_id']) + '-' + str(df_tours.iloc[idx]['poi_id']) + '*' + str(df_tours.iloc[idx]['time_visit']) + 'by' + str(df_tours.iloc[idx]['guide_id'])

        self.compute_distance()

    def __str__(self):
        return f'TOUR: {self.tour_id}\n' + super().__str__()

    def satisfied_mandatory(self) -> bool:
        return not self.has_overlaps()

    def obj_fun_gap(self) -> float:
        gap_h = 0
        total_h = 0

        for day in range(self.days):
            tmp_gap_h = 0
            find_visit = False

            first_visit = -1
            last_visit = -1
            for hour in range(self.hours):
                if self.timeline[day][hour] is not None:
                    if first_visit == -1:
                        first_visit = hour
                        last_visit = hour
                    else:
                        last_visit = hour

                    if tmp_gap_h > 0:   #end of gap
                        gap_h += tmp_gap_h
                        tmp_gap_h = 0
                    else:
                        find_visit = True
                elif find_visit:
                    tmp_gap_h += 1
            if first_visit != -1:
                total_h += last_visit - first_visit + 1

        return gap_h/total_h
    
    def obj_fun_gaps_in_week(self) -> float:
        day_visit = []
        for day in range(self.days):
            if not all(slot is None for slot in self.timeline[day]):
                day_visit.append(day)

        if len(day_visit) <= 1:
            return 0
        
        count = 0
        for day in range(1, len(day_visit)):
            if day_visit[day] - day_visit[day-1] > 1:
                count += day_visit[day] - day_visit[day-1] -1
            
        return count/self.days
    
    def num_days_with_visits(self) -> int:
        count = 0
        for day in range(self.days):
            if not all(slot is None for slot in self.timeline[day]):
                count += 1
        return count
    
    def num_visit_per_day(self) -> list:
        visit_per_day = []
        for day in range(self.days):
            count = 0
            hours = []
            for hour in range(self.hours):
                if self.timeline[day][hour] is not None:
                    count += 1
                    hours.append(hour)
            if count > 0:
                visit_per_day.append((day, count, hours))
        return visit_per_day
    
    def obj_fun_num_days(self) -> float:
        return self.num_days_with_visits()/self.days
  
    def fairness_score(self, print_stats = False) -> float:
        if not self.satisfied_mandatory():
            mand = 1000 * len(self.find_overlaps())
        else:
            mand = 0
        
        gap = self.obj_fun_gap() * 10
        gaps_in_week = self.obj_fun_gaps_in_week()
        num_days = self.obj_fun_num_days()
        distance = self.distance / 60

        if print_stats:
            print(f'Overlaps: {mand}')
            print(f'gap:',gap)
            print(f'gaps_in_week:',gaps_in_week)
            print(f'num_days:',num_days)
            print(f'distance:',distance)

        return (mand + gap + gaps_in_week + num_days + distance) * -1
    
    def dominate(self, other) -> bool:
        if self.obj_fun_gap() > other.obj_fun_gap():
            return False
        if self.obj_fun_gaps_in_week() > other.obj_fun_gaps_in_week():
            return False
        if self.obj_fun_num_days() > other.obj_fun_num_days():
            return False
        
        if self.fairness_score() < other.fairness_score():
            return False

        return True
    
    def num_gaps_in_days(self) -> int:   
        gaps = 0
        list_day_gaps = []
        for day in range(self.days):
            tmp_gaps = 0
            day_gaps = 0
            find_lecture = False
            for hour in range(self.hours):
                if self.timeline[day][hour] is not None:
                    if tmp_gaps > 0:    #end of gap
                        gaps += tmp_gaps
                        day_gaps += tmp_gaps
                        tmp_gaps = 0
                    else:
                        find_lecture = True
                elif find_lecture:
                        tmp_gaps += 1
            if day_gaps > 0:
                list_day_gaps.append([day, day_gaps])
        
        return list_day_gaps

    def num_gaps_in_week(self) -> tuple: 
        day_lecture = []
        for day in range(self.days):
            if not all(slot is None for slot in self.timeline[day]):
                day_lecture.append(day)
            
        if len(day_lecture) == 0:
            return 0, day_lecture
        
        count = 0
        for day in range(1, len(day_lecture)):
            if day_lecture[day] - day_lecture[day-1] > 1:
                count += day_lecture[day] - day_lecture[day-1] -1
        
        return count, day_lecture
       