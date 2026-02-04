import subprocess
import glob

repos_file = open("../student_repos_ssh", "r")

for line in repos_file:
    repo_name = line.strip().split("/")[-1].replace(".git", "")

    assignment_cwd = f"{repo_name}/a2"

    try:
        grading = open(f"{assignment_cwd}/GRADING", "w")
    except FileNotFoundError:
        try:
            assignment_cwd = f"{repo_name}/A2"
            grading = open(f"{assignment_cwd}/GRADING", "w")
        except FileNotFoundError:
            try:
                assignment_cwd = f"{repo_name}/distsys/a2"
                grading = open(f"{assignment_cwd}/GRADING", "w")
            except FileNotFoundError:
                print(f"Could not find assignment directory for {repo_name}, skipping...")
            continue
    except FileExistsError:
        continue

    grading.write("Assignment 2 - Networking\n")

    grading.write("""Measurement Technique (20/20 Points)
+10 REPORT shows results for TCP and UDP tests.
+10 The test results show at least method, buffer size, and elapsed time.

Code Function and Results (50/50 Points)
+25 The code implements complete TCP (13) and UDP (13) transactions, where
    the receiver does in fact read all of the data being sent. 
+15 Various buffer sizes are tested within the given range.
+10 The programs are invoked with the specified arguments. 

Commentary (30/30 Points)
+15 The student observes the general throughput grow as buffer size increases
+10 The student reflects on the difference between the UDP and TCP performance 
    and postulates the reason. (correct or not)
+5  The observations are at least marginally correct or insightful, and the data
    which they were made upon was not flawed by the program or measurement. 

Total: 100/100 Points
""")

    grading.close()

    




