class Vehicle:
    """
    Represents a vehicle in the MDVRP (Multi-Depot Vehicle Routing Problem).
    
    Attributes:
        max_duration (float): Maximum duration the vehicle can travel.
        max_capacity (float): Maximum capacity of the vehicle.
    """
    def __init__(self, max_duration, max_capacity):
        self.max_duration = max_duration
        self.max_capacity = max_capacity


class Customer:
    """
    Represents a customer node in the MDVRP.

    Attributes:
        key (int): Unique identifier for the customer.
        x (float): X-coordinate of the customer's location.
        y (float): Y-coordinate of the customer's location.
        stacking_time (float): Time required to stack/unstack goods for this customer.
        capacity (float): Goods' demand of the customer.
    """
    def __init__(self, key, x, y, stacking_time, capacity):
        self.key = key
        self.x = x
        self.y = y
        self.stacking_time = stacking_time
        self.capacity = capacity


class Depot:
    """
    Represents a depot in the MDVRP.

    Attributes:
        key (int): Unique identifier for the depot.
        x (float): X-coordinate of the depot's location.
        y (float): Y-coordinate of the depot's location.
    """
    def __init__(self, key, x, y):
        self.key = key
        self.x = x
        self.y = y


class Result:
    """
    Represents a solution result for an MDVRP instance.
    
    Attributes:
        generation (int): The generation number of the solution in the coevolutionary algorithm.
        instance (int): Unique identifier of the instance.
        capacity (float): Total capacity utilized in this solution.
        distance (float): Total distance covered in this solution.
        vehicle (Vehicle): The vehicle used in the solution.
        depot (Depot): The depot assigned to this solution.
        customers (list): A list of Customer objects representing the route.
    """
    def __init__(self, generation, instance):
        self.generation = generation
        self.instance = instance
        self.capacity = 0
        self.distance = 0.0
        self.vehicle = None
        self.depot = None
        self.customers = []


class Fitness:
    """
    Represents the fitness of a solution in the MDVRP.

    Attributes:
        generation (int): The generation number of the solution.
        instance (int): Unique identifier of the instance.
        value (float): Fitness value of the solution (e.g., based on total distance, capacity, etc.).
        phenotype (str): A descriptive string representing the solution's phenotype.
        best_instance (bool): Flag indicating if this is the best solution for its generation.
    """
    def __init__(self, generation, instance, value, phenotype):
        self.generation = generation
        self.instance = instance
        self.value = value
        self.phenotype = phenotype
        self.best_instance = False
