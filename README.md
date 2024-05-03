# Open-Science-Bot

![Tests](https://github.com/kir486680/Open-Science-Bot/actions/workflows/python-app.yml/badge.svg)


ACTIVE DEVELOPMENT

# Introduction
The emerging open science movement provides an opportunity to topple decades of scientific inequity by creating tools that enable engagement in science by underprivileged or marginalized communities. In this movement, scientific data, code, and knowledge, are shared openly in findable, accessible, interoperable, and reusable (F.A.I.R.) forms. However, it is not enough to make software and code available. Scientists need the opportunity to test their hypotheses in a way that increases their understanding while contributing to the broader scientific community.  

Take as an example, electrodeposition which is a method for coating a thin layer of one metal on top of a different metal to modify its surface properties. It is widely used industrially to create corrosion-resistant coatings for automobiles, improve electrical and thermal conductivity in electrical components, and manufacture screens. Optimizing the composition, surface finish, and density of an electroplated alloy is a tedious manual process that involves controlling the concentration of ions and surfactants, the cathodic current, and the temperature of the plating solution. State of the art autonomous deposition tools are currently only possible in well-funded research labs such as at NIST and NRC, where there are active projects within this space.

# Project Description
This research proposes a low-cost and open-source electrochemistry robot. The robot will be a platform for investigating electrochemistry at a price that is suitable for high school science labs but with sufficient precision and extensibility to benefit academic and industrial research.

The following robot has 
- lego xyz stage. The end effector of the xyz stage has a gripper, holder, and a pump. The gripper is able to grip metal samples, the holder is able to hold reference electrodes(you have to preinstall them manually), and the pump is able to pump  electrolyte from the beaker(currently connected to the two beakers)
- chemical reactor where the counter electrode is preinstalled, and you are able to submerge the metal sample from the gripper, the preinstalled reference, and pump the liquid which are all held by the end-effector of the xyz stage described above. 
- metal holder simply holds the metal samplse. 
- potentiostat which is controlled by the software. This is the biggest pain point of the project right now. You need to run the PSPythonSDK/MeasurementExample.py script in palmsdk folder on the windows laptop in order to get the data from the potentiostat. (when you are in the PSPythonSDK folder, just type ```python MeasurementExample.py```). If you want to run the experiment manually, you need to use the PSTrace app on windows. However, also keep in mind that in order to run the potentiostat script you need to use Python 3.8 or below. 

