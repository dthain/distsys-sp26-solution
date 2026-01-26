import subprocess
import sys

repos_file = open("../student_repos_ssh", "r")

if len(sys.argv)!=2:
    print("usage: argument is the assignment number eg '3'")
    sys.exit(1)

assignment_number = sys.argv[1]

non_conformers = []
resolved = []

for line in repos_file:
    repo_url = line.strip()
    repo_name = repo_url.split("/")[-1].replace(".git", "")
    
    p = subprocess.run(["git", "fetch", 'origin', f'a{assignment_number}'], cwd=repo_name)

    if p.returncode != 0:
        p = subprocess.run(["git", "fetch", 'origin', f'A{assignment_number}'], cwd=repo_name)
    
    if p.returncode != 0:
        print(f"Error fetching assignment {assignment_number} for {repo_name}")
        non_conformers.append(repo_name)

for deviant in non_conformers:
    print(f"Attempting to solve tag name for {deviant}...")

    p = subprocess.run(["git", "fetch", "--all"], cwd=deviant)

    if p.returncode != 0:
        print(f"Error fetching all for {deviant}")
        continue

    p = subprocess.run(["git", "tag", '-l'], cwd=deviant, capture_output=True)

    if p.returncode != 0 or p.stdout is None:
        print(f"Error listing tags for {deviant}")
        continue

    p.stdout = p.stdout.decode('utf-8')
    tags = p.stdout.split('\n')
    
    possible_tags = [t for t in tags if f'{assignment_number}' in t]

    if len(possible_tags)==0:
        print(f"No matches for assingment {assignment_number} in {tags}")
        continue

    tag_index = 0

    if len(possible_tags)>1:
        print(f"Multiple matches for assignment {assignment_number} in {tags}")
        print("Enter the list index of the desired tag: Type a non-integer to skip")
        response = input()
        if response.isdigit():
            tag_index = int(response)
        else:
            continue
    else:
        print(f"Single match found: {possible_tags[0]}")
        print("Press Enter to checkout this tag, or type anything else to skip")
        response = input()
        if not response:
            tag_index = 0
        else:
            continue

    selected_tag = possible_tags[tag_index]

    p = subprocess.run(["git", "checkout", selected_tag], cwd=deviant)

    if p.returncode != 0:
        print(f"Error checking out tag {selected_tag} for {deviant}")
        continue
    
    resolved.append(deviant)

remaining = set(non_conformers) - set(resolved)

print("Could not solve the following repositories:")

for r in remaining:
    print(r)