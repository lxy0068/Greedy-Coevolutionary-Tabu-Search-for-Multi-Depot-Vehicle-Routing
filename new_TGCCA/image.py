import os
import utils
import imageio
import directory



class Image:
    full_images = []

    def __init__(self, generation, instance):
        self.generation = generation
        self.instance = instance
        self.image_counter = 1
        directory.Directory.create_directories(self.generation, self.instance)

    @staticmethod
    def save_fitness_image(plt):
        plt.tight_layout()
        plt.savefig(os.path.join(utils.images_dir, utils.fitness_values_name), bbox_inches='tight', pad_inches=0.1, dpi=150)

    def save(self, plt):
        path = os.path.join(utils.images_dir, utils.generation_dir, self.generation, utils.instance_dir, self.instance)
        if not os.path.exists(path):
            os.makedirs(path)
        plt.tight_layout()
        plt.savefig(os.path.join(path, f'{utils.image_name}{self.image_counter}.png'), bbox_inches='tight', pad_inches=0.1, dpi=120)
        self.image_counter += 1

    @staticmethod
    def create_best_instances_gif(indexes):
        folder_path = utils.images_dir
        images = []
        file_names = Image.full_images

        for i, file_name in enumerate(file_names):
            if i in indexes:
                images.append(imageio.imread(file_name))
        if images:
            output_path = os.path.join(folder_path, f'{utils.best_instances_gif_name}.gif')
            imageio.mimsave(output_path, images, duration=1)

    def create_instance_gif(self):
        folder_path = os.path.join(utils.images_dir, utils.generation_dir, self.generation, utils.instance_dir, self.instance)
        images = []
        file_names = self.get_file_names(folder_path)

        if file_names:
            Image.full_images.append(os.path.join(folder_path, file_names[-1]))

        for file_name in file_names:
            images.append(imageio.imread(os.path.join(folder_path, file_name)))
        if images:
            imageio.mimsave(f'{folder_path}.gif', images, duration=0.5)

    def get_file_names(self, folder_path):
        file_names = [os.fsdecode(file) for file in os.listdir(folder_path) if file.endswith('.png')]
        return self.sort_to_order(file_names)

    @staticmethod
    def sort_to_order(file_names):
        file_names.sort(key=lambda i: int(''.join(filter(str.isdigit, i))))
        return file_names
