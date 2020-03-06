# ADAS_using_OpenVino
Advanced Driver Assistance System (team-project) - developed for the Intel Edge AI Scholarshap @Udacity

## Introduction
[...]

## Motivation
Making roads a safer place and ADAS available to the majority of people, not only to those who can’t afford a new Car with special and expensive addons.

## Current Features
- Car detection
- Tracking speed visually
- tracking distance to car in front of us
- based on speed and distance -> calculating if minimum breaking distance is kept
- Detection of blue direction signs on german highways (to be replaced by a model-based sign detection in the near future)
- Weather detection (will be used to increase the minimum breaking distance in case it is raining)
- displaying lane-lines

## Features we are currenlty working on
- road sign detection, to also include for example warnings for Stop-signs

## Planned Features
- tracking of pedestrians, bikes etc. to the make the application more secure for urban usage
- traffic-light detection to automatically break/accelerate
- model-based lane-detection (in the future used to keep the lane)

## Description
[...]


## To-Do
- optimizing and cleaning up current state (make it stage ready for the showcase and easier to read for you and the judges) (@Patrick.Hartmann)
- Weather detection (@Aarthi Alagammai)

#### Open:
- Sign detection for german highway, if we find a good dataset (…)
- Improvement of car detection, because the current one from OpenVino is never detecting the car on the right lane (…)
- Converting models to IR and applying them (…)
- multithreading for the models, to increase execution time (…)
- better text-recognition (very poor results, we only have one result that is actually displaying the right text)

## Execution Instructions
(Note: The project uses a 2019 version of OpenVino, which still has to include a CPU_EXTENSION directory to run, it is set by default for macOS, for other OS's it needs to be passed in the with input argument "-c")
### For macOS
- clone or download the repository
- if you have OpenVino installed with root permision, in your terminal run "sudo -i"
- Source the OpenVino environment by executing following on your terminal: "source /opt/intel/openvino/bin/setupvars.sh"
- In your terminal change the directory to the repository folder that contains main.py
- run it better executing "python3 main.py -m frozen_inference_graph.xml


# Acknowledgments/Licenses
- Intel Edge AI Scholarship Challenge
- Car-Icon made by "Nikita Golubev" "https://www.flaticon.com/authors/nikita-golubev" from https://www.flaticon.com/"
