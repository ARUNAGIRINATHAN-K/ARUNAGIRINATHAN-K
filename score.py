import requests
import os

USERNAME = "ARUNAGIRINATHAN-K"
TOKEN = os.getenv("GITHUB_TOKEN", None)  # GitHub Actions provides this automatically

headers = {"Authorization": f"token {TOKEN}"} if TOKEN else {}

# --- Get user data ---
user = requests.get(f"https://api.github.com/users/{USERNAME}", headers=headers).json()
repos = requests.get(f"https://api.github.com/users/{USERNAME}/repos?per_page=100", headers=headers).json()
events = requests.get(f"https://api.github.com/users/{USERNAME}/events/public", headers=headers).json()

# Make sure repos/events are lists
if not isinstance(repos, list):
    repos = []
if not isinstance(events, list):
    events = []

# --- Extract stats ---
followers = user.get("followers", 0)
stars = sum(repo.get("stargazers_count", 0) for repo in repos)
forks = sum(repo.get("forks_count", 0) for repo in repos)
prs = sum(1 for e in events if e.get("type") == "PullRequestEvent")
issues = sum(1 for e in events if e.get("type") == "IssuesEvent")
commits = sum(len(e["payload"].get("commits", [])) for e in events if e.get("type") == "PushEvent")

# --- Custom formula ---
score = (commits * 0.5) + (stars * 5) + (forks * 3) + (prs * 4) + (issues * 2) + (followers * 2)

# --- Level system ---
level = int(score // 500)
progress = int((score % 500) / 500 * 100)

# --- Progress bar (10 blocks) ---
filled = progress // 10
bar = "▓" * filled + "░" * (10 - filled)

# --- Update README ---
with open("README.md", "r") as f:
    content = f.read()

start = "<!--SCORE_START-->"
end = "<!--SCORE_END-->"
before = content.split(start)[0]
after = content.split(end)[1] if end in content else ""

new_section = f"""{start}
🏆 **GitHub Score:** {int(score)}

📊 Formula: (Commits ×0.5 + Stars ×5 + Forks ×3 + PRs ×4 + Issues ×2 + Followers ×2)

🎮 **Level {level}**
[{bar}] {progress}%
{end}"""

with open("README.md", "w") as f:
    f.write(before + new_section + after)
