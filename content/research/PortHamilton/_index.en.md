---
title: "Passivity-based control using Port-Hamiltonian representation"
date: 2023-11-17 # ソート用
---

Passivity-based control is a method that easily stabilizes systems by utilizing a property of physical systems called passivity in control.
The fundamental idea is to use the conserved quantity (energy) of mechanical systems as a candidate Lyapunov function in control.
This method can be applied to nonlinear systems, such as spacecrafts, which are difficult to control using linear control methods.
We are developing nonlinear controllers that achieve Lyapunov stability of closed-loop systems by designing artificial potential functions dependent on position and velocity for systems described by the port-Hamiltonian model.
Recently, by sharpening these potential functions, we have been developing a method to realize a robust controller, known as sliding mode control, within the framework of passivity-based control.