# Cashflow Tracker WebApp

## Description
A web application built with Flask and SQLite for tracking personal income and expenses.
Users can authenticate, record financial transactions, and view a dashboard with summaries.
This is for my CS50x final project and I'm using VS Code Copilot extension,
as per the rule allowance stated on CS50x final project section.
I chose this web app as I record the income and expenses of one of my businesses,
in Excel. This could help make the transition to a more professional way of saving
this information. This is not a groceries expenses type of app, but instead the
formal income and expenses of a business.

## Basic Features
- User authentication with hashed passwords (similar to CS50x Finance)
- Record income and expenses.
- Dashboard for financial overview

## Future Enhancements if possible
- Filters by date, category, or amount
- Charts and graphs
- Export/import to CSV
- Profit calculation
- Tax tracking
- And more

## Technologies
- Python
- Flask
- SQLite
- Bootstrap (for quick web design)

## Installation
1. Clone the repository.
2. Install dependencies: `pip install -r requirements.txt`
3. Run the app: `flask run`

## Usage
- Register a new user account.
- Log in to access the application.
- Add income or expense entries.
- View the dashboard for financial summaries.

## Decision making
- As stated in a comment in layout.html, I'm using Bootstrap 5 Quick Snippets Extension
by publisher:"Anbuselvan Annamalai" for quicker html generation.
- As I'm not that familiar with Flask yet, reusing some code from problem set 9 'finance', from
cs50x(2026)
- Tried to use GitHub Copilot Agent, integrated with VSCode, but as for today on May 2026, tokens ran out extremely fast. I was able to write only layout.html and welcome.html with it. Switching to Web Based Chats like ChatGPT, Claude and Gemini. Aside from layout.html and welcome.html, I'm not copying code but, instead, asking AI for sintax corrections, tools, decorators, libraries, etc.
- I wanted to try some kind of encryption to make data inaccesible even to the administrator,
but after some research, seems like end to end encryption would make the backend harder or
even imposible as per my quick investigation. I would need a deeper research to find a solution.
For now, the data will be accesible by the admin.
