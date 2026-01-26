import subprocess

repos_file = open("../student_repos_ssh", "r")

for line in repos_file:
    repo_url = line.strip()
    repo_name = repo_url.split("/")[-1].replace(".git", "")
    
    
    print(f"Cloning {repo_name} from {repo_url}...")
    subprocess.run(["git", "clone", repo_url, repo_name])