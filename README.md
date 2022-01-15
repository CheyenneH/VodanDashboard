# VodanDashboard

For the course Data Science in Practice 2021 (https://studiegids.universiteitleiden.nl/courses/102469/data-science-in-practice) our task was to create a prototype for a dashboard that visualized statistics about hospitals in Africa. The data used in this project is all mock data, so no actual medical data from hospitals is used. This data is completely artifial and therefore might not be correct or make sense. This repository hosts the necessary files for running the dashboard as well as a guide how to run this project on any machine that can run Python. 

In this report our accomanying report is also published, but we removed some personal information from the people involved that was present in the final report that was handed in for the course. 

## Requirements

In order to be able to run the files the following installations must be done
* Python. We worked with version 3.9.5 and haven't tested any other version but we suspect that any python version above 3.7 should work. This can be done by following this tutorial: https://realpython.com/installing-python/#how-to-install-python-on-windows . Make sure you also install 'pip' with it. 
You should now be able to check both you pyhton and pip version by typing "python --version" and "pip --version" in the command line. If you get a result like "Python 3.9.5" and "pip 21.1.3 from path/to/pip" then everything is installed correctly.  
* The following Python packages are needed:
  *  pandas (run "pip install pandas")
  *  dash (run "pip install dash")
  *  nest_asyncio (run "pip install nest_asyncio")
  *  plotly (comes with dash)

## How to run
If you are not sure how to work with GitHub repositories check out this source: https://docs.github.com/en/repositories/creating-and-managing-repositories/cloning-a-repository
* clone this repository to your computer and navigate in the command promt to the cloned repository
* enter the following command "python dashboard.py"
* Got to the local host webpage on your PC to view the dashboard, this is desplayed in the command line as well and is often "http://127.0.0.1:8050/"
