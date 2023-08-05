
For configuration file syntax information please visit http://inicheck.readthedocs.io/en/latest/


lyte_probe
----------

| **add_average_column**
| 	If true will average together all the columns
| 		*Default: False*
| 		*Type: bool*
| 

| **assumed_depth**
| 	Depth in cms to assumed a linear depth profile to with the timeseries data
| 		*Default: None*
| 		*Type: int*
| 

| **bottom_depth**
| 	Depth in CM where the movement stopped
| 		*Default: None*
| 		*Type: float*
| 

| **calibration_coefficients**
| 	Polynomial coefficients to use for processing the column_to_plot data
| 		*Default: 1*
| 		*Type: float*
| 

| **color**
| 	Decimal RGB Color to use for the plot
| 		*Default: 0 .455 .784 1*
| 		*Type: float*
| 

| **columns_to_plot**
| 	List of columns to plot in the data
| 		*Default: sensor_1*
| 		*Type: string*
| 

| **detect_surface**
| 	Use the NIR sensors to determine the location of the snow surface.
| 		*Default: False*
| 		*Type: bool*
| 

| **filename**
| 	Filename to be plotted
| 		*Default: None*
| 		*Type: criticalfilename*
| 

| **fill_solid**
| 	Determines whether to fill in the profile solid to the y axis
| 		*Default: True*
| 		*Type: bool*
| 

| **plot_labels**
| 	a list of tuples containing labels to add to the plot
| 		*Default: None*
| 		*Type: string*
| 

| **problem_layer**
| 	Depth in centimeters to place a red horizontal line on the plot.
| 		*Default: None*
| 		*Type: float*
| 

| **smoothing**
| 	Rolling window over each column to apply an averaging filter
| 		*Default: None*
| 		*Type: int*
| 

| **surface_depth**
| 	Depth in CM where the snow surface begins
| 		*Default: 0*
| 		*Type: float*
| 

| **title**
| 	Plot title for the Lyte probe
| 		*Default: lyte probe*
| 		*Type: string*
| 

| **use_filename_title**
| 	Use the filename to for the lyte plot title
| 		*Default: True*
| 		*Type: bool*
| 

| **xlabel**
| 	Label to put under the x axis
| 		*Default: Hardness (mN)*
| 		*Type: string*
| 

| **xlimits**
| 	Range in the X Axis to plot
| 		*Default: None*
| 		*Type: floatpair*
| 

| **ylabel**
| 	Label on the y axis
| 		*Default: Depth from surface (cm)*
| 		*Type: string*
| 

| **ylimits**
| 	Range of depths in cm to plot
| 		*Default: -100 0*
| 		*Type: floatpair*
| 


snow_micropen
-------------

| **color**
| 	Decimal RGB Color to use for the plot
| 		*Default: 0.211 .27 .31 1*
| 		*Type: float*
| 

| **filename**
| 	Filename to be plotted
| 		*Default: None*
| 		*Type: criticalfilename*
| 

| **fill_solid**
| 	Determines whether to fill in the profile solid to the y axis
| 		*Default: False*
| 		*Type: bool*
| 

| **plot_labels**
| 	a list of tuples containing labels to add to the plot
| 		*Default: None*
| 		*Type: string*
| 

| **problem_layer**
| 	Depth in centimeters to place a red horizontal line on the plot.
| 		*Default: None*
| 		*Type: float*
| 

| **smoothing**
| 	Rolling window over each column to apply an averaging filter
| 		*Default: None*
| 		*Type: int*
| 

| **title**
| 	Plot title the snow micro pen
| 		*Default: snow micropen*
| 		*Type: string*
| 

| **use_filename_title**
| 	Use the filename to for the SMP title
| 		*Default: True*
| 		*Type: bool*
| 

| **xlabel**
| 	Label to put under the x axis
| 		*Default: Force (mN)*
| 		*Type: string*
| 

| **xlimits**
| 	Range in the X Axis to plot
| 		*Default: None*
| 		*Type: floatpair*
| 

| **ylabel**
| 	Label on the y axis
| 		*Default: Depth from surface (cm)*
| 		*Type: string*
| 

| **ylimits**
| 	Range of depths in cm to plot
| 		*Default: -100 0*
| 		*Type: floatpair*
| 


hand_hardness
-------------

| **color**
| 	Decimal RGB Color to use for the plot
| 		*Default: 0.603 0.6 0.84 1*
| 		*Type: float*
| 

| **filename**
| 	Filename to be plotted
| 		*Default: None*
| 		*Type: criticalfilename*
| 

| **plot_labels**
| 	a list of tuples containing labels to add to the plot
| 		*Default: None*
| 		*Type: string*
| 

| **problem_layer**
| 	Depth in centimeters to place a red horizontal line on the plot.
| 		*Default: None*
| 		*Type: float*
| 

| **title**
| 	Plot title for the hand hardness profile
| 		*Default: Hand Hardness*
| 		*Type: string*
| 

| **xlabel**
| 	Label to put under the x axis
| 		*Default: Hand Hardness*
| 		*Type: string*
| 

| **xlimits**
| 	Range in the X Axis to plot
| 		*Default: None*
| 		*Type: floatpair*
| 

| **ylabel**
| 	Label on the y axis
| 		*Default: Depth from surface (cm)*
| 		*Type: string*
| 

| **ylimits**
| 	Range of depths in cm to plot
| 		*Default: -100 0*
| 		*Type: floatpair*
| 


output
------

| **dpi**
| 	Resolution of the image to produce
| 		*Default: 500*
| 		*Type: int*
| 

| **figure_size**
| 	Must be a list of two items specifying figure size in inches
| 		*Default: 6 10*
| 		*Type: float*
| 

| **file_type**
| 	File format of the figure to be outputted
| 		*Default: png*
| 		*Type: string*
| 		*Options:*
 *png jpg pdf svg eps*
| 

| **filename**
| 	filename for the outputted figure
| 		*Default: None*
| 		*Type: string*
| 

| **output_dir**
| 	Location to save figures
| 		*Default: ./output*
| 		*Type: directory*
| 

| **show_plot**
| 	Show the plot to be outputted
| 		*Default: True*
| 		*Type: bool*
| 

