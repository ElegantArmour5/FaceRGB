# FaceRGB

Process first 900 frames of live camera feed and output csv file of all RGB values of all landmarks in .csv format.

# .CSV Explanation
`Frame` - The number of the respective frame (0 to 899)
`X` - Value of X coordinate
`Y` - Value of Y coordinate
`R` - Red colour intensity
`G` - Green colour intensity
`B` - Green colour intensity

# How to run the code
Ensure python is installed on the system (if not download at python.org). Code was developed using Python 3.12.4

Download files in the repository and open command prompt or terminal and navigate to correct directory (use cd to change directory)

Download prerequisites from `requirements.txt` file using `pip install -r requirements.txt` (copy and paste in cmd/terminal)

If pip not found error, ensure pip has been added to PATH.

To run the app, use `python app.py` after navigating to the correct directory.
