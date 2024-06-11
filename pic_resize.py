import os
import sys
import platform
from PIL import Image

def clear_screen():
    """Clears the terminal screen based on the operating system."""
    if platform.system() == 'Windows':
        os.system('cls')
    else:
        os.system('clear')

def resize_images(percentage):
    # Get the current directory
    directory = os.getcwd()

    # Get the list of files in the directory
    files = os.listdir(directory)

    # Filter JPG and PNG files
    image_files = [file for file in files if file.lower().endswith(('.jpg', '.jpeg', '.png'))]

    # Check if there are any image files
    if len(image_files) == 0:
        print("No JPG or PNG files found in the directory.")
        return

    # Create a new directory for resized images
    new_directory = f"resized_images_{percentage}"
    os.makedirs(new_directory, exist_ok=True)

    print(f"Resizing images by {percentage}% ...")

    # Resize each image
    for file in image_files:
        # Open the image
        image_path = os.path.join(directory, file)
        image = Image.open(image_path)

        # Calculate the new width and height
        width, height = image.size
        new_width = int(width * percentage / 100)
        new_height = int(height * percentage / 100)

        # Resize the image
        resized_image = image.resize((new_width, new_height))

        # Save the resized image with a new filename
        new_filename = f"resized_{percentage}_{file}"
        new_image_path = os.path.join(new_directory, new_filename)

        # Save the resized image as JPEG or PNG based on the original file extension
        if file.lower().endswith(('.jpg', '.jpeg')):
            resized_image.save(new_image_path, 'JPEG')
        elif file.lower().endswith('.png'):
            resized_image.save(new_image_path, 'PNG')

        print(f"Resized {file} and saved as {new_filename}")

    print("Image resizing complete.")

def main():
    # Clear the screen
    clear_screen()

    # Check if the percentage argument is provided
    if len(sys.argv) != 2:
        print("Please provide a valid scale factor percentage argument.")
        print("Usage: pic_resize.py <percentage> (1 - 400)")
        print("Example: pic_resize.py 200")
        return

    # Get the resize percentage from the command line argument
    try:
        percentage = int(sys.argv[1])
        if percentage < 1 or percentage > 400:
            print("Please provide a resize percentage between 1 and 400.")
            return
    except ValueError:
        print("Please provide a valid scale factor percentage argument.")
        print("Usage: pic_resize.py <percentage> (1 - 400)")
        print("Example: pic_resize.py 200")
        return

    # Resize the images
    resize_images(percentage)

if __name__ == "__main__":
    main()

