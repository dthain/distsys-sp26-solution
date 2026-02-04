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

    tag_name = f'a{assignment_number}'

    # skip if already done
    p = subprocess.run(["git", "tag", '-l'], cwd=repo_name, capture_output=True)
    current_tag = p.stdout.decode('utf-8').strip()

    if current_tag.lower() == tag_name.lower():
        print(f"{repo_name} already on correct tag {current_tag}")
        resolved.append(repo_name)
        continue

    p = subprocess.run(["git", "fetch", 'origin', tag_name], cwd=repo_name)

    if p.returncode != 0:
        p = subprocess.run(["git", "fetch", 'origin', f'A{assignment_number}'], cwd=repo_name)

        if p.returncode != 0:
            print(f"Error fetching assignment {assignment_number} for {repo_name}")
            non_conformers.append(repo_name)
            continue

        tag_name = f'A{assignment_number}'

    p = subprocess.run(["git", "checkout", tag_name], cwd=repo_name)

    if p.returncode != 0:
        print(f"Error checking out tag {tag_name} for {repo_name}")
        non_conformers.append(repo_name)
        continue

    resolved.append(repo_name)


for deviant in non_conformers.copy():
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
        response = input().strip()
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
    non_conformers.remove(deviant)

print("Could not solve the following repositories:")

for r in non_conformers:
    print(r)


print("\n\nChecking for late submissions. The latest 5 commits are as follows:")

last_commits = {}

for repo_name in resolved:
    # should not fail
    p = subprocess.run(["git", "log", "-1"], cwd=repo_name, capture_output=True)

    date = [l for l in p.stdout.decode('utf-8').split('\n') if 'Date:' in l][0].split('Date:')[1].strip()

    from dateutil import parser

    commit_date = parser.parse(date)
    last_commits[repo_name] = commit_date

sorted_commits = sorted(last_commits.items(), key=lambda x: x[1], reverse=True)

for repo_name, commit_date in sorted_commits[:5]:
    print(f"{repo_name}: {commit_date}")



    


