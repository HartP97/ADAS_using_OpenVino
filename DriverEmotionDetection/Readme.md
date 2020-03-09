# Drowsiness detection with OpenVINO

Driver drowsiness detection is a car safety technology which prevents accidents when the driver is getting drowsy. Various studies have suggested that around 20% of all road accidents are fatigue-related, up to 50% on certain roads. Driver fatigue is a significant factor in a large number of vehicle accidents. Recent statistics estimate that annually 1,200 deaths and 76,000 injuries can be attributed to fatigue related crashes. 

## PLEASE CLICK [here](https://youtu.be/yXz26rTGm9U) or the image down below to watch the video
[![example_output_vid](Self-developed-ADAS/output_example.png)](https://youtu.be/yXz26rTGm9U)

# Existing System

Here we are used SVM(support vector machine) to classify the components in the input video. While cropping the region of interest components in the video is not accurate. Sometimes it will show regions wrong. To sense the eyes first we have to create boundary boxes for that and a classification algorithm. The algorithm of SVM will not support.## Create files and folders

# Proposed System

Here we took the existing Emotion Ferplus data from onnx model zoo and retrained it according to our requirement. It is currently made for 5 classes to identify the state of driver. 

High Sleepy : System indicates that driver should stop driving at the earliest.
Drowsy : System indicates that Driver is driving with difficulty and an action should be taken immediately  like playing music or changing the driver
Perfect: Here the Driver is driving the vehicle with 100 % consciousness and very safe and the Cruise mode is also on. Driver is also taking care of climatic conditions.
Active: Here the Driver is driving the vehicle with  85-100 % consciousness and cruise mode is not on
Normal: This mode is activated when driver is driving safely and need to check with Climate conditions

# Data Set

The data consists of 128px*128px RGB images of faces. The faces have been automatically registered so that the face is more or less centered and occupies about the same amount of space in each image. The task is to categorize each face based on the emotion shown in the facial expression in to one of five categories described above. Training set consists of 2400 examples and test set is of size 600.

# OpenVINO conversion
The onnx file format is converted into IR files with Model optimizer of FP16 precision. 

# Results
 The Mean precision accuracy for test set is around 85 % with FP16 precision. On i5 core CPU with integrated GPU the frame rate is around 35 FPS.



