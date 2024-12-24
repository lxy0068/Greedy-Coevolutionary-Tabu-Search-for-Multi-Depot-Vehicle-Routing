import csv
import classes


class File(object):
    data = []

    @staticmethod
    def read(file_name):
        with open(file_name) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=' ')
            for row in csv_reader:
                File.data.append(row)
        return File.get_objects()

    @staticmethod
    def get_objects():
        vehicles = []
        customers = []
        depots = []
        rows = File.get_rows()

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
        vehicle_num = int(File.data[0][3])
        customer_num = int(File.data[0][2])
        depot_num = int(File.data[0][3])

        vehicle_rows = File.data[1:vehicle_num + 1]
        customer_rows = File.data[vehicle_num + 1:vehicle_num + customer_num + 1]
        depot_rows = File.data[vehicle_num + customer_num + 1: vehicle_num + customer_num + depot_num + 1]
        return [vehicle_rows, File.clean(customer_rows), File.clean(depot_rows)]

    @staticmethod
    def clean(rows):
        cleaned = []
        for i in rows:
            row = []
            for j in i:
                if j != '':
                    row.append(j)
            cleaned.append(row)
        return cleaned

