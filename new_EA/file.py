import csv
import classes

class File(object):
    # Class-level storage for data read from a file.
    data = []

    @staticmethod
    def read(file_name):
        """
        Read data from a CSV file and store it in the class-level data attribute.

        Args:
            file_name (str): The name of the CSV file to read.

        Returns:
            list: A list containing vehicles, customers, and depots as separate lists of objects.
        """
        with open(file_name) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=' ')
            for row in csv_reader:
                File.data.append(row)
        return File.get_objects()

    @staticmethod
    def get_objects():
        """
        Convert the raw data into objects for vehicles, customers, and depots.

        Returns:
            list: A list containing vehicles, customers, and depots as separate lists of objects.
        """
        vehicles = []
        customers = []
        depots = []
        rows = File.get_rows()

        for i in range(3):
            for j in rows[i]:
                if i == 0:
                    # First section corresponds to vehicles.
                    vehicles.append(classes.Vehicle(float(j[0]), float(j[1])))
                elif i == 1:
                    # Second section corresponds to customers.
                    customers.append(classes.Customer(float(j[0]), float(j[1]), float(j[2]), float(j[3]), float(j[4])))
                elif i == 2:
                    # Third section corresponds to depots.
                    depots.append(classes.Depot(float(j[0]), float(j[1]), float(j[2])))
        return [vehicles, customers, depots]

    @staticmethod
    def get_rows():
        """
        Extract rows for vehicles, customers, and depots from the raw data.

        Returns:
            list: A list of rows categorized as vehicles, customers, and depots.
        """
        vehicle_num = int(File.data[0][3])
        customer_num = int(File.data[0][2])
        depot_num = int(File.data[0][3])

        vehicle_rows = File.data[1:vehicle_num + 1]
        customer_rows = File.data[vehicle_num + 1:vehicle_num + customer_num + 1]
        depot_rows = File.data[vehicle_num + customer_num + 1: vehicle_num + customer_num + depot_num + 1]
        
        # Clean rows to remove empty strings or irregular spacing.
        return [vehicle_rows, File.clean(customer_rows), File.clean(depot_rows)]

    @staticmethod
    def clean(rows):
        """
        Remove empty strings or irregular spacing from rows.

        Args:
            rows (list): List of rows to clean.

        Returns:
            list: Cleaned rows with no empty strings.
        """
        cleaned = []
        for i in rows:
            row = []
            for j in i:
                if j != '':
                    row.append(j)
            cleaned.append(row)
        return cleaned
