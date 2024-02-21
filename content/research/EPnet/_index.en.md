---
title: "Nonlinear System Identification using Machine Learning"
date: 2023-11-15
author: "辻，山﨑"
---




Controlling systems, such as spacecraft and aircraft, requires the identification of their mathematical models. 
However, building these models solely from a priori physical knowledge has its limitations. <!-- Control of systems, such as spacecraft and aircraft, requires identification of the mathematical model of the system, but there are limitations to build mathematical models from only a priori physical knowledge. -->
Therefore, “system identification,” a method of constructing mathematical models from data obtained by measuring system behavior, has been the subject of active research. <!-- has been actively researched. -->

Our team proposes system identification methods for complex nonlinear systems using neural networks, which have the property of approximating any continuous function. <!-- Our aim is to construct state-space models of highly nonlinear systems, and we have proposed a system identification method utilizing neural networks that can approximate any continuous function. -->
The proposed architecture consists of a state estimator, $E_{\theta}$, and an output predictor, $P_{\phi}$. 
It is designed to reconstruct the original state-space representation. <!-- and because of this structure, we can reconstruct the original dynamics. -->
These components, $E_{\theta}$ and $P_{\phi}$, are neural networks, making the identification of nonlinear systems feasible. <!-- Since these components, $E_{\theta}$ and $P_{\phi}$, are neural networks, the identification of nonlinear systems is possible. -->
Additionally, the identified model can be employed in control designs that require fast online computations, including model predictive control, because the structure enables multi-step-ahead prediction in a single computation. <!-- The model also has the advantage of being applicable to controllers that require fast online computation, including model predictive control, because the structure enables multi-step-ahead prediction in a single computation.  -->

We are currently working on the identification of systems with complex physical phenomena that could not be modeled accurately before. 
We are also applying this method to real systems, such as an automatic driving vehicle.
