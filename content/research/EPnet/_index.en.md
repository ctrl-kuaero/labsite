---
title: "Nonlinear System Identification using Machine Learning"
date: 2023-11-15
---




Precise control of systems such as aerospace aircraft requires accurate identification of the mathematical model of the system, but there are limitations to constructing a mathematical model from only a priori physical knowledge. Therefore, “System Identification”, a method of constructing mathematical models from data obtained by measuring system behavior, has been actively researched.

Our aim is to construct state-space models of highly nonlinear systems, and we have proposed a system identification method utilizing neural nets that can approximate any continuous function.	The proposed model consists of a state estimator that estimates the system state variables from past input-output time series and an output predictor that predicts future outputs from the estimated states and future inputs. The architecture provides the advantage of being able to predict multiple-step-ahead in a single computation, making it applicable to controllers that require fast computation online, including model predictive control.

We are currently working on the identification of systems containing complex physical phenomena that could not be modeled before, and on the integration of the proposed model into real-world systems to achieve optimal control that could not be realized with conventional models.
