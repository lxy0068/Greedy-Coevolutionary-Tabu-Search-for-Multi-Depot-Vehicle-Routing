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
    print('Best instance: ')
    print('Generation: ' + str(best_instance.generation))
    print('Instance: ' + str(best_instance.instance))
    print('Fitness: ' + str(round(best_instance.value, 2)))
    print('Phenotype: ' + str(best_instance.phenotype))


def main(file_name, algorithm, iterations, population_size, phenotype_coding, num_trials=30):
    directory.Directory().delete_directories()
    objects = file.File.read('../datasets/' + file_name)

    all_fitness_values = []
    all_runtimes = []
    all_stability_data = []

    for trial in range(num_trials):
        start_time = time.time()
        task = Task(D=len(objects[1]), nFES=iterations, benchmark=evaluation.Evaluation(
            objects, iterations, population_size, phenotype_coding), optType=OptimizationType.MINIMIZATION)
        alg = algorithm(seed=randint(1000, 10000), task=task, NP=population_size)

        result, fitness = alg.run()
        runtime = time.time() - start_time

        # Debugging output for fitness format
        print(f"Trial {trial + 1}: Type of fitness - {type(fitness)}")

        # Ensure fitness is handled appropriately
        try:
            if isinstance(fitness, list) and len(fitness) > 0:
                # Assuming a list of fitness values
                all_fitness_values.append(fitness[-1].value)
                all_stability_data.append([f.value for f in fitness])
            elif hasattr(fitness, 'value'):
                # Assuming fitness is a single object with a 'value' attribute
                all_fitness_values.append(fitness.value)
                all_stability_data.append([fitness.value])
            elif isinstance(fitness, (int, float)):
                # Assuming fitness is directly a scalar
                all_fitness_values.append(fitness)
                all_stability_data.append([fitness])
            else:
                raise ValueError(f"Unexpected format of fitness returned by the algorithm: {type(fitness)}")
        except Exception as e:
            print(f"Error processing fitness on trial {trial + 1}: {e}")
            continue

        all_runtimes.append(runtime)

        # Print the best instance from the fitness list if possible
        try:
            best_instance = evaluation.Evaluation.find_overall_best_instance(fitness)
            print_result(best_instance)
        except Exception as e:
            print(f"Error finding best instance on trial {trial + 1}: {e}")

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

    algorithm_name = "Greedy Cooperative Co-evolutionary Algorithm"
    if all_fitness_values:
        Graph.draw_solution_quality(all_fitness_values, algorithm_name)
    if all_runtimes:
        Graph.draw_computational_efficiency(range(1, len(all_runtimes) + 1), all_runtimes, algorithm_name)
    if all_stability_data:
        Graph.draw_robustness_and_stability(all_stability_data, algorithm_name)


if __name__ == '__main__':
    main('C-mdvrptw/pr00', GeneticAlgorithm, 25, 5, method.Method.FIRST, num_trials=30)