# Weather_classification
Weather classification Project using Convolutional Neural Network
This project is developed as part for Intel Edge AI Scholarhip Challenge 2020 
# Goal
Develop a weather classification application to be deployable at the edge using Intel's OpenVINO Toolkit.
# Motivation
There is a huge development and scope for ADAS system in the current era.The weather classification has a huge impact on our daily lives as wells affects vechile assistant systems, outdoor video surveillance systems.So we designed a system using Convolutional Neural Networks to classify weather into 6 different categories like Rain, Cloudy ,Haze ,Thunder ,Snow ,Sunny.The main aim of this project is to support weather classification as a new feature to the ADAS system the team was developing and deploy it as edge application.
# Work Done
The dataset is split into 80:10:10 for training:validation:testing
The results achieved 
```
Test Loss: 5.794341

Test Accuracy of cloudy: 76% (1174/1531)
Test Accuracy of  haze: 84% (1270/1496)
Test Accuracy of rainy: 92% (1443/1555)
Test Accuracy of  snow: 94% (1390/1478)
Test Accuracy of sunny: 89% (1340/1504)
Test Accuracy of thunder: 99% (1544/1556)

Test Accuracy (Overall): 89% (8161/9120)
```
To convert pytorch to onnx: https://michhar.github.io/convert-pytorch-onnx/
```
import torch
import torch.onnx

# A model class instance (class not shown)
model = MyModelClass()

# Load the weights from a file (.pth usually)
state_dict = torch.load(weights_path)

# Load the weights now into a model net architecture defined by our class
model.load_state_dict(state_dict)

# Create the right input shape (e.g. for an image)
dummy_input = torch.randn(sample_batch_size, channel, height, width)
torch.onnx.export(model, dummy_input, "onnx_model_name.onnx")
```No extra dependencies needed, since pytorch itself provides us the library: 
https://pytorch.org/docs/stable/onnx.html#supported-operators
```
# Sample Output
```
Actual Weather-Cloudy
Predicted Weather-Cloudy
```
![Sample image](https://github.com/AarthiAlagammai/Weather_classification/blob/master/sample%20image.png)

# OpenVino Deployed output
![Deployed Appplication using OpenVino](https://github.com/AarthiAlagammai/Weather_classification/blob/master/weather%20output1.png)

# How to Use the Edge App
Direction of usage: Using the terminal, entering a command starting with `python app.py .` to run the application, and with some flags such as `-i` to specify the input image file, `-t` to specify type such as "IMG", then `-m` to specify the model xml file, and finally `-c` to specify the CPU extension, an inference at the edge can be made. This has been taken as a part of Intel edge ai course.


## Original Dataset link: 

