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

# Example

You can run examples/main.py which is basically a preprogrammed sequence to pick up a piece of metal, pump some liquid in the reactor, submerge both electrodes, take them out of the bath, and drop off the electrodes in the location near the metal holder. Keep in mind that the actual MeasurementExample.py needs to be run separately. 

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