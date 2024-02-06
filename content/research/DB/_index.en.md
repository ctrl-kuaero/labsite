---
title: "Data-Driven Optimal Feedback Control"
date: 2023-11-10
author: "H. Asakura"
---

When controlling a system, some properties, for example, fast response and small input energy consumption, may be required. 
A control that maximizes or minimizes the objective function, which represents the quantity of the achievement of target goals, is called an “optimal control.”
Optimal control, especially for nonlinear systems, has been researched actively. 
The problem of finding optimal control inputs as time series data can be reduced to Hamilton's canonical equations using the calculus of variations.
However, when the obtained feedforward optimal control is applied to the real system, challenges, such as instability or undesirable performance, may arise due to uncertainties, disturbances, and modeling errors. 
Hence, it is generally required to have a feedback structure in control.
An optimal feedback control law can be derived from a value function that is a solution to the Hamilton-Jacobi-Bellman (HJB) equation, but finding this solution is extremely difficult.

In this laboratory, therefore, instead of directly solving the HJB equation, we develop an optimal feedback control law for nonlinear systems based on a database containing solutions to Hamilton's canonical equations. 
The optimal control input at each time is determined by finding the nearest data among the database to the current state.
Recently, we have been conducting additional research, including the modeling of value functions using neural networks. 
Furthermore, we are validating the effectiveness of our proposed method by applying it to real machines, such as drones. 
