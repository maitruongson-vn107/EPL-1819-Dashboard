# EPL-1819-Dashboard
Dashboard showing information about English Premier League season 2018-2019, via Neo4j Graph Database

**ABOUT THE PROJECT**


**STEPS TO RUN THE APPLICATION**

**1. Set Neo4j Local Server**

Create a Neo4j local server with these default settings:

- URL: bolt://localhost:7687
- DB Name: "neo4j"
- Username: "sonmt"
- Password: "S1o0n720" 

If you want to customize username & password, 
you can change the constant value in `/utils/constant.py` file

**2. Create Python environments**

Use **anaconda** to create new virtual environment with Python 3.8: \
`conda create -n epl_dashboard_env python==3.8`

Activate recently created environment: \
`conda activate epl_dashboard_env`

Install required packages for the application: \
`pip3 install -f requirements.txt`

**3. Run Application**

3.1. Load Data From CSV Files to Neo4j DB

`python data_loaders/data_loaders.py` 

This command will reset the current DB "ne4j" in the local machine 
and start loading EPL 18/19 data from the CSV files to the graph database. \
The whole process will take about 15 minutes.

3.2. Run the dashboard

`python view/main_window.py`

This command will start the dashboard.

