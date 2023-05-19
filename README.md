# Open-Science-Bot

![Tests](https://github.com/kir486680/Open-Science-Bot/actions/workflows/python-app.yml/badge.svg)


## Software TODO:
- [ ] establish wiki/documentation of code practices 
- [ ] create unit tests for basic kinematics
  - [ ] full range of gantry motion
  - [ ] math test for inverse/forward kinematics
- [ ] establish good communication between Arduino and Mindstorms brain
- [ ] documenting existing code/removing unneeded code


# Introduction
The emerging open science movement provides an opportunity to topple decades of scientific inequity by creating tools that enable engagement in science by underprivileged or marginalized communities. In this movement, scientific data, code, and knowledge, are shared openly in findable, accessible, interoperable, and reusable (F.A.I.R.) forms. However, it is not enough to make software and code available. Scientists need the opportunity to test their hypotheses in a way that increases their understanding while contributing to the broader scientific community.  

Take as an example, electrodeposition which is a method for coating a thin layer of one metal on top of a different metal to modify its surface properties. It is widely used industrially to create corrosion-resistant coatings for automobiles, improve electrical and thermal conductivity in electrical components, and manufacture screens. Optimizing the composition, surface finish, and density of an electroplated alloy is a tedious manual process that involves controlling the concentration of ions and surfactants, the cathodic current, and the temperature of the plating solution. State of the art autonomous deposition tools are currently only possible in well-funded research labs such as at NIST and NRC, where there are active projects within this space.

# Project Description
This research proposes a low-cost and open-source electroplating robot. The robot will be a platform for investigating electrodeposition at a price that is suitable for high school science labs but with sufficient precision and extensibility to benefit academic and industrial research. Over the summer we will demonstrate proof-of-principle for the design of this robot and then show it can be replicated by incorporating it into a senior-level elective in MSE on scientific robots. The robots will share a decentralized “memory” via a web hosted database, forming an internet of scientific things where experiments in one location inform those at all others.

The platform will be developed using Legos as a basis since they offer great modularity and reusability. A Raspberry PI will control an arm that will pick up substrates, immerse them in a plating solution, and carry them for subsequent characterization. A separate microcontroller will be used to change the electrolyte solution concentration between runs and control a potentiostat to drive the cathodic deposition of the metals. Characterization of the uniformity and surface finish of the coated plate will be performed using a VGA camera and image segmentation. An IPFS protocol will be used to store the processing conditions and results of each experiment. Finally, an active learning program will use a host of regression algorithms to design the next deposition run. 
 
# Outcomes
The critical advantage of this robot is that it can be used by people who have modest budgets and can provide touch points for materials scientists, roboticists, computer scientists, and ethicists. A major outcome of this project will be the open sourcing of the instructions for constructing and operating this platform and its deployment into local schools. 
