---
title: "Construction of Mathematical Optimization Algorithms"
date: 2023-11-22
author: "山本"
---



Refueling spacecraft in space is difficult, so it is an important issue to minimize fuel consumption. 
Obtaining the trajectory that minimizes fuel consumption requires solving the $L^{1}$-optimal control problem, a challenge known for its complexity. <!-- The trajectory with the minimum fuel consumption can be obtained by solving the $L^{1}$-optimal control problem, which is known to be difficult to solve. --> 
The $L^{1}$-optimal control input exhibits sparsity, staying at zero for most of the control period, which allows strategies that take advantage of this feature.<!-- Moreover, the $L^{1}$-optimal control input is characterized by sparsity, i.e., it is zero for most of the control time, and can be used for control that takes advantage of this property.  -->
We are conducting research on various mathematical optimization algorithms, including algorithms for solving the $L^{1}$-optimal control problem. 

Additionally, we investigate optimization algorithms with stochastic parameters to find global optimal solutions in problems characterized by multiple local optima. <!-- We also study optimization algorithms with stochastic parameters as a method for finding global optimal solutions to problems which have multiple local optimal solutions.  -->
This approach is expected to identify global optimal solutions even for problems where deterministic methods may only find local optimal solutions.  

We develop optimization algorithms for diverse applications and provide theoretical proofs of their convergence and other essential properties. <!-- We develop optimization algorithms for various purposes and conduct theoretical proofs of convergence and other properties. -->
