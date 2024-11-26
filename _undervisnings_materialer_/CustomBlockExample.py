# Adding parent folder to include path, only relevant for this showcase
import sys
sys.path.append('..')

# Importing IMPP and OpenCV
import IMPP
import cv2

img = cv2.imread('Peppers.tiff') # Reading test image
cv2.imshow("Original", img) # Display original for comparison

## Create custom PostProcessingBlock ##
# Functionality: add red to image
class AddRed(IMPP.PostProcessingBlock): # Create class for custom PostProcessingBlock inheriting from PostProcessingBlock
    def __init__(self, amount: int) -> None: # Store amount of red to add in object
        self.amount = amount

    def run(self, input): # Override 'run' function from PostProcessingBlock, function that is run in the pipeline
        height = input.shape[0] # Get height of input image
        width = input.shape[1] # Get width of input image

        for y in range(0, height): # Loop height
            for x in range(0, width): # Loop width
                input[y, x, 2] = min(input[y, x, 2] + self.amount, 255) # Add amount to red channel of the pixel, max value at 255
        
        return input # Return the modified image

## Running custom PostProcessingBlock (without pipeline) ##
customBlock = AddRed(50) # Create object of custom PostProcessingBlock
customOutput = customBlock.run(img.copy()) # Call run function from object of custom PostProcessingBlock with a copy of the img
cv2.imshow("Custom block output", customOutput) # Show output of custom PostProcessingBlock

cv2.waitKey(0) # Wait for user to press key (blocking call)
