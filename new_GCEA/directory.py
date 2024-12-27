import os
import utils
import shutil


class Directory(object):
    """
    A utility class for managing directory structures.
    Provides methods to create and delete directories
    for images, generations, and instances.
    """

    @staticmethod
    def create_directories(generation, instance):
        """
        Creates a hierarchical directory structure for storing images.
        
        Parameters:
        - generation (str): The generation identifier used to name the generation directory.
        - instance (str): The instance identifier used to name the instance directory.
        
        Actions:
        - Creates the main image directory.
        - Creates a generation-specific directory inside the image directory.
        - Creates an instance-specific directory inside the generation directory.
        """
        Directory.create_image_dir()
        Directory.create_generation_dir(generation)
        Directory.create_instance_dir(generation, instance)

    @staticmethod
    def delete_directories():
        """
        Deletes the main image directory if it exists.
        
        Actions:
        - Removes the entire images directory recursively.
        
        Note:
        - This action is irreversible and deletes all contents within the directory.
        """
        if os.path.exists(utils.images_dir):
            shutil.rmtree(utils.images_dir)

    @staticmethod
    def create_image_dir():
        """
        Creates the main image directory if it does not already exist.
        
        Directory Structure:
        - utils.images_dir: The base directory for all image-related files.
        """
        if not os.path.exists(utils.images_dir):
            os.makedirs(utils.images_dir)

    @staticmethod
    def create_generation_dir(generation):
        """
        Creates a directory for a specific generation inside the main image directory.
        
        Parameters:
        - generation (str): The generation identifier used for the directory name.
        
        Directory Structure:
        - utils.images_dir/utils.generation_dir/{generation}
        """
        generation_path = os.path.join(utils.images_dir, utils.generation_dir, generation)
        if not os.path.exists(generation_path):
            os.makedirs(generation_path)

    @staticmethod
    def create_instance_dir(generation, instance):
        """
        Creates a directory for a specific instance inside a generation directory.
        
        Parameters:
        - generation (str): The generation identifier.
        - instance (str): The instance identifier used for the directory name.
        
        Directory Structure:
        - utils.images_dir/utils.generation_dir/{generation}/utils.instance_dir/{instance}
        """
        instance_path = os.path.join(
            utils.images_dir, utils.generation_dir, generation, utils.instance_dir, instance
        )
        if not os.path.exists(instance_path):
            os.makedirs(instance_path)
