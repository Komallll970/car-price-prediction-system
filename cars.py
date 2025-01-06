import pandas as pd
import numpy as np
import pickle as pk
import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Load the model
model = pk.load(open('model.pkl', 'rb'))
# Load data
cars_data = pd.read_csv('Cardetails.csv')

# Extract car brand names
def get_brand_name(car_name):
    return car_name.split(' ')[0].strip()

cars_data['name'] = cars_data['name'].apply(get_brand_name)



# Create the main window
root = tk.Tk()
root.title("Car Price Prediction Model")
root.state('zoomed')

# Load and set background image
background_image = Image.open("C:/Users/KOMAL/Desktop/car-price-predictor/bgcar.png")  # Specify the path to your background image
background_photo = ImageTk.PhotoImage(background_image)
background_label = tk.Label(root, image=background_photo)
background_label.place(relwidth=1, relheight=1)

tk.Label(root, text="CAR PRICE PREDICTION MODEL", fg="blue", font="Arial 26 bold").place(x=350, y=0)


# Variables
name_var = tk.StringVar()
year_var = tk.IntVar(value=2024)
km_driven_var = tk.IntVar(value=100)
fuel_var = tk.StringVar()
seller_type_var = tk.StringVar()
transmission_var = tk.StringVar()
owner_var = tk.StringVar()
mileage_var = tk.DoubleVar(value=10.0)
engine_var = tk.IntVar(value=700)
max_power_var = tk.DoubleVar(value=0)  # Ensure consistency in data types (float for max_power)
seats_var = tk.IntVar(value=4)

# Function for prediction
def predict_price():
    try:
        input_data_model = pd.DataFrame(
            [[name_var.get(), year_var.get(), km_driven_var.get(), fuel_var.get(), seller_type_var.get(),
              transmission_var.get(), owner_var.get(), mileage_var.get(), engine_var.get(), max_power_var.get(),
              seats_var.get()]],
            columns=['name', 'year', 'km_driven', 'fuel', 'seller_type', 'transmission', 'owner', 'mileage', 'engine',
                     'max_power', 'seats'])

        # Encode categorical features
        encoding_dict = {
            'owner': {'First Owner': 1, 'Second Owner': 2, 'Third Owner': 3, 'Fourth & Above Owner': 4, 'Test Drive Car': 5},
            'fuel': {'Diesel': 1, 'Petrol': 2, 'LPG': 3, 'CNG': 4},
            'seller_type': {'Individual': 1, 'Dealer': 2, 'Trustmark Dealer': 3},
            'transmission': {'Manual': 1, 'Automatic': 2},
            'name': {brand: idx+1 for idx, brand in enumerate(cars_data['name'].unique())}
        }
        
        for col, mapping in encoding_dict.items():
            input_data_model[col] = input_data_model[col].map(mapping)
        
        # Convert all inputs to float as expected by most models
        input_data_model = input_data_model.astype(float)

        car_price = model.predict(input_data_model)
        messagebox.showinfo("Predicted Price", f"Predicted Price for Car: Rs. {car_price[0]:,.2f}")
    except Exception as e:
        messagebox.showerror("Error", str(e))

# Function to show analysis graphs with new data
def show_analysis():
    try:
        fig, axs = plt.subplots(2, 2, figsize=(6, 4))
        fig.suptitle('Car Data Analysis',fontsize=16, fontweight='bold')

        transmission_counts = cars_data['transmission'].value_counts()
        axs[0, 0].bar(transmission_counts.index, transmission_counts.values, color='skyblue')
        axs[0, 0].set_title('Transmission Type Analysis')
        axs[0, 0].set_xlabel('Transmission')
        axs[0, 0].set_ylabel('Count')

        #brand_km_data = cars_data.groupby('name')['km_driven'].mean().sort_values(ascending=False).head(10)
        #axs[0, 1].bar(brand_km_data.index, brand_km_data.values, color='orange')
        #axs[0, 1].set_title('Top 10 Car Brands by Average KM Driven')
        #axs[0, 1].set_xlabel('Car Brand')
        #axs[0, 1].set_ylabel('Average KM Driven')
        
        
        # Graph 2: Top 10 Car Brands by Average Selling Price
        brand_price_data = cars_data.groupby('name')['selling_price'].mean().sort_values(ascending=False).head(5)
        axs[0, 1].bar(brand_price_data.index, brand_price_data.values, color='green')
        axs[0, 1].set_title('Top 5 Car Brands by Average Selling Price')
        axs[0, 1].set_xlabel('Car Brand')
        axs[0, 1].set_ylabel('Average Selling Price (Rs.)')


    

        fuel_counts = cars_data['fuel'].value_counts()
        axs[1, 0].pie(fuel_counts.values, labels=fuel_counts.index, autopct='%1.1f%%', colors=['#ff9999', '#66b3ff', '#99ff99', '#ffcc99'])
        axs[1, 0].set_title('Fuel Type Distribution')

        brand_km_data = cars_data.groupby('name')['km_driven'].mean().sort_values(ascending=False).head()
        axs[1, 1].bar(brand_km_data.index, brand_km_data.values, color='orange')
        axs[1, 1].set_title('Top 5 Car Brands by Average KM Driven')
        axs[1, 1].set_xlabel('Car Brand')
        axs[1, 1].set_ylabel('Average KM Driven')

        plt.tight_layout()
        plt.show()
    except Exception as e:
        messagebox.showerror("Error", str(e))

# Input form layout on the left
tk.Label(root, text="Car Brand", font="Arial 12 bold").place(x=50, y=120)
brand_dropdown = ttk.Combobox(root, textvariable=name_var, values=list(cars_data['name'].unique()))
brand_dropdown.place(x=250, y=120)

tk.Label(root, text="Year", font="Arial 12 bold").place(x=50, y=160)
tk.Spinbox(root, from_=1994, to=2024, textvariable=year_var).place(x=250, y=160)

tk.Label(root, text="KM Driven", font="Arial 12 bold").place(x=50, y=200)
tk.Spinbox(root, from_=100, to=200000, textvariable=km_driven_var).place(x=250, y=200)

tk.Label(root, text="Fuel Type", font="Arial 12 bold").place(x=50, y=240)
fuel_dropdown = ttk.Combobox(root, textvariable=fuel_var, values=list(cars_data['fuel'].unique()))
fuel_dropdown.place(x=250, y=240)

tk.Label(root, text="Seller Type", font="Arial 12 bold").place(x=50, y=280)
seller_dropdown = ttk.Combobox(root, textvariable=seller_type_var, values=list(cars_data['seller_type'].unique()))
seller_dropdown.place(x=250, y=280)

tk.Label(root, text="Transmission", font="Arial 12 bold").place(x=50, y=320)
transmission_dropdown = ttk.Combobox(root, textvariable=transmission_var, values=list(cars_data['transmission'].unique()))
transmission_dropdown.place(x=250, y=320)

tk.Label(root, text='Owner', font='Arial 12 bold').place(x=50, y=360)
owner_dropdown = ttk.Combobox(root, textvariable=owner_var, values=list(cars_data['owner'].unique()))
owner_dropdown.place(x=250, y=360)

tk.Label(root, text='Mileage', font='Arial 12 bold').place(x=50, y=400)
tk.Spinbox(root, from_=10, to=40, textvariable=mileage_var).place(x=250, y=400)

tk.Label(root, text='Engine CC', font='Arial 12 bold').place(x=50, y=440)
tk.Spinbox(root, from_=700, to=5000, textvariable=engine_var).place(x=250, y=440)

tk.Label(root, text='Max Power', font='Arial 12 bold').place(x=50, y=480)
tk.Spinbox(root, from_=0, to=200, textvariable=max_power_var).place(x=250, y=480)

tk.Label(root, text='Seats', font='Arial 12 bold').place(x=50, y=520)
tk.Spinbox(root, from_=2, to=7, textvariable=seats_var).place(x=250, y=520)

# Predict and Analysis Buttons
tk.Button(root, text='Predict', command=predict_price, font='Arial 12 bold', bg='#4CAF50', fg='white').place(x=50, y=580)
tk.Button(root, text='Analysis', command=show_analysis, font='Arial 12 bold', bg='#2196F3', fg='white').place(x=150, y=580)

# Run the main application loop
root.mainloop()



