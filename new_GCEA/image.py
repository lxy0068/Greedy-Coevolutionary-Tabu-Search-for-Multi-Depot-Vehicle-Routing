import os
import utils
import imageio
import directory

class Image:
    """
    A class to handle saving and creating images and GIFs for algorithm visualization.
    
    Attributes:
        full_images (list): A class-level list storing paths to all generated images.
    """

    full_images = []  # Stores paths to all generated images.

    def __init__(self, generation, instance):
        """
        Initializes an Image object for a specific generation and instance. 
        Creates necessary directories for saving images.

        Args:
            generation (str): The generation identifier.
            instance (str): The instance identifier.
        """
        self.generation = generation
        self.instance = instance
        self.image_counter = 1  # Counter for naming sequential images.
        directory.Directory.create_directories(self.generation, self.instance)

    @staticmethod
    def save_fitness_image(plt):
        """
        Saves a plot as an image for fitness values.

        Args:
            plt (matplotlib.pyplot): The plot object to save.
        """
        plt.savefig(utils.images_dir + utils.fitness_values_name)

    def save(self, plt):
        """
        Saves a plot as an image in the appropriate directory structure for a given generation and instance.

        Args:
            plt (matplotlib.pyplot): The plot object to save.
        """
        plt.savefig(utils.images_dir + utils.generation_dir + self.generation + utils.instance_dir + self.instance +
                    utils.image_name + str(self.image_counter))
        self.image_counter += 1  # Increment the counter for the next image.

    @staticmethod
    def create_best_instances_gif(indexes):
        """
        Creates a GIF from the best instance images across different generations.

        Args:
            indexes (list): List of indexes corresponding to the best instance images.
        """
        folder_path = utils.images_dir
        images = []
        file_names = Image.full_images

        for i in range(len(file_names)):
            if i in indexes:
                images.append(imageio.imread(file_names[i]))  # Add best instance images to the GIF.
        imageio.mimsave(folder_path + utils.best_instances_gif_name + '.gif', images, duration=1)  # Save as GIF.

    def create_instance_gif(self):
        """
        Creates a GIF from all the images generated for a specific instance.

        The GIF represents the progression of the instance through various stages.
        """
        folder_path = utils.images_dir + utils.generation_dir + self.generation + utils.instance_dir + self.instance
        images = []
        file_names = self.get_file_names(folder_path)  # Retrieve all image file names in the folder.

        # Add the last image path to the full_images list for future use.
        Image.full_images.append(folder_path + '/' + file_names[-1])

        for i in file_names:
            images.append(imageio.imread(folder_path + '/' + i))  # Add each image to the GIF sequence.
        imageio.mimsave(folder_path + '.gif', images, duration=0.5)  # Save as GIF with a 0.5-second frame duration.

    def get_file_names(self, folder_path):
        """
        Retrieves and sorts the file names in a given folder.

        Args:
            folder_path (str): The path to the folder containing the image files.

        Returns:
            list: A list of sorted file names.
        """
        file_names = []
        for file in os.listdir(folder_path):
            file_names.append(os.fsdecode(file))  # Decode file names for compatibility.
        return self.sort_to_order(file_names)  # Return sorted file names.

    @staticmethod
    def sort_to_order(file_names):
        """
        Sorts file names in numerical order based on digits extracted from the names.

        Args:
            file_names (list): A list of file names to be sorted.

        Returns:
            list: A list of file names sorted in ascending numerical order.
        """
        file_names.sort(key=lambda i: int(''.join(filter(str.isdigit, i))))  # Sort based on extracted numerical values.
        return file_names
