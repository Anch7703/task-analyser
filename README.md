Task Analyzer
A full-stack task prioritization system built using Django (backend) and HTML/CSS/JavaScript (frontend).
It analyzes tasks based on urgency, importance, estimated hours, and dependencies, and ranks them using different priority strategies.

Features
Backend (Django + DRF)
/api/tasks/analyze/ — Analyze custom tasks
/api/tasks/suggest/ — Get suggested tasks
Strategies: Smart Balance, Fastest Wins, High Impact, Deadline Driven
Handles urgency, importance, quickness & dependency load
Clean JSON responses

Frontend
Add tasks manually or via JSON
Choose strategy
Cyberpunk-styled UI
Displays score, explanation, and due date
Toast notifications

Setup

cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python manage.py runserver
Then open:
frontend/index.html

Structure

task-analyser/
├── backend/
├── frontend/
└── requirements.txt
Tech Stack
Django
Django REST Framework
JavaScript (Fetch API)

Author
Anchal L. Kolkar
Task management, full-stack logic & cyberpunk UI enthusiast 😈🔥
