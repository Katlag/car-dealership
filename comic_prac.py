class Comic:
    #   the count for each comic sold is added to the store summary
    stock_sold_count = 0
    price_total = 0.00

    def __init__(self, name, stock, price):
        self.__name = name
        self.__stock = stock
        self.__price = price
        self.__sold = 0

    def get_stock_sold_count(self):
        """Getter function, gets current stock sold count - returns the amount of comics sold in total"""
        return self.stock_sold_count

    def get_price_total(self):
        """Getter function, gets current price total - returns the total price of comics sold"""
        return self.price_total

    def get_name(self):
        """Getter function, gets current name - returns the comics's name"""
        return self.__name

    def get_stock(self):
        """Getter function, gets current stock - returns the comic's stock"""
        return self.__stock

    def get_price(self):
        """Getter function, gets current price - returns the comics's price"""
        return self.__price

    def get_sold(self):
        """Getter function, gets current sold - returns how many of comics's are sold"""
        return self.__sold

    #   sell one comic function
    def sell_one_comic(self):
        """sells one comic, adds 1 to sold and takes 1 off current stock, and adds price+stock to store summary"""
        if self.__stock < 1:
            messagebox.showwarning('No more comics', 'There are no more comics in stock, please restock to sell more')
            return
        self.__stock -= 1
        self.__sold += 1
        self.stock_sold_count += 1;
        self.price_total += self.__price;
        print(self.stock_sold_count)
        messagebox.showinfo('Sell a comic', 'You have successfully sold a comic')

    #   Sell multiple comic function
    def sell_multiple_comics(self, quantity):
        """sells multiple comics to user, adds x amount to sold and deducts x amount to sold, adds price+stock to store summary"""
        if (self.__stock - quantity) < 0:
            print("Stock can not be less than one")
            return
        self.__stock -= quantity
        self.__sold += quantity
        self.stock_sold_count += quantity
        self.price_total += (self.__price * quantity);
        print(self.stock_sold_count)

    #   restock comic function
    def restock_comic(self, restock_quantity):
        """restocks up to 100 comics for a chosen comic"""

        if (self.__stock + restock_quantity) > 100:
            print("Stock can not be over 100")
            return
        self.__stock += restock_quantity

    #   sets a new name for the comic
    def set_name(self, new_name):
        """Setter function - sets a new name for the comic.

        Args:
            new_name: creates a new name for the comic

        return: updates comic list and changes/creates new name for a comic
        """
        if new_name == "" or new_name is None or type(new_name) is not str:
            print("Name should be a string")
            return
        self.__name = new_name

    #   sets a new stock number for the comic
    def set_stock(self, new_stock):
        """Setter function - sets a new stock number for the comic.

        Args:
            new_stock: creates a new stock number for the comic

        return: updates comic list and changes/creates new stock for the comic
        """
        # catches any invalid values being passed from the UI
        if new_stock is None or type(new_stock) is not int:
            print("Stock must be an integer")
            return
            # simple boundary test - is the stock positive?
        if new_stock < 0:
            print("Stock must be a positive number")
            return
        if new_stock > 100:
            print("stock can not be over 100")
            return
        self.__stock = new_stock

    #   sets a new price for the comic
    def set_price(self, new_price):
        """Setter function - sets a new price number for the comic.

        Args:
            new_price: creates a new price for the comic

        return: updates comic list and changes/creates new price for the comic
        """
        # catches any invalid values being passed from the UI
        if new_price is None or type(new_price) is not float:
            print("Price must be a positive number")
            return
        # simple boundary test - is the price positive?
        if new_price <= 0:
            print("Price must be a positive number")
            return
        self.__price = new_price

    def print_details(self):
        """Prints a summary of the comic's details to the console."""
        print("Title:", self.__name)
        print("Stock:", self.__stock)
        print("Price:", self.__price)
        print("Sold:", self.__sold)


from tkinter import *
from tkinter import messagebox

#  comic list where all comics created, or existing, are stored
comic_list = []
comic_list.append(Comic("Super Dude", 8, 5.99))
comic_list.append(Comic("Lizard Man", 12, 8.99))
comic_list.append(Comic("Water Woman", 3, 10.99))

root = Tk()

root.title("Comic Book Store")
root.configure(background="#DCD8F7", pady="5", padx="7")

main_window_width = 450.0
main_window_height = 540.0

screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

#   positions the GUI in the center of the screen
main_x = screen_width / 2 - main_window_width / 2
main_y = screen_height / 2 - main_window_height / 2

root.geometry("%dx%d+%d+%d" % (main_window_height, main_window_height, main_x, main_y))
root.option_add("*Font", "LucindaGrande 18")

root.resizable(False, False)


def get_comic(cname):
    """Function gets the name of chosen comic from comic list

    Args:
        cname: the comic name taken from the list

    return: gets chosen comic and returns user to function
    """
    #   finds the comic in comic list
    for comic in comic_list:
        if comic.get_name() == cname:
            return comic
    print("Comic not found")  # debug message, will print to console


def update_details():
    """updates details of the comic list and prints to GUI"""

    comic_name = comic_selector.get(ACTIVE)
    current_comic = get_comic(comic_name)
    print(current_comic)

    #   updates details for the comics details listed below
    str_name.set("Title: " + current_comic.get_name())
    str_stock.set("Stock: " + str(current_comic.get_stock()))
    str_price.set("Price: $ " + str(current_comic.get_price()))
    str_sold.set("Sold: " + str(current_comic.get_sold()))


def close_window(window):
    """Closes the window of the function, and returns user to  GUI

    Args:
        window: the current window the user is in
    """
    window.destroy()  # destroys the current window user is in


def sell_multiple_comics(comic):
    """Sells only multiple comics of a chosen comic - user must type in the amount they want to sell

    Args:
        comic: gets the name of comic user wants to sell

    return: if no more comics are in stock, error message comes up and returns you to the GUI
    """
    #   if there are no comics in the comic list, function can not be used anymore
    if len(comic_list) == 0:
        messagebox.showerror("Error", "You have no more comics")
        return

    #   when the stock is less than 1, user will be informed that no comics are left in the stock
    if comic.get_stock() < 1:
        messagebox.showwarning('Sell comics', 'There are no more comics in stock, please restock to sell more')
        return
    close_window

    sell_multiple_comics_window = Toplevel(root)
    sell_multiple_comics_window.title("Sell multiple comics: ")
    sell_multiple_comics_window.option_add("*Font", "LucidaGrande 17")

    sell_multiple_comics_width = 656
    sell_multiple_comics_height = 140

    #   positions the label in the center of the screen
    sell_multiple_comics_x = screen_width / 2 - sell_multiple_comics_width / 2
    sell_multiple_comics_y = screen_height / 2 - sell_multiple_comics_height / 2

    sell_multiple_comics_window.geometry("%dx%d+%d+%d" % (
        sell_multiple_comics_width, sell_multiple_comics_height, sell_multiple_comics_x, sell_multiple_comics_y))

    #   creates and adds labels to text entry areas
    Label(sell_multiple_comics_window,
          text="How many copies of {} would you like to sell?".format(comic.get_name())).grid(row=0, column=0,
                                                                                              columnspan=5,
                                                                                              sticky=N + E + S + W)
    str_new_amountsold = StringVar("")
    str_error_msg = StringVar("")

    Entry(sell_multiple_comics_window, textvariable=str_new_amountsold).grid(row=1, column=0, columnspan=5,
                                                                             sticky=N + E + S + W)

    Label(sell_multiple_comics_window, width=50, textvariable=str_error_msg, fg="red").grid(row=2, column=0,
                                                                                            columnspan=5,
                                                                                            sticky=N + E + S + W)

    Button(sell_multiple_comics_window, text="Cancel", width=10,
           command=lambda: close_window(sell_multiple_comics_window)).grid(
        row=5, column=1, sticky=N + E + S + W)

    Button(sell_multiple_comics_window, text="Sell", width=10,
           command=lambda: sell_multiple_and_close(comic, str_error_msg, sell_multiple_comics_window,
                                                   str_new_amountsold.get())).grid(row=5, column=2,
                                                                                   sticky=N + E + S + W)


def sell_multiple_and_close(comic, error, window, str_new_amountsold):
    """Sells chosen amount of comics and reduces stock, adds to sold

    Args:
        comic: gets the comic user wants to sell
        error: error is shown when user enters an invalid number or boundary
        window: closes the current window the user is in when 'cancel' button is pressed
        str_new_amountsold: adds to the amount of comics sold

    returns: returns user to the current window if an error is made within the function
    """

    #   If any field is blank, no comics can be sold
    if "" in [str_new_amountsold]:
        error.set("No field can be blank")
        return

    #   if quantity is not a number, but a written word, it will not sell
    try:
        quantity = int(str_new_amountsold)
    except ValueError:
        error.set("Please enter a whole, positive number")
        return
    except TypeError as err:
        error.set(err)
        return

    #   If quantity is 0 or a negative number, it will not sell
    if quantity <= 0:
        error.set("Please enter a whole, positive number")
        return
    #   if quantity is 1 user can not sell, as this function only sells multiple comics
    if quantity <= 1:
        error.set("You can only sell multiple comics")
        return
    #   if quantity is greater than 100, and goes over the limit - no comics can be sold
    if quantity > comic.get_stock():
        error.set("Quantity is too large, you currently have {} comics in stock".format(comic.get_stock()))
        return

    #   updates details for sold and stock
    comic.sell_multiple_comics(quantity)
    update_details()
    close_window(window)

    messagebox.showinfo('Sell multiple comics', 'You have successfully sold {} comics'.format(quantity))


def sell_one_comic():
    """sells a single comic to user and increases sold by 1, reduces stock by 1"""

    #   if there are 0 comics in stock, user can not sell anymore unless they restock
    if len(comic_list) == 0:
        messagebox.showerror("Error", "You have no more comics")
        return

    #   updates details for sold and stock
    get_comic(comic_selector.get(ACTIVE)).sell_one_comic()
    update_details()


def restock_comic(comic):
    """User can restock up to 100 comics for a chosen comic in the list

    Args:
        comic: gets name of chosen comic that user wants to restock

    return: if more than 100 comics have been restocked, user will be returned to the GUI and shown error message
    """
    #   if there are no comics in the comic list, function can not be used anymore
    if len(comic_list) == 0:
        messagebox.showerror("Error", "You have no more comics")
        return

    restock_comic_window = Toplevel(root)
    restock_comic_window.title("Restock comic: ")
    restock_comic_window.option_add("*Font", "LucidaGrande 17")

    restock_comic_width = 683
    restock_comic_height = 140

    #   positions the label in the center of the screen
    restock_comic_x = screen_width / 2 - restock_comic_width / 2
    restock_comic_y = screen_height / 2 - restock_comic_height / 2

    restock_comic_window.geometry(
        "%dx%d+%d+%d" % (restock_comic_width, restock_comic_height, restock_comic_x, restock_comic_y))

    if comic.get_stock() >= 100:
        messagebox.showwarning('No comics left', 'You can only restock 100 comics at a time')
        restock_comic_window.destroy()
        return

    #   creates and adds label to text entry areas
    Label(restock_comic_window, width=52,
          text="How many comic's would you like to restock for {}?".format(comic.get_name())).grid(row=0, column=0,
                                                                                                   columnspan=5,
                                                                                                   sticky=N + E + S + W)
    str_new_amountstock = StringVar("")
    str_error_msg = StringVar("")

    Entry(restock_comic_window, textvariable=str_new_amountstock).grid(row=1, column=0, columnspan=5,
                                                                       sticky=N + E + S + W)

    Label(restock_comic_window, textvariable=str_error_msg, fg="red").grid(row=2, column=0, columnspan=5,
                                                                           sticky=N + E + S + W)

    Button(restock_comic_window, text="Cancel", width=10, command=lambda: close_window(restock_comic_window)).grid(
        row=5,
        column=1,
        sticky=N + S + E + W)

    Button(restock_comic_window, text="Restock", width=10, command=lambda: restock_comic_and_close(comic, str_error_msg,
                                                                                                   restock_comic_window,
                                                                                                   str_new_amountstock.get())).grid(
        row=5,
        column=2,
        sticky=N + S + E + W)


def restock_comic_and_close(comic, error, window, str_new_amountstock):
    """restocks 'x' amount of comics, prints it to the list and closes the function

    Args:
        comic: gets the comic user wants to sell from comic list
        error: error message is shown when user enters an invalid number or boundary
        window: closes the current window the user is in when 'cancel' button is pressed
        str_new_amountstock: adds to the current amount of comics in stock

    returns: returns user to the current window if an error is made within the function
    """

    #   If any field is blank, no comics can be restocked
    if "" in [str_new_amountstock]:
        error.set("No field can be blank")
        return

    #   If quantity is not a number, comic will not be restocked
    try:
        restock_quantity = int(str_new_amountstock)
    except ValueError:
        error.set("Please enter a positive, whole number")
        return
    except TypeError as err:
        error.set(err)
        return

    #   If quantity is 0 or a negative number, comic can not be restocked
    if restock_quantity <= 0:
        error.set("Quantity must be above 0")
        return

    #   if quantity is over 100, user can not restock as there is a limit of 100 comics in stock per comic
    if restock_quantity + comic.get_stock() > 100:
        error.set("You can only have up to 100 comics in stock. You currently have {}".format(comic.get_stock()))
        return

    #   updates the stock for the current comic
    comic.restock_comic(restock_quantity)
    update_details()
    close_window(window)

    messagebox.showinfo('Restock', 'You have restocked {} copies'.format(restock_quantity))


def update_comic_selector():
    """updates the comic selector after a change has been made"""

    comic_selector.delete(0, END)
    for comic in comic_list:
        comic_selector.insert(END, comic.get_name())


def create_and_close(new_name, new_stock, new_price, window, error):
    """user can create a new comic which is added to the existing list of comics

    Args:
        new_name: gets the new name of the comic and updates list
        new_stock: gets the new stock number and updates list
        new_price: gets the new price and updates list
        window: closes the current window the user is in when 'cancel' button is pressed
        error: error message is shown when user enters an invalid number or boundary

    returns: returns user to the current window if an error is made within the function
    """

    #   If any field is blank, no comics can be created
    if "" in [new_name, new_stock, new_price]:
        error.set("No field can be blank")
        return

    # check for comics with same name, after cleaning up the input values
    for c in comic_list:
        if c.get_name().strip().lower() == new_name.strip().lower():
            error.set("You can't have 2 comics with the same name")
            return

    #   checks to make sure stock is a valid number
    try:
        new_stock = int(new_stock)
    except ValueError:
        error.set("Stock must be a positive, whole number")
        return
    if new_stock < 0:
        error.set("Stock must be a positive number")  # stock can not be less than 0
        return
    if new_stock > 100:
        error.set("Stock must be 100 or less")  # stock can not be over 100
        return

    #   checks to make sure the price is a valid number as well
    try:
        new_price = float(new_price)
    except ValueError:
        error.set("Price must be a positive, whole number")
        return
    if new_price == 0:
        error.set("The comic can't have a price of $0.00")  # price must have a set number above 0
        return
    if new_price <= 0:
        error.set("Price must be a positive number")  # price can not be less than 0 eg. a negative number
        return

    #   details are updated for the new comic
    comic = Comic(new_name, new_stock, new_price)
    comic_list.append(comic)
    update_comic_selector()
    update_details()
    close_window(window)

    messagebox.showinfo('New comic', 'You have created {}'.format(comic.get_name()))


def new_comic():
    """opens a label where user can write in a name, price, a set amount of stock for a new comic"""

    new_comic_window = Toplevel(root)
    new_comic_window.title("Create new comic")
    new_comic_window.option_add("*Font", "LucidaGrande 17")

    new_comic_width = 470
    new_comic_height = 175

    #   positions the label in the center of the screen
    new_comic_x = screen_width / 2 - new_comic_width / 2
    new_comic_y = screen_height / 2 - new_comic_height / 2

    new_comic_window.geometry("%dx%d+%d+%d" % (new_comic_width, new_comic_height, new_comic_x, new_comic_y))

    #   creates and adds labels to text entry areas
    Label(new_comic_window, text="Title:").grid(row=0, column=0, sticky=E)
    Label(new_comic_window, text="Stock:").grid(row=1, column=0, sticky=E)
    Label(new_comic_window, text="Price: $").grid(row=2, column=0, sticky=E)

    str_new_name = StringVar("")
    str_new_stock = StringVar("")
    str_new_price = StringVar("")
    str_error_msg = StringVar("")

    Entry(new_comic_window, textvariable=str_new_name).grid(row=0, column=1, sticky=N + E + S + W)
    Entry(new_comic_window, textvariable=str_new_stock).grid(row=1, column=1, sticky=N + E + S + W)
    Entry(new_comic_window, textvariable=str_new_price).grid(row=2, column=1, sticky=N + E + S + W)

    Label(new_comic_window, width=35, textvariable=str_error_msg, fg="red").grid(row=4, column=0, columnspan=2,
                                                                                 sticky=N + E + S + W)

    Button(new_comic_window, text="Cancel ", width=7, command=lambda: close_window(new_comic_window)).grid(row=5,
                                                                                                           column=0,
                                                                                                           sticky=E)
    Button(new_comic_window, text="Create", width=7, command=lambda: create_and_close(str_new_name.get(),
                                                                                      str_new_stock.get(),
                                                                                      str_new_price.get(),
                                                                                      new_comic_window,
                                                                                      str_error_msg)).grid(row=5,
                                                                                                           column=1,
                                                                                                           sticky=W)


def save_and_close(comic, new_name, new_price, window, error):
    """Saves what you've put in edit details, prints to the listbox and closes the function

    Args:
        comic: gets the comic user wants to sell from comic list
        new_name: gets the new name of the comic and updates comics list
        new_price: gets the new price of the comic and updates comic price
        window: closes the current window user is in when user presses 'cancel' or 'save' button
        error: error message is shown when user enters an invalid number or boundary

    returns: returns user to the current window if an error is made within the function
    """
    #   If any field is blank, no comics can be edited
    if "" in [new_name, new_price]:
        error.set("No field can be blank")
        return

    #   if price is not negative or is not a whole number
    try:
        float_price = float(new_price)
        if float_price >= 0:
            comic.set_price(float_price)
            update_details()
        else:
            error.set("Price must be a positive number")
            return
    except ValueError:
        error.set("Price must be a positive, whole number")
        return

    #   if price is set to 0, user must have a set price for a comic that is above 0
    try:
        float_price = float(new_price)
        if float_price <= 0:
            error.set("The comic can't have a price of $0.00")
            return
    except ValueError:
        error.set("Price must be a number")
        return

    #   details are updated for the edited comic
    comic.set_name(new_name)
    update_comic_selector()
    update_details()
    close_window(window)

    messagebox.showinfo("Edited", "You have edited {}".format(comic.get_name()))


def edit_details():
    """opens a label where user can edit the comics, name and price"""

    #   if there are no comics in the comic list, function can not be used anymore
    if len(comic_list) == 0:
        messagebox.showerror("Error", "You have no more comics")
        return

    edit_window = Toplevel(root)
    edit_window.title("Edit comic details")
    edit_window.option_add("*Font", "LucidaGrande 17")

    edit_details_width = 400
    edit_details_height = 145

    #   positions the label in the center of the screen
    edit_details_x = screen_width / 2 - edit_details_width / 2
    edit_details_y = screen_height / 2 - edit_details_height / 2

    edit_window.geometry("%dx%d+%d+%d" % (edit_details_width, edit_details_height, edit_details_x, edit_details_y))

    #   creates and adds labels to text entry areas
    Label(edit_window, text="Title: ").grid(row=0, column=0, sticky=E)
    Label(edit_window, text="Price: $").grid(row=2, column=0, sticky=E)

    comic_name = comic_selector.get(ACTIVE)
    current_comic = get_comic(comic_name)

    str_current_name = StringVar(edit_window, current_comic.get_name())
    str_current_price = StringVar(edit_window, str(current_comic.get_price()))
    str_error_msg = StringVar("")

    Entry(edit_window, textvariable=str_current_name).grid(row=0, column=1, sticky=E + W)
    Entry(edit_window, textvariable=str_current_price).grid(row=2, column=1, sticky=E + W)

    Label(edit_window, textvariable=str_error_msg, fg="red", width=30).grid(row=4, column=0, columnspan=2,
                                                                            sticky=N + E + S + W)

    Button(edit_window, text="Cancel", width=7, command=lambda: close_window(edit_window)).grid(row=5, column=0,
                                                                                                sticky=E)
    Button(edit_window, text="Save", width=7, command=lambda: save_and_close(current_comic,
                                                                             str_current_name.get(),
                                                                             str_current_price.get(),
                                                                             edit_window,
                                                                             str_error_msg,
                                                                             )).grid(row=5, column=1, sticky=W)


def delete_comic(comic):
    """Deletes chosen comic from the list

    Args:
        comic: gets the comic user wants to sell from comic list

    return: returns user to GUI, if user agrees to delete comic and updates the comic
    """
    #   if there are no comics in the comic list, function can not be used anymore
    if len(comic_list) == 0:
        messagebox.showerror("Error", "You have no more comics")
        return

    #   asks user before they delete the comic with a yes or no answer type question
    MsgBox = messagebox.askquestion('Delete comic', 'Are you sure you want to delete {}'.format(comic.get_name()),
                                    icon='warning')
    if MsgBox == 'yes':
        comic_list.remove(comic)  # removes comic from comic list
        del comic
        update_comic_selector()
    else:
        messagebox.showinfo('Return',
                            'You will now return to the application')  # returns user to application without deleting comic
    return


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


def store_summary():
    """displays amount of comics sold in total and the price accumulated from those comics sold"""

    #   positions store summary in the center of the page
    width = 300.0
    height = 110.0
    x = screen_width / 2 - width / 2
    y = screen_height / 2 - height / 2

    store_window = Toplevel(root)
    store_window.title("Store summary")
    store_window.option_add("*Font", "LucidaGrande 17")
    store_window.geometry("%dx%d+%d+%d" % (width, height, x, y))

    price_count = 0.00
    comic_count = 0

    #   gets the total amount of comics sold and price accumulated and adds it to the store summary
    for c in comic_list:
        price_count += c.get_price_total()
        comic_count += c.get_stock_sold_count()

    #   total amounts are placed in a small box
    string_total_sold = f'Total Comics Sold: {comic_count}'
    string_total_price = f'Store balance: $ {price_count}'

    Label(store_window, text=string_total_sold).grid(row=0, column=0, sticky=W)
    Label(store_window, text=string_total_price).grid(row=1, column=0, sticky=W)

    Button(store_window, text="Ok", width=10, command=lambda: close_window(store_window)).grid(row=6, column=0,
                                                                                               sticky=S + W)


def onselect(ebt):
    """Updates comic list when you press on a comic name

    Args:
        ebt: updates the comic automatically - keeps track of update patterns
    """

    #   comic details update after 200 milliseconds (0.2 seconds) when clicked on
    root.after(200, update_details)


comic_selector = Listbox(root, height=12, width=20, background="#F0F0F5")  # creates the listbox
update_comic_selector()
comic_selector.grid(row=0, column=1, rowspan=5, columnspan=1)  # puts the listbox onto the window
comic_selector.bind('<Button-1>', onselect)

# variables for storing label text in
str_name = StringVar(value="Title: ")
str_stock = StringVar(value="Stock: ")
str_price = StringVar(value="Price: $ ")
str_sold = StringVar(value="Sold: ")

# labels for all the comic details
comic_name = Label(root, textvariable=str_name, padx=10, width=17, height="2", anchor="w", background="#DCD8F7").grid(
    row=0,
    column=2,
    sticky=W)
stock = Label(root, textvariable=str_stock, padx=10, width=17, height="2", anchor="w", background="#DCD8F7").grid(row=1,
                                                                                                                  column=2,
                                                                                                                  sticky=W)
price = Label(root, textvariable=str_price, padx=10, width=17, height="2", anchor="w", background="#DCD8F7").grid(row=2,
                                                                                                                  column=2,
                                                                                                                  sticky=W)
sold = Label(root, textvariable=str_sold, padx=10, width=17, height="2", anchor="w", background="#DCD8F7").grid(row=3,
                                                                                                                column=2,
                                                                                                                sticky=W)
#   All buttons displayed on the interface
#   the button to sell a single comic
btn_sell_one_comic = Button(root, text="Sell a comic", background="#DBECF5",
                            command=lambda: sell_one_comic()).grid(row=5,
                                                                   column=1,
                                                                   sticky=N + E + S + W)
#   the button to sell more than one comic
btn_sell_multiple_comics = Button(root, text="Sell multiple comics", background="#DBECF5",
                                  command=lambda: sell_multiple_comics(get_comic(comic_selector.get(ACTIVE)))).grid(
    row=5,
    column=2,
    sticky=N + E + S + W)

#   the button to restock a comic
btn_restock_comic = Button(root, text="Restock comic", background="#DBECF5",
                           command=lambda: restock_comic(get_comic(comic_selector.get(ACTIVE)))).grid(row=6,
                                                                                                      column=1,
                                                                                                      sticky=N + E + S + W)

#   the button to edit the details of a comic
btn_edit_details = Button(root, text="Edit details", background="#DBECF5", command=lambda: edit_details()).grid(row=6,
                                                                                                                column=2,
                                                                                                                sticky=N + E + S + W)
#   the button to create a new comic
btn_new_comic = Button(root, text="Create new comic", background="#DBECF5", command=lambda: new_comic()).grid(row=7,
                                                                                                              column=1,
                                                                                                              sticky=N + E + S + W)

#   the button to delete a comic
btn_delete_comic = Button(root, text="Delete comic", background="#DBECF5", command=lambda: delete_comic(get_comic(
    comic_selector.get(ACTIVE)))).grid(row=7, column=2, sticky=N + E + S + W)

#   the button that creates a summary of the comic eg. price and stock number
btn_store_summary = Button(root, text="Store summary", background="#DBECF5", command=lambda: store_summary()).grid(
    row=8,
    column=1,
    sticky=N + E + S + W)

#   the button to exit the application
exit_button = Button(root, text="Exit", background="#DBECF5", command=lambda: exit_application()).grid(row=8, column=2,
                                                                                                       sticky=N + E + S + W)

root.mainloop()
