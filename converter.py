## Import the necessary modules, os for file processing and cv2 for the conversion
import os
import cv2

## Reading the folders in that directory and then getting the length to store in a variable
size = len(os.listdir("dataset"))
num = 1

while num != (size+1):
    
    # Create new directory to store values
    path = f'binary/{num}'

    os.mkdir(f'binary/{num}')

    # The current directory
    dataset = f"dataset/{num}/"
    
    
    for file in os.listdir(dataset):
        get_dir = (os.path.join(dataset, file)) # get the full path from the root of your project directory to the file

        # Convert to grayscale
        img_grey = cv2.imread(get_dir, cv2.IMREAD_GRAYSCALE)
        thresh = 210

        # Convert to binary
        img_binary = cv2.threshold(img_grey, thresh, 255, cv2.THRESH_BINARY)[1]

        # Save the binary file in the new directory
        cv2.imwrite(f'{path}/{file}', img_binary)
        
    num+=1
print("successful")

## Runtime = 40 seconds