# EPL-1819-Dashboard
**OTH Regensburg (Summer Semester 2022)** \
**"Knowledge Graphs" Course - Individual Project** \
Dashboard showing information about English Premier League season 2018-2019, via Neo4j Graph Database

**ABOUT THE PROJECT**

English Premier League is one of the top national league in Europe as well as all over the world.

For the "Knowledge Graphs" course at OTH summer 2022, I created a dashboard application which provides information about
EPL season 2018-2019, using neo4j as the local database server.

**STEPS TO RUN THE APPLICATION**

**1. Set Neo4j Local Server**

Create a new Neo4j DBMS or use a currently working one.

Within that DBMS, create a database named **"epl1819"**. 
All the configurations are listed below:

- URL: bolt://localhost:7687
- DB Name: "epl1819"
- Username: "neo4j"
- Password: "S1o0n720" 

If you want to customize these configurations, 
you can change the constant values in `/utils/constant.py` file

**2. Create Python environments**

Use **anaconda** to create new virtual environment with Python 3.8: \
`conda create -n epl_dashboard_env python==3.8`

Activate recently created environment: \
`conda activate epl_dashboard_env`

Install required packages for the application: \
`pip3 install -f requirements.txt`

**3. Run Application**

3.1. Load Data From CSV Files to Neo4j DB

`python main_data_loader.py` 

This command will reset the current DB "neo4j" in the local machine 
and start loading EPL 18/19 data from the CSV files to the graph database. \
The whole process will take less than 2 minutes.

3.2. Run the dashboard

`python main_dashboard.py`

This command will start the dashboard. The main window will be firstly showed.

