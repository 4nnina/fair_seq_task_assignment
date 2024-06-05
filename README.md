# Multi-sided Fairness in Sequential Task Assignment

## Running the code

```cmd
cd src
python main.py
```

There are two case studies: the timetable creation problem for the University domain and the tour scheduling in the tourist domain. The datasets are in the folders `dataset/university` and `dataset/tourism` respectively.

In `src` there is the source code structured as follows:

- `data_classes.py` contains the implementation of the classes and of the methods to compute fairness.
- `utils_py.py` contains the MOSA implementation with the classical Simulated Annealing with only **random perturbations** and the one with the **fairness-driven perturbations**.
- `main.py` is an example of execution for all the classes with random and fairness-driven perturbations.

You can modify the fairness computation and add a new function modifying the `data_classes.py` file and, if necessary, adding the condition on `perturbate_with_heu` function in `utils.py`.

## Classes

#### University domain

`TimelineProfessors()` uses the *professor identifier* as input to create a random timeline with courses to be taught and fill the table of the soft constraints declared.

`TimelineStudents()` uses the *degree_name* and *year* as input to create a random timeline with the courses of the year of the degree chosen.

#### Tourism domain

`TimelineGuides()` uses the *guide identifier* as input to create a random timeline with the visits to perform and fill the table of the soft constraint declared, also saving the closing hours of the points of interest.

`TimelineTours()` uses the *tour identifier* as input to create a random timeline with guided visits to the points of interest.

## Fairness score

The method `.fairness_score()` will return the fairness score of the object created. For Students and Tourists, the fairness score of each function can be seen in more detail by adding the True parameter (`object.fairness_score(True)`).

