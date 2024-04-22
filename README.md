# 6102 Group assignment

## INSTRUCTIONS
      Comparative Road Network Analysis in MongoDB and Neo4j



Objective

This assignment aims to achieve an in-depth understanding of MongoDB and Neo4j by performing a series of queries on a road network dataset.
Compare how these databases handle different types of queries, focusing on conditional logic, aggregation, and basic data retrieval.
The second part of this assignment t is about finding paths using the Graph Data Science (GDS) library in Neo4j
This assignment will give you practical insights into the performance characteristics of MongoDB and Neo4j, as well as an understanding of graph algorithm execution in Neo4j.
Below are instructions for each part.

Dataset Overview

Your dataset represents connections between cities, each with a specified distance. The data is structured with three columns in a csv file: FromCity, ToCity, and Distance.
Example:
fromCity	toCity	Distance
Atlanta	Richmond	800
Paris	Strasbourg 	500
Breslau 	Prague	300
Frankfurt	Cologne	190
Salzburg	Berlin	740


##############
Generating the Dataset for both parts 

You can generate a dataset for this assignment using a simple Python generator. Make sure your dataset adheres to the following criteria:
The dataset should represent a network of roads between cities with specified distances.
Ensure that no two entries (roads) have the same pair of cities in columns 1 (FromCity) and 2 (ToCity) in your CSV file.
Make sure to have at least 100k rows or more. Once to write the simple generator, then you can generate whatever number of rows you want.
The larger the dataset, the more accurate the performance measurement results. I recommend having more than 100k but that's the least amount of rows/data.
Tip: You can use the Faker module in Python to generate fake data easily.
You can use any dataset you can find in the web. 
Make sure the data generation makes sense and each node has multiple incoming and outgoing paths. 
###############



Part 1: Basic Querying and Data Analysis

Tasks:

List Roads from/to 'Atlanta' with Distances and Destinations: Both MongoDB and Neo4j can easily manage this type of query, which involves basic filtering and data retrieval.
Find Roads Longer than 150 km, with Details: Again, both databases can execute this query. It involves a simple numerical comparison and data projection.
Total Road Length Connected to 'Frankfurt': This task is straightforward in Neo4j and a bit more challenging in MongoDB as it involves using the aggregation to sum distances.
Determine Shortest and Longest Road from 'Amman': Both databases can achieve this task. In MongoDB, it might require using sort and limit operations, while in Neo4j, it involves ordering and limiting the results within Cypher queries.

Make sure to include the cities mentioned in the tasks in your dataset.

This assignment aims to enhance your understanding of querying and data analysis in database systems, focusing on MongoDB and Neo4j.
You will be working with road network data, performing tasks that require different levels of querying capabilities.
By the end of this assignment, you should be proficient in executing and comparing diverse types of queries in both MongoDB and Neo4j.

Deliverables:

Code.
Provide the actual code or scripts written for MongoDB and Neo4j for each of the tasks.  
Provide the code written to generate the dataset to test it.
document the code. 
Performance Metrics:
Record and include the performance metrics for each query in both MongoDB and Neo4j. This could involve noting the execution time for each query and any relevant performance-related observations. See the code example below on how to use the time module to simply measure the time for executions. 
Results Documentation:
Present the results of each query in a structured format, such as text outputs, tables, or screenshots. This should clearly show the data retrieved or calculated by each query.
Visualization of Results:
Plot the results or performance metrics for a visual comparison between MongoDB and Neo4j on each task. You can use matplotlib library, which is designed for such scenarios.
Analysis and Observations:
A brief analysis of the results, focusing on the comparison between the performance and ease of querying in MongoDB versus Neo4j. Highlight any notable differences, challenges, or insights observed during the execution of the tasks.

-------------------------------------------------------------------

Part 2: Graph Algorithm in Neo4j' Graph Data Science Library

Tasks:


1. Depth First Search (DFS)
Task 1: DFS from 'Atlanta'
Objective: Explore Atlanta's network using DFS and record the path sequence.
Expected Output: A list of cities visited in the DFS order, starting from Atlanta.
Task 2: DFS from 'London'
Objective: Perform DFS starting from London, noting the traversal sequence.
Expected Output: A sequential list of cities visited in the DFS order from London.

2.  First Search (BFS)
Task 3: BFS from 'Atlanta'
Objective: Implement BFS from Atlanta, documenting the city sequence reached.
Expected Output: A list of cities showing the expansion pattern from Atlanta using BFS.
Task 4: BFS from 'London'
Objective: Execute BFS starting from London and record the order of cities explored.
Expected Output: A list of cities visited in the BFS sequence from London.
3. Visualization and Timing Analysis
Task 5.1: DFS Timing and Visualization
Objective: Compare DFS execution times from Atlanta and London; visualize the paths (you can you matplotlib library in Python, which is easy to use).
Expected Output: A plot showing DFS paths and timings from both cities.
Task 5.2: BFS Timing and Visualization
Objective: Compare BFS execution times from Atlanta and London; visualize the paths.
Expected Output: A plot illustrating BFS paths and timings from both cities.
Task 5.3: Direct DFS and BFS Comparison
Objective: Directly compare DFS and BFS for each city, in terms of paths and timings.
Expected Output: Comparative plots for Atlanta and London, highlighting differences between DFS and BFS.
NOTE: Make sure to include the cities mentioned in your dataset. 
Also, make sure that each node has many paths ranging from small to long ones. Make sure that you have many paths for each city for good testing (not like 5 or 10 paths) considering the large dataset.
Make sure that the generated data makes since (not 10000 miles distance between Atlanta and Baltimore).

Part 2 of this assignment delves into using graph algorithms, specifically DFS and BFS algorithms for traversals and path finding algorithms, within Neo4j's Graph Data Science Library. It aims to provide hands-on experience with graph-based analysis and visualization, enhancing understanding of graph algorithms in practical scenarios.
Recording and Analyzing Execution Times

For Tasks 1 to 4, each involving DFS and BFS from both Atlanta and London, you will measure how long it takes for each search to complete. Here's how to approach this:
Before Starting the Search:
Record the current time. In Python, you can use time.time() from the time module to get the current time.
Perform the Search:
Execute the DFS or BFS algorithm. This is where your code explores the city network.
After Completing the Search:
Record the time again. The difference between this time and the start time is the execution time for the search.
Analyze the Times:
Compare the execution times for DFS and BFS. This will give you an idea of which algorithm is faster under different conditions.

Below is a demo Python snippet that shows how to use time in Python by importing the time module.

import time

# Start the timer
start_time = time.time()

# Perform the search (DFS or BFS)
# ...

# Stop the timer
end_time = time.time()

# Calculate execution time
execution_time = end_time - start_time
print(f"something like the task for ... took... {execution_time} seconds.")

Deliverables:

Python Script:
A comprehensive single .py file with well-commented sections for DFS, BFS, timings, and visualizations.
Clear distinction of each task.
A well-documented code using comments #
Execution Timings:
Recorded and analyzed execution times for each DFS and BFS query.
Visualization Plots:
Comparative plots for DFS and BFS paths from Atlanta and London.
Visualization of timing differences for DFS and BFS searches.
Report:
A summary of findings, analyzing the results and execution efficiency of DFS and BFS.
Insights on the characteristics of each algorithm based on the plots and timings.
Please attach screenshots for each plot and name it according to the task.
Also, include the .py script that generates that dataset to test it.
Please submit your files in a zip code and name it as DW_Section_10_GROUP(#)_PROJECT.zip
One student representing the group can upload the work. 


NOTE:
The DFS and BFS algorithms in the Neo4j GDS library are pre-implemented. You just need to copy the algorithms mentioned and just set the parameters according to your dataset and record the execution times.
Please look at:
Pathfinding algorithms in Neo4j, which includes BFS and DFS: 
 
Path finding - Neo4j Graph Data Science
This chapter provides explanations and examples for each of the path finding algorithms in the Neo4j Graph Data Science library.
Neo4j Graph Data Platform

DFS:
https://neo4j.com/docs/graph-data-science/current/algorithms/dfs/
BFS:
https://neo4j.com/docs/graph-data-science/current/algorithms/bfs/


---------------------------

Tips:

Implementing DFS and BFS:
For each city (Atlanta and London), write the code or queries for performing DFS and BFS.
Ensure that your code accurately follows the DFS and BFS algorithms.
Recording Execution Time:
Use timing functions to record how long each search takes to complete.
This will involve capturing the start time before the search begins and the end time after it concludes.
Visualization:
Use a plotting library to create visual representations of the search paths.
Include the execution times in your plots for a clear comparison.
Analysis:
Write a small report in a text file for the analysis section, discuss the differences in execution times and what they might indicate about the efficiency of each algorithm in different scenarios.


Also, you're free to do other pathfinding algorithms from the one listed on the Neo4j website. 
Note that this is a required assignment .
It's separate from the 2 assignments and quizzes that I'll count the best three grades out of the four. 

--------------

Learning Outcomes
The goal of this assignment is to equip students with practical skills in querying and graph analysis using MongoDB and Neo4j, enhancing their understanding of database systems and pathfinding algorithms. Through this, students will develop their ability to analyze and visualize complex data, preparing them for real-world data handling and decision-making tasks.

Submission date and time: 
I'm giving you 30+ days to finish it. I understand you have other courses and tasks to do. 
Thus, as mentioned in the syllabus, the due date will be on 04/23 at or before 11:50. 


All the Best-
