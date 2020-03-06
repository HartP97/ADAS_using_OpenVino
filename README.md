# ADAS_using_OpenVino
Advanced Driver Assistance System (team-project) - developed for the Intel Edge AI Scholarshap @Udacity

## Introduction
[...]

## Motivation
[...]

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
### For macOS
- clone or download the repository
- if you have OpenVino installed with root permision, in your terminal run "sudo -i"
- Source the OpenVino environment by executing following on your terminal: "source /opt/intel/openvino/bin/setupvars.sh"
- In your terminal change the directory to the repository folder that contains main.py
- run it better executing "python3 main.py -m frozen_inference_graph.xml


# Acknowledgments/Licenses
- Intel Edge AI Scholarship Challenge
- Car-Icon made by "Nikita Golubev" "https://www.flaticon.com/authors/nikita-golubev" from https://www.flaticon.com/"
