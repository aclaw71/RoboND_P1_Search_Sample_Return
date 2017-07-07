## Project 1: Search and Sample Return

---

![Project1][image1]

**The goals / steps of this project are the following:**  

**Training / Calibration**  

* Download the simulator and take data in "Training Mode"
* Test out the functions in the Jupyter Notebook provided
* Add functions to detect obstacles and samples of interest (golden rocks)
* Fill in the `process_image()` function with the appropriate image processing steps (perspective transform, color threshold etc.) to get from raw images to a map.  The `output_image` you create in this step should demonstrate that your mapping pipeline works.
* Use `moviepy` to process the images in your saved dataset with the `process_image()` function.  Include the video you produce as part of your submission.

**Autonomous Navigation / Mapping**

* Fill in the `perception_step()` function within the `perception.py` script with the appropriate image processing functions to create a map and update `Rover()` data (similar to what you did with `process_image()` in the notebook). 
* Fill in the `decision_step()` function within the `decision.py` script with conditional statements that take into consideration the outputs of the `perception_step()` in deciding how to issue throttle, brake and steering commands. 
* Iterate on your perception and decision function until your rover does a reasonable (need to define metric) job of navigating and mapping.  

[//]: # (Image References)

[image0]: ./misc/Simulator.png
[image1]: ./misc/rover_image.jpg
[image2]: ./calibration_images/example_grid1.jpg
[image3]: ./calibration_images/example_rock1.jpg 
[image4]: ./output/rock_threshed.jpg
[image5]: ./output/warped_example.jpg
[image6]: ./output/warped_threshed.jpg
[image7]: ./output/rover_demo_pass.jpg
[image8]: ./output/CT.png
 
---
### Writeup / README

#### Brief 

Here's the Writeup/README for the project 1 of RoboND. 

### Notebook Analysis
#### 1. Run the functions provided in the notebook on test images (first with the test data provided, next on data you have recorded). Add/modify functions to allow for color selection of obstacles and rock samples.

Here I followed the advice given by Ryan on his project walkthrough video tutorial. I managed to implement a terrain, obstacle and find_rock thresheld functions to differentiate the terrain, obstacle and rock out of the image. The output are shown below. 

![alt text][image5]
![alt text][image6]
![alt text][image3]
![alt text][image4]

#### 2. Populate the `process_image()` function with the appropriate analysis steps to map pixels identifying navigable terrain, obstacles and rock samples into a worldmap.  Run `process_image()` on your test data using the `moviepy` functions provided to create video output of your result. 

The output by following the given functions to populate the 'process_image()' function. 

![alt text][image8]

### Autonomous Navigation and Mapping

#### 1. Fill in the `perception_step()` (at the bottom of the `perception.py` script) and `decision_step()` (in `decision.py`) functions in the autonomous mapping scripts and an explanation is provided in the writeup of how and why these functions were modified as they were.


Changes in `perception_step()`:

- To improve fidelity, the worldmap will only get updated if the rover's roll and pitch are within certain set threshed. The final roll and pitch limits are 0.25 which are based trial and error approach. 

- To prevent the rover passing over the rock, the rock pixel are mapped and the rock distances are computed. The minumum rock pixel is taken as the center of the rock coordinates so that the rover can drive towards the rock. 

Changes in `drive_rover()`:

- To maintain fidelity, the maximum velocity of rover is set to 0.8 and the throttle value of rover is set to 0.3. 

Changes in `decision_step()`:

- Initial position of rover is recorded for return to home purpose

- Set a condition to stop the rover when all rock samples are collected 

- Enable rover to detect rock, drive slowly towards it and pick up the rock 

- Add a random state to randomly impose a -5 steering angle to avoid unwanted situations such as driving in a loop on an opened navigable path, strucking in front of obstacles, etc. 


#### 2. Launching in autonomous mode your rover can navigate and map autonomously.  Explain your results and how you might improve them in your writeup.  

**Note: running the simulator with different choices of resolution and graphics quality may produce different results, particularly on different machines!  Make a note of your simulator settings (resolution and graphics quality set on launch) and frames per second (FPS output to terminal by `drive_rover.py`) in your writeup when you submit the project so your reviewer can reproduce your results.**

![alt text][image0]
The screen resolution I chose is 800x600 with the good graphics quality. The FPS output varies from 35 to 38. 

Finally, the rover is able to navigate by itself and picking up rocks out of its sight view.

![alt text][image7]

The image above shows one of the trials that has passed the project requirement (covering 40% of environment at least 60% fidelity with one rock detection). 

I got the rover to cover up the world map of 91.2% at 61.4% fidelity with 5 rocks found and picked.  

A few observations after running the rover I noticed are described below. 


- Sometimes the rover would struck in front of the obstacles or even on the edges of walls. 

- Sometimes the rover would rush over the rock and thus causing the rock out of the sight and the rover would navigate away the direction of rock. 

- The fidelity would usually start about 82% and further dropping in the rock exploration. Setting the max velocity of rover higher would hurt the fidelity.   
 
- The rover would navigate the places that has been explored before and take a few trials to explore the unmapped regions. 

My few future improvements on this project

- train the rover able to learn more about the images and know whether this regions is already visited and thus avoid to visit the regions again 

- train the rover to be able to return to home using path planning algorithm 

- train the rover with more modes to avoid common situations such struck, obstacles blocking, etc



**Credits**

Thank you, Ryan and the awesome team for putting this project together. Also, not forget to thank the Udacity Robotics Slack community with their unselfishness to share and help in this project.  




