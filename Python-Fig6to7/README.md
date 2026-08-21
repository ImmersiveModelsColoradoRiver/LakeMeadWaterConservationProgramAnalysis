# Python-Fig6to7

This code iterates through an Excel sheet of compacted data from multiple different immersive model sessions for Lake Mead and creates graphs that show the differences and successes of each session.

## Description of Contents
1. **ManagerSessionsData.xlsx** - Excel sheet that is the input for both Python scripts. It contains condensed results -- USBR protection elevations/volumes, reservoir elevation/storage volumes, and calculated ratio of storage to protection volume from immersive model sessions for Lake Mead.
2. **LakeMeadWaterBankDivideInflow2026-3-17-Anonymized.xlsx** - Excel model file with collaborator entries used in the model session on March 17, 2026 shown in Figure 6. The worksheet *Readme-Directions* provides a summary of the model file. The worsheet *Master* contains entries for the model session.
3. **SessionDotPlot-Updated-8-4-2026.py** - This Python script reads through the input and produces a dot plot representation of Lake Mead Storage to Protection Ratio vs. Chosen Protection Volume. A secondary x-axis displays the corresponding protection elevation.
4. **SessionDotPlotUpdated-8-4-2026.png** - This graph shows when collaborators in sessions succeeded and did not succeed in stabilizing Lake Mead's storage relative to the selected protection volume.
5. **TimeSeries-2026-3-17.py** - This Python script reads through the input and produces a time series graph for a selected immersive model session.
6. **TimeSeries-2026-3-17.png** - This line graph shows the storage and protection limit through the modeled years for one immersive model session. A secondary y-axis displays the corresponding Lake Mead elevation.

## Directions to Reproduce Results

### Software Needed
The software applications needed to reproduce these results are Microsoft Excel, Python, and PyCharm.

### Reproducibility

To reproduce the results, follow the directions below.

1. Install Microsoft Excel.
   - Search "https://excel.cloud.microsoft/" in a search engine.
   - Sign in or create an account.
   - If Excel is not purchased, follow Microsoft's provided instructions to purchase Excel.
   - Open Excel and sign in.

2. Install Python.
   - Search "https://www.python.org/" in a search engine.
   - Scroll down to the "Download" section and click the latest Python version.
   - Scroll down to the "Files" section.
   - Read the "Description" column in the table, choose the best description for the device in use, then follow the row to the left to the "Version" column and click on the installer option.
   - Go to the device's downloads and find the installer chosen in Step 2d.
   - Click on the installer and follow the directions.

3. Install PyCharm.
   - Search "https://www.jetbrains.com/pycharm/" in a search engine.
   - Select "Download".
   - Ensure the installer is correct for the device in use, then select "Download".
   - Go to the device's downloads and find the installer chosen in Step 3c.
   - Select the installer and follow the directions.

4. Download this repository.
   - Scroll to the top of this page and select **Code**.
   - Select **Download ZIP**.
   - Go to the device's downloads and unzip the repository.

5. Open the Python script.
   - Open the folder **ManagerSessionData-Updated-8-4-26**.
   - Open either **SessionDotPlot-Updated-8-4-2026.py** or **TimeSeries-2026-3-17.py** in PyCharm.

6. Select a Python interpreter.

7. Install the required Python packages.
   - Open **Settings** in PyCharm.
   - Select **Project**, then **Python Interpreter**, then click **+**.
   - Search for **pandas** and select **Install Package**.
   - Repeat for **openpyxl**.
   - Repeat for **numpy**.
   - Repeat for **matplotlib**.

8. Click the green play arrow at the top of the page.

9. The selected Python script will generate its corresponding figure (**SessionDotPlotUpdated-8-4-2026.png** or **TimeSeries-2026-3-17.png**) in the same folder.

## Model Repository

A blank version of the immersive model file with full documentation and directions can be found on Hydroshare at:

Rosenberg, D. E., Porse, E., Akbar, H., Myers, A., Fager, B. (2026). Immersive Model for Lake Mead Based on the Principle of Divide Reservoir Inflow, HydroShare, http://www.hydroshare.org/resource/1fcd5325c0a7400099f1698bc72cecd7.
