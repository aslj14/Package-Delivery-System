# Author: Ariel Johnson
# Student ID: 002973040
# Title: Task 2-WGUPS Routing Program Implementation

import csv
import datetime

# This will load the CSV files
with open("WGUPS Address File.csv") as addresses:
    AddressesCSV = csv.reader(addresses)
    AddressesCSV = list(AddressesCSV)
with open("WGUPS Distance Table.csv") as distances:
    DistancesCSV = csv.reader(distances)
    DistancesCSV = list(DistancesCSV)


# This will create the hash table
class ChainingHashTable:
    def __init__(self, openingcapacity=40):
        self.board = []
        for i in range(openingcapacity):
            self.board.append([])

    # This will place a new article into the chaining hash table and then update an article in the list
    def place(self, key, article):
        vessel = hash(key) % len(self.board)
        vessel_list = self.board[vessel]
        # This updates the key if the key is already included in the bucket (vessel)
        for vk in vessel_list:
            # Print the (value_of_key)
            if vk[0] == key:
                vk[1] = article
                return True
        # If the key is not in the vessel, then the article will be inserted at the end of the list
        value_of_key = [key, article]
        vessel_list.append(value_of_key)
        return True

    # This looks through the hash table for the article with the key that matches
    # It will return the article if it is found, or none if it is not found
    def look(self, key):
        vessel = hash(key) % len(self.board)
        vessel_list = self.board[vessel]
        # Print the (vessel_list)
        # Look through the vessel for the key
        for vk in vessel_list:
            # Print the (value_of_key)
            if vk[0] == key:
                return vk[1]  # This is the value
        return None

    # This removes the article that has the matching key from the hash table
    def remove(self, key):
        vessel = hash(key) % len(self.board)
        vessel_list = self.board[vessel]
        # This removes the article if it is there
        if key in vessel_list:
            vessel_list.remove(key)

# This is where storage for the needed guidelines about the packages are
class UPSPackages:
    def __init__(self, pID, pStreet, pCity, pState, pZip, pWeight, pDeadline, pStatus, pNotations, pDeparture,
                 pDelivery):
        self.pID = pID
        self.pStreet = pStreet
        self.pCity = pCity
        self.pState = pState
        self.pZip = pZip
        self.pWeight = pWeight
        self.pDeadline = pDeadline
        self.pStatus = pStatus
        self.pNotations = pNotations
        self.pDeparture = None  # Time of departure
        self.pDelivery = None  # Time of delivery

    def __str__(self):
        return "Package ID: %s | Address: %-20s, %s, %s %s | Deadline: %s | Weight: %s | Status: %s | Departure Time: %s | Delivery Time: %s" % (self.pID, self.pStreet, self.pCity, self.pState, self.pZip, self.pWeight, self.pDeadline, self.pStatus, self.pDeparture, self.pDelivery)
    # In this method the status of a package is updated and this is contingent upon the time that is entered
    def updatePackageStatus(self, enteredTime):
        if self.pDelivery == None:
            self.pStatus = "The package is at the hub."
        elif enteredTime < self.pDeparture:
            self.pStatus = "The package is at the hub."
        elif enteredTime < self.pDelivery:
            self.pStatus = "The package is en route."
        else:
            self.pStatus = "The package has been delivered."
        if self.pID == 9:  # This will switch package 9's address to the accurate address once the package has een received.
            if enteredTime > datetime.timedelta(hours=10, minutes=20):
                self.pStreet = "410 S State St"
                self.pZip = "84111"
            else:
                self.pStreet = "300 State St"
                self.pZip = "84103"

# This creates the Packages with the information from the CSV file to be input into the hash table
def getDataFromPackage(filename):
    with open(filename) as packages:
        packageDetails = csv.reader(packages, delimiter=",")
        next(packageDetails)
        for package in packageDetails:
            ID = int(package[0])
            # Print the package ID
            street = package[1]
            # Print the package street
            city = package[2]
            # Print the package city
            state = package[3]
            # Print the package state
            postal = package[4]
            # Print the package zip code
            weight = package[5]
            # Print the package weight
            deadline = package[6]
            # Print the package delivery deadline
            notations = package[7]
            # Print the package notes
            status = "The package is at the hub."
            departure = None
            delivery = None

            # This places the package details into the hash table
            thePackages = UPSPackages(ID, street, city, state, postal, weight, deadline, notations, status, departure, delivery)
            # Print (packages)
            thePackageHash.place(ID, thePackages)

# This is the hash table for the packages
thePackageHash = ChainingHashTable()


# Qualifications for the creation of a truck
class Trucks:
    def __init__(self, tSpeed, tMiles, tLocation, tDeparture, tPackages):
        self.tSpeed = tSpeed
        self.tMiles = tMiles
        self.tLocation = tLocation
        self.tTime = tDeparture
        self.tDeparture = tDeparture
        self.tPackages = tPackages

    def __str__(self):
        return "%s, %s, %s, %s, %s, %s" % (self.tSpeed, self.tMiles, self.tLocation, self.tTime, self.tDeparture, self.tPackages)


# This discovers the minimal distance for the next address
def addresses(theAddress):
    for row in AddressesCSV:
        if theAddress in row[2]:
            return int(row[0])


# This discovers the minimal distance that links two addresses
def Between(address1, address2):
    theDistance = DistancesCSV[address1][address2]
    if theDistance == '':
        theDistance = DistancesCSV[address2][address1]
    return float(theDistance)


# This pulls in data from the CSV file into the function
getDataFromPackage('WGUPS Package File.csv')

# This manually loads the trucks and then designates a departure time
firstTruck = Trucks(18, 0.0, "4001 South 700 East", datetime.timedelta(hours=8),[1,13,14,15,16,19,20,27,29,30,31,34,37,40])
secondTruck = Trucks(18, 0.0, "4001 South 700 East", datetime.timedelta(hours=11),[2,3,4,5,9,18,26,28,32,35,36,38])
thirdTruck = Trucks(18, 0.0, "4001 South 700 East", datetime.timedelta(hours=9, minutes=5),[6,7,8,10,11,12,17,21,22,23,24,25,33,39])

# Print Welcome message
print("Welcome to the program!")

# This algorithm will make the deliveries of the packages that are on the truck
def deliverTruckPackages(trucks):
    # A list is created for all of the packages that are supposed to be delivered
    incoming = []
    # This places the packages from the hash table into the "incoming" list
    for idPackage in trucks.tPackages:
        thePackage = thePackageHash.look(idPackage)
        incoming.append(thePackage)

    trucks.tPackages.clear()
    # The algorithm will run while there are still more packages that need to be delivered
    while len(incoming) > 0:
        upcomingAddress = 2000
        upcomingPackage = None
        for thePackage in incoming:
            if thePackage.pID in [25, 6]:
                upcomingPackage = thePackage
                upcomingAddress = Between(addresses(trucks.tLocation), addresses(thePackage.pStreet))
                break
            if Between(addresses(trucks.tLocation), addresses(thePackage.pStreet)) <= upcomingAddress:
                upcomingAddress = Between(addresses(trucks.tLocation), addresses(thePackage.pStreet))
                upcomingPackage = thePackage
        trucks.tPackages.append(upcomingPackage.pID)
        incoming.remove(upcomingPackage)
        trucks.tMiles += upcomingAddress
        trucks.tLocation = upcomingPackage.pStreet
        trucks.tTime += datetime.timedelta(hours=upcomingAddress / 18)
        upcomingPackage.pDelivery = trucks.tTime
        upcomingPackage.pDeparture = trucks.tDeparture

        # incoming.remove(upcomingPackage)
        # print(upcomingPackage.packageStreet)


# This calls the trucks that are leaving to deliver the packages
deliverTruckPackages(firstTruck)
deliverTruckPackages(thirdTruck)
# Guarantees that Truck 3 will not leave until Truck 1 or Truck 2 have returned
secondTruck.tDeparture = min(firstTruck.tTime, thirdTruck.tTime)
deliverTruckPackages(secondTruck)

# Title of program
print("")
print("WESTERN GOVERNOR'S UNIVERSITY POSTAL SERVICE")
# All of the truck's miles combined
print("*" * 60)
print("The total miles are: ", (firstTruck.tMiles + secondTruck.tMiles + thirdTruck.tMiles))
print("*" * 60)

while True:

    # print(firstTruck.tMiles + secondTruck.tMiles + thirdTruck.tMiles))
    timeOfUser = input("If you'd like to see the status of each package, please input a time. (Format must be: HH:MM): ")
    (hours, minutes) = timeOfUser.split(":")
    changeOfTime = datetime.timedelta(hours=int(hours), minutes=int(minutes))
    try:
        entry = [int(input("Please enter the package ID to get the details of a specific package or do not input anything and press enter to get the details of all packages: "))]
    except ValueError:
        entry = range(1, 41)
    print("All package details at time: ", changeOfTime)
    for idPackage in entry:
        thePackage = thePackageHash.look(idPackage)
        thePackage.updatePackageStatus(changeOfTime)
        print(str(thePackage))
    # All of the truck's miles combined
    print("*" * 60)
    print("The total miles are: ", (firstTruck.tMiles + secondTruck.tMiles + thirdTruck.tMiles))
    print("*" * 60)