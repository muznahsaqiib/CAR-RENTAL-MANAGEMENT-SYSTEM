import json
import uuid
import datetime


class Car:
    def __init__(self, car_id, make, model, year, rentpricePerday, available=True):
        self.car_id = car_id
        self.make = make
        self.model = model
        self.year = year
        self.available = available
        self.rentpricePerday = rentpricePerday

    def disp(self):
        print("             CAR DETAILS           ")
        print("Car ID:", self.car_id)
        print("Make:", self.make)
        print("Model:", self.model)
        print("Year:", self.year)
        print("Rent Price:", self.rentpricePerday)
        print("Availability:", "Available" if self.available else "Not Available")
        
    def updateCarName(self, new_model):
        self.model = new_model
   
class Admin:
    def __init__(self, password):
        self.password = password
        self.rental_info_file = "rental_info.json"

    def login(self):
        while True:
            p = input("Enter password: ")
            if p == self.password:
                print("ACCESS GRANTED!")
                print()
                break
            else:
                print("ACCESS DENIED! Please try again.")


    def carInventory(self):
        print("         CAR INVENTORY       ")
        print("1. Display all cars")
        print("2. Update car name")
        print("3. Update car rent prices")
        print("4. Add cars")
        print("5. Delete cars")
        print("6. Check rental record.")
        print("7.Total bookings.")

        choice = int(input("Enter your choice: "))
        inventory_file = "cars.json"
        with open(inventory_file, "r") as file:
            inventory = json.load(file)

        if choice == 1:
            if isinstance(inventory, list):
                if len(inventory) > 0:
                    for car_data in inventory:
                        car = Car(
                            car_data["car_id"],
                            car_data["make"],
                            car_data["model"],
                            car_data["year"],
                            car_data["Rent Price"],
                            car_data["availablity"]
                        )
                        car.disp()
                        print()
                else:
                    print("No cars found in the inventory.")
            else:
                print("Invalid inventory data. Please check the JSON file.")

        elif choice == 2:
            car_id = int(input("Enter the car ID for which you want to update the model: "))
            for car_data in inventory:
                if car_data["car_id"] == car_id:
                    new_model = input("Enter the new model for this car: ")
                    car_data["model"] = new_model
                    print("Car model updated successfully.")
                    break
            else:
                print("Car not found with the given car ID.")

        elif choice == 3:
            car_id = int(input("Enter the car ID for which you want to update the rent price: "))
            for car_data in inventory:
                if car_data["car_id"] == car_id:
                    new_rent_price = (input("Enter the new rent price for this car: "))
                    car_data["Rent Price"] = new_rent_price
                    print("Car rent price updated successfully.")
                    break
            else:
                print("Car not found with the given car ID.")

        elif choice == 4:
            car_id = int(input("Enter the car ID: "))
            make = input("Enter the make: ")
            model = input("Enter the model: ")
            year = int(input("Enter the year: "))
            rent_price = float(input("Enter the rent price: "))
            new_car = {
                "car_id": car_id,
                "make": make,
                "model": model,
                "year": year,
                "Rent": rent_price,
                "available": True
            }
            inventory.append(new_car)
            print("Car added successfully.")

        elif choice == 5:
            car_id = int(input("Enter the car ID of the car you want to delete: "))
            for car_data in inventory:
                if car_data["car_id"] == car_id:
                    inventory.remove(car_data)
                    print("Car deleted successfully.")
                    break
            else:
                print("Car not found with the given car ID.")

        elif choice == 6:
            
            with open("rental_info.json", "r") as file:
                rental_info = json.load(file)

            print("--- RENTAL INFORMATION ---")
            for rental_entry in rental_info:
                print("Customer Name:", rental_entry["customer name"])
                print("Customer Email:", rental_entry["customer contact"])
                print("Car ID:", rental_entry["car_id"])
                print("Make:", rental_entry["make"])
                print("Model:", rental_entry["model"])
                print("Year:", rental_entry["year"])
                print("Rent Price per Day:", rental_entry["rent_price_per_day"])
                print("Rental Date:", rental_entry["rental_date"])
                print("Return Date:", rental_entry["return_date"])
                print("negotiated_price:",rental_entry["negotiated_price"])
                print()
        elif choice==7:
            
            with open("rental_info.json", "r") as file:
                rental_info = json.load(file)

            total_bookings = len(rental_info)
            print("Total Bookings:", total_bookings)
        with open(inventory_file, "w") as file:
            json.dump(inventory, file, indent=4)     


class Customer(Car):   
    
    def __init__(self, name, contact, address, cars):
        self.name = name
        self.contact = contact
        self.address = address        
        self.cars = cars
        self.negotiation_attempts = 0
        self.max_negotiation_attempts = 3
        self.customer_price = 0
        self.admin_last_price = 0
        self.price_range_percentage = 15
    
    def negotiation(self):
            self.admin_last_price = int(input("Enter the last price set by the admin: "))
            max_customer_price = self.admin_last_price - (self.admin_last_price * self.price_range_percentage / 100)

            while self.negotiation_attempts < self.max_negotiation_attempts:
                self.customer_price = int(input(f"Enter your proposed price (within {self.price_range_percentage}% below {self.admin_last_price}): "))

                if self.customer_price >= max_customer_price:
                    print("Customer proposed price:", self.customer_price)
                    break
                else:
                    print("Invalid price. Please propose a price within the allowed range.")

                self.negotiation_attempts += 1

            if self.negotiation_attempts < self.max_negotiation_attempts:
                print("Negotiation successful! Final price:", self.customer_price)
            else:
                print("Negotiation unsuccessful. Final price:", self.admin_last_price)


    def rentcar(self):
        
        with open("cars.json", "r") as file:
            inventory = json.load(file)

        print("         WELCOME!         ")
        print("Select the company of which you want to rent a car.")

        for i, car_make in enumerate(self.cars):
            
            print(f"{i + 1}. {car_make[0]['make']}")

        pick = int(input("Enter your choice: "))

        if 1 <= pick <= len(self.cars):
            car_make = self.cars[pick - 1]
            available_cars = [car for car in car_make if car["available"]]
            
            print(f"      {car_make[0]['make'].upper()}      ")
            if len(available_cars) > 0:
                for i, car in enumerate(available_cars):
                   
                    print(f"{i + 1}. {car['model']}")

                car_choice = int(input("Enter the number corresponding to the car model: "))
                if 1 <= car_choice <= len(available_cars):
                    selected_car = available_cars[car_choice - 1]
                    selected_car["available"] = False
                    car = Car(selected_car['car_id'], selected_car['make'], selected_car['model'], selected_car['year'], selected_car['RentpricePerday'])
                    car.disp()

                    o = input("ARE YOU SATISFIED WITH THE PRICE OR WANT SOME NEGOTIATION? (Y/N): ")
                    if o.lower() == "y":
                        print(self.negotiation())
                        
                    ans = input("Do you want to rent this car? (Y/N): ")
                   
                    if ans.lower() == "y":  
                        negotiated_price = self.customer_price if self.negotiation_attempts < self.max_negotiation_attempts else self.admin_last_price
                        
            

                        rental_info = []

                        entry = {
                            "customer name": self.name,
                            "customer contact": self.contact,
                            "car_id": car.car_id,
                            "make": car.make,
                            "model": car.model,
                            "year": car.year,
                            "rent_price_per_day": car.rentpricePerday,
                            
                            "rental_date": datetime.date.today().isoformat(),
                            "return_date": ""
                        }
                        entry["negotiated_price"] = negotiated_price
                        

                        rental_info.append(entry)
                        try:
                            with open("rental_info.json", "r") as file:
                                existing_rental_info = json.load(file)
                        except FileNotFoundError:
                            existing_rental_info = []
                        existing_rental_info.extend(rental_info)
                        
                        with open("rental_info.json", "w") as file:
                            json.dump(existing_rental_info, file, indent=4)
                                                                               
                        with open("cars.json", "r") as car_file:
                            inventory = json.load(car_file)

                        for car_entry in inventory:
                            if car_entry["car_id"] == car.car_id:
                                car_entry["availablity"] = False  
                                break

                        with open("cars.json", "w") as car_file:
                            json.dump(inventory, car_file, indent=4)

                            print("Car Rented Successfully!")

                else:
                    print("Invalid choice!")
            else:
                print("No available cars for rent.")

        else:
            print("Invalid choice!")

    def store_rental_info(self,rental_info):
        with open("rental_history.json", "a") as file:
            json.dump(rental_info, file)
            file.write("\n")


    def returnCar(self):
        print("        Return car       ")
        carID = int(input("Enter car ID: "))

        with open("rental_info.json", "r") as file:
            rental_info = json.load(file)

        for rental_entry in rental_info:
            if rental_entry["car_id"] == carID:
                if not rental_entry["return_date"]:
                    rental_entry["return_date"] = datetime.date.today().isoformat()
                    rental_entry["available"] = True
                    print("Thank you for returning the car.")
                else:
                    print("The car is already returned.")
                break
        else:
            print("Car not found.")

        with open("rental_info.json", "w") as file:
            json.dump(rental_info, file, indent=4)


    def signup(self):
        n = self.name
        c = self.contact
        a = self.address

        registration = str(uuid.uuid4())
        with open("customer.json", "a+") as file:
            content = file.read()
            if content:
                customer = json.loads(content)
            else:
                customer = {}            
            if registration in customer:
                print("Customer already registered!")
                return                        
            customer[registration] = {"name": n, "contact": c, "address": a}
            file.seek(0)  
            file.write(json.dumps(customer, indent=4))
            file.truncate()                
            print(n, "has been registered successfully!")     
            print("1: Rent a Car")
            print("2: Return a Car")
            option = int(input("Enter your Choice: "))
            if option == 1:
                self.rentcar()
            elif option == 2:
                self.returnCar()
            else:
                print("Invalid choice!")

        
def main():
        
    
   
            
        cars = [
    [
        {"car_id": 1, "make": "Mercedes", "model": "Mercedes-Benz GLA SUV", "RentpricePerday": "35k", "year": 2013,
         "available": True},
        {"car_id": 2, "make": "Mercedes", "model": "Mercedes-Benz GLC Coupe", "RentpricePerday": "40k", "year": 2017,
         "available": True},
        {"car_id": 3, "make": "Mercedes", "model": "Mercedes-Maybach GLS SUV", "RentpricePerday": "38k", "year": 2020,
         "available": True},
        {"car_id": 4, "make": "Mercedes", "model": "Mercedes-Benz S-Class Sedan", "RentpricePerday": "45k",
         "year": 2022, "available": True},
        {"car_id": 5, "make": "Mercedes", "model": "Mercedes G-Wagen", "RentpricePerday": "50k", "year": 2023,
         "available": True}
    ],
    [
        {"car_id": 6, "make": "Rolls Royce", "model": "Rolls Royce Ghost", "RentpricePerday": "39k", "year": 2021,
         "available": True},
        {"car_id": 7, "make": "Rolls Royce", "model": "Rolls Royce Phantom", "RentpricePerday": "33k", "year": 2022,
         "available": True},
        {"car_id": 8, "make": "Rolls Royce", "model": "Rolls Royce Cullinan", "RentpricePerday": "55k", "year": 2020,
         "available": True},
        {"car_id": 9, "make": "Rolls Royce", "model": "Rolls-Royce Wraith", "RentpricePerday": "30k", "year": 2021,
         "available": True},
        {"car_id": 10,"make": "Rolls Royce", "model": "Rolls-Royce Dawn", "RentpricePerday": "32k", "year": 2021,
         "available": True}
    ],
    [
        {"car_id": 11, "make": "Ford", "model": "Ford Mustang", "RentpricePerday": "29k", "year": 2021,
         "available": True},
        {"car_id": 12, "make": "Ford", "model": "Ford Explorer", "RentpricePerday": "42k", "year": 2022,
         "available": True},
        {"car_id": 13, "make": "Ford", "model": "Ford F-150", "RentpricePerday": "35k", "year": 2020,
         "available": True},
        {"car_id": 14, "make": "Ford", "model": "Ford Escape", "RentpricePerday": "50k", "year": 2021,
         "available": True},
        {"car_id": 15, "make": "Ford", "model": "Ford Focus", "RentpricePerday": "30k", "year": 2021,
         "available": True}
    ],
    [
        {"car_id": 16, "make": "Toyota", "model": "Toyota Camry", "RentpricePerday": "35k", "year": 2021,
         "available": True},
        {"car_id": 17, "make": "Toyota", "model": "Toyota Corolla", "RentpricePerday": "20k", "year": 2022,
         "available": True},
        {"car_id": 18, "make": "Toyota", "model": "Toyota Highlander", "RentpricePerday": "19k", "year": 2020,
         "available": True},
        {"car_id": 19, "make": "Toyota", "model": "Toyota Highlander", "RentpricePerday": "22k", "year": 2021,
         "available": True},
        {"car_id": 20, "make": "Toyota", "model": "Toyota Tacoma", "RentpricePerday": "25k", "year": 2021,
         "available": True}
    ],
    [
        {"car_id": 21, "make": "Honda", "model": "Honda Civic", "RentpricePerday": "15k", "year": 2021,
         "available": True},
        {"car_id": 22, "make": "Honda", "model": "Honda Accord", "RentpricePerday": "30k", "year": 2022,
         "available": True},
        {"car_id": 23, "make": "Honda", "model": "Honda CR-V ", "RentpricePerday": "35k", "year": 2020,
         "available": True},
        {"car_id": 24, "make": "Honda", "model": "Honda Pilot", "RentpricePerday": "29k", "year": 2021,
         "available": True},
        {"car_id": 25, "make": "Honda", "model": "Honda Odyssey", "RentpricePerday": "44k", "year": 2021,
         "available": True}
    ]
]
        with open("cars.json", "w") as carFile:
            carFile.write("[")
            carFile.write("\n")
            for i, car_group in enumerate(cars):                
                for j, car in enumerate(car_group):
                    carFile.write("{\n")
                    carFile.write(f'"car_id": {car["car_id"]},\n')
                    carFile.write(f'"make": "{car["make"]}",\n')
                    carFile.write(f'"model": "{car["model"]}",\n')
                    carFile.write(f'"Rent Price":"{car["RentpricePerday"]}",\n')
                    carFile.write(f'"year": {car["year"]},\n')
                    carFile.write(f'"availablity":"{car["available"]}"\n')
                    carFile.write("}")
                    if j != len(car_group) - 1:
                        carFile.write(",")
                    carFile.write("\n")                
                if i != len(cars) - 1:
                    carFile.write(",")
                carFile.write("\n")                
            carFile.write("]")   
        while True:
            print("         CAR RENTAL MANAGMENT SYSTEM         ")
            print("                  WELCOME                    ") 
            
            print("             1.LOGIN AS ADMIN                ")
            print("             2.LOGIN AS COSTUMER             ")
            opt=int(input(("    Enter your Choice:")))
            if opt==1:   
                while True:  
                    password="1502"   
                    admin = Admin(password)
                    admin.login()
                    admin.carInventory()
                    print()
                    break
                    
                
            if opt==2:
                while True:
                    n = input("Enter your Full name: ")
                    c = (input("Enter your contact number or email: "))
                    a = input("Enter your permanent address: ")
                    c1 = Customer(n, c, a,  cars)                    
                    
                    c1.signup()
                    break

if __name__ == '__main__':
    main()
    

        
