# Multi-sided Fairness in Sequential Task Assignment

## Running the code

There are two case studies: the timetable creation problem for the University domain and the tour scheduling in the tourist domain. The datasets are in the folders `dataset/university` and `dataset/tourism` respectively.

In `src` there is the source code structured as follows:

📂 `global_sol`  contains the files with the implementation of the classes, methods, and functions for the **global solution**.
📂 ` local_sol` folder contains the files with the implementation of the classes, methods, and functions for the **local solution**.
📄 `utils.py` contains the function necessary for the execution of **MOSA** and **FaST-MOSA**, both for local and global subproblems.
📄 `results_tourism.ipynb` is an example of execution for the *Tourism traveling planning* problem.
📄 `results_university.ipynb` is an example of execution for the *University timetable construction* problem.

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

In order to obtain the local solution with **FaST-MOSA** it is necessary to call the function `getBestSolLocal(obj, initialTemp, finalTemp, alpha, maxPerturbation, True)`, which takes 6 parameters, i.e., the object of sub-problem's timeline, the initial temperature, the final temperature, a parameter alpha, the number of perturbations at each iteration, and the boolean value.

Then, it is possible to convert the local solutions into the global one by creating the objects `GlobalUniveristyFromLocal()` or `GlobalTourismFromLocal()`, which takes two mandatory arguments and a third if we want to impose one solution over the other. 

To run the algorithm to find the global solution for the university domain, it is possible to call the function `getBestSol()`.
