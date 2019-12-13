# cs506-Bus-Congestion
Final project of cs506

- Make sure all dependencies have been install through install 'requirements.txt' under root directory

- To find the optimized route, you only need to run 'python optimizer.py' under src directory,
then you can find all optimized route(if possible) under src/optimized directory. However, it's really time consuming to wait program finished. You can just pick up random one html file generated to see the result.

- run 'python q1.py' under src directory to generate q1.html within the folder. It's the answer for question one in our final report

- run 'python q3.py' under src directory to generate q3.html within the folder. It's the answer for question three in our final report


# Each of folder under root:

- /bot: 
1. scripts to auto capture real-time MBTA data and save them to local
2. fine-grained scraped MBTA data under /bot/output from 20191026 to 20191110

- /csv:
sample csv files for testing and keys for web services(Google)

- /report:
all writing work submitted

- /script:
scripts for scraping data and all data preprocessing work

- /src: 
all source codes to run the optimization task
