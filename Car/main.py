class Car:
    def __init__(self, name, speed):
        self.name = name
        self.speed = speed
        self.maxspeed = 200
        self.minspeed = 0

    def drive(self):
        if self.speed == 0:
            print(f"{self.name} is not moving.")
        elif 1 <= self.speed <= 20:
            print(f"{self.name} is driving chilled with {self.speed} m/ph.")
        elif 21 <= self.speed <= 50:
            print(f"{self.name} is driving by the book with {self.speed} m/ph.")
        elif 51 <= self.speed <= 120:
            print(f"{self.name} is driving sportily with {self.speed} m/ph.")
        elif 121 <= self.speed <= self.maxspeed:
            print(f"{self.name} is driving way too fast with {self.speed} m/ph.")
        else:
            print(f"{self.name} exceeds the maximum speed!")

    def accelerate(self, amount):
        try:
            amount = int(amount)
        except ValueError:
            print("Please enter an integer value.")
            return
        if amount <= 0:
            print("Amount must be greater than 0.")
            return

        self.speed += amount
        if self.speed > self.maxspeed:
            self.speed = self.maxspeed
        print(f"{self.name} is accelerating to {self.speed} m/ph.")
        self.drive()

    def brake(self, amount):
        try:
            amount = int(amount)
        except ValueError:
            print("Please enter an integer value.")
            return
        if amount <= 0:
            print("Amount must be greater than 0.")
            return
        self.speed -= amount
        if self.speed < self.minspeed:
            self.speed = self.minspeed
        print(f"{self.name} is slowing down to {self.speed} m/ph.")
        self.drive()

class Garage:
    def __init__(self):
        self.cars = {}

    def add_car(self, car):
        if car.name in self.cars:
            print(f"{car.name} is already in the garage.")
            return
        self.cars[car.name] = car
        print(f"{car.name} added to the garage.")

    def get_car(self, name):
        if name in self.cars:
            return self.cars[name]
        else:
            print(f"Car '{name}' is not in the garage!")
            return None

    def list_cars(self):
        print("Cars in the garage:")
        for name in self.cars:
            print(f"- {name}")

garage = Garage()

garage.add_car(Car("Opel", 90))
garage.add_car(Car("Mercedes", 120))
garage.add_car(Car("BMW", 60))

while True:
    print("\n--- Garage Menu ---")
    garage.list_cars()
    choice = input("Which car do you want to drive? (or 'exit'): ")

    if choice == "exit":
        print("Exiting program.")
        break

    car = garage.get_car(choice)
    if car is None:
        continue

    while True:
        print("\n--- Driving Menu ---")
        print("1. Accelerate")
        print("2. Brake")
        print("3. Show status")
        print("4. Change car")
        print("5. Exit program")

        action = input("Choose an action: ")

        if action == "1":
            amount = (input("Accelerate by: "))
            car.accelerate(amount)

        elif action == "2":
            amount = (input("Brake by: "))
            car.brake(amount)

        elif action == "3":
            car.drive()

        elif action == "4":
            break

        elif action == "5":
            print("Exiting program.")
            exit()

        else:
            print("Invalid choice. Please select a valid option.")
