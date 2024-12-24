import image
import numpy as np
import matplotlib.pyplot as plt


class Graph:
    """
    Graph class for visualizing various metrics and solution-related data in evolutionary algorithms.
    """

    def __init__(self, customers, depots):
        """
        Initialize the Graph object with customers and depots.

        Args:
            customers (list): List of customer objects.
            depots (list): List of depot objects.
        """
        self.customers = customers
        self.depots = depots

    @staticmethod
    def draw_fitness_graph(fitness_list, algorithm_name="EA"):
        """
        Plot and save a bar chart showing fitness values across generations.

        Args:
            fitness_list (list): List of fitness objects containing fitness values, generations, and instances.
            algorithm_name (str): Name of the algorithm being visualized.
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

        image.Image.save_fitness_image(plt)
        plt.close()

    @staticmethod
    def draw_legend():
        """
        Draw a legend for the current plot.
        """
        plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.05), fancybox=True, shadow=True, ncol=5)

    @staticmethod
    def draw_convergence_rate(convergence_data, algorithm_name="EA"):
        """
        Plot and save a graph showing the convergence rate over generations.

        Args:
            convergence_data (dict): Contains 'average', 'best', and 'worst' fitness values per generation.
            algorithm_name (str): Name of the algorithm being visualized.
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
        plt.savefig(image.utils.images_dir + f'convergence_rate_{algorithm_name}.png')
        plt.close()

    @staticmethod
    def draw_solution_quality(final_fitness_values, algorithm_name="EA"):
        """
        Plot and save a bar chart showing the solution quality across multiple trials.

        Args:
            final_fitness_values (list): List of final fitness values for multiple trials.
            algorithm_name (str): Name of the algorithm being visualized.
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
        plt.savefig(image.utils.images_dir + f'solution_quality_{algorithm_name}.png')
        plt.close()

    @staticmethod
    def draw_diversity_of_solutions(diversity_data, algorithm_name="EA"):
        """
        Plot and save a graph showing the diversity of solutions over generations.

        Args:
            diversity_data (list): Diversity values (e.g., standard deviation of solutions) per generation.
            algorithm_name (str): Name of the algorithm being visualized.
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
        plt.savefig(image.utils.images_dir + f'diversity_of_solutions_{algorithm_name}.png')
        plt.close()

    @staticmethod
    def draw_computational_efficiency(problem_sizes, runtimes, algorithm_name="EA"):
        """
        Plot and save a graph showing computational efficiency for different problem sizes.

        Args:
            problem_sizes (list): Sizes of the problem (e.g., number of customers).
            runtimes (list): Execution times corresponding to problem sizes.
            algorithm_name (str): Name of the algorithm being visualized.
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
        plt.savefig(image.utils.images_dir + f'computational_efficiency_{algorithm_name}.png')
        plt.close()

    @staticmethod
    def draw_robustness_and_stability(stability_data, algorithm_name="EA"):
        """
        Plot and save a boxplot showing robustness and stability of the algorithm across runs.

        Args:
            stability_data (list): Fitness values from multiple runs.
            algorithm_name (str): Name of the algorithm being visualized.
        """
        if not stability_data:
            return

        plt.figure(figsize=(12, 8), dpi=120)
        plt.boxplot(stability_data)
        plt.xlabel('Algorithm Runs')
        plt.ylabel('Final Fitness Value')
        plt.title(f'Robustness and Stability of Algorithm Across Multiple Runs - {algorithm_name}')
        plt.tight_layout()
        plt.savefig(image.utils.images_dir + f'robustness_and_stability_{algorithm_name}.png')
        plt.close()

    @staticmethod
    def get_fitness_data(fitness_list):
        """
        Extract fitness values and corresponding titles from the fitness list.

        Args:
            fitness_list (list): List of fitness objects.

        Returns:
            list: A list of [fitness_value, title] pairs.
        """
        if not fitness_list:
            return []
        return [[i.value, f'{i.generation}.{i.instance}'] for i in fitness_list]

    def draw(self, results, fitness):
        """
        Plot and save the graph for the solution's fitness and routes.

        Args:
            results (list): Results containing customer routes.
            fitness (object): Fitness object with generation and instance data.
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
        Add text annotations for generation and fitness value on the plot.

        Args:
            fitness (object): Fitness object with generation and fitness data.
        """
        plt.suptitle(f'Generation: {fitness.generation}, Instance: {fitness.instance}', fontsize=16)
        plt.title(f'Fitness: {round(fitness.value, 2)}', fontsize=14)

    def draw_depots(self):
        """
        Plot depot locations on the graph.
        """
        coordinates = self.get_coordinates(self.depots)
        for index, (x, y) in enumerate(coordinates):
            label = 'Depot' if index == 0 else ''
            plt.scatter(x, y, alpha=0.8, c='blue', edgecolors='black', s=100, label=label, zorder=2)

    def draw_customers(self):
        """
        Plot customer locations on the graph.
        """
        coordinates = self.get_coordinates(self.customers)
        for index, (x, y) in enumerate(coordinates):
            label = 'Customer' if index == 0 else ''
            plt.scatter(x, y, alpha=0.8, c='green', edgecolors='black', s=50, label=label, zorder=2)

    def draw_connections(self, results, fitness):
        """
        Plot the connections (routes) between depots and customers.

        Args:
            results (list): Results containing routes for customers.
            fitness (object): Fitness object with generation and instance data.
        """
        img = image.Image(str(fitness.generation), str(fitness.instance))
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
        Extract coordinates from a list of data objects.

        Args:
            data (list): List of objects with x and y attributes.

        Returns:
            list: A list of [x, y] coordinates.
        """
        return [[i.x, i.y] for i in data]

    def get_connection_coordinates(self, results):
        """
        Get the coordinates for plotting connections between depots and customers.

        Args:
            results (object): Results containing depot and customer data.

        Returns:
            list: List of coordinates including the depot at the start and end.
        """
        coordinates = self.get_coordinates(results.customers)
        coordinates.insert(0, [results.depot.x, results.depot.y])
        coordinates.append([results.depot.x, results.depot.y])
        return coordinates
