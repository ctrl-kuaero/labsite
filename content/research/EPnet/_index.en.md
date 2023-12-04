---
title: "Nonlinear System Identification using Machine Learning"
date: 2023-11-15
author: "辻，山﨑"
---




Control of systems, such as spacecraft and aircraft, requires identification of the mathematical model of the system, but there are limitations to build mathematical models from only a priori physical knowledge. 
Therefore, “system identification,” a method of constructing mathematical models from data obtained by measuring system behavior, has been actively researched.

Our aim is to construct state-space models of highly nonlinear systems, and we have proposed a system identification method utilizing neural networks that can approximate any continuous function.	
The proposed structure of the model consists of a state estimator $E_{\theta}$ and an output predictor $P_{\phi}$, which can reconstruct the original state-space model.
Since these components are neural networks, the identification of nonlinear systems is possible.
The model also has the advantage of being applicable to controllers that require fast online computation, including model predictive control, because the structure enables multi-step-ahead prediction in a single computation. 

We are currently working on the identification of systems with complex physical phenomena that could not be modeled accurately before. 
We are also applying this method to real systems, such as an automatic driving vehicle.
