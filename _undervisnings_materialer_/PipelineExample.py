# Adding parent folder to include path, only relevant for this showcase
import sys
sys.path.append('..')

# Importing IMPP and OpenCV
import IMPP
import cv2

img = cv2.imread('Peppers.tiff') # Reading test image
cv2.imshow("Original", img) # Display original for comparison

## Create a pipeline object ##
# The pipeline object constructor takes in a list of PostProcessingBlock objects #
# The list can be created before the pipeline or as part of the constructor call for the pipeline #

## Scenario 1: Creating a list of PostProcessBlock objects first and using it in the constructor for the pipeline ##
# Functionality: Converts to gray then blurs using a gaussian filter with the size of 5
ppbs = [IMPP.ConvertToGray(), IMPP.GaussianBlur(5)] # List of PostProcessingBlock objects
pipeline1 = IMPP.PostProcessingPipeline(ppbs) # Construction of pipeline object

## Scenario 2: The PostProcessingBlock objects are constructed in the pipelines constructor call
# Functionality: Converts to gray then blurs using a gaussian filter with the size of 5
pipeline2 = IMPP.PostProcessingPipeline([IMPP.ConvertToGray(), IMPP.GaussianBlur(5)]) # Construction of pipeline object and PostProcessingBlock objects

## Using the pipeline to process images ##
outputImg1 = pipeline1.run(img.copy()) # Running the pipeline on a copy of the image
cv2.imshow("Output of pipeline1", outputImg1) # Displaying output image

outputImg2 = pipeline2.run(img.copy()) # Running the pipeline on a copy of the image
cv2.imshow("Output of pipeline2", outputImg2) # Displaying output image

cv2.waitKey(0) # Wait for user to press key (blocking call)
