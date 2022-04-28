# LastFM-Album-Analysis
 Testing album plays for correlation

This set of scripts was written for my 2022 Undergraduate Dissertation, and provides a set of tools to gather the playcount for the top 200 albums of the 2010s (Billboard) and determine the strength of the correlation with respect to track order in a given window of time.

For this dissertation, I ran lastfm.py once per week in the File Input mode, gathering a snapshot of the plays for each album listed. The file input reads from the alltimealbums.txt file, or can be ran in individual album query mode.

linesrecursive.py then takes two weeks of data and compares them, calculating the Product Moment Correlation Coefficient for the data, and comparing it to the Critical Value for sample size N. These can then be visualised using MatPlotLib.

