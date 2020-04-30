from Car import Car
from tkinter import *
from tkinter import messagebox
from tkinter import ttk
import csv

# program opens and read all csv files
toyotaCSV = open('toyota.csv', 'r')
toyotaData = csv.reader(toyotaCSV)

subaruCSV = open('subaru.csv', 'r')
subaruData = csv.reader(subaruCSV)

holdenCSV = open('holden.csv', 'r')
holdenData = csv.reader(holdenCSV)

hondaCSV = open('honda.csv', 'r')
hondaData = csv.reader(hondaCSV)


# combines the data from all csv's to the car list
def csvParser(file):
    """Function combines data from each of the csv files into the car list

    Args:
        file: csv file the data is being exported from

    """
    for row in file:
        if row in [[]]:  # if row is empty, will continue checking in the next row
            continue
        else:
            name = str(row[0].strip())
            model = str(row[1].strip())
            year = int(row[2].strip())
            colour = str(row[3].strip())
            price = float(row[4].strip())
            availability = int(row[5].strip())
            carList.append(Car(name, model, year, colour, price))  # appends all features to car list


carList = []
csvParser(toyotaData)
csvParser(subaruData)
csvParser(holdenData)
csvParser(hondaData)


def get_model(mname):
    """Function gets the name of chosen car from car list

    Args:
        mname: the car model taken from the list

    return: gets chosen car model and returns user to gui
    """
    #   finds the car in car list
    for model in carList:
        if model.get_model() == mname:
            return model
    print("Car not found")  # debug message, will print to console


root = Tk()

root.title("Used Car Dealership")
root.configure(background="#E3D2AF", pady="10", padx="8")

main_window_width = 450.0
main_window_height = 538.0

screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

#   positions the GUI in the center of the screen
main_x = screen_width / 2 - main_window_width / 2
main_y = screen_height / 2 - main_window_height / 2

root.geometry("%dx%d+%d+%d" % (main_window_height, main_window_height, main_x, main_y))
root.option_add("*Font", "LucindaGrande 16")

root.resizable(False, False)


def update_details():
    """updates details of the car list and prints to GUI"""

    model_name = car_selector.get(ACTIVE)
    current_car = get_model(model_name)

    #   updates details for the car details listed below
    str_name.set("Brand: " + str(current_car.get_name()))
    str_availability.set("Availability: " + str(current_car.get_availability()))
    str_year.set("Year: " + str(current_car.get_year()))
    str_colour.set("Colour: " + str(current_car.get_colour()))
    str_price.set("Price: $ " + str(current_car.get_price()))


def addtoContactList():
    """stores contact details from each customer in the contactList"""
    global contactList
    contactList.append()  # appends contact details to list (Global so it can be used in multiple functions)
    print(contactList)
    messagebox.showinfo('Added', 'Details have been added')
    update_details()


contactList = []


def sold_list(car):
    """stores all the cars that have been sold in the soldList

        Args:
        car: gets the name of the chosen car being sold

    """
    global soldList
    # appends all cars sold to the soldList (Global so it can be used in multiple functions)
    soldList.append([car.get_name(), car.get_model(), car.get_year(), car.get_colour(), car.get_price()])
    print(soldList)
    update_details()


soldList = []


def extraFeatureList(error, window, car):
    """stores all extra features chosen by customers in the allSoldFeaturesList
        Args:
        error: error message is shown when user does not select any extra feature in checkbox
        window: closes the current window the user is in when features are appended to list
        car: gets the name of the chosen car being sold

    return: returns user to the gui once features have been appended to list
    """
    for item in varList_extra:
        if item.get() != "":  # if checkbox is selected it will be appended to the feature list
            featureList.append(item.get())

    if len(featureList) == 0:  # checks list that contains checkboxes values. If length of list = 0, error will show
        error.set("Please select any extra options")
        return
    else:
        messagebox.showinfo('Added', "You have successfully bought the {} {} with extra features for {}".format(
            car.get_name(), car.get_model(), car.get_extra_features() + car.get_price()))

        get_model(car_selector.get(ACTIVE)).sell_car()  # sells cars and reduces availability by 1
        sold_list(car)  # sold_list function is called in order to store all cars sold in a separate list
        contact_details(car)  # contact details function is called in order for customer to add details
        delete_car(car)
        close_window(window)
        update_details()


featureList = []  # temporarily stores features in this list, then removes in the receipt function
allSoldFeaturesList = []  # all features are stored in this list once added


def cars_purchased(car):
    """exports all list information to a separate csv that contains all cars sold, price accumulated and contact info

        Args:
        car: gets the name of the chosen car

    returns: returns user to the gui when message box is clicked 'ok'

    """

    if len(carList) == 0:  # if there are no cars in the car list, function can not be used anymore
        messagebox.showerror("Error", "You have no more cars")
        return

    if car.get_stock_sold_count() == 0:  # if no cars have been sold yet, function can not be accessed
        messagebox.showerror('Selection of cars missing', "You have not sold any cars yet")
        return

    #   asks user before they delete the car with a yes or no answer type question
    MsgBox = messagebox.askquestion('Used car dealership summary',
                                    'Information will be exported to a csv. Would you like to continue?',
                                    icon='question')
    if MsgBox == 'yes':
        # total prices can add to this count
        price_count = 0.00
        car_count = 0
        extra_count = 0.00

        #   gets the total amount of cars sold, price accumulated, extra features cost and adds it to csv purchased
        for c in carList:
            price_count += c.get_price_total()
            car_count += c.get_stock_sold_count()
            extra_count += c.get_extra_features()

        else:
            with open('carsPurchased.csv', 'w') as file:  # opens existing csv file to write to
                writer = csv.writer(file)

                # Prints Purchase summary at the top of the csv
                writer.writerow(['Purchase summary: '])

                # Exports number of cars bought to csv
                csv_cars_bought = soldList
                cars_bought_str = 'All Cars bought: ' + str(csv_cars_bought)
                writer.writerow([cars_bought_str])

                # Exports all extra features purchased to csv
                csv_extra_features = allSoldFeaturesList
                extra_features_str = 'All Extra features purchased' + str(csv_extra_features)
                writer.writerow([extra_features_str])

                # Exports final extra features cost to csv
                extra_features_price = f'All Extra Features Total: $ {extra_count}'
                writer.writerow([extra_features_price])

                # Exports delivery option to csv
                csv_contact = contactList
                contact_str = 'All contact details: ' + str(csv_contact)
                writer.writerow([contact_str])

                # Exports total price to csv
                price_total_str = f'Total price accumulated: $ {price_count}'
                writer.writerow([price_total_str])

                # Exports total cars sold to csv
                sold_total_str = f'Total Cars Sold: {car_count}'
                writer.writerow([sold_total_str])

            messagebox.showinfo('Exported to csv',
                                "Used car dealership information has been finalised and exported to a csv. Please check ")

    else:
        messagebox.showinfo('Return',
                            'You will now return to the application')  # returns user to application without exporting
    return


def sell_car(car):
    """sells a single car to user, reduces availability by 1 and appends info to a list
        extra features also come as an option to add to car if user is wanting

        Args:
        car: gets the name of the chosen car user is wanting to sell

    returns: returns user to the gui if message box error shows, or if user presses 'cancel' for purchasing car

    """
    if len(carList) == 0:  # if there are no cars in the car list, function can not be used anymore
        messagebox.showerror("Error", "You have no more cars")
        return

    if car.get_availability() < 1:  # if car has been sold already, it can not be sold again
        messagebox.showwarning('Sell car', "The {} {} has been sold and is no longer available to buy.".format
        (car.get_name(), car.get_model()))
        return
        close_window

    global extraSelect
    extraSelect = False

    global varList_extra  # declares list scope as global, so the extraFeatureList function can use it
    varList_extra = []  # stores values of checkboxes
    # Every time function is called, varList_extra will be initialised empty

    MsgBox = messagebox.askquestion('Add extra options',
                                    'Would you like to purchase any extra options (eg. insurance) for the {} {} '.format
                                    (car.get_name(), car.get_model()), icon='info')

    if MsgBox == 'yes':  # if user agrees to wanting extra options

        width = 410
        height = 270
        #   positions the window in the center of the screen
        x = screen_width / 2 - width / 2
        y = screen_height / 2 - height / 2

        car_window = Toplevel(root)
        car_window.title("Extra options")
        car_window.option_add("*Font", "LucidaGrande 10")
        car_window.geometry("%dx%d+%d+%d" % (width, height, x, y))

        Label(car_window,
              text="*Select any extra features to add for the {} {}*".format(car.get_name(), (car.get_model()))).grid(
            row=0,
            column=1,
            sticky=N + E + W + S)

        extraSelect = True
        model_name = car_selector.get(ACTIVE)

        if model_name == car.get_model():
            var1 = StringVar()  # checkbutton for extended warranty
            Checkbutton(car_window, text="Extended warranty($710)", variable=var1, onvalue="Extended warranty($710)",
                        offvalue="", command=lambda: car.extended_warranty()).grid(row=1, column=1, sticky=W)

            var2 = StringVar()  # checkbutton for after market wheels
            Checkbutton(car_window, text="After market wheels($320)", variable=var2,
                        onvalue="After market wheels($320)",
                        offvalue="", command=lambda: car.after_market()).grid(row=2, column=1, sticky=W)

            var3 = StringVar()  # checkbutton for tinted windows
            Checkbutton(car_window, text="Tinted windows(450)", variable=var3, onvalue="Tinted windows(450)",
                        offvalue="", command=lambda: car.tinted_windows()).grid(row=3, column=1, sticky=W)

            var4 = StringVar()  # checkbutton for liability coverage
            Checkbutton(car_window, text="Liability coverage ($500)", variable=var4,
                        onvalue="Liability coverage ($500)",
                        offvalue="", command=lambda: car.liability_coverage()).grid(row=4, column=1, sticky=W)

            var5 = StringVar()  # checkbutton for collision coverage
            Checkbutton(car_window, text="Collision coverage($2000)", variable=var5,
                        onvalue="Collision coverage($2000)",
                        offvalue="", command=lambda: car.collision_coverage()).grid(row=5, column=1, sticky=W)

            var6 = StringVar()  # checkbutton for sound system coverage
            Checkbutton(car_window, text="Sound system coverage($750)", variable=var6,
                        onvalue="Sound system coverage($750)",
                        offvalue="", command=lambda: car.sound_system_coverage()).grid(row=6, column=1, sticky=W)

            var7 = StringVar()
            Checkbutton(car_window, text="Theft coverage ($700)", variable=var7, onvalue="Theft coverage ($700)",
                        offvalue="", command=lambda: car.theft_coverage()).grid(row=7, column=1, sticky=W)

            # adds extra options to the varList_extra
            varList_extra.append(var1)
            varList_extra.append(var2)
            varList_extra.append(var3)
            varList_extra.append(var4)
            varList_extra.append(var5)
            varList_extra.append(var6)
            varList_extra.append(var7)

        str_error_msg = StringVar("")

        Label(car_window, textvariable=str_error_msg, fg="red").grid(row=9, column=1, columnspan=5,
                                                                     sticky=N + E + S + W)

        Button(car_window, text="Add", padx=11,
               command=lambda: [extraFeatureList(str_error_msg, car_window, car)]).grid(row=11, column=1, sticky=E,
                                                                                        padx='5')

        Button(car_window, text="Cancel",
               command=lambda: close_window(car_window)).grid(row=11, column=2, sticky=W)

    else:
        MsgBox = messagebox.askquestion('Puchase', "You are purchasing the {} {} without any extra options. "
                                                   "Please press yes to confirm".format(car.get_name(),
                                                                                        car.get_model()), icon='info')
        if MsgBox == 'yes':

            messagebox.showinfo('Sold', "You've  successfully bought the {} {} for {} without extra options ".format(
                car.get_name(), car.get_model(), car.get_price()))

            get_model(car_selector.get(ACTIVE)).sell_car()  # sells the car, reduces availability by 1
            sold_list(car)  # calls sold)list function and appends sold car to the list
            delete_car(car)  # deletes car from csv
            close_window(car_window)
            contact_details(car)  # contact details function is called so customer can enter their info
            update_details()
            return

        else:
            messagebox.showinfo('Return', 'Your purchase has been cancelled')
            close_window(car_window)  # returns user to application without deleting car
            return


def delete_car(car):
    """Deletes chosen car from its designated csv file

    Args:
        car: gets the car user wants to delete from the car list

    returns: if there are no cars left in the car list, user will be retured to the application
    """
    if len(carList) == 0:  # if there are no cars in the car list, function can not be used anymore
        messagebox.showerror("Error", "You have no more cars")
        return

    for car in soldList:  # gets every car in sold list
        selectCSV = open((car[0]) + '.csv', 'r')  # opens csv that is equivalent to first value of each car in sold list
        selectData = csv.reader(selectCSV)
        select_list = []
        for row in selectData:
            if row in [[]]:  # if csv has empty row, program will continue and go to next row
                continue
            else:
                select_list.append(row)
        for obj in select_list:  # finds if car in sold list matches car in object
            if car[1] in obj:
                select_list.remove(obj)  # object is removed from select list
            else:
                continue
            # opens csv that is equivalent to first value of each car in sold list
            selectWriter = csv.writer(open((car[0]) + '.csv', 'w', newline='\n'))
            selectWriter.writerows(select_list)  # writes the select list to the open csv


def contact_details(car):
    """Deletes chosen car from the list

    Args:
        car: gets the car that has been sold from the car list

    returns: returns user to GUI if no cars are in the car list anymore
    """
    if len(carList) == 0:  # if there are no cars in the car list, function can not be used anymore
        messagebox.showerror("Error", "You have no more cars")
        return

    width = 540.0
    height = 250.0
    x = screen_width / 2 - width / 2
    y = screen_height / 2 - height / 2

    contact_window = Toplevel(root)
    contact_window.title("Contact details")
    contact_window.option_add("*Font", "LucidaGrande 17")
    contact_window.geometry("%dx%d+%d+%d" % (width, height, x, y))

    Label(contact_window, text="Please enter your contact details **required**", width=30).grid(row=0, column=0,
                                                                                                columnspan=2,
                                                                                                sticky=N + E + S + W)

    #   creates and adds labels to text entry areas
    Label(contact_window, text="First Name: ").grid(row=1, column=0, sticky=E)
    Label(contact_window, text="Last Name: ").grid(row=2, column=0, sticky=E)
    Label(contact_window, text="Address: ").grid(row=3, column=0, sticky=E)
    Label(contact_window, text="Phone: ").grid(row=4, column=0, sticky=E)

    str_error_msg = StringVar("")
    str_firstname = StringVar("")
    str_lastname = StringVar("")
    str_address = StringVar("")
    str_phone = StringVar("")

    Entry(contact_window, textvariable=str_firstname).grid(row=1, column=1, sticky=E + W)
    Entry(contact_window, textvariable=str_lastname).grid(row=2, column=1, sticky=E + W)
    Entry(contact_window, textvariable=str_address).grid(row=3, column=1, sticky=E + W)
    Entry(contact_window, textvariable=str_phone).grid(row=4, column=1, sticky=E + W)

    Label(contact_window, textvariable=str_error_msg, fg="red", width=40).grid(row=5, column=0, columnspan=2,
                                                                               sticky=N + E + S + W)

    Button(contact_window, text="Save", width=7, command=lambda: add_details_and_close(str_error_msg,
                                                                                       contact_window,
                                                                                       str_firstname.get(),
                                                                                       str_lastname.get(),
                                                                                       str_address.get(),
                                                                                       str_phone.get(),
                                                                                       car)).grid(row=6, column=0,
                                                                                                  sticky=E)


def add_details_and_close(error, window, firstname, lastname, address, phone, car):
    """saves what you've put in contact details, appends to contactList and closes function

    Args:
        error: error message is shown when user enters an invalid number or boundary
        window: closes the current window user is in when details are added
        firstname: gets the customers first name typed into the string
        lastname: gets the customers last name typed into the string
        address: gets the customers address typed into the string
        phone: gets the customers phone number typed into the string
        car: gets the car that is being sold (And contact info for that car can be added)

    returns: returns user to the current window if an error is made within the function
    """
    if "" in [firstname, lastname, address, phone]:  # checks no fields in the contact form are blank
        error.set("No field can be blank")
        return

    if len(address) < 5:  # checks to see the address is over 5 characters in order to be legitimate
        error.set("Address must be over 5 characters")
        return

    # checks to see the first name is valid
    if not firstname.isalpha():  # checks to see the first-name contains only letters, no numbers
        error.set("First name must be characters A-Z")
        return
    elif len(firstname) <= 1:  # checks to see the first-name is over 1 letter in order to be legitimate
        error.set("First name must be be over 1 character")
        return

    # checks to see the last name is valid
    if not lastname.isalpha():  # checks to see the last-name contains only letters, no numbers
        error.set("Last name must be characters from A-Z")
        return
    elif len(lastname) <= 1:  # checks to see the last-name is over 1 letter in order to be legitimate
        error.set("Last name must be over 1 character")
        return

    # checks to see the phone number is valid
    if not phone.isdigit():  # checks to see the phone number does not have letters
        error.set('Please enter digits as your phone number')
        return
    elif len(phone) < 7 or len(phone) > 11:  # phone number must be between 7 and 11 digits in order to be legitimate
        error.set("Phone number must be between 7 and 11 digits")
        return


    # all details from the strings are appended to the contact list
    else:
        contactList.append([firstname, lastname])
        contactList.append(phone)
        contactList.append(address)
        print(firstname, lastname, phone, address)

    messagebox.showinfo('Added', 'Details have been added')
    update_details()
    close_window(window)
    receipt(firstname, lastname, car, phone, address)  # calls function to display customers receipt


def receipt(firstname, lastname, car, phone, address):
    """Prints a receipt out for the customer after car is sold - includes contact info and car details + final price

    Args:
        firstname: gets the customers first name
        lastname: gets the customers last name
        car: gets the car that has been sold
        phone: gets the customers phone number
        address: gets the customers address
    """
    width = 430.0
    height = 245.0
    # positions window in center of screen
    x = screen_width / 2 - width / 2
    y = screen_height / 2 - height / 2

    receipt_window = Toplevel(root)
    receipt_window.title("Used Car Dealership Receipt")
    receipt_window.option_add("*Font", "LucidaGrande 15")
    receipt_window.geometry("%dx%d+%d+%d" % (width, height, x, y))

    # labels all print info eg. car bought, contact info, extra features bought and total cost
    Label(receipt_window, text="**{} {}s purchase: **".format(firstname, lastname, ).title()).grid(
        row=0, column=0, sticky=N + E + S + W)

    Label(receipt_window,
          text="Car bought: {} {}, {}, {}, {}".format(car.get_name(), car.get_model(), car.get_year(),
                                                      car.get_colour(),
                                                      car.get_price())).grid(row=1, column=0, sticky=W)

    Label(receipt_window, text='Extra Options: {}'.format(featureList)).grid(row=2, column=0, sticky=W)

    Label(receipt_window, text='Full name: {} {}'.format(firstname,
                                                         lastname).title()).grid(row=3, column=0, sticky=W)

    Label(receipt_window, text='Address: {}'.format(address)).grid(row=4, column=0, sticky=W)
    Label(receipt_window, text='Phone: {}'.format(phone)).grid(row=5, column=0, sticky=W)

    Label(receipt_window, text='Final cost: ${}'.format(car.get_extra_features()
                                                        + car.get_price())).grid(row=6, column=0, sticky=W)

    Button(receipt_window, text="Ok", width=15, command=lambda: close_window(receipt_window)).grid(row=8, column=0,
                                                                                                   sticky=W)

    for feature in featureList:  # appends every feature in feature list to allSoldFeatures list
        allSoldFeaturesList.append(feature)
    featureList.clear()  # clears feature list so error checking can begin again

    cars_purchased(car)


def new_car(car):
    """opens a label where user can write in a brand, model, year, colour and price for a new car

    Args:
        car: the new car that has been created
    """
    width = 530.0
    height = 280.0
    # positions window in the middle of the screen
    x = screen_width / 2 - width / 2
    y = screen_height / 2 - height / 2

    newcar_window = Toplevel(root)
    newcar_window.title("Add new car")
    newcar_window.option_add("*Font", "LucidaGrande 17")
    newcar_window.geometry("%dx%d+%d+%d" % (width, height, x, y))

    Label(newcar_window, text="Please enter details for a new car:", width=30).grid(row=0, column=0, columnspan=2,
                                                                                    sticky=N + E + S + W)

    #   creates and adds labels to text entry areas
    Label(newcar_window, text="Brand: ").grid(row=1, column=0, sticky=E)
    Label(newcar_window, text="Model: ").grid(row=2, column=0, sticky=E)
    Label(newcar_window, text="Year: ").grid(row=3, column=0, sticky=E)
    Label(newcar_window, text="Colour: ").grid(row=4, column=0, sticky=E)
    Label(newcar_window, text="Price: ").grid(row=5, column=0, sticky=E)

    str_error_msg = StringVar("")
    str_new_brand = StringVar("")
    str_new_model = StringVar("")
    str_new_colour = StringVar("")
    str_new_year = StringVar("")
    str_new_price = StringVar("")

    # combobox is specifically used for a drop-down menu - can't be edited as state is read only.
    ttk.Combobox(newcar_window, textvariable=str_new_brand, state="readonly",
                 values=["Toyota", "Subaru", "Holden", "Honda"]).grid(row=1, column=1, sticky=E + W)

    Entry(newcar_window, textvariable=str_new_model).grid(row=2, column=1, sticky=E + W)
    Entry(newcar_window, textvariable=str_new_year).grid(row=3, column=1, sticky=E + W)

    ttk.Combobox(newcar_window, textvariable=str_new_colour, state="readonly",
                 values=["White", "Black", "Silver", "Blue", "Red", "Blue", "Green", "Yellow"]).grid(row=4, column=1,
                                                                                                     sticky=E + W)

    Entry(newcar_window, textvariable=str_new_price).grid(row=5, column=1, sticky=E + W)

    Label(newcar_window, textvariable=str_error_msg, fg="red", width=40).grid(row=6, column=0, columnspan=2,
                                                                              sticky=N + E + S + W)

    Button(newcar_window, text="Cancel", width=7, command=lambda: close_window(newcar_window)).grid(row=7, column=1,
                                                                                                    sticky=W)

    Button(newcar_window, text="Save", width=7, command=lambda: save_and_close(str_error_msg,
                                                                               newcar_window,
                                                                               car,
                                                                               str_new_brand.get(),
                                                                               str_new_model.get(),
                                                                               str_new_year.get(),
                                                                               str_new_colour.get(),
                                                                               str_new_price.get())).grid(row=7,
                                                                                                          column=0,
                                                                                                          sticky=E)


def save_and_close(error, window, car, new_brand, new_model, new_year, new_colour, new_price):
    """User can create a new car which is added to the existing list of cars, and designated csv file

    Args:
        error: error message is shown when user enters an invalid number or boundary
        window: the current 'new car' window the user is in
        car: the new car that has been created
        new_brand: gets the new brand of the car and updates list
        new_model: gets the new model of the car and updates list
        new_year: gets the new year of the car and updates list
        new_colour: gets the new colour of the car and updates list
        new_price: gets the new price of the car and updates list

    returns: returns user to the current window if an error is made within the function
    """
    if "" in [new_brand, new_model, new_year, new_colour, new_price]:  # checks no fields in the contact form are blank
        error.set("No field can be blank")
        return

    # check for car models with same name, after cleaning up the input values
    for c in carList:
        if c.get_model().strip().lower() == new_model.strip().lower():
            error.set("You can't have 2 cars with the same model")
            return

        # checks to make sure year is valid
    try:
        new_year = int(new_year)
    except ValueError:
        error.set("Year must be a positive, whole number")
        return
    if new_year < 1980:
        error.set("Year must be between 1980-2020")  # year can not be less than 1980
        return
    if new_year > 2020:
        error.set("Year must be between 1980-2020")  # year can not be over 2020
        return

        # checks to make sure the price is a valid number as well
    try:
        new_price = float(new_price)
    except ValueError:
        error.set("Price must be a positive, whole number")
        return
    if new_price == 0:
        error.set("The car can't have a price of $0.00")  # price must have a set number above 0
        return
    if new_price <= 0:
        error.set("Price must be a positive number")  # price can not be less than 0 eg. a negative number
        return

    # Capitalizes model and colour when it is appended car_list and its designated csv
    new_model.title()
    new_colour.title()

    selectCSV = open(new_brand + '.csv', 'r')  # opens csv that is equivalent to first value of each car in sold list
    selectData = csv.reader(selectCSV)
    select_list = []
    for row in selectData:
        if row in [[]]:  # if csv has empty row, program will continue and go to next row
            continue
        else:
            select_list.append(row)

    selavailability = 1  # sets availability value as 1
    select_list.append([new_brand, new_model, new_year, new_colour, new_price, selavailability])

    # opens csv that is equivalent to first value of each car in sold list
    selectWriter = csv.writer(open(new_brand + '.csv', 'w', newline='\n'))
    selectWriter.writerows(select_list)  # writes the select list to the open csv

    #   details are updated for the new car
    car = Car(new_brand, new_model, new_year, new_colour, new_price)  # new car is appended to the car list
    carList.append(car)
    messagebox.showinfo('Added', 'Car has been added')
    update_car_selector()
    update_details()
    close_window(window)

    update_details()
    close_window(window)


def close_window(window):
    """Closes the window of the function, and returns user to  GUI

    Args:
        window: the current window the user is in
    """
    window.destroy()  # destroys the current window user is in


def exit_application():
    """Asks user if they want to exit the application. Closes the GUI and ends program

    return: if user presses 'no', user will be returned to the GUI and program will not end/close
    """
    #   message box asks if user wants to exit the application with a simple yes or no type answer
    MsgBox = messagebox.askquestion('Exit Application', 'Are you sure you want to exit the application',
                                    icon='warning')
    if MsgBox == 'yes':
        root.destroy()  # ends the program
    else:
        messagebox.showinfo('Return', 'You will now return to the application')  # returns user to application
    return


def update_car_selector():
    # updates selector box for cars in car list when new changes are made
    car_selector.delete(0, END)
    for car in carList:
        car_selector.insert(END, car.get_model())


def onselect(ebt):
    """Updates car selector when you press on a car name

    Args:
        ebt: updates the car info automatically - keeps track of update patterns
    """
    #  car details update after 200 milliseconds (0.2 seconds) when clicked on
    root.after(200, update_details)


def store_summary():
    """displays amount of cars sold in total and the price accumulated from those car sold,
     as well as extra features price accumulated"""
    #   positions store summary in the center of the page
    width = 300.0
    height = 130.0
    x = screen_width / 2 - width / 2
    y = screen_height / 2 - height / 2

    store_window = Toplevel(root)
    store_window.title("Used Car Dealership summary")
    store_window.option_add("*Font", "LucidaGrande 15")
    store_window.geometry("%dx%d+%d+%d" % (width, height, x, y))

    # all numbers are set to 0 as nothing has been sold at the beginning
    price_count = 0.00
    car_count = 0
    extra_count = 0.00

    #   gets the total amount of cars sold, price accumulated, extra features cost and adds it to the store summary
    for c in carList:
        price_count += c.get_price_total()
        car_count += c.get_stock_sold_count()
        extra_count += c.get_extra_features()

    #   total amounts are placed in a small box
    string_total_sold = f'Total Cars Sold: {car_count}'
    string_total_price = f'Store balance: $ {price_count}'
    string_total_extra = f'Extra features: $ {extra_count}'

    Label(store_window, text=string_total_sold).grid(row=0, column=0, sticky=W)
    Label(store_window, text=string_total_extra).grid(row=1, column=0, sticky=W)
    Label(store_window, text=string_total_price).grid(row=2, column=0, sticky=W)

    Button(store_window, text="Ok", width=10, command=lambda: close_window(store_window)).grid(row=6, column=0,
                                                                                               sticky=S + W)


# listbox for the cars
car_selector = Listbox(root, height=14, width=22, background="#F0F0F5")  # creates the listbox
update_car_selector()
car_selector.grid(row=0, column=1, rowspan=5, columnspan=1)  # puts the listbox onto the window
car_selector.bind('<Button-1>', onselect)

# variables for storing label text in
str_name = StringVar(value="Brand: ")
str_availability = StringVar(value="Availability: ")
str_year = StringVar(value="Year: ")
str_colour = StringVar(value="Colour: ")
str_price = StringVar(value="Price: $ ")

# labels for all the car details
name = Label(root, textvariable=str_name, padx=10, width=19, anchor="w", background="#E3D2AF").grid(
    row=0, column=2, sticky=W, )

availability = Label(root, textvariable=str_availability, padx=10, width=19, anchor="w", background="#E3D2AF").grid(
    row=1, column=2, sticky=W)

year = Label(root, textvariable=str_year, padx=10, width=19, anchor="w", background="#E3D2AF").grid(
    row=2, column=2, sticky=W)

colour = Label(root, textvariable=str_colour, padx=10, width=19, anchor="w", background="#E3D2AF").grid(
    row=3, column=2, sticky=W)

price = Label(root, textvariable=str_price, padx=10, width=19, anchor="w", background="#E3D2AF").grid(
    row=4, column=2, sticky=W)

#   the button to sell a car
btn_sell_car = Button(root, text="Sell a car", background="#E4E7DC", pady="7", padx="7",
                      command=lambda: sell_car(get_model(car_selector.get(ACTIVE)))).grid(row=6,
                                                                                          column=1,
                                                                                          sticky=N + E + S + W)

#   the button to add users contact details
btn_new_car = Button(root, text="Add new car", background="#E4E7DC",
                     command=lambda: new_car(get_model(car_selector.get(ACTIVE)))).grid(row=6,
                                                                                        column=2,
                                                                                        sticky=N + E + S + W)

#   the button that creates a csv with all cars purchased
btn_cars_purchased = Button(root, text="Cars purchased summary", background="#E4E7DC", pady="7", padx="7",
                            command=lambda: cars_purchased(get_model(car_selector.get(ACTIVE)))).grid(row=7,
                                                                                                      column=1,
                                                                                                      sticky=N + E + S + W)

#   the button that creates a summary of the used car dealership eg. price and amount sold
btn_store_summary = Button(root, text="Store Summary", background="#E4E7DC",
                           command=lambda: store_summary()).grid(row=7,
                                                                 column=2,
                                                                 sticky=N + E + S + W)

#   the button to exit the application
exit_button = Button(root, text="Exit", background="#E4E7DC", pady="7", padx="7",
                     command=lambda: exit_application()).grid(row=8, column=1, sticky=N + E + S + W, columnspan=2)

root.mainloop()
