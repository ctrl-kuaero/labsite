---
title: "Data-Driven Optimal Feedback Control"
date: 2023-11-10 # ソート用
---

When controlling a system, we aim for a desirable transient response and reducing input energy consumption. Control that maximizes or minimizes the value of a cost function, quantifying the achievement of such specifications, is called optimal control. The optimal feedback control law can be designed by obtaining the value function, a solution of the Hamilton-Jacobi-Bellman (HJB) equation. However, solving the HJB equation is extremely challenging.

On the other hand, the problem of obtaining optimal control inputs as time series data is attributed to the Hamilton's equations through calculus of variations. 
In reality, however, applying the feedforward control inputs to the system does not always result in the desired response due to disturbances. Therefore, an optimal feedback control law is generally preferred.

In our lab, we propose building optimal feedback control laws based on a database containing solutions of the Hamilton's equations instead of directly solving the HJB equation. Currently, we are modeling the value function using neural networks and validating effectiveness of proposed method by applying it to real-world scenarios, such as drone applications.