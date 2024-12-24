import graph
import image
import method
import classes
import operator
import numpy as np

class Evaluation(object):
    # Class-level list to store fitness instances across all generations.
    fitness_list = []

    def __init__(self, objects, iterations, population_size, phenotype_coding):
        """
        Initialize the Evaluation object with the problem parameters.

        Args:
            objects (list): Contains vehicles, customers, and depots.
            iterations (int): Total number of iterations for the genetic algorithm.
            population_size (int): Size of the population.
            phenotype_coding (method.Method): Phenotype encoding method (e.g., FIRST or SECOND).
        """
        self.Lower = 0
        self.Upper = 10
        self.penalty = 20
        self.vehicles = objects[0]
        self.customers = objects[1]
        self.depots = objects[2]
        self.instance_counter = 0
        self.generation_counter = 1
        self.population_size = population_size
        self.generations = iterations / population_size
        self.phenotype_coding = phenotype_coding

    def function(self):
        """
        Wrapper function to create and return the evaluation function.

        Returns:
            callable: Evaluation function that computes the fitness value for a genotype.
        """
        def evaluate(d, genotype):
            self.set_instance_counter()
            self.set_generation_counter()

            results = []
            customers_counter = 0
            vehicle_depot_counter = 0
            vehicle_depot_changed = False
            phenotype = self.to_phenotype(genotype)
            curr_result = classes.Result(self.generation_counter, self.instance_counter)
            g = graph.Graph(self.customers, self.depots)

            for i in range(d):
                customers_counter += 1
                curr_result = self.set_vehicle_depot(curr_result, vehicle_depot_counter)

                # Determine the customers involved in the current step.
                prev_customer = self.find_previous_customer(i, vehicle_depot_changed, phenotype)
                curr_customer = self.find_customer(phenotype[i])
                next_customer = self.find_next_customer(i, phenotype)

                # Update the current result with the new customer.
                curr_result = self.get_result(curr_result, prev_customer, curr_customer)
                curr_result = self.add_customer_to_result(curr_result, curr_customer)
                vehicle_depot_changed = False

                # Check if vehicle depot needs to change based on the phenotype coding.
                if self.phenotype_coding == method.Method.SECOND and \
                        curr_result.depot.customers_num == customers_counter:
                    vehicle_depot_changed = True

                if not self.check_next_customer(curr_result, curr_customer, next_customer) or vehicle_depot_changed:
                    curr_result = self.get_last_distance(curr_result, curr_customer)

                    # Apply penalty if the constraints are violated.
                    if self.check_for_penalty(curr_result):
                        self.add_penalty(curr_result)
                    results.append(curr_result)

                    # Reset for the next vehicle or depot.
                    if self.phenotype_coding == method.Method.FIRST or \
                            (self.phenotype_coding == method.Method.SECOND and
                             curr_result.depot.customers_num == customers_counter):
                        vehicle_depot_changed = True
                        vehicle_depot_counter = self.set_vehicle_depot_counter(vehicle_depot_counter)
                        customers_counter = 0
                    curr_result = classes.Result(self.generation_counter, self.instance_counter)

            # Calculate fitness and visualize results.
            fitness = self.create_fitness(results, phenotype)
            g.draw(results, fitness)

            # Handle end of generation and instance.
            if self.instance_counter == self.population_size:
                self.find_best_instance()
                if self.generation_counter == self.generations:
                    self.create_best_instances_gif()
                    self.create_fitness_image()

            return fitness.value

        return evaluate

    def set_instance_counter(self):
        """Increment the instance counter."""
        self.instance_counter += 1

    def set_generation_counter(self):
        """Update the generation counter when all instances in the population are evaluated."""
        if self.instance_counter > self.population_size:
            self.generation_counter += 1
            self.instance_counter = 1

    def set_vehicle_depot_counter(self, vehicle_depot_counter):
        """
        Increment the vehicle depot counter, cycling back to zero if it exceeds the number of vehicles.

        Args:
            vehicle_depot_counter (int): Current vehicle depot counter.

        Returns:
            int: Updated vehicle depot counter.
        """
        if (vehicle_depot_counter + 1) >= len(self.vehicles):
            return 0
        return vehicle_depot_counter + 1

    def set_vehicle_depot(self, curr_result, vehicle_depot_counter):
        """
        Assign the vehicle and depot to the current result based on the vehicle depot counter.

        Args:
            curr_result (classes.Result): Current result object.
            vehicle_depot_counter (int): Current vehicle depot counter.

        Returns:
            classes.Result: Updated result object with vehicle and depot assigned.
        """
        curr_result.vehicle = self.vehicles[vehicle_depot_counter]
        curr_result.depot = self.depots[vehicle_depot_counter]
        return curr_result

    @staticmethod
    def find_overall_best_instance(fitness):
        """
        Find the best fitness instance globally.

        Args:
            fitness (float): Fitness value to search for.

        Returns:
            classes.Fitness: The matching fitness instance.
        """
        for i in Evaluation.fitness_list:
            if i.value == fitness:
                return i

    def find_best_instance(self):
        """
        Identify and mark the best fitness instance for the current generation.
        """
        instances = [i for i in Evaluation.fitness_list if i.generation == self.generation_counter]
        best_instance = min(instances, key=operator.attrgetter('value'))
        best_instance.best_instance = True

    def find_customer(self, key):
        """
        Locate a customer by its key.

        Args:
            key (int): The customer's key.

        Returns:
            Customer: The corresponding customer object.
        """
        for i in self.customers:
            if i.key == key:
                return i

    def find_previous_customer(self, i, vehicle_depot_changed, phenotype):
        """
        Find the previous customer in the route, considering changes in depot or start of the route.

        Args:
            i (int): Index of the current customer.
            vehicle_depot_changed (bool): Whether the vehicle depot was recently changed.
            phenotype (list): Current phenotype sequence.

        Returns:
            Customer or int: The previous customer or -1 if no previous customer exists.
        """
        if i == 0 or vehicle_depot_changed:
            return -1
        return self.find_customer(phenotype[i - 1])

    def find_next_customer(self, i, phenotype):
        """
        Find the next customer in the route.

        Args:
            i (int): Index of the current customer.
            phenotype (list): Current phenotype sequence.

        Returns:
            Customer or int: The next customer or -1 if no next customer exists.
        """
        if (i + 1) >= len(self.customers):
            return -1
        return self.find_customer(phenotype[i + 1])

    @staticmethod
    def check_for_penalty(curr_result):
        """
        Determine if a penalty should be applied based on vehicle constraints.

        Args:
            curr_result (classes.Result): Current result object.

        Returns:
            bool: True if a penalty is required, False otherwise.
        """
        return curr_result.distance > curr_result.vehicle.max_duration

    def check_next_customer(self, curr_result, curr_customer, next_customer):
        """
        Check if the next customer can be visited without violating vehicle constraints.

        Args:
            curr_result (classes.Result): Current result object.
            curr_customer (Customer): Current customer.
            next_customer (Customer or int): Next customer or -1.

        Returns:
            bool: True if the next customer can be visited, False otherwise.
        """
        if next_customer == -1:
            return False

        next_capacity = curr_result.capacity + next_customer.capacity
        next_distance = curr_result.distance + self.get_distance(curr_result.depot, curr_customer, next_customer)

        return next_capacity <= curr_result.vehicle.max_capacity and next_distance <= curr_result.vehicle.max_duration

    @staticmethod
    def create_best_instances_gif():
        """Create a GIF showing the best instances across generations."""
        indexes = [i for i in range(len(Evaluation.fitness_list)) if Evaluation.fitness_list[i].best_instance]
        image.Image.create_best_instances_gif(indexes)

    @staticmethod
    def create_fitness_image():
        """Generate a fitness graph for visualization."""
        graph.Graph.draw_fitness_graph(Evaluation.fitness_list)

    def create_fitness(self, results, phenotype):
        """
        Create a fitness object for the current evaluation and add it to the fitness list.

        Args:
            results (list): List of results for the current evaluation.
            phenotype (list): Current phenotype sequence.

        Returns:
            classes.Fitness: The newly created fitness object.
        """
        fitness = classes.Fitness(self.generation_counter, self.instance_counter,
                                  self.get_fitness(results), phenotype)
        Evaluation.fitness_list.append(fitness)
        return fitness

    @staticmethod
    def get_distance(depot, customer_one, customer_two):
        """
        Calculate the Euclidean distance between two points, considering the depot if needed.

        Args:
            depot (Depot): Depot object.
            customer_one (Customer or int): First customer or -1.
            customer_two (Customer or int): Second customer or -1.

        Returns:
            float: Calculated distance.
        """
        x1, y1 = (depot.x, depot.y) if customer_one == -1 else (customer_one.x, customer_one.y)
        x2, y2 = (depot.x, depot.y) if customer_two == -1 else (customer_two.x, customer_two.y)
        return np.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

    @staticmethod
    def get_fitness(results):
        """
        Calculate the total distance for a given set of results as the fitness value.

        Args:
            results (list): List of results.

        Returns:
            float: Total fitness value.
        """
        return sum(result.distance for result in results)

    def get_result(self, curr_result, prev_customer, curr_customer):
        """
        Update the current result with distance and capacity based on the current customer.

        Args:
            curr_result (classes.Result): Current result object.
            prev_customer (Customer or int): Previous customer or -1.
            curr_customer (Customer): Current customer.

        Returns:
            classes.Result: Updated result object.
        """
        curr_result.capacity += curr_customer.capacity
        curr_result.distance += self.get_distance(curr_result.depot, prev_customer, curr_customer)
        return curr_result

    def get_last_distance(self, curr_result, curr_customer):
        """
        Add the distance from the last customer back to the depot.

        Args:
            curr_result (classes.Result): Current result object.
            curr_customer (Customer): Last customer in the route.

        Returns:
            classes.Result: Updated result object.
        """
        curr_result.distance += self.get_distance(curr_result.depot, curr_customer, -1)
        return curr_result

    @staticmethod
    def add_customer_to_result(curr_result, curr_customer):
        """
        Add the current customer to the result's customer list.

        Args:
            curr_result (classes.Result): Current result object.
            curr_customer (Customer): Customer to add.

        Returns:
            classes.Result: Updated result object.
        """
        curr_result.customers.append(curr_customer)
        return curr_result

    def add_penalty(self, curr_result):
        """
        Apply a penalty to the current result for constraint violations.

        Args:
            curr_result (classes.Result): Current result object.

        Returns:
            classes.Result: Updated result object with penalty applied.
        """
        curr_result.distance += self.penalty
        return curr_result

    @staticmethod
    def to_first_phenotype(genotype):
        """
        Convert the genotype to a phenotype using the FIRST encoding method.

        Args:
            genotype (list): Genotype sequence.

        Returns:
            list: Phenotype sequence.
        """
        return (np.argsort(np.argsort(genotype)) + 1).tolist()

    def to_second_phenotype(self, genotype):
        """
        Convert the genotype to a phenotype using the SECOND encoding method.

        Args:
            genotype (list): Genotype sequence.

        Returns:
            list: Phenotype sequence.
        """
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
        """
        Convert the genotype to a phenotype based on the selected encoding method.

        Args:
            genotype (list): Genotype sequence.

        Returns:
            list: Phenotype sequence.
        """
        if self.phenotype_coding == method.Method.FIRST:
            return self.to_first_phenotype(genotype)
        elif self.phenotype_coding == method.Method.SECOND:
            return self.to_second_phenotype(genotype)
