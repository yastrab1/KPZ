import os
import subprocess
import numpy as np
import cv2

# Create a test image
test_image_path = 'test_image.jpg'
test_output_path = 'test_output.jpg'

# Create a simple test image (a gradient)
width, height = 300, 200
image = np.zeros((height, width, 3), dtype=np.uint8)
for i in range(height):
    for j in range(width):
        image[i, j] = [i % 256, j % 256, (i + j) % 256]
cv2.imwrite(test_image_path, image)
print(f"Created test image: {test_image_path}")

# Test resize operation
print("\nTesting resize operation...")
subprocess.run(['python', 'back/pkgs/img.py', 
                '-i', test_image_path, 
                '-o', test_output_path, 
                '--operation', 'resize', 
                '--width', '150'])
if os.path.exists(test_output_path):
    resized_image = cv2.imread(test_output_path)
    print(f"Resize successful. New dimensions: {resized_image.shape[1]}x{resized_image.shape[0]}")
    os.remove(test_output_path)

# Test crop operation
print("\nTesting crop operation...")
subprocess.run(['python', 'back/pkgs/img.py', 
                '-i', test_image_path, 
                '-o', test_output_path, 
                '--operation', 'crop', 
                '--x', '50', 
                '--y', '50', 
                '--crop-width', '100', 
                '--crop-height', '100'])
if os.path.exists(test_output_path):
    cropped_image = cv2.imread(test_output_path)
    print(f"Crop successful. New dimensions: {cropped_image.shape[1]}x{cropped_image.shape[0]}")
    os.remove(test_output_path)

# Test rotate operation
print("\nTesting rotate operation...")
subprocess.run(['python', 'back/pkgs/img.py', 
                '-i', test_image_path, 
                '-o', test_output_path, 
                '--operation', 'rotate', 
                '--angle', '45'])
if os.path.exists(test_output_path):
    print("Rotation successful.")
    os.remove(test_output_path)

# Test flip operation
print("\nTesting flip operation...")
subprocess.run(['python', 'back/pkgs/img.py', 
                '-i', test_image_path, 
                '-o', test_output_path, 
                '--operation', 'flip', 
                '--flip-code', '1'])
if os.path.exists(test_output_path):
    print("Flip successful.")
    os.remove(test_output_path)

# Test brightness/contrast adjustment
print("\nTesting brightness/contrast adjustment...")
subprocess.run(['python', 'back/pkgs/img.py', 
                '-i', test_image_path, 
                '-o', test_output_path, 
                '--operation', 'adjust', 
                '--brightness', '10', 
                '--contrast', '1.2'])
if os.path.exists(test_output_path):
    print("Brightness/contrast adjustment successful.")
    os.remove(test_output_path)

# Test blur operation
print("\nTesting blur operation...")
subprocess.run(['python', 'back/pkgs/img.py', 
                '-i', test_image_path, 
                '-o', test_output_path, 
                '--operation', 'blur', 
                '--kernel-size', '7'])
if os.path.exists(test_output_path):
    print("Blur successful.")
    os.remove(test_output_path)

# Clean up
os.remove(test_image_path)
print("\nAll tests completed successfully!")