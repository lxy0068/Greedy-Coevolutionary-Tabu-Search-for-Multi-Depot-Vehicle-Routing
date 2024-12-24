import os
import utils
import imageio
import directory

class Image:
    """
    The Image class handles image saving, organizing, and generating GIFs for visualizing
    evolutionary algorithm results, such as best instance animations and route solutions.
    """
    full_images = []  # Class-level storage for full images.

    def __init__(self, generation, instance):
        """
        Initialize the Image object and create necessary directories.

        Args:
            generation (str): The generation number as a string.
            instance (str): The instance number as a string.
        """
        self.generation = generation
        self.instance = instance
        self.image_counter = 1
        directory.Directory.create_directories(self.generation, self.instance)

    @staticmethod
    def save_fitness_image(plt):
        """
        Save the fitness graph as an image.

        Args:
            plt (matplotlib.pyplot): The plot object to save.
        """
        plt.savefig(utils.images_dir + utils.fitness_values_name)

    def save(self, plt):
        """
        Save a plot image for the current instance and generation.

        Args:
            plt (matplotlib.pyplot): The plot object to save.
        """
        plt.savefig(utils.images_dir + utils.generation_dir + self.generation +
                    utils.instance_dir + self.instance + utils.image_name + str(self.image_counter))
        self.image_counter += 1

    @staticmethod
    def create_best_instances_gif(indexes):
        """
        Create a GIF from the images of the best instances.

        Args:
            indexes (list): List of indexes corresponding to the best instance images.
        """
        folder_path = utils.images_dir
        images = []
        file_names = Image.full_images

        for i in range(len(file_names)):
            if i in indexes:
                images.append(imageio.imread(file_names[i]))
        imageio.mimsave(folder_path + utils.best_instances_gif_name + '.gif', images, duration=1)

    def create_instance_gif(self):
        """
        Create a GIF for the current instance using saved images.
        """
        folder_path = utils.images_dir + utils.generation_dir + self.generation + utils.instance_dir + self.instance
        images = []
        file_names = self.get_file_names(folder_path)

        Image.full_images.append(folder_path + '/' + file_names[-1])

        for i in file_names:
            images.append(imageio.imread(folder_path + '/' + i))
        imageio.mimsave(folder_path + '.gif', images, duration=0.5)

    def get_file_names(self, folder_path):
        """
        Retrieve and sort file names from a directory.

        Args:
            folder_path (str): The path of the folder to retrieve file names from.

        Returns:
            list: Sorted list of file names in the folder.
        """
        file_names = []
        for file in os.listdir(folder_path):
            file_names.append(os.fsdecode(file))
        return self.sort_to_order(file_names)

    @staticmethod
    def sort_to_order(file_names):
        """
        Sort file names in ascending numerical order.

        Args:
            file_names (list): List of file names to sort.

        Returns:
            list: Numerically sorted list of file names.
        """
        file_names.sort(key=lambda i: int(''.join(filter(str.isdigit, i))))
        return file_names
