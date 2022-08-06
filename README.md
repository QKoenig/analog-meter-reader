# Analog Meter Reader

The goal of this project is to create python script using openCV thats able to both detect and determine the orientation of analog gas meters.
 ---
 Ideally a camera could be placed on a static mount orthogonal and centered with the meter to take semi-standardized pictures at fixed time intervals. This script could then be configured to analyze the images taken and convert them into numerical data for further statistical analysis. This is the original image I started with.
![original meter image](readme-images/meter.jpg)
 
 Which I cropped to allow for fewer false positives when using Huegh Circles. Given a fixed camera, the same cropping could be done on every image as a preprocessing step.
 
 ![original meter image](meter_cropped.jpeg)
 
 The image is first converted to greyscale and slightly blured with a gaussian filter as a preprocessing step. To find the meters I run openCV's implementation of the Hough Circle algorithm, which is not ideal for a couple of reasons. First, there are a number of parameters that require tuning depending on the image, primarily min and max radius. Second, it returns many other circular things within the frame resulting in many false negatives. Finally, it may fail to detect a meter as a circle which could cause issues both in missing data points. Depending on how you differentiate the meters, these last two issues can be very large problems and an alternate method of manually boxing or finding the centers of the meters would likely be more robust (you would probably need to use a similarity metric between the images to ensure the camera hasn't moved too much). Regardless, here are the result of a tuned Hough Circle algorithm on the cropped image. 
 
 ![original meter image](readme-images/houghCircles.jpg)
 
 *Note all image processing is done using the greyscaled and blurred image, the original is just used to display results. 
 
 As you can see the algorithm does a fairly good job when tuned for the given image; however, some of the circles are misaligned which is an issue for my method to determine the orientation of the needle. To help resolve this I used the (rather large) assumption that the circles would be roughly on the dial but maybe not centered. My idea was to find the "center of mass" of the surrounding area in which dark pixels are weighted greater than light pixels, with the idea that it would result in a point closer to the true center than the original circle placement. This was accomplished by iterating over a square centered on the original circle with side lengths equal to half the radius. Below is a visualization of the square as well as the improved circle centers in red.
 
  ![original meter image](readme-images/com.jpg)
  
  The next task was to find the pixels that make up each of the 360 lines around the new centers which was accomplished using Bresenham's line algorith, which unfortunately only can produce lines of slopes between 0 and 1 (pictured in green). I get the remaning lines by reflecting the initial ones accross combinations of the x axis, y axis, and y = x.
  
  ![original meter image](readme-images/lines.jpg)
  
  Finally, to determine the orientation of the needle, I found the line with the lowest pixel intensity (most dark pixels). This does a surprisingly good job for its simplicity.
  
  ![original meter image](readme-images/best_line.jpg)
  
  
