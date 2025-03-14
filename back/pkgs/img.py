import argparse
import cv2
import numpy as np
import os
import sys

def resize_image(image, width=None, height=None, scale=None):
    """
    Resize an image to the specified dimensions.

    Args:
        image: The input image
        width: Target width (if None, will be calculated from height and aspect ratio)
        height: Target height (if None, will be calculated from width and aspect ratio)
        scale: Scale factor (if provided, width and height are ignored)

    Returns:
        Resized image
    """
    if scale is not None:
        return cv2.resize(image, None, fx=scale, fy=scale, interpolation=cv2.INTER_AREA)

    if width is None and height is None:
        return image

    h, w = image.shape[:2]

    if width is None:
        aspect_ratio = w / h
        width = int(height * aspect_ratio)
    elif height is None:
        aspect_ratio = h / w
        height = int(width * aspect_ratio)

    return cv2.resize(image, (width, height), interpolation=cv2.INTER_AREA)

def crop_image(image, x, y, width, height):
    """
    Crop an image to the specified region.

    Args:
        image: The input image
        x: X-coordinate of the top-left corner
        y: Y-coordinate of the top-left corner
        width: Width of the crop region
        height: Height of the crop region

    Returns:
        Cropped image
    """
    return image[y:y+height, x:x+width]

def rotate_image(image, angle, center=None):
    """
    Rotate an image by the specified angle.

    Args:
        image: The input image
        angle: Rotation angle in degrees
        center: Center of rotation (if None, the center of the image is used)

    Returns:
        Rotated image
    """
    h, w = image.shape[:2]
    if center is None:
        center = (w // 2, h // 2)

    rotation_matrix = cv2.getRotationMatrix2D(center, angle, 1.0)
    return cv2.warpAffine(image, rotation_matrix, (w, h))

def flip_image(image, flip_code):
    """
    Flip an image horizontally, vertically, or both.

    Args:
        image: The input image
        flip_code: 0 for vertical flip, 1 for horizontal flip, -1 for both

    Returns:
        Flipped image
    """
    return cv2.flip(image, flip_code)

def adjust_brightness_contrast(image, brightness=0, contrast=1.0):
    """
    Adjust the brightness and contrast of an image.

    Args:
        image: The input image
        brightness: Brightness adjustment (0 = no change, positive = brighter, negative = darker)
        contrast: Contrast adjustment (1.0 = no change, >1.0 = more contrast, <1.0 = less contrast)

    Returns:
        Adjusted image
    """
    return cv2.convertScaleAbs(image, alpha=contrast, beta=brightness)

def apply_blur(image, kernel_size=5):
    """
    Apply Gaussian blur to an image.

    Args:
        image: The input image
        kernel_size: Size of the Gaussian kernel

    Returns:
        Blurred image
    """
    return cv2.GaussianBlur(image, (kernel_size, kernel_size), 0)

def main():
    parser = argparse.ArgumentParser(description='Image manipulation utility')

    # Input and output arguments
    parser.add_argument('-i', '--input', required=True, help='Input image path')
    parser.add_argument('-o', '--output', required=True, help='Output image path')

    # Operation selection
    parser.add_argument('--operation', choices=['resize', 'crop', 'rotate', 'flip', 'adjust', 'blur'], 
                        required=True, help='Operation to perform')

    # Resize parameters
    parser.add_argument('--width', type=int, help='Target width for resize')
    parser.add_argument('--height', type=int, help='Target height for resize')
    parser.add_argument('--scale', type=float, help='Scale factor for resize')

    # Crop parameters
    parser.add_argument('--x', type=int, help='X-coordinate for crop')
    parser.add_argument('--y', type=int, help='Y-coordinate for crop')
    parser.add_argument('--crop-width', type=int, help='Width for crop')
    parser.add_argument('--crop-height', type=int, help='Height for crop')

    # Rotate parameters
    parser.add_argument('--angle', type=float, help='Rotation angle in degrees')

    # Flip parameters
    parser.add_argument('--flip-code', type=int, choices=[0, 1, -1], 
                        help='Flip code: 0 for vertical, 1 for horizontal, -1 for both')

    # Brightness/contrast parameters
    parser.add_argument('--brightness', type=float, default=0, help='Brightness adjustment')
    parser.add_argument('--contrast', type=float, default=1.0, help='Contrast adjustment')

    # Blur parameters
    parser.add_argument('--kernel-size', type=int, default=5, help='Kernel size for blur')

    args = parser.parse_args()

    # Check if input file exists
    if not os.path.isfile(args.input):
        print(f"Error: Input file '{args.input}' does not exist")
        sys.exit(1)

    # Read the input image
    image = cv2.imread(args.input)
    if image is None:
        print(f"Error: Could not read image '{args.input}'")
        sys.exit(1)

    # Perform the selected operation
    if args.operation == 'resize':
        if args.width is None and args.height is None and args.scale is None:
            print("Error: For resize operation, provide at least one of: --width, --height, --scale")
            sys.exit(1)
        result = resize_image(image, args.width, args.height, args.scale)

    elif args.operation == 'crop':
        if args.x is None or args.y is None or args.crop_width is None or args.crop_height is None:
            print("Error: For crop operation, provide all of: --x, --y, --crop-width, --crop-height")
            sys.exit(1)
        result = crop_image(image, args.x, args.y, args.crop_width, args.crop_height)

    elif args.operation == 'rotate':
        if args.angle is None:
            print("Error: For rotate operation, provide --angle")
            sys.exit(1)
        result = rotate_image(image, args.angle)

    elif args.operation == 'flip':
        if args.flip_code is None:
            print("Error: For flip operation, provide --flip-code")
            sys.exit(1)
        result = flip_image(image, args.flip_code)

    elif args.operation == 'adjust':
        result = adjust_brightness_contrast(image, args.brightness, args.contrast)

    elif args.operation == 'blur':
        result = apply_blur(image, args.kernel_size)
    else:
        raise ValueError("Unknown operation '{}'".format(args.operation))

    # Save the result
    cv2.imwrite(args.output, result)
    print(f"Image successfully processed and saved to '{args.output}'")

if __name__ == "__main__":
    main()
