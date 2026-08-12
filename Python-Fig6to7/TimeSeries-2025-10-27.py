"""
Purpose:
--------
This script creates a time series plot for a selected manager session from the
ManagerSessionsData.xlsx file.

The plot displays:
    • Lake Mead storage over the four modeled time periods (left y-axis)
    • The selected protection storage limit (red horizontal line)
    • A secondary y-axis showing the corresponding Lake Mead elevation

The session to plot is selected using its session name (for example,
"2025-10-27").
"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

# -----------------------------
# Locate the Excel input file
# -----------------------------

# Get the path of this Python script
code_file = Path(__file__)

# Build the path to the Excel workbook
input_file = code_file.parent / 'ManagerSessionsData.xlsx'


# -----------------------------
# Read the Excel workbook
# -----------------------------

# Read the workbook into a pandas DataFrame
ensemble = pd.read_excel(input_file)

# Convert the four simulation columns to numeric values.
# Any invalid entries become NaN.
ensemble.iloc[:, 3:7] = ensemble.iloc[:, 3:7].apply(pd.to_numeric, errors="coerce")


# -----------------------------
# Define session layout
# -----------------------------

# Each manager session occupies three rows
session_data = 3

# Total number of rows in the spreadsheet
length = len(ensemble)


# -----------------------------
# Create empty lists for storing data
# -----------------------------

# Stores storage values for every session
all_years = []

# Stores elevation values for every session
all_elevs = []

# Stores protection storage values
protect_storages = []

# Stores protection elevations
protect_elevs = []

# Stores session names (dates)
session_names = []


# -----------------------------
# Read each manager session
# -----------------------------

# Loop through the spreadsheet three rows at a time
for first in range(0, length, session_data):

    # Select one manager session
    sessions = ensemble.iloc[first:first + session_data, 3:7]

    # First row contains storage values
    years = sessions.iloc[0].values

    # Save storage values
    all_years.append(years)

    # Save the session name from the first column
    session_names.append(str(ensemble.iloc[first, 0]))

    # Third row contains elevations
    elevs = sessions.iloc[2].values

    # Save elevation values
    all_elevs.append(elevs)

    # Read the protection storage/elevation column
    protect_s = ensemble.iloc[first:first + session_data, 2]

    # First row = protection storage
    storage = protect_s.iloc[0]

    # Save protection storage
    protect_storages.append(storage)

    # Third row = protection elevation
    protect_e = ensemble.iloc[first:first + session_data, 2]

    elevation = protect_e.iloc[2]

    # Save protection elevation
    protect_elevs.append(elevation)


# Convert storage list to a NumPy array
all_years = np.array(all_years)


# -----------------------------
# Select the manager session to plot
# -----------------------------

# Specify the desired manager session
target_session = "2025-10-27"

# Find the index of that session
session_index = session_names.index(target_session)

# Retrieve the storage values for the selected session
selected_storage = all_years[session_index]

# Retrieve the protection storage
selected_protect_s = protect_storages[session_index]

# Retrieve the elevation values
selected_elevation = all_elevs[session_index]

# Retrieve the protection elevation
selected_protect_e = protect_elevs[session_index]


# -----------------------------
# Create x-axis labels
# -----------------------------

# Read the four simulation column names
year_header = np.array(list(ensemble.columns)[3:7])


# Create a horizontal series representing the protection limit
selected_protect_s_series = np.repeat(selected_protect_s, len(year_header))


# -----------------------------
# Create the figure
# -----------------------------

# Create figure and primary axis
fig, ax1 = plt.subplots()

# Plot simulated storage through time
ax1.plot(
    year_header,
    selected_storage,
    marker='o',
    markersize=8,
    linewidth=3,
    label='Storage',
    color='tab:blue'
)

# Plot the protection storage limit
ax1.plot(
    year_header,
    selected_protect_s_series,
    marker='d',
    markersize=8,
    color='red',
    linewidth=3,
    label='Protection Limit'
)


# -----------------------------
# Configure storage axis
# -----------------------------

# Define desired storage tick locations
storage_ticks = [
    0.0,
    4.5,
    5.7,
    selected_protect_s,
    selected_storage.max()
]

# Set y-axis limits
ax1.set_ylim(0, selected_storage.max() * 1.05)

# Apply tick locations
ax1.set_yticks(storage_ticks)

# Label the primary y-axis
ax1.set_ylabel(
    'Storage (million acre-feet)',
    fontweight='bold',
    fontsize=20
)

# Format tick labels
ax1.tick_params(axis='y', labelsize=17)
ax1.tick_params(axis='x', labelsize=17)

# Make tick labels bold
for label in ax1.get_xticklabels() + ax1.get_yticklabels():
    label.set_fontweight('bold')

# Add gridlines
ax1.grid(linewidth=1)

# No x-axis label
ax1.set_xlabel(None, fontweight='bold', fontsize=20)


# -----------------------------
# Build storage-elevation relationship
# -----------------------------

# Combine every storage value into one array
all_S_data = np.concatenate(all_years)

# Combine every elevation into one array
all_E_data = np.concatenate(all_elevs)

# Include protection storage values
S_anchor_base = np.concatenate([protect_storages, all_S_data]).astype(float)

# Include protection elevations
E_anchor_base = np.concatenate([protect_elevs, all_E_data]).astype(float)

# Add zero-storage point
S_anchor = np.append(S_anchor_base, 0.0)
E_anchor = np.append(E_anchor_base, 0.0)

# Remove missing values
valid_indices = ~np.isnan(S_anchor) & ~np.isnan(E_anchor)
S_anchor = S_anchor[valid_indices]
E_anchor = E_anchor[valid_indices]

# Sort storage values
order = np.argsort(S_anchor)
S_sorted = S_anchor[order]
E_sorted = E_anchor[order]


# -----------------------------
# Create secondary elevation axis
# -----------------------------

# Create a second y-axis
ax2 = ax1.twinx()

# Match the limits of the primary axis
ax2.set_ylim(ax1.get_ylim())

# Match the storage tick locations
ax2.set_yticks(storage_ticks)

# Interpolate elevations corresponding to storage ticks
elev_labels = np.interp(storage_ticks, S_sorted, E_sorted)


# -----------------------------
# Add desired elevation reference points
# -----------------------------

# Desired storage values
extra_storage = [4.5, 5.7]

# Desired elevation labels
extra_elevs = [1000, 1020]

# Ensure these storage values exist
storage_ticks = np.unique(np.concatenate([storage_ticks, extra_storage]))

# Recompute elevations
elev_labels = np.interp(storage_ticks, S_sorted, E_sorted)

# Force exact labels for known storage values
for i, s in enumerate(storage_ticks):
    if np.isclose(s, 4.5):
        elev_labels[i] = 1000

    if np.isclose(s, 5.7):
        elev_labels[i] = 1020

    if np.isclose(s, selected_protect_s):
        elev_labels[i] = selected_protect_e


# Apply tick locations
ax1.set_yticks(storage_ticks)
ax2.set_yticks(storage_ticks)

# Apply elevation labels
ax2.set_yticklabels(
    [f"{e:.0f}" for e in elev_labels],
    fontweight='bold'
)

# Label the secondary axis
ax2.set_ylabel(
    'Elevation (feet)',
    fontweight='bold',
    fontsize=20
)

# Format tick labels
ax2.tick_params(axis='y', labelsize=17)


# -----------------------------
# Finish the figure
# -----------------------------

# Add legend
ax1.legend(loc='best', fontsize=17, frameon=True)

# Save the figure
plt.savefig('TimeSeries-2025-10-27.png')

# Display the figure
plt.show()