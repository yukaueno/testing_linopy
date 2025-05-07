# testing_linopy
I tested the Linopy library to evaluate its performance in generating optimization models.

I was searching new libs with promising results to generate optimizations models.

And I found Linopy with good results compared with Pyomo and JuMP. This motivated me to explore more.

![image](https://github.com/user-attachments/assets/9ba0c6ba-1db4-473a-8ebf-28302f44e7ae)


There are other comparative studies, such those by GAMS and AIMMS, that offer valuable insights into the performance of libraries like Pyomo, JuMP, and GurobiPy.

This graph is from GAMS:
(https://www.gams.com/blog/2023/07/performance-in-optimization-models-a-comparative-analysis-of-gams-pyomo-gurobipy-and-jump/)
![image](https://github.com/user-attachments/assets/b56ea32c-efa4-4515-9451-17869eb6e1b5)

To gain practical experience with Linopy and compare its performance, I utilize the experimental setup from the GAMS experiment repository (https://github.com/justine18/performance_experiment).

This experiment includes two models, IJLK and Supply Chain, both characterized by sparse variables and constraints to aim to stress model generation.

 

Firstly, I code the IJKLM model in Linopy (run_linopy.py)

But I encountered memory limitations when N = 600 or 1500. During analysis, I examined the generated “.lp” e “.mps” files for potential errors, but I found no errors.

However, I did observe that Linopy's variable definition, particularly when dealing with character indexes, might be inefficient. Utilizing the Masking Arrays method, as suggested in the documentation

(https://linopy.readthedocs.io/en/latest/creating-variables.html#Masking-Arrays), appeared to create a significant number of unnecessary variables. For instance, with N = 100, while the model required 185 variables, Linopy generated 16.000, many of which were 'None'.



Additionally, I encountered challenges when attempting to generate the model with a time limit of 0. It appears that Linopy includes model generation time in this limit, whereas other libraries may not. This could also be related to the high number of generated variables.



I didn't implement the Supply Chain model, because of similarity, I could find the same problem.



Given that Linopy is a relatively new library, I believe that it will have more improvements. It's also possible that my implementation approach can be refined too. I found similar memory-related issues reported in the Linopu issue tracker

(https://github.com/PyPSA/linopy/issues/248).



Overall , while I initially had high hopes for Linopy's performance, I encountered some implementation challenges compared to more established libraries. As a newer library, its documentation is still developing, and I look forward to seeing its evolution.
