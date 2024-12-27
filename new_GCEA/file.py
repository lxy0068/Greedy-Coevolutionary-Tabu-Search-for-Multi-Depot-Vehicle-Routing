import csv
import classes


class File(object):
    """
    A utility class for reading, parsing, and managing data from a CSV file.
    The class facilitates the conversion of raw CSV data into structured objects,
    such as vehicles, customers, and depots.
    """
    data = []  # Class-level variable to store raw CSV data

    @staticmethod
    def read(file_name):
        """
        Reads data from a given CSV file, stores it in the 'data' variable, and converts
        the rows into objects of relevant types.

        Args:
            file_name (str): The path to the CSV file to be read.

        Returns:
            list: A list containing three sub-lists:
                  - List of Vehicle objects
                  - List of Customer objects
                  - List of Depot objects
        """
        with open(file_name) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=' ')
            for row in csv_reader:
                File.data.append(row)  # Append each row to the class-level data
        return File.get_objects()

    @staticmethod
    def get_objects():
        """
        Converts rows of data into specific object types (Vehicle, Customer, Depot)
        based on their respective definitions.

        Returns:
            list: A list of lists containing objects:
                  - vehicles: List of Vehicle objects
                  - customers: List of Customer objects
                  - depots: List of Depot objects
        """
        vehicles = []  # List to store Vehicle objects
        customers = []  # List to store Customer objects
        depots = []  # List to store Depot objects
        rows = File.get_rows()  # Retrieve cleaned and categorized rows

        for i in range(3):
            for j in rows[i]:
                if i == 0:
                    vehicles.append(classes.Vehicle(float(j[0]), float(j[1])))
                elif i == 1:
                    customers.append(classes.Customer(float(j[0]), float(j[1]), float(j[2]), float(j[3]), float(j[4])))
                elif i == 2:
                    depots.append(classes.Depot(float(j[0]), float(j[1]), float(j[2])))
        return [vehicles, customers, depots]

    @staticmethod
    def get_rows():
        """
        Categorizes and cleans raw data rows into separate categories:
        vehicles, customers, and depots.

        Returns:
            list: A list containing three lists of categorized rows:
                  - vehicle_rows: Raw data for vehicles
                  - customer_rows: Cleaned data for customers
                  - depot_rows: Cleaned data for depots
        """
        # Extract the number of vehicles, customers, and depots
        vehicle_num = int(File.data[0][3])
        customer_num = int(File.data[0][2])
        depot_num = int(File.data[0][3])

        # Slice data into respective categories
        vehicle_rows = File.data[1:vehicle_num + 1]
        customer_rows = File.data[vehicle_num + 1:vehicle_num + customer_num + 1]
        depot_rows = File.data[vehicle_num + customer_num + 1: vehicle_num + customer_num + depot_num + 1]
        return [vehicle_rows, File.clean(customer_rows), File.clean(depot_rows)]

    @staticmethod
    def clean(rows):
        """
        Cleans raw rows by removing empty string elements.

        Args:
            rows (list): A list of lists, where each sub-list represents a row.

        Returns:
            list: A cleaned list of rows with empty elements removed.
        """
        cleaned = []
        for i in rows:
            row = []
            for j in i:
                if j != '':  # Remove empty strings
                    row.append(j)
            cleaned.append(row)
        return cleaned
