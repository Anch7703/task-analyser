Smart Task Analyzer
A full-stack task-prioritization system built using Django (backend) and HTML/CSS/JavaScript (frontend).
It evaluates urgency, importance, estimated hours, and dependencies to compute a priority score using multiple strategies.

1. Setup Instructions
Backend Setup
cd backend
python -m venv venv
venv\Scripts\activate     # Windows
pip install -r requirements.txt
python manage.py runserver
Backend runs at:
http://127.0.0.1:8000
Frontend Setup
Simply open:
frontend/index.html
in any browser.
No additional dependencies needed.

2. Algorithm Explanation (300–500 words)
The Smart Task Analyzer computes a priority score for each task based on four core factors: urgency, importance, quickness, and dependency load. The goal is to create a scoring formula flexible enough to work across multiple strategies while still remaining intuitive, transparent, and easy to modify.

Urgency is derived from the task’s due date. Tasks closer to today have a higher urgency score, while tasks with no due date default to a moderate baseline. The urgency calculation normalizes days remaining into a 0–1 scale, ensuring consistency across different date ranges.

Importance is handled directly using the user’s 1–10 rating. This value is normalized into a 0–1 scale for consistency within the scoring formulas.

Quickness represents how “light” a task is. A task requiring fewer hours receives a higher quickness score. This is calculated as 1 / estimated_hours (normalized), allowing the system to naturally favor short tasks in certain strategies.

Dependency load accounts for tasks blocked by other tasks. A task with many dependencies has a lower dependency score. For normalization, dependency counts are scaled relative to the maximum dependency count in the current set, preventing division-by-zero errors and balancing tasks proportionally.

Once these base scores are computed, the system applies one of four priority strategies:

1. Smart Balance (default)
Balances all factors:
0.35 * importance + 0.30 * urgency + 0.20 * quickness + 0.15 * dependencies
Useful when all factors matter equally.

2. Fastest Wins
Favors quick tasks:
0.6 * quickness + 0.2 * urgency + 0.2 * importance
Great for productivity boosts.

3. High Impact
Favors tasks with high importance:
0.7 * importance + 0.2 * dependency + 0.1 * urgency
Useful for major deliverables.

4. Deadline Driven
Favors tasks with the nearest due date:
0.7 * urgency + 0.2 * importance + 0.1 * quickness
Each strategy returns a numeric score and an explanation string, helping users understand why a task is ranked a certain way.
This hybrid approach provides both flexibility and clarity while keeping the system easy to extend.

3. Design Decisions
Separate backend and frontend for clarity and easier debugging.
Used Django + DRF because it provides structured serialization and clean REST endpoints.
Chose simple JSON communication to keep integration lightweight.
Designed scoring to be modular, allowing new strategies to be added easily.
Implemented CORS to allow local HTML files to communicate with Django during development.

4. Time Breakdown
Task	Time Spent
Setting up Django project	 20mins
Building API endpoints	45mins
Scoring logic & strategy formulas	45mins
Frontend UI (cyberpunk theme)	50mins
Fetch integration & bug fixing	20mins
Testing & polishing	20mins
README + documentation	15mins

Total: ~ 3 hours 35 mins

Bonus Challenges Attempted:
Multiple Priority Strategies
(Smart Balance, Fastest Wins, High Impact, Deadline Driven)
Detailed Explanation Strings
(shows importance, urgency, quickness, dependencies)
Dependency Handling in Scoring
JSON Input Support
(paste JSON directly)
UI Enhancements
(cyberpunk theme, colored priority boxes — they LOVE this)
Toast Notifications
(for user feedback)

6. Future Improvements
If given more time, I would like to add:
User authentication + saved task history
A database-backed task manager (CRUD operations)
Weighted strategies customizable by user
A progress dashboard with charts
Drag-and-drop UI for editing tasks
Deploy backend API publicly (Render / Railway)
Convert frontend into a full React app

Final Note
This project demonstrates scoring logic, backend API design, data processing, and UI integration — combining algorithmic thinking with clean implementation.
Author
Anchal L. Kolkar
Task management, full-stack logic & cyberpunk UI enthusiast 😈🔥
