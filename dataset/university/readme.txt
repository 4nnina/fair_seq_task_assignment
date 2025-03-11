The file schedule.csv shows the timeline of the first semester (from October to January) of an academic year.
The fields of the file are:
id --> id of the professor
week_day --> the day of the week on which the lesson is scheduled
hour -->  the start time of the lesson. (If a lecture extends over more than one hour, the file will consist of multiple rows, e.g., the lesson on Monday from 10:30 to 12:30 is represented as (id, Mon, 10, ... ) and (id, Mon, 11, ...))
semester --> it will be 1 or 2. It depends on the semester. (so far, only the first semester is in the file)
academic_year --> the academic year of the schedule. In our case '2023/2024'
module --> it is a string of the module/course
degree --> the name of the degree program
room --> where the lecture takes place
degree_year --> the year to which the course belongs


In the file constraint_professor.csv, there are the constraints of each professor.
The fields of the file are:
id --> id of the professor
week_day --> the day of the week the lesson is not desired
hour_begin --> the time at which the professor starts not desiring to lecture
hour_end --> the time when the professor finishes not wanting to lecture
level --> it will be undesired or impossible
note --> some notes written in natural language by the professor, if it is present week_day,hour_begin,hour_end,level must be empty
constraint --> the translation of the constraints given by the previous fields into a standardized rule

In the file, there are two types of constraints:
1. Time slots selected via web app, in the form "not (week_day, [hour_begin, hour_end])" or "NOT (week_day, [hour_begin, hour_end])"
    NOT --> means impossible slots
    not --> means undesired slots
2. Additional comments added by some professors. They are written in natural language and have the fields "week_day,hour_begin,hour_end,level" empty. 
    There are several constraints in &. But not all have to be satisfied.

    Keywords used:
        Commuter -->  a professor who lives in another region or far from the university
        Two_cons_days --> the professor prefers to have the lecture on two consecutive days
        other_venue --> the professor has lectures at another university at the time slots indicated in the notes
        x h --> means that the professor prefer having x consecutive hour of lecture

        NOT --> not desired
        OK --> means preferred slots

        * --> is a placeholder of all working days
        -inf --> beginning of working hours
        inf --> end of working hours


The file lecture_timeslots.csv contains for each module of each degree the hourly timeslots to be allocated.

The file map_module_id.csv contains the mapping between module_id contains in lecture_timeslots.csv and the module name of schedule.