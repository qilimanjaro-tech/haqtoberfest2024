# Optimization algorithms challenge

In this folder you will find different information that will help you get through the challenge on optimization of classical problems using quantum algorithms.

- In the notebook [concepts.ipynb](concepts.ipynb) you will find an introduction to the algorithms that we will be using and a brief explanation of all the steps required to solve the optimization problem, together with different references to external material that can help you understand the concepts. After each section it is described the part of the challenge related to that, divided into small steps to guide you during the resolution.

- The notebook [challenge.ipynb](challenge.ipynb) is the recopilation of all the challenges proposed in [concepts.ipynb](concepts.ipynb), but without all the additional information.

- During this challenge you will be solving the Knapsack Problem, the instances to be solved can be found in the file [problem_instances.json](problem_instances.json). The code found in the notebook [problem_instances.ipynb](problem_instances.ipynb) can be used to extract all the information about the instances. You don't need to solve all of them, it is recommended to start with the smaller ones first since the algorithms will run much faster. Different instances are included so that you can check that you code works correctly for any of them and do a better benchmark of the results.

- In [tutorials.ipynb](tutorials.ipynb) you will find some example code written in `qibo` showing the basic functionalities to run gate-based and quantum annealing algorithms.

You can install all the required Python libraries to solve this challenge by running `pip install -r requirements.txt` in your virtual environment. You can make use additional libraries under reasonable circumstances such as wanting to try some specific optimizer (in case of doubt ask your mentor), but it has to be specified at the beginning of the code of your deliverable.
