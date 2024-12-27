import os
import numpy as np
import matplotlib.pyplot as plt
from image import Image


class Graph:
    """
    A class to handle graph plotting for visualizing various aspects of evolutionary algorithms
    and optimization problems, including fitness trends, convergence rates, solution quality,
    diversity, and computational efficiency.
    
    Attributes:
        customers (list): A list of customer objects with their coordinates.
        depots (list): A list of depot objects with their coordinates.
    """

    def __init__(self, customers, depots):
        """
        Initializes the Graph object with customers and depots.

        Args:
            customers (list): A list of customer objects.
            depots (list): A list of depot objects.
        """
        self.customers = customers
        self.depots = depots

    @staticmethod
    def draw_fitness_graph(fitness_list, algorithm_name="EA"):
        """
        Draws a bar graph showing fitness values across generations and instances.

        Args:
            fitness_list (list): A list of fitness objects, each containing generation and instance data.
            algorithm_name (str): Name of the algorithm (default is "EA").
        """
        if not fitness_list:
            return

        generations = fitness_list[-1].generation
        instances = fitness_list[-1].instance

        data = Graph.get_fitness_data(fitness_list)
        values = [i[0] for i in data]
        titles = [i[1] for i in data]

        plt.figure(figsize=(20, 10), dpi=150)
        plt.rcParams.update({'font.size': 14})

        counter = 0
        color_map = plt.cm.get_cmap('viridis', generations)
        for i in range(generations):
            plt.bar(titles[counter:(counter + instances)], values[counter:(counter + instances)],
                    0.8, alpha=0.7, label='Generation ' + str(i + 1), color=color_map(i))
            counter += instances

        plt.xticks([])
        plt.ylabel('Fitness')
        plt.xlabel('Instances')
        Graph.draw_legend()
        plt.suptitle(f'Fitness values through generations - {algorithm_name}', fontsize=20)

        Image.save_fitness_image(plt)
        plt.close()

    @staticmethod
    def draw_legend():
        """
        Draws a customized legend for plots with detailed formatting.
        """
        plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.05), fancybox=True, shadow=True, ncol=5)

    @staticmethod
    def draw_convergence_rate(convergence_data, algorithm_name="EA"):
        """
        Draws a plot showing the convergence rate across generations.

        Args:
            convergence_data (dict): Contains average, best, and worst fitness values for each generation.
            algorithm_name (str): Name of the algorithm (default is "EA").
        """
        if not convergence_data or 'average' not in convergence_data:
            return

        plt.figure(figsize=(12, 8), dpi=120)
        generations = range(len(convergence_data['average']))
        plt.plot(generations, convergence_data['average'], label='Average Fitness', color='blue')
        plt.plot(generations, convergence_data['best'], label='Best Fitness', color='green')
        plt.plot(generations, convergence_data['worst'], label='Worst Fitness', color='red')
        plt.xlabel('Generations')
        plt.ylabel('Fitness Value')
        plt.title(f'Convergence Rate Over Generations - {algorithm_name}')
        plt.legend()
        plt.grid(True)
        plt.tight_layout()
        plt.savefig(os.path.join("images", f'convergence_rate_{algorithm_name}.png'))
        plt.close()

    @staticmethod
    def draw_solution_quality(final_fitness_values, algorithm_name="EA"):
        """
        Draws a bar chart illustrating final fitness values across trials.

        Args:
            final_fitness_values (list): Final fitness values from multiple trials.
            algorithm_name (str): Name of the algorithm (default is "EA").
        """
        if not final_fitness_values:
            return

        plt.figure(figsize=(12, 8), dpi=120)
        trials = range(1, len(final_fitness_values) + 1)
        plt.bar(trials, final_fitness_values, color='purple', alpha=0.7)
        plt.xlabel('Trial')
        plt.ylabel('Final Fitness Value')
        plt.title(f'Solution Quality Across Multiple Trials - {algorithm_name}')
        plt.tight_layout()
        plt.savefig(os.path.join("images", f'solution_quality_{algorithm_name}.png'))
        plt.close()

    @staticmethod
    def draw_diversity_of_solutions(diversity_data, algorithm_name="EA"):
        """
        Draws a plot showing the diversity of solutions across generations.

        Args:
            diversity_data (list): Diversity values (e.g., standard deviations) for each generation.
            algorithm_name (str): Name of the algorithm (default is "EA").
        """
        if not diversity_data:
            return

        plt.figure(figsize=(12, 8), dpi=120)
        generations = range(len(diversity_data))
        plt.plot(generations, diversity_data, label='Diversity (Standard Deviation)', color='orange')
        plt.xlabel('Generations')
        plt.ylabel('Diversity')
        plt.title(f'Diversity of Solutions Over Generations - {algorithm_name}')
        plt.legend()
        plt.grid(True)
        plt.tight_layout()
        plt.savefig(os.path.join("images", f'diversity_of_solutions_{algorithm_name}.png'))
        plt.close()

    @staticmethod
    def draw_computational_efficiency(problem_sizes, runtimes, algorithm_name="EA"):
        """
        Plots the computational efficiency in terms of runtime against problem size.

        Args:
            problem_sizes (list): Sizes of problems (e.g., number of customers).
            runtimes (list): Runtime values in seconds corresponding to problem sizes.
            algorithm_name (str): Name of the algorithm (default is "EA").
        """
        if not problem_sizes or not runtimes:
            return

        plt.figure(figsize=(12, 8), dpi=120)
        plt.plot(problem_sizes, runtimes, marker='o', linestyle='-', color='brown', label='Runtime')
        plt.xlabel('Problem Size (Number of Customers)')
        plt.ylabel('Runtime (seconds)')
        plt.title(f'Computational Efficiency - {algorithm_name}')
        plt.legend()
        plt.grid(True)
        plt.tight_layout()
        plt.savefig(os.path.join("images", f'computational_efficiency_{algorithm_name}.png'))
        plt.close()

    @staticmethod
    def draw_robustness_and_stability(stability_data, algorithm_name="EA"):
        """
        Visualizes the robustness and stability of an algorithm with boxplots.

        Args:
            stability_data (list): Data from multiple algorithm runs for visualization.
            algorithm_name (str): Name of the algorithm (default is "EA").
        """
        if not stability_data:
            return

        plt.figure(figsize=(12, 8), dpi=120)
        plt.boxplot(stability_data)
        plt.xlabel('Algorithm Runs')
        plt.ylabel('Final Fitness Value')
        plt.title(f'Robustness and Stability of Algorithm Across Multiple Runs - {algorithm_name}')
        plt.tight_layout()
        plt.savefig(os.path.join("images", f'robustness_and_stability_{algorithm_name}.png'))
        plt.close()

    @staticmethod
    def get_fitness_data(fitness_list):
        """
        Extracts fitness data for visualization.

        Args:
            fitness_list (list): List of fitness objects.

        Returns:
            list: Extracted fitness values and their corresponding labels.
        """
        if not fitness_list:
            return []
        return [[i.value, f'{i.generation}.{i.instance}'] for i in fitness_list]

    def draw(self, results, fitness):
        """
        Visualizes the solution graph, including customers, depots, and their connections.

        Args:
            results (list): A list of results representing connections.
            fitness (object): Fitness object containing the generation and fitness value.
        """
        plt.figure(figsize=(12, 12), dpi=120)
        self.draw_depots()
        self.draw_customers()
        Graph.draw_legend()
        self.draw_text(fitness)
        self.draw_connections(results, fitness)
        plt.close()

    def draw_text(self, fitness):
        """
        Draws generation and fitness details as text on the graph.

        Args:
            fitness (object): Fitness object containing generation and value.
        """
        plt.suptitle(f'Generation: {fitness.generation}, Instance: {fitness.instance}', fontsize=16)
        plt.title(f'Fitness: {round(fitness.value, 2)}', fontsize=14)

    def draw_depots(self):
        """
        Plots depot locations on the graph.
        """
        coordinates = self.get_coordinates(self.depots)
        for index, (x, y) in enumerate(coordinates):
            label = 'Depot' if index == 0 else ''
            plt.scatter(x, y, alpha=0.8, c='blue', edgecolors='black', s=100, label=label, zorder=2)

    def draw_customers(self):
        """
        Plots customer locations on the graph.
        """
        coordinates = self.get_coordinates(self.customers)
        for index, (x, y) in enumerate(coordinates):
            label = 'Customer' if index == 0 else ''
            plt.scatter(x, y, alpha=0.8, c='green', edgecolors='black', s=50, label=label, zorder=2)

    def draw_connections(self, results, fitness):
        """
        Draws connections between depots and customers.

        Args:
            results (list): A list of results representing connections.
            fitness (object): Fitness object containing generation and fitness value.
        """
        try:
            img = Image(str(fitness.generation), str(fitness.instance))
        except AttributeError as e:
            print(f"Error: {e}. The 'image' module might not have the 'Image' class.")
            return

        img.save(plt)

        for i in results:
            color = np.random.random(3)
            coordinates = self.get_connection_coordinates(i)

            for index in range(len(coordinates) - 1):
                plt.plot([coordinates[index][0], coordinates[index + 1][0]],
                         [coordinates[index][1], coordinates[index + 1][1]],
                         alpha=0.6, c=color, linewidth=2, zorder=1)
                img.save(plt)
        img.create_instance_gif()

    @staticmethod
    def get_coordinates(data):
        """
        Retrieves the (x, y) coordinates from a list of objects.

        Args:
            data (list): A list of objects containing x and y attributes.

        Returns:
            list: A list of [x, y] coordinates.
        """
        return [[i.x, i.y] for i in data]

    def get_connection_coordinates(self, results):
        """
        Generates the connection coordinates including depot and customer routes.

        Args:
            results (object): Results object containing customers and depots.

        Returns:
            list: A list of coordinates forming a connection route.
        """
        coordinates = self.get_coordinates(results.customers)
        coordinates.insert(0, [results.depot.x, results.depot.y])
        coordinates.append([results.depot.x, results.depot.y])
        return coordinates
