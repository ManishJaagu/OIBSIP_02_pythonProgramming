''' Author- Jagu Manish || Python Programming Internship at Oasis Infobyte

------------------ TASK 2  - BMI CALCULATOR -----------------------
Project Description: (Advanced)
For Beginners: Create a command-line BMI calculator in Python. Prompt users for their weight (in kilograms) and height (in meters). Calculate the BMI and classify it into categories (e.g., underweight, normal, overweight) based on predefined ranges. Display the BMI result and category to the user.
For Advanced: Develop a graphical BMI calculator with a user-friendly interface (GUI) using libraries like Tkinter or PyQt. Allow users to input weight and height, calculate BMI, and visualize the result. Enable data storage for multiple users, historical data viewing, and BMI trend analysis through statistics and graphs.
Key Concepts and Challenges:
1. User Input Validation: Ensure valid user inputs within reasonable ranges and handle errors gracefully.
2. BMI Calculation: Accurately implement the BMI formula.
3. Categorization: Classify BMI values into health categories based on predefined ranges.
4. GUI Design (for Advanced): Create an intuitive interface with labels, input fields, and result displays.
5. Data Storage (for Advanced): Implement user data storage, possibly using file storage or a small database.
6. Data Visualization (for Advanced): Visualize historical BMI data with graphs or charts.
7. Error Handling (for Advanced): Address potential issues with data storage or retrieval.
8. User Experience (for Advanced): Ensure a responsive and user-friendly GUI with clear instructions and feedback.

IDE used: Pycharm
Tip: Use VS Code for better performance.

information on BMI: https://www.cdc.gov/healthyweight/assessing/bmi/adult_bmi/index.html
'''
import tkinter as tk
from tkinter import messagebox, simpledialog
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


# Initialize the CSV file for storing data if it doesn't exist
def initialize_data_file():
    try:
        pd.read_csv('bmi_data.csv')
    except FileNotFoundError:
        df = pd.DataFrame(columns=['Weight', 'Height', 'Measurement_Type', 'BMI', 'Weight_Status'])
        df.to_csv('bmi_data.csv', index=False)


initialize_data_file()


# Calculate BMI and determine weight status
def calculate_bmi():
    global weight_status
    try:
        weight = float(weight_entry.get())
        height = float(height_entry.get())
        measurement_type = measurement_var.get()

        if weight <= 0 or height <= 0:
            raise ValueError("Weight and height must be positive numbers.")

        if measurement_type == 'k':
            bmi = weight / (height * height)
        elif measurement_type == 'p':
            bmi = (weight / (height * height)) * 703
        else:
            raise ValueError("Invalid measurement type selected.")

        bmi = round(bmi, 2)

        if bmi < 18.5:
            weight_status = "Underweight"
        elif 18.5 <= bmi <= 24.9:
            weight_status = "Healthy Weight"
        elif 25.0 <= bmi < 29.9:
            weight_status = "Overweight"
        else:
            weight_status = "Obesity"

        result_label.config(text=f"Your BMI is: {bmi}\nWeight Status: {weight_status}")

        # Save data to CSV
        data = {
            'Weight': weight,
            'Height': height,
            'Measurement_Type': measurement_type,
            'BMI': bmi,
            'Weight_Status': weight_status
        }
        df = pd.DataFrame([data])
        df.to_csv('bmi_data.csv', mode='a', header=False, index=False)

    except ValueError as e:
        messagebox.showerror("Input Error", str(e))


# Display historical BMI data and trends
def view_historical_data():
    df = pd.read_csv('bmi_data.csv')
    if df.empty:
        messagebox.showinfo("No Data", "No historical data available.")
        return

    top = tk.Toplevel()
    top.title("Historical BMI Data")

    text = tk.Text(top, width=60, height=20)
    text.pack()
    text.insert(tk.END, df.to_string(index=False))

    # Plotting BMI trend
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(df.index, df['BMI'], marker='o', linestyle='-', color='b')
    ax.set_title('BMI Trend')
    ax.set_xlabel('Record Number')
    ax.set_ylabel('BMI')
    ax.grid(True)

    canvas = FigureCanvasTkAgg(fig, master=top)
    canvas.draw()
    canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)


# Create the main window
root = tk.Tk()
root.title("BMI Calculator")

# Create and place widgets
tk.Label(root, text="Enter your weight:").grid(row=0, column=0, padx=10, pady=10, sticky='e')
weight_entry = tk.Entry(root)
weight_entry.grid(row=0, column=1, padx=10, pady=10)

tk.Label(root, text="Enter your height:").grid(row=1, column=0, padx=10, pady=10, sticky='e')
height_entry = tk.Entry(root)
height_entry.grid(row=1, column=1, padx=10, pady=10)

tk.Label(root, text="Measurement Type:").grid(row=2, column=0, padx=10, pady=10, sticky='e')
measurement_var = tk.StringVar()
tk.Radiobutton(root, text='Kilograms (kg)', variable=measurement_var, value='k').grid(row=2, column=1, padx=10, pady=5,
                                                                                      sticky='w')
tk.Radiobutton(root, text='Pounds (lbs)', variable=measurement_var, value='p').grid(row=2, column=1, padx=10, pady=5,
                                                                                    sticky='e')

calculate_button = tk.Button(root, text="Calculate BMI", command=calculate_bmi)
calculate_button.grid(row=3, column=0, columnspan=2, padx=10, pady=10)

result_label = tk.Label(root, text="", font=("Helvetica", 12))
result_label.grid(row=4, column=0, columnspan=2, padx=10, pady=10)

view_button = tk.Button(root, text="View Historical Data", command=view_historical_data)
view_button.grid(row=5, column=0, columnspan=2, padx=10, pady=10)

# Run the application
root.mainloop()
