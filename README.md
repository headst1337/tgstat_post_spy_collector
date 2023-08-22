# TGStat Post Spy Collector

Welcome to the **TGStat Post Spy Collector**, an elegant and powerful tool to automatically analyze, collect, and filter data using the TGStat API. The system systematically archives information from Telegram posts in a dedicated database, providing an efficient solution for all your monitoring needs.

## 📦 Dependencies

Before diving in, ensure that you have **Python 3.11** installed and an active subscription to [TGStat API](https://tgstat.ru/api/search).

## 🔧 Getting Started

### 1. Clone this repository 🚀
`git clone https://github.com/username/repo.git`

### 2. Create a virtual environment
`python3 -m venv env`

### 3. Activate the virtual environment
_For Linux/macOS:_ `source env/bin/activate`\
_For Windows:_ `.\env\Scripts\activate.bat`

### 4. Install the dependencies
`pip install -r requirements.txt`

### 5. Create a .env configuration file 📝
Add the following variables to a `.env` file in the root folder of the project.

```env
SECRET_KEY=
ADMIN_USERNAME=
ADMIN_PASSWORD=
TGSTAT_TOKEN=   # Obtain it from: https://tgstat.ru/my/profile
KEYWORDS=       # See the documentation: https://api.tgstat.ru/docs/ru/extended-syntax.html
DATABASE_URL="mysql+mysqlconnector://<username>:<password>@<host>/<database_name>"
```

### 6. Customize options ⚙️
Tailor the interval in `scheduler.py` and the number of iterations in `parse.py` to match your subscription plan.

### 7. Ready, set, go!
Run the project with the command: `python run.py`

## 🎉 Congratulations!

You've successfully set up **TGStat Post Spy Collector**! Feel free to reach out if you have any questions or suggestions.
