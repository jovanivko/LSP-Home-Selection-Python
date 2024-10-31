import matplotlib.pyplot as plt
from PIL import Image
import os

def create_image_grid(image_folder, num_images, offset, output_filename, grid_shape, img_size):
    """
    Combines the PNG plots into one image in a grid.

    Args:
    - image_folder (str): The directory where PNG images are stored.
    - num_images (int): The number of images to combine.
    - output_filename (str): The name of the output file for the combined image.
    - grid_shape (tuple): The grid shape (rows, cols) in which to combine the images.
    """
    figsize = (grid_shape[1] * img_size[0], grid_shape[0] * img_size[1])

    fig, axes = plt.subplots(grid_shape[0], grid_shape[1], figsize=figsize)
    # Iterate over images and axes to load and display each image in the grid
    for idx, ax in enumerate(axes.flat):
        if idx < num_images:
            img_path = os.path.join(image_folder, f'criterion_{offset + idx + 1}_plot.png')  # assuming sequential filenames
            img = Image.open(img_path)
            ax.imshow(img)
            ax.axis('off')
        else:
            ax.axis('off')

    # Adjust layout
    plt.tight_layout()

    # Save the final grid as a PNG file
    plt.savefig(f"{image_folder}/{output_filename}", dpi=300)
    plt.show()


# Generate first image with 14 plots in a 3x5 grid
create_image_grid('criterion', 16, 0, 'combined_plots_1.png', (4, 4), img_size=(1.875, 2.625))

# Generate second image with 12 plots in a 3x4 grid
create_image_grid('criterion', 10, 15, 'combined_plots_2.png', (3, 4), img_size=(1.875, 2.625))
