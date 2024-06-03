# Open-Science-Bot

![Tests](https://github.com/kir486680/Open-Science-Bot/actions/workflows/python-app.yml/badge.svg)


ACTIVE DEVELOPMENT

# Introduction
The emerging open science movement provides an opportunity to topple decades of scientific inequity by creating tools that enable engagement in science by underprivileged or marginalized communities. In this movement, scientific data, code, and knowledge, are shared openly in findable, accessible, interoperable, and reusable (F.A.I.R.) forms. However, it is not enough to make software and code available. Scientists need the opportunity to test their hypotheses in a way that increases their understanding while contributing to the broader scientific community.  

Take as an example, electrodeposition which is a method for coating a thin layer of one metal on top of a different metal to modify its surface properties. It is widely used industrially to create corrosion-resistant coatings for automobiles, improve electrical and thermal conductivity in electrical components, and manufacture screens. Optimizing the composition, surface finish, and density of an electroplated alloy is a tedious manual process that involves controlling the concentration of ions and surfactants, the cathodic current, and the temperature of the plating solution. State of the art autonomous deposition tools are currently only possible in well-funded research labs such as at NIST and NRC, where there are active projects within this space.

# Project Description
This research proposes a low-cost and open-source electrochemistry robot. The robot will be a platform for investigating electrochemistry at a price that is suitable for high school science labs but with sufficient precision and extensibility to benefit academic and industrial research.

The following robot has 
- lego xyz stage, which is controlled by Lego Mindstorm Inventor motors and brain, where two motors drive the x and y axes. The motor controlling the y-axis is on the cart carrying the end effectors. The two end effectors of the xyz stage that the cart carries have a gripper, a holder, and a tube connected to a pump. Both end effectors are controlled by another two Lego Mindstorm Inventor motors, and one of them carries the gripper used to grip metal samples and is actuated by a Hitech servo motor. The other end effector carries the reference electrode holder (you have to preinstall them manually), and a tube connected to a pump that pumps electrolytes from the beaker (currently connected to the two beakers).
- another pump connected to the chemical reactor used to drain the reactor after each experiment.
- chemical reactor where the counter electrode is preinstalled, and you are able to submerge the metal sample from the gripper, the preinstalled reference, and pump the liquid which are all held by the end-effector of the xyz stage described above. 
- a metal holder which simply holds the metal samples. 
- potentiostat which is controlled by the software. This is the biggest pain point of the project right now. You need to run the PSPythonSDK/MeasurementExample.py script in palmsdk folder on the windows laptop in order to get the data from the potentiostat. (when you are in the PSPythonSDK folder, just type ```python MeasurementExample.py```). If you want to run the experiment manually, you need to use the PSTrace app on windows. However, also keep in mind that in order to run the potentiostat script you need to use Python 3.8 or below. 

# Example

You can run examples/main.py, which is a preprogrammed sequence that does the following: (Keep in mind that the actual MeasurementExample.py needs to be run separately)
1. Pick up a piece of metal by moving the xyz stage over the metal holder, lower the gripper end effector over the piece of metal, gripping it, and then raise the end effector.
2. The xyz stage will be moved above the reactor, the end effector carrying the pump will be lowered, and the pump will pump some liquid into the reactor.
3. After enough liquid has been pumped into the reactor, the second end effector with the piece of metal will be lowered into the reactor. The experiment will begin.
4. After the experiment, both end effectors will be raised. The second pump will drain the liquid from the reactor.
5. The xyz stage will be moved to a nearby spot to drop off the metal sample. The xyz stage will then be moved back to the (0,0,0) location.

# What is next?

1. You need to be able to somehow call the MeasurementExample.py from the examples/main.py. For that, you might need to setup a server on the raspi using fastapi python package, and also run a server on the windows computer which could execute MeasurementExample.py. I was not able to find a direct way to run the potentiostat from the raspi, but it should be possible... So choose whatever option you think is worth your time.
2. Do active learning. Familiarize yourself with the active_learning/activeLearning.ipynb, and you can use this template code to set up a real system using the robot. The purpose of that demo is to see how you can autonomously find the concentration of electrolyte A and B to achieve a specific goal(in this example the goal is to run an experiment with a peak of 100mV as signified by ```if np.abs(Y_next - 100) < 1: ```)
3. Automate electrolyte replacement in the bath. I have already purchased a pump and Robert will be designing the 3D model for that. 



So what are the specific steps? 

1. find a specific electrochemical experiment that you want to be running(ask prof. Jae for that). Preferrably its some experiment where you are trying to find the ideal peak voltage by changing electrolyte composition.  
2. you can try to manually do data gathering and see if the active learning algorithm guides you in the correct direction. What I mean by manually is to manually run ```python MeasurementExample.py``` or even just use the PSTrace app during the time.sleep while running the ```examples/main.py```. So the workflow woudl be something like this:
    1. run ```python examples/main.py```
    2. during the ```time.sleep(100)``` you can manually run the ```python MeasurementExample.py```(or PSTrace software) to get the data 
    3. Feed this data to the active learning algorithm and make it predict a new concentration of electrolyte A and B
    4. Adjust examples/main.py to pump the amount of electrolyte suggested at the previous step
    5. pour out the liquid from the bath and clean the bath(could be automated).
    6. go back to step 1. 
