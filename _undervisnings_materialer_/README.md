# IMPP - Image Processing Pipeline
IMPP is a Python framework incorperating OpenCV in a pipeline workflow. The framework also comes with some implementation of commonly used functionalities in computer vision.

IMPP is built with the goal to make it easier to use and not performance.

Be advised IMPP is currently under development!

## How to include IMPP

1. Download and include the `IMPP.py` and `IMPPRequirements.txt` files in your project directory
2. Install requirements for IMPP using the following command: `pip install -r IMPPRequirements.txt`
2. Import `IMPP`, like any other module in python

## How to use the pipeline in IMPP

See `PipelineExample.py` in the folder `Examples`.

## How to use custom PostProcessingBlocks

See `CustomBlockExample.py` in the folder `Examples`.

&nbsp;

# Current PostProcessingBlocks

List of currently implemented PostProcessingBlocks.


## Generics

***

### PostProcessingBlock

Base class for all PostProcessingBlock.

**PostProcessingBlock.run(self, input)**

Returns `input`.

***

### CustomKernel

Extended base class for kernel based PostProcessingBlocks.

**CustomKernel.__init__(self, kernel, showOutput = False, outputWindowName = 'CustomKernel')**

| Variable | Type | Description |
| --- | --- | --- |
| kernel | Numpy 2d array | The kernel that should be applied to the input when the block is run |
| showOutput | bool | Toggles the displaying of output (intended for debugging) |
| outputWindowName | string | Name given to the display window (intended for debugging) |

**CustomKernel.run(self, input)**

Expects `input` to be an image.

Returns the image processed with the kernel stored in the object.

***

&nbsp;
## Conversions

***

### ConvertToGray

Converts a color image to a grayscale image.

**ConvertToGray.__init__(self, showOutput = False, outputWindowName = 'Grayscale')**

| Variable | Type | Description |
| --- | --- | --- |
| showOutput | bool | Toggles the displaying of output (intended for debugging) |
| outputWindowName | string | Name given to the display window (intended for debugging) |

**ConvertToGray.run(self, input)**

Expects `input` to be a color image.

Returns a grayscaled version of the image.

***

### GetRedChannel

Creates a grayscale image from the red channel of a color image.

**GetRedChannel.__init__(self, showOutput = False, outputWindowName = 'RedChannel')**

| Variable | Type | Description |
| --- | --- | --- |
| showOutput | bool | Toggles the displaying of output (intended for debugging) |
| outputWindowName | string | Name given to the display window (intended for debugging) |

**GetRedChannel.run(self, input)**

Expects `input` to be a color image.

Returns a grayscale image based only on the red channel of the input.

***

### GetGreenChannel

Creates a grayscale image from the green channel of a color image.

**GetGreenChannel.__init__(self, showOutput = False, outputWindowName = 'GreenChannel')**

| Variable | Type | Description |
| --- | --- | --- |
| showOutput | bool | Toggles the displaying of output (intended for debugging) |
| outputWindowName | string | Name given to the display window (intended for debugging) |

**GetGreenChannel.run(self, input)**

Expects `input` to be a color image.

Returns a grayscale image based only on the green channel of the input.

***

### GetBlueChannel

Creates a grayscale image from the blue channel of a color image.

**GetBlueChannel.__init__(self, showOutput = False, outputWindowName = 'BlueChannel')**

| Variable | Type | Description |
| --- | --- | --- |
| showOutput | bool | Toggles the displaying of output (intended for debugging) |
| outputWindowName | string | Name given to the display window (intended for debugging) |

**GetBlueChannel.run(self, input)**

Expects `input` to be a color image.

Returns a grayscale image based only on the blue channel of the input.

***

&nbsp;
## Blurring

***

### AverageBlur

Applies an average blur to an image. Uses CustomKernel, see run from CustomKernel. Kernel used is genereted in the constructor.

**AverageBlur.__init__(self, filterSize, showOutput = False, outputWindowName = 'AverageBlur')**

| Variable | Type | Description |
| --- | --- | --- |
| filterSize | int | Size of the kernel used in the filtering process |
| showOutput | bool | Toggles the displaying of output (intended for debugging) |
| outputWindowName | string | Name given to the display window (intended for debugging) |

***

### GaussianBlur

Applies a gaussian blur to an image. Uses CustomKernel, see run from CustomKernel. Kernel used is genereted in the constructor.

**GaussianBlur.__init__(self, filterSize, showOutput = False, outputWindowName = 'GaussianBlur')**

| Variable | Type | Description |
| --- | --- | --- |
| filterSize | int | Size of the kernel used in the filtering process |
| showOutput | bool | Toggles the displaying of output (intended for debugging) |
| outputWindowName | string | Name given to the display window (intended for debugging) |

***

### MedianBlur

Applies a median blur to an image.

**MedianBlur.__init__(self, filterSize, showOutput = False, outputWindowName = 'MedianBlur')**

| Variable | Type | Description |
| --- | --- | --- |
| filterSize | int | Size of the kernel used in the filtering process |
| showOutput | bool | Toggles the displaying of output (intended for debugging) |
| outputWindowName | string | Name given to the display window (intended for debugging) |

**MedianBlur.run(self, input)**

Expects `input` to be an image.

Returns the blurred input image.

***

### BilateralFilter

Applies bilateral filetring to an image.

**BilateralFilter.__init__(self, filterSize, sigmaColor, sigmaSpace, showOutput = False, outputWindowName = 'BilateralFilter')**

| Variable | Type | Description |
| --- | --- | --- |
| filterSize | int | Size of the kernel used in the filtering process |
| sigmaColor | int | Filter sigma in the color space. A larger value of the parameter means that farther colors within the pixel neighborhood will be mixed together, resulting in larger areas of semi-equal color. |
| sigmaSpace | int | Filter sigma in the coordinate space. A larger value of the parameter means that farther pixels will influence each other as long as their colors are close enough. When d>0, it specifies the neighborhood size regardless of sigmaSpace. Otherwise, d is proportional to sigmaSpace. |
| showOutput | bool | Toggles the displaying of output (intended for debugging) |
| outputWindowName | string | Name given to the display window (intended for debugging) |

**BilateralFilter.run(self, input)**

Expects `input` to be an image.

Returns the filtered input image.

***

&nbsp;
## Sharpening

***

### LaplacianSharpen

Sharpens an image using laplacian sharpen.

**LaplacianSharpen.__init__(self, scale: float = 1, diagonal: bool = True, showOutput: bool = False, outputWindowName: str = 'LaplacianSharpen')**

| Variable | Type | Description |
| --- | --- | --- |
| scale | float | Scaling of the kernel used in the filtering process |
| diagonal | bool | Defines whether or not diagonal pixels are included in the kernel |
| showOutput | bool | Toggles the displaying of output (intended for debugging) |
| outputWindowName | string | Name given to the display window (intended for debugging) |

**LaplacianSharpen.run(self, input)**

Expects `input` to be an image.

Returns the sharpened input image.

***

### UnsharpMasking

Sharpens an image using unsharp masking.

**UnsharpMasking.__init__(self, filterSize: int = 3, showOutput: bool = False, outputWindowName: str = 'UnsharpMasking')**

| Variable | Type | Description |
| --- | --- | --- |
| filterSize | int | Size of the kernel used in the filtering process |
| showOutput | bool | Toggles the displaying of output (intended for debugging) |
| outputWindowName | string | Name given to the display window (intended for debugging) |

**UnsharpMasking.run(self, input)**

Expects `input` to be an image.

Returns the sharpened input image.

***

&nbsp;
## Thresholding

***

### Threshold

Thresholds an image using lower and upper bounds.

**Threshold.__init__(self, lowerBound: int, upperBound: int, mode: int = cv2.THRESH_BINARY, showOutput: bool = False, outputWindowName: str = 'Threshold')**

| Variable | Type | Description |
| --- | --- | --- |
| lowerBound | int | Lower boundary of the threshold |
| upperBound | int | Upper boundary of the threshold |
| mode | int | Thresholding mode |
| showOutput | bool | Toggles the displaying of output (intended for debugging) |
| outputWindowName | string | Name given to the display window (intended for debugging) |

**Threshold.run(self, input)**

Expects `input` to be an image.

Returns a binary image.

***

### AdaptiveThreshold

Thresholds an image adaptively.

**AdaptiveThreshold.__init__(self, upperBound: int, blockSize: int, constant: int, adaptionMode: int = cv2.ADAPTIVE_THRESH_GAUSSIAN_C, thresholdMode: int = cv2.THRESH_BINARY, showOutput: bool = False, outputWindowName: str = 'AdaptiveThreshold')**

| Variable | Type | Description |
| --- | --- | --- |
| upperBound | int | Upper boundary of the threshold |
| blockSize | int | Size of the neighborhood that is used to calculate a threshold value for a pixel |
| constant | int | Constant subtracted from the mean or weighted mean |
| adaptionMode | int | Adaption mode |
| thresholdMode | int | Thresholding mode |
| showOutput | bool | Toggles the displaying of output (intended for debugging) |
| outputWindowName | string | Name given to the display window (intended for debugging) |

**AdaptiveThreshold.run(self, input)**

**Threshold.run(self, input)**

Expects `input` to be an image.

Returns a binary image.

***

### OtsuBinarization

Thresholds an image using otsu binarization.

**OtsuBinarization.__init__(self, showOutput: bool = False, outputWindowName: str = 'OtsuBinarization')**

| Variable | Type | Description |
| --- | --- | --- |
| showOutput | bool | Toggles the displaying of output (intended for debugging) |
| outputWindowName | string | Name given to the display window (intended for debugging) |

**OtsuBinarization.run(self, input)**

Expects `input` to be an image.

Returns a binary image.

***

&nbsp;
## Contours

***

### DetectContours

Detects contours in an image.

**DetectContours.__init__(self, mode: int = cv2.RETR_EXTERNAL, method: int = cv2.CHAIN_APPROX_SIMPLE, printResult: bool = False, draw: bool = False, drawInfo: ContourDrawInfo = None, outputWindowName: str = 'DetectContours')**

| Variable | Type | Description |
| --- | --- | --- |
| mode | int | Contour retrieval mode |
| method | int | Contour approximation method |
| printResult | bool | Toggles the output being printed to the terminal (intended for debugging) |
| draw | bool | Toggles the displaying of output (intended for debugging) |
| drawInfo | ContourDrawInfo | Object containing information on how to draw the output (intended for debugging) |
| outputWindowName | string | Name given to the display window (intended for debugging) |

**DetectContours.run(self, input)**

Expects `input` to be an image.

Returns a list of contours.

***

### ThresholdContours

Thresholds a list of contours based on contour area.

**ThresholdContours.__init__(self, minArea: float, maxArea: float, printDebug: bool = False)**

| Variable | Type | Description |
| --- | --- | --- |
| minArea | float | Minimum area of contours |
| maxArea | float | Maximum area of contours |
| printDebug | bool | Toggles the output being printed to the terminal (intended for debugging) |

**DetectContours.run(self, input)**

Expects `input` to be a list of contours.

Returns a list of contours.

***

&nbsp;
## Shapes

***

### DetectShapes

Detect shapes in a list of contours.

**DetectShapes.__init__(self, closed: bool = True, epsilon: float = 0.04, printResult: bool = False)**

| Variable | Type | Description |
| --- | --- | --- |
| closed | bool | Flag indicating whether the curves are closed or not |
| epsilon | float | Parameter specifying the approximation accuracy. This is the maximum distance between the original curve and its approximation. |
| printResult | bool | Toggles the output being printed to the terminal (intended for debugging) |

**DetectShapes.run(self, input)**

Expects `input` to be a list of contours.

Returns a list of Shape objects.

***