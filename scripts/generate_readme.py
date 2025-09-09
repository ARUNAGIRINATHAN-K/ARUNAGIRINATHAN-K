import datetime

def main():
    username = "ARUNAGIRINATHAN-K"
    today = datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")

    content = f"""# Hi, I'm {username} 👋

Welcome to my profile!  
This README is **auto-generated** using GitHub Actions.

---

### 📊 GitHub Stats
![GitHub Stats](https://github-readme-stats.vercel.app/api?username={username}&show_icons=true&theme=tokyonight)

### ⏰ Last Updated
`{today}`

"""
    with open("README.md", "w", encoding="utf-8") as f:
        f.write(content)

if __name__ == "__main__":
    main()
