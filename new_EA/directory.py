import os
import utils
import shutil


class Directory:
    """
    A utility class for managing directory operations related to the evolutionary algorithm.

    Provides methods to create and delete directories for storing images, generations, and instance-specific data.
    """

    @staticmethod
    def create_directories(generation, instance):
        """
        Creates the necessary directories for storing images, generation-specific, and instance-specific data.

        Args:
            generation (str): The generation identifier for which the directory will be created.
            instance (str): The instance identifier for which the directory will be created.
        """
        Directory.create_image_dir()
        Directory.create_generation_dir(generation)
        Directory.create_instance_dir(generation, instance)

    @staticmethod
    def delete_directories():
        """
        Deletes the images directory and its contents if it exists.

        This is used to clean up temporary files or reset the workspace.
        """
        if os.path.exists(utils.images_dir):
            shutil.rmtree(utils.images_dir)

    @staticmethod
    def create_image_dir():
        """
        Creates the main directory for storing images if it doesn't already exist.

        The directory path is defined in the `utils.images_dir` variable.
        """
        if not os.path.exists(utils.images_dir):
            os.makedirs(utils.images_dir)

    @staticmethod
    def create_generation_dir(generation):
        """
        Creates a directory for a specific generation inside the images directory.

        Args:
            generation (str): The generation identifier for which the directory will be created.
        
        The path format is `utils.images_dir + utils.generation_dir + generation`.
        """
        generation_path = os.path.join(utils.images_dir, utils.generation_dir, generation)
        if not os.path.exists(generation_path):
            os.makedirs(generation_path)

    @staticmethod
    def create_instance_dir(generation, instance):
        """
        Creates a directory for a specific instance within a specific generation directory.

        Args:
            generation (str): The generation identifier for which the directory will be created.
            instance (str): The instance identifier for which the directory will be created.

        The path format is `utils.images_dir + utils.generation_dir + generation + utils.instance_dir + instance`.
        """
        instance_path = os.path.join(utils.images_dir, utils.generation_dir, generation, utils.instance_dir, instance)
        if not os.path.exists(instance_path):
            os.makedirs(instance_path)
