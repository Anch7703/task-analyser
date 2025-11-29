Task Analyzer — Smart Task Prioritization System
A full-stack task analysis and prioritization tool built using Django (backend) and HTML/CSS/JavaScript (frontend).
It evaluates tasks based on urgency, importance, dependencies, estimated hours, and priority strategy — returning a detailed score and explanation for each task.

This project was created as part of an internship assignment to demonstrate backend logic, APIs, scoring algorithms, and frontend integration.

Live Features
Backend (Django + DRF)
/api/tasks/analyze/ — Analyze custom tasks

/api/tasks/suggest/ — Suggest tasks based on stored data

Strategy-based scoring:
Smart Balance
Fastest Wins
High Impact
Deadline Driven

Dependency impact handling
Urgency, importance & quickness calculations
CORS enabled

Frontend (HTML/CSS/JS)
Add tasks manually
Paste JSON directly

Select strategy
Click Analyze / Suggest
Cyberpunk-themed UI
Toast notifications
Dynamic results rendering

How It Works
1. User inputs tasks
Each task includes:
Title
Due date
Estimated hours
Importance (1–10)
Dependencies

2. User picks a strategy
Each strategy weighs the task factors differently.

3. Backend calculates scores
Using algorithms for:
Urgency (based on due date)
Importance
Quickness
Dependency load
Selected strategy

4. Frontend displays ranked tasks
Beautiful UI showing:
Score
Explanation
Due date
Priority level
