# Multi-sided Fairness in Sequential Task Assignment

## Running the code

There are two case studies: the timetable creation problem for the University domain and the tour scheduling in the tourist domain. The datasets are in the folders `dataset/university` and `dataset/tourism` respectively.

In `src`, there is the source code structured as follows:

📂 `global_sol`  contains the files with the implementation of the classes, methods, and functions for the **global solution**.

📂 `local_sol` folder contains the files with the implementation of the classes, methods, and functions for the **local solution**.

📄 `utils.py` contains the function necessary for the execution of **MOSA** and **FaST-MOSA**, both for local and global subproblems.

📄 `results_tourism.ipynb` is an example of execution for the *Tourism traveling planning* problem.

📄 `results_university_global.ipynb` is an example of execution for the *University timetable construction* problem.
📄 `results_university_prof.ipynb` is an example of execution for the *University timetable construction* starting from professors' soft constraints.
📄 `results_university_stud.ipynb` is an example of execution for the *University timetable construction* starting from students' soft constraints.


You can modify the fairness computation and add a new function modifying the `data_classes` files and, if necessary, adding the condition on `perturbate_with_heu` function in `utils`.

## Classes

#### 📚   University timetable construction

`TimelineProfessors()` uses the *professor identifier* as input to create a random timeline with courses to be taught and fill the table of the soft constraints declared.

`TimelineStudents()` uses the *degree_name* and *year* as input to create a random timeline with the courses of the year of the degree chosen.

#### 🌍   Tourism traveling planning

`TimelineGuides()` uses the *guide identifier* as input to create a random timeline with the visits to perform and fill the table of the soft constraint declared, also saving the closing hours of the points of interest.

`TimelineTours()` uses the *tour identifier* as input to create a random timeline with guided visits to the points of interest.

## Fairness score

The method `.fairness_score()` will return the fairness score of the object created. For Students and Tourists, the fairness score of each function can be seen in more detail by adding the True parameter (`object.fairness_score(True)`).

In order to obtain the solution with **FaST-MOSA**, it is necessary to call the function `getBestSol(obj, initialTemp, finalTemp, alpha, maxPerturbation, True, seed)`, which takes 7 parameters, i.e., the timeline, the initial temperature, the final temperature, a parameter alpha, the number of perturbations at each iteration, the boolean value (i.e., FaST or random perturbations) and a seed.

To start from a local solution, it is necessary to use the `getBestSolLocal` method and then the `getBestSol` one.
`getBestSolLocal` takes 7 parameters: the timeline, the initial temperature, the final temperature, a parameter alpha, the number of perturbations at each iteration, the mode (i.e. *single* for professor and guides, or *cohort* for students and tourists) and the boolean value (i.e., FaST or random perturbations).


