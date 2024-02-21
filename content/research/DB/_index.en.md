---
title: "Data-Driven Optimal Feedback Control"
date: 2023-11-10
author: "H. Asakura"
---

When controlling a system, certain specifications, such as fast response and reduced input energy consumption, may be required.
Control that maximizes or minimizes the objective function, which represents the degree of the achievement of target goals, is known as “optimal control.”
Optimal control, especially for nonlinear systems, has been researched actively. 
The problem of finding optimal control inputs as time series data can be reduced to Hamilton's canonical equations using the calculus of variations.
However, applying the obtained feedforward optimal control inputs to a real system can lead to challenges like instability or undesirable performance due to uncertainties, disturbances, and modeling errors. 
Therefore, incorporating a feedback structure in the control system is generally required.
An optimal feedback control law can be derived from a value function that is a solution to the Hamilton-Jacobi-Bellman (HJB) equation, but finding this solution is extremely difficult.

In this laboratory, we have focused on developing an optimal feedback control law for nonlinear systems by utilizing a database containing solutions to Hamilton's canonical equations, instead of directly solving the HJB equation. 
The optimal control input for each instance is determined using data identified as closest to the current state in the database. 
Recently, we have been conducting additional research, including the modeling of value functions using neural networks. 
Furthermore, we are validating the effectiveness of our proposed method by applying it to real machines, such as drones. 
