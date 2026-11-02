import tkinter as tk
from tkinter import ttk, messagebox
import json
from pathlib import Path

# JSON file will be created in the project folder
DATA_FILE = Path(__file__).resolve().parent / "vehicles.json"


# Load saved vehicle records
def load_vehicles():
    if DATA_FILE.exists():
        try:
            with open(DATA_FILE, "r", encoding="utf-8") as file:
                data = json.load(file)

            if not isinstance(data, list):
                raise ValueError("Invalid vehicle data")

            for vehicle in data:
                if not all(
                    key in vehicle
                    for key in ("registration", "owner", "type")
                ):
                    raise ValueError("Invalid vehicle record")

            return sorted(
                data,
                key=lambda v: v["registration"].upper()
            )

        except (json.JSONDecodeError, ValueError, OSError) as error:
            messagebox.showerror(
                "File Error",
                f"Could not load vehicle records:\n{error}"
            )
            return []

    # Initial sample records
    return [
        {"registration": "PB10AB1234", "owner": "Rahul", "type": "Car"},
        {"registration": "PB10CD2345", "owner": "Aman", "type": "Bike"},
        {"registration": "PB10EF3456", "owner": "Surabhi", "type": "Scooter"},
        {"registration": "PB10GH4567", "owner": "Priya", "type": "Car"},
        {"registration": "PB10JK5678", "owner": "Neha", "type": "Bike"}
    ]


vehicles = load_vehicles()


# Save records permanently
def save_vehicles():
    try:
        with open(DATA_FILE, "w", encoding="utf-8") as file:
            json.dump(vehicles, file, indent=4)

        return True

    except OSError as error:
        messagebox.showerror(
            "Save Error",
            f"Could not save vehicle records:\n{error}"
        )
        return False


# Binary Search Algorithm
def binary_search(target):
    low = 0
    high = len(vehicles) - 1

    while low <= high:
        mid = (low + high) // 2
        current = vehicles[mid]["registration"].upper()

        if current == target:
            return vehicles[mid]

        elif current < target:
            low = mid + 1

        else:
            high = mid - 1

    return None


# Display vehicle records
def display_vehicles(records=None):
    for item in table.get_children():
        table.delete(item)

    if records is None:
        records = vehicles

    for vehicle in records:
        table.insert(
            "",
            "end",
            values=(
                vehicle["registration"],
                vehicle["owner"],
                vehicle["type"]
            )
        )


# Search vehicle
def search_vehicle():
    target = search_entry.get().strip().upper()

    if not target:
        messagebox.showwarning(
            "Input Required",
            "Please enter a registration number."
        )
        return

    result = binary_search(target)

    if result:
        display_vehicles([result])

        messagebox.showinfo(
            "Vehicle Found",
            f"Registration: {result['registration']}\n"
            f"Owner: {result['owner']}\n"
            f"Vehicle Type: {result['type']}"
        )

    else:
        display_vehicles([])

        messagebox.showinfo(
            "Not Found",
            "Vehicle record not found."
        )


# Show all records
def show_all():
    search_entry.delete(0, tk.END)
    display_vehicles()


# Add new vehicle
def add_vehicle():
    registration = reg_entry.get().strip().upper()
    owner = owner_entry.get().strip()
    vehicle_type = type_combo.get().strip()

    if not registration or not owner or not vehicle_type:
        messagebox.showwarning(
            "Missing Information",
            "Please fill in all fields."
        )
        return

    if binary_search(registration):
        messagebox.showerror(
            "Duplicate Record",
            "This registration number already exists."
        )
        return

    new_vehicle = {
        "registration": registration,
        "owner": owner,
        "type": vehicle_type
    }

    vehicles.append(new_vehicle)

    # Keep records sorted for Binary Search
    vehicles.sort(
        key=lambda v: v["registration"].upper()
    )

    # Save before confirming success
    if not save_vehicles():
        vehicles.remove(new_vehicle)
        vehicles.sort(
            key=lambda v: v["registration"].upper()
        )
        return

    display_vehicles()

    reg_entry.delete(0, tk.END)
    owner_entry.delete(0, tk.END)
    type_combo.set("")

    messagebox.showinfo(
        "Success",
        "Vehicle added and saved permanently!"
    )


# Main application window
root = tk.Tk()
root.title("Vehicle Registration Search System")
root.geometry("850x650")
root.configure(bg="#eef2f7")
root.resizable(False, False)

# Header
header = tk.Frame(root, bg="#17365d", height=90)
header.pack(fill="x")

tk.Label(
    header,
    text="VEHICLE REGISTRATION SYSTEM",
    font=("Arial", 21, "bold"),
    bg="#17365d",
    fg="white"
).pack(pady=(18, 4))

tk.Label(
    header,
    text="DAA Project | Binary Search Algorithm",
    font=("Arial", 11),
    bg="#17365d",
    fg="#dbeafe"
).pack()

# Search section
search_frame = tk.LabelFrame(
    root,
    text=" Search Vehicle ",
    font=("Arial", 12, "bold"),
    bg="#eef2f7",
    padx=15,
    pady=15
)
search_frame.pack(fill="x", padx=25, pady=18)

search_entry = ttk.Entry(
    search_frame,
    width=35,
    font=("Arial", 12)
)
search_entry.grid(row=0, column=0, padx=8, pady=5)

ttk.Button(
    search_frame,
    text="Search",
    command=search_vehicle
).grid(row=0, column=1, padx=8)

ttk.Button(
    search_frame,
    text="Show All",
    command=show_all
).grid(row=0, column=2, padx=8)

# Add vehicle section
add_frame = tk.LabelFrame(
    root,
    text=" Add New Vehicle ",
    font=("Arial", 12, "bold"),
    bg="#eef2f7",
    padx=15,
    pady=12
)
add_frame.pack(fill="x", padx=25, pady=5)

tk.Label(
    add_frame,
    text="Registration No.",
    bg="#eef2f7"
).grid(row=0, column=0, padx=8, pady=5)

reg_entry = ttk.Entry(add_frame, width=22)
reg_entry.grid(row=1, column=0, padx=8, pady=5)

tk.Label(
    add_frame,
    text="Owner Name",
    bg="#eef2f7"
).grid(row=0, column=1, padx=8, pady=5)

owner_entry = ttk.Entry(add_frame, width=22)
owner_entry.grid(row=1, column=1, padx=8, pady=5)

tk.Label(
    add_frame,
    text="Vehicle Type",
    bg="#eef2f7"
).grid(row=0, column=2, padx=8, pady=5)

type_combo = ttk.Combobox(
    add_frame,
    values=["Car", "Bike", "Scooter", "Truck", "Bus"],
    width=17,
    state="readonly"
)
type_combo.grid(row=1, column=2, padx=8, pady=5)

ttk.Button(
    add_frame,
    text="Add Vehicle",
    command=add_vehicle
).grid(row=1, column=3, padx=8)

# Vehicle records table
table_frame = tk.LabelFrame(
    root,
    text=" Vehicle Records ",
    font=("Arial", 12, "bold"),
    bg="#eef2f7",
    padx=10,
    pady=10
)
table_frame.pack(fill="both", expand=True, padx=25, pady=15)

columns = ("registration", "owner", "type")

table = ttk.Treeview(
    table_frame,
    columns=columns,
    show="headings",
    height=9
)

table.heading("registration", text="Registration Number")
table.heading("owner", text="Owner Name")
table.heading("type", text="Vehicle Type")

table.column("registration", width=250, anchor="center")
table.column("owner", width=200, anchor="center")
table.column("type", width=200, anchor="center")

table.pack(fill="both", expand=True)

# Footer
tk.Label(
    root,
    text="Academic Demonstration Project | Python + Binary Search",
    font=("Arial", 9),
    bg="#eef2f7",
    fg="#555555"
).pack(pady=(0, 10))

# Display loaded records
display_vehicles()

root.mainloop()