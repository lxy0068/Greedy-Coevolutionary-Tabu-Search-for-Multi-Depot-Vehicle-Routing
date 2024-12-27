import graph
import image
import method
import classes
import operator
import numpy as np
import random

class Evaluation(object):
    # Class for evaluating solutions to the Multi-Depot Vehicle Routing Problem (MDVRP)

    fitness_list = []  # Static list to store fitness values for instances

    def __init__(self, objects, iterations, population_size, phenotype_coding):
        # Initialize the evaluation object with parameters and data structures
        self.Lower = 0  # Lower bound for mutation
        self.Upper = 10  # Upper bound for mutation
        self.penalty = 20  # Penalty for exceeding constraints
        self.vehicles = objects[0]  # List of vehicles
        self.customers = objects[1]  # List of customers
        self.depots = objects[2]  # List of depots
        self.instance_counter = 0  # Tracks current instance count in a generation
        self.generation_counter = 1  # Tracks current generation
        self.population_size = population_size  # Size of population in cooperative evolution
        self.generations = iterations // population_size  # Total number of generations
        self.phenotype_coding = phenotype_coding  # Coding method for genotypes
        self.subpopulations = []  # Stores subpopulations for cooperative evolution
        self.subpop_fitness = []  # Fitness values for subpopulations

    def function(self):
        # Generate an evaluation function for fitness calculation

        def evaluate(d, genotype):
            # Evaluate a single genotype, returning its fitness value
            self.set_instance_counter()
            self.set_generation_counter()

            phenotype = self.to_phenotype(genotype)  # Decode genotype to phenotype
            results = self.simulate_route(d, phenotype)  # Simulate the vehicle route
            fitness = self.create_fitness(results, phenotype)  # Calculate fitness

            graph.Graph(self.customers, self.depots).draw(results, fitness)  # Visualize results

            if self.instance_counter == self.population_size:
                # Perform operations at the end of a generation
                self.find_best_instance()
                if self.generation_counter == self.generations:
                    # Final operations after all generations
                    self.create_best_instances_gif()
                    self.create_fitness_image()

            return fitness.value

        return evaluate

    def set_instance_counter(self):
        # Increment the instance counter for each evaluation
        self.instance_counter += 1

    def set_generation_counter(self):
        # Increment the generation counter when a generation completes
        if self.instance_counter > self.population_size:
            self.generation_counter += 1
            self.instance_counter = 1

    def greedy_cooperative_co_evolution(self, population):
        # Perform greedy cooperative co-evolution to optimize population
        self.split_into_subpopulations(population)  # Split population into subpopulations

        for subpop_index in range(len(self.subpopulations)):
            # Optimize each subpopulation
            self.subpopulations[subpop_index] = self.greedy_optimize_subpopulation(self.subpopulations[subpop_index])

        new_population = self.merge_subpopulations()  # Merge optimized subpopulations
        return new_population

    def split_into_subpopulations(self, population):
        # Divide the population into subpopulations for cooperative evolution
        num_subpops = len(population[0]) // 2  # Number of subpopulations
        self.subpopulations = [[] for _ in range(num_subpops)]

        for individual in population:
            for i in range(num_subpops):
                if len(self.subpopulations[i]) < self.population_size:
                    self.subpopulations[i].append(individual[i::num_subpops])

    def greedy_optimize_subpopulation(self, subpopulation):
        # Apply greedy optimization to a single subpopulation
        new_subpopulation = []
        for i in range(len(subpopulation)):
            target = subpopulation[i]  # Current individual
            a, b, c = random.sample([x for x in range(len(subpopulation)) if x != i], 3)  # Select three other individuals
            mutant = self.mutate(subpopulation[a], subpopulation[b], subpopulation[c])  # Create mutant
            trial = self.crossover(target, mutant)  # Perform crossover
            target_fitness = self.evaluate_fitness(target)  # Evaluate fitness of target
            trial_fitness = self.evaluate_fitness(trial)  # Evaluate fitness of trial
            if trial_fitness < target_fitness:
                new_subpopulation.append(trial)  # Replace if trial is better
            else:
                new_subpopulation.append(target)
        return new_subpopulation

    def merge_subpopulations(self):
        # Merge optimized subpopulations back into a single population
        new_population = []
        for i in range(self.population_size):
            merged_individual = []
            for subpop in self.subpopulations:
                merged_individual.extend(subpop[i % len(subpop)])
            new_population.append(merged_individual)
        return new_population

    def mutate(self, a, b, c):
        # Perform mutation on three individuals to create a new candidate
        mutant = a + 0.8 * (b - c)
        mutant = np.clip(mutant, self.Lower, self.Upper)  # Ensure mutation stays within bounds
        return mutant

    def crossover(self, target, mutant):
        # Perform crossover between a target individual and a mutant
        trial = np.array([mutant[i] if random.random() < 0.9 else target[i] for i in range(len(target))])
        return trial

    def simulate_route(self, d, phenotype):
        # Simulate a vehicle routing problem using the given phenotype
        results = []
        customers_counter = 0
        vehicle_depot_counter = 0
        vehicle_depot_changed = False
        curr_result = classes.Result(self.generation_counter, self.instance_counter)

        for i in range(d):
            customers_counter += 1
            curr_result = self.set_vehicle_depot(curr_result, vehicle_depot_counter)

            prev_customer = self.find_previous_customer(i, vehicle_depot_changed, phenotype)
            curr_customer = self.find_customer(phenotype[i])
            next_customer = self.find_next_customer(i, phenotype)

            curr_result = self.get_result(curr_result, prev_customer, curr_customer)
            curr_result = self.add_customer_to_result(curr_result, curr_customer)
            vehicle_depot_changed = False

            if self.phenotype_coding == method.Method.SECOND and curr_result.depot.customers_num == customers_counter:
                vehicle_depot_changed = True

            if not self.check_next_customer(curr_result, curr_customer, next_customer) or vehicle_depot_changed:
                curr_result = self.get_last_distance(curr_result, curr_customer)

                if self.check_for_penalty(curr_result):
                    self.add_penalty(curr_result)
                results.append(curr_result)

                if self.phenotype_coding == method.Method.FIRST or (self.phenotype_coding == method.Method.SECOND and
                                                                   curr_result.depot.customers_num == customers_counter):
                    vehicle_depot_changed = True
                    vehicle_depot_counter = self.set_vehicle_depot_counter(vehicle_depot_counter)
                    customers_counter = 0
                curr_result = classes.Result(self.generation_counter, self.instance_counter)
        return results

    def set_vehicle_depot(self, curr_result, vehicle_depot_counter):
        # Assign a vehicle and depot to the current result
        curr_result.vehicle = self.vehicles[vehicle_depot_counter]
        curr_result.depot = self.depots[vehicle_depot_counter]
        return curr_result

    @staticmethod
    def find_overall_best_instance(fitness):
        # Find the overall best instance with the specified fitness value
        for i in Evaluation.fitness_list:
            if i.value == fitness:
                return i

    def find_best_instance(self):
        # Identify the best instance in the current generation
        instances = [i for i in Evaluation.fitness_list if i.generation == self.generation_counter]
        best_instance = min(instances, key=operator.attrgetter('value'))
        best_instance.best_instance = True

    def find_customer(self, key):
        # Locate a customer in the dataset by its key
        for i in self.customers:
            if i.key == key:
                return i

    def find_previous_customer(self, i, vehicle_depot_changed, phenotype):
        # Find the previous customer in the route
        if i == 0 or vehicle_depot_changed is True:
            return -1
        return self.find_customer(phenotype[i - 1])

    def find_next_customer(self, i, phenotype):
        # Find the next customer in the route
        if (i + 1) >= len(self.customers):
            return -1
        return self.find_customer(phenotype[i + 1])

    @staticmethod
    def check_for_penalty(curr_result):
        # Check if the result exceeds allowed constraints, requiring a penalty
        return curr_result.distance > curr_result.vehicle.max_duration

    def check_next_customer(self, curr_result, curr_customer, next_customer):
        # Verify if the next customer can be visited without violating constraints
        if next_customer == -1:
            return False

        next_capacity = curr_result.capacity + next_customer.capacity
        next_distance = curr_result.distance + self.get_distance(curr_result.depot, curr_customer, next_customer)

        return next_capacity <= curr_result.vehicle.max_capacity and next_distance <= curr_result.vehicle.max_duration

    def create_best_instances_gif(self):
        # Generate a GIF of the best instances across all generations
        indexes = [i for i in range(len(Evaluation.fitness_list)) if Evaluation.fitness_list[i].best_instance]
        image.Image.create_best_instances_gif(indexes)

    def create_fitness_image(self):
        # Create an image to visualize fitness trends over generations
        graph.Graph.draw_fitness_graph(Evaluation.fitness_list)

    def create_fitness(self, results, phenotype):
        # Calculate and store fitness for a given phenotype
        fitness = classes.Fitness(self.generation_counter, self.instance_counter, self.get_fitness(results), phenotype)
        Evaluation.fitness_list.append(fitness)
        return fitness

    @staticmethod
    def get_distance(depot, customer_one, customer_two):
        # Calculate Euclidean distance between two points
        if customer_one == -1:
            x1, y1 = depot.x, depot.y
        else:
            x1, y1 = customer_one.x, customer_one.y

        if customer_two == -1:
            x2, y2 = depot.x, depot.y
        else:
            x2, y2 = customer_two.x, customer_two.y

        return np.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

    @staticmethod
    def get_fitness(results):
        # Calculate the total fitness (distance) from simulation results
        return sum(result.distance for result in results)

    def get_result(self, curr_result, prev_customer, curr_customer):
        # Update the result with details of the current customer
        curr_result.capacity += curr_customer.capacity
        curr_result.distance += self.get_distance(curr_result.depot, prev_customer, curr_customer)
        return curr_result

    def get_last_distance(self, curr_result, curr_customer):
        # Calculate the distance from the last customer back to the depot
        curr_result.distance += self.get_distance(curr_result.depot, curr_customer, -1)
        return curr_result

    @staticmethod
    def add_customer_to_result(curr_result, curr_customer):
        # Add a customer to the current result's customer list
        curr_result.customers.append(curr_customer)
        return curr_result

    def add_penalty(self, curr_result):
        # Apply a penalty to the current result's distance
        curr_result.distance += self.penalty
        return curr_result

    @staticmethod
    def to_first_phenotype(genotype):
        # Decode genotype to phenotype using the first coding method
        return (np.argsort(np.argsort(genotype)) + 1).tolist()

    def to_second_phenotype(self, genotype):
        # Decode genotype to phenotype using the second coding method
        divider = 10 / len(self.depots)
        scale = [0]
        for i in range(len(self.depots)):
            setattr(self.depots[i], 'phenotype', [])
            scale.append(scale[-1] + divider)

        ordered = Evaluation.to_first_phenotype(genotype)

        for i in range(len(genotype)):
            for j in range(len(scale)):
                if genotype[i] == scale[-1]:
                    self.depots[-1].phenotype.append(ordered[i])
                    break
                if scale[j] <= genotype[i] < scale[j + 1]:
                    self.depots[j].phenotype.append(ordered[i])
                    break

        phenotype = []
        for i in self.depots:
            setattr(i, 'customers_num', len(i.phenotype))
            phenotype += i.phenotype
            delattr(i, 'phenotype')

        return phenotype

    def to_phenotype(self, genotype):
        # Convert genotype to phenotype based on the specified coding method
        if self.phenotype_coding == method.Method.FIRST:
            return self.to_first_phenotype(genotype)
        elif self.phenotype_coding == method.Method.SECOND:
            return self.to_second_phenotype(genotype)

    def set_vehicle_depot_counter(self, vehicle_depot_counter):
        # Update the vehicle depot counter cyclically for the next assignment
        if (vehicle_depot_counter + 1) >= len(self.vehicles):
            return 0
        return vehicle_depot_counter + 1
