"""
Purpose:
--------
This script reads Lake Mead manager session data from an Excel file and creates
a scatter plot showing the ratio of Lake Mead storage to the chosen
protection storage volume for each session.

Each dot represents one modeled year within a manager session.
    • x-axis: Chosen protection storage volume (MAF)
    • y-axis: Storage-to-protection ratio (Storage / Protection Volume)

Dots are:
    • Blue by default.
    • Red if the Reclamation user chose to sell water.
    • Circle by default.
    • Diamond if the ratio of storage to protection storage is below 1.0.


"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path


# -----------------------------
# Locate the input Excel file
# -----------------------------

# Get the path of this Python script
code_file = Path(__file__)

# Create the path to the Excel file located in the same folder
input_file = code_file.parent / 'ManagerSessionsData.xlsx'


# -----------------------------
# Read the Excel file
# -----------------------------

# Read the Excel workbook into a pandas DataFrame
ensemble = pd.read_excel(input_file)

# Convert all data columns to numeric values
# Any non-numeric entries become NaN.
ensemble.iloc[:, 3:] = ensemble.iloc[:, 3:].apply(pd.to_numeric, errors="coerce")


# -----------------------------
# Organize the data
# -----------------------------

# Each manager session occupies three rows in the spreadsheet
session_data = 3

# Find the first row containing data in the first simulation column
first_data_row = ensemble.iloc[:, 3].first_valid_index()

# Remove any rows before the first data row and reset the index
df = ensemble.iloc[first_data_row:].copy().reset_index(drop=True)

# Total number of rows remaining
length = len(df)


# -----------------------------
# Create empty lists for storing data
# -----------------------------

# Stores simulated storage volumes for every session
all_years = []

# Stores simulated elevations for every session
all_elevs = []

# Stores the protection storage volume selected for each session
protect_storages = []

# Stores the protection elevation selected for each session
protect_elevs = []

# Stores the session names (dates)
session_names = []


# -----------------------------
# Read each manager session
# -----------------------------

# Loop through the spreadsheet three rows at a time
for first in range(0, length, session_data):

    # Select the three rows belonging to one manager session
    sessions = df.iloc[first:first + session_data, 3:]

    # First row contains storage values
    years = sessions.iloc[0].values

    # Save storage values
    all_years.append(years)

    # Third row contains elevation values
    elevs = sessions.iloc[2].values

    # Save elevation values
    all_elevs.append(elevs)

    # Column 2 contains the protection storage/elevation values
    protect_col = df.iloc[first:first + session_data, 2]

    # First row = protection storage volume
    protect_storage = protect_col.iloc[0]

    # Save protection storage
    protect_storages.append(protect_storage)

    # Third row = protection elevation
    protect_elevation = protect_col.iloc[2]

    # Save protection elevation
    protect_elevs.append(protect_elevation)

    # First column contains the manager session name/date
    session_name = df.iloc[first, 0]

    # Save the session name
    session_names.append(session_name)


# -----------------------------
# Convert lists to NumPy arrays
# -----------------------------

# Convert storage values to NumPy array
all_storages = np.array(all_years)

# Convert elevation values to NumPy array
all_elevs = np.array(all_elevs)

# Convert protection storage values to float array
protect_storages = np.array(protect_storages, dtype=float)

# Convert protection elevations to float array
protect_elevs = np.array(protect_elevs, dtype=float)


# -----------------------------
# Calculate storage/protection ratio
# -----------------------------

# Empty list to store the dimensionless ratios
dimensionless_list = []

# Loop through every session
for idx, ps in enumerate(protect_storages):

    # If protection storage is zero or missing, fill with NaNs
    if ps == 0 or np.isnan(ps):
        dimensionless = np.full(all_storages[idx].shape, np.nan)

    # Otherwise compute storage/protection ratio
    else:
        dimensionless = all_storages[idx] / ps

    # Round ratios to one decimal place
    dimensionless = np.round(dimensionless, 1)

    # Save ratios
    dimensionless_list.append(dimensionless)

# Convert list to NumPy array
dimensionless_list = np.array(dimensionless_list)


# -----------------------------
# Sessions to highlight
# -----------------------------

# Dictionary of session names and their desired highlight color
highlight_sessions = {
    "2025-5-22": "red",
    "2025-8-18": "red",
    "2025-10-27": "red",
    "2026-4-22": "red",
    "2026-6-23": "red",
    "2026-7-20": "red",
    "2026-7-30": "red"
}


# -----------------------------
# Create figure
# -----------------------------

# Create a figure
plt.figure(figsize=(12, 7))

# Get the current axes
ax = plt.gca()

# Empty lists
all_x = []
all_y = []


# -----------------------------
# Plot all points
# -----------------------------

# Loop through every manager session
for i in range(len(protect_storages)):

    # Use one x-value (protection storage) for every point in this session
    x_values = [protect_storages[i]] * len(dimensionless_list[i])

    # Corresponding storage ratios
    y_values = dimensionless_list[i]

    # Default colors based on storage ratio
    colors = ["red" if y < 1.0 else "blue" for y in y_values]

    # Use diamonds below 1.0 and circles above 1.0
    markers = ["D" if y < 1.0 else "o" for y in y_values]

    # Override colors if the session is highlighted
    if session_names[i] in highlight_sessions:
        colors = [highlight_sessions[session_names[i]]] * len(y_values)

    # Plot every point individually
    for x, y, c, m in zip(x_values, y_values, colors, markers):
        plt.scatter(x, y, color=c, marker=m, s=100, alpha=0.9)


# Draw a horizontal reference line at ratio = 1
plt.axhline(1.0, color='purple', linewidth=2.0, linestyle='--')


# Label the x-axis
plt.xlabel('Chosen Protection Volume\n(MAF)', fontsize=18, fontweight='bold')

# Label the y-axis
plt.ylabel('Lake Mead Storage to Protection Ratio\n(storage volume/protection volume)', fontsize=18, fontweight='bold')


# -----------------------------
# Bottom x-axis (Protection Storage)
# -----------------------------

# Convert protection storage array to list
unique_storage = protect_storages.tolist()

# Create formatted labels
storage_labels = [f"{s:.1f}" for s in unique_storage]

# Set tick locations
ax.set_xticks(unique_storage)

# Set tick labels
ax.set_xticklabels(storage_labels, fontsize=18, fontweight='bold')

# Format y-axis tick labels
plt.yticks(fontsize=18, fontweight='bold')


# -----------------------------
# Top x-axis (Protection Elevation)
# -----------------------------

# Create a second x-axis
ax_top = ax.twiny()

# Match limits with bottom axis
ax_top.set_xlim(ax.get_xlim())

# Use same tick locations
ax_top.set_xticks(unique_storage)

# Format protection elevation labels
elev_labels = [
    f"{int(e)}" if abs(e - round(e)) < 1e-6 else f"{e:.1f}"
    for e in protect_elevs
]

# Apply labels
ax_top.set_xticklabels(elev_labels, fontsize=18, fontweight='bold')

# Label the top axis
ax_top.set_xlabel('Chosen Protection Elevation (feet)',
                  fontsize=18, fontweight='bold')


# Make y-axis tick labels bold
for label in ax.get_yticklabels():
    label.set_fontweight('bold')


# Add gridlines
ax.grid(True, linestyle='--', alpha=0.6)

# Force y-axis to start at zero
ax.set_ylim(bottom=0)


# Adjust spacing
plt.tight_layout()

# Save the figure
plt.savefig("SessionDotPlotUpdated-8-4-2026.png", dpi=200)

# Display the figure
plt.show()