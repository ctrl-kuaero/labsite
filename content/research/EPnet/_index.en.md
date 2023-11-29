---
title: "Nonlinear System Identification using Machine Learning"
date: 2023-11-15
---




Control of systems such as spacecraft and aircraft requires identification of the mathematical model of the system, but there are limitations to build mathematical models from only a priori physical knowledge. 
Therefore, “system identification,” a method of constructing mathematical models from data obtained by measuring system behavior, has been actively researched.

Our aim is to construct state-space models of highly nonlinear systems, and we have proposed a system identification method utilizing neural networks that can approximate any continuous function.	
The proposed model consists of a state estimator $E_{\theta}$ and an output predictor $P_{\phi}$ , and the architecture provides the advantage of being able to predict multiple-step-ahead outputs in a single computation, making it applicable to controllers that require fast online computation, including model predictive control.

We are currently working on the identification of systems with complex physical phenomena that could not be modeled before. 
We are also applying this method to real systems such as an automatic driving vehicle.
