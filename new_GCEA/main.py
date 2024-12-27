import os
import utils
import numpy as np
import matplotlib.pyplot as plt
import imageio
import directory
import time
import file
import method
import evaluation
from random import randint
from NiaPy.util import Task, OptimizationType
from NiaPy.algorithms.basic.ga import GeneticAlgorithm
from graph import Graph, Image


def print_result(best_instance):
    """
    Prints details about the best solution instance found during optimization.

    Args:
        best_instance (object): The best instance containing generation, instance number, fitness value, and phenotype.
    """
    print('Best instance: ')
    print('Generation: ' + str(best_instance.generation))
    print('Instance: ' + str(best_instance.instance))
    print('Fitness: ' + str(round(best_instance.value, 2)))
    print('Phenotype: ' + str(best_instance.phenotype))


def main(file_name, algorithm, iterations, population_size, phenotype_coding, num_trials=30):
    """
    Main function for running the optimization process. It executes the given algorithm multiple times, 
    collects results, and generates performance graphs.

    Args:
        file_name (str): Path to the dataset file.
        algorithm (class): The optimization algorithm to use (e.g., GeneticAlgorithm).
        iterations (int): Maximum number of function evaluations (iterations) for the optimization.
        population_size (int): Number of individuals in the population.
        phenotype_coding (enum): The method of phenotype encoding.
        num_trials (int): Number of independent trials to run (default is 30).
    """
    # Clean up directories before starting
    directory.Directory().delete_directories()

    # Load dataset and initialize objects
    objects = file.File.read('../datasets/' + file_name)

    # Initialize metrics
    all_fitness_values = []  # Stores final fitness values from all trials
    all_runtimes = []  # Stores runtimes for all trials
    all_stability_data = []  # Stores stability data (fitness values across runs)

    for trial in range(num_trials):
        start_time = time.time()  # Start time for the trial

        # Create an optimization task
        task = Task(
            D=len(objects[1]),  # Dimensionality of the task (number of customers)
            nFES=iterations,  # Maximum number of function evaluations
            benchmark=evaluation.Evaluation(
                objects, iterations, population_size, phenotype_coding
            ),  # Custom evaluation function
            optType=OptimizationType.MINIMIZATION  # Optimization type (minimization)
        )

        # Initialize the algorithm with a random seed
        alg = algorithm(seed=randint(1000, 10000), task=task, NP=population_size)

        # Run the algorithm and get the result
        result, fitness = alg.run()
        runtime = time.time() - start_time  # Calculate runtime for the trial

        # Debugging: Output the type of fitness returned
        print(f"Trial {trial + 1}: Type of fitness - {type(fitness)}")

        # Process and validate the fitness results
        try:
            if isinstance(fitness, list) and len(fitness) > 0:
                # Handle a list of fitness objects
                all_fitness_values.append(fitness[-1].value)  # Append the last fitness value
                all_stability_data.append([f.value for f in fitness])  # Store all fitness values
            elif hasattr(fitness, 'value'):
                # Handle a single fitness object
                all_fitness_values.append(fitness.value)
                all_stability_data.append([fitness.value])
            elif isinstance(fitness, (int, float)):
                # Handle scalar fitness values
                all_fitness_values.append(fitness)
                all_stability_data.append([fitness])
            else:
                raise ValueError(f"Unexpected format of fitness returned by the algorithm: {type(fitness)}")
        except Exception as e:
            print(f"Error processing fitness on trial {trial + 1}: {e}")
            continue

        # Store runtime
        all_runtimes.append(runtime)

        # Attempt to find and print the best instance
        try:
            best_instance = evaluation.Evaluation.find_overall_best_instance(fitness)
            print_result(best_instance)
        except Exception as e:
            print(f"Error finding best instance on trial {trial + 1}: {e}")

    # Calculate and display average metrics
    average_fitness = np.mean(all_fitness_values) if all_fitness_values else None
    average_runtime = np.mean(all_runtimes) if all_runtimes else None

    if average_fitness is not None:
        print(f'Average Final Fitness: {average_fitness}')
    else:
        print('No valid fitness values recorded.')

    if average_runtime is not None:
        print(f'Average Runtime: {average_runtime} seconds')
    else:
        print('No runtime data recorded.')

    # Visualization and Performance Analysis
    algorithm_name = "Greedy Cooperative Co-evolutionary Algorithm"

    # Plot solution quality
    if all_fitness_values:
        Graph.draw_solution_quality(all_fitness_values, algorithm_name)

    # Plot computational efficiency
    if all_runtimes:
        Graph.draw_computational_efficiency(
            range(1, len(all_runtimes) + 1), all_runtimes, algorithm_name
        )

    # Plot robustness and stability
    if all_stability_data:
        Graph.draw_robustness_and_stability(all_stability_data, algorithm_name)


if __name__ == '__main__':
    main('C-mdvrptw/pr00', GeneticAlgorithm, 25, 5, method.Method.FIRST, num_trials=30)
