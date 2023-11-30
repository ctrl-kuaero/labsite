---
title: "Data-Driven Optimal Feedback Control"
date: 2023-11-10
---

When controlling a system, some properties, for example, fast response and small input energy consumption, may be required.  
A control that maximizes or minimizes the value of the objective function, which represents the quantity of the achievement of target goals, is called an "optimal control." 
The problem of finding optimal control inputs as time series data can be reduced to Hamilton's canonical equations using the calculus of variations.
However, when the obtained feedforward optimal control is applied to the real system, challenges, such as instability or undesirable performance, may arise due to uncertainties, disturbances, or modeling errors. 
Hence, it is better to have a feedback structure in control.
An optimal feedback control law can be derived from a value function that is a solution to the Hamilton-Jacobi-Bellman (HJB) equation, but finding this solution is extremely difficult.

In this laboratory, therefore, instead of directly solving the HJB equation, we calculate an optimal feedback control law based on a database containing solutions to Hamilton's canonical equations. 
During control, the optimal input at each time is determined by finding the nearest data among the database to the current state.
Recently, we have been conducting further research, such as value functions modeling using neural networks and verifying the effectiveness of this method by applying it to real machines, such as drones. 