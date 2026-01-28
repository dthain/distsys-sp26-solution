import subprocess
import glob

repos_file = open("../student_repos_ssh", "r")

for line in repos_file:
    repo_name = line.strip().split("/")[-1].replace(".git", "")

    assignment_cwd = f"../grading/{repo_name}/a1"

    try:
        grading = open(f"{assignment_cwd}/GRADING", "w")
    except FileNotFoundError:
        try:
            assignment_cwd = f"../grading/{repo_name}/A1"
            grading = open(f"{assignment_cwd}/GRADING", "w")
        except FileNotFoundError:
            print(f"Could not find assignment directory for {repo_name}, skipping...")
            continue
    except FileExistsError:
        continue

    grading.write("Assignment 1 - Measurement\n")

    grading.write("----------------------------\n")

    grading.write("\nMeasurement Technique: (20/20)\n")
    grading.write("----------------------------\n")

    grading.write("\nResults (50/50)\n")
    grading.write("----------------------------\n")

    grading.write("\nCommentary (30/30)\n")
    grading.write("----------------------------\n")

    grading.write("\nTotal: 100/100\n")

    grading.close()

    




