# 📚 PeerTutor

A peer-to-peer tutoring marketplace built with Django where students can find, 
message, and book sessions with verified tutors.

## Features
- 🔍 Browse and search tutors by subject and rate
- 💬 Real-time messaging between students and tutors
- 📅 Session booking and management
- ⭐ Reviews and ratings system
- 👨‍👩‍👧 Parent portal
- 🏆 Badges and achievements *(coming soon)*

## Tech Stack
- **Backend:** Django 6, Python 3.14
- **Database:** PostgreSQL (production), SQLite (development)
- **Frontend:** Bootstrap 5, vanilla JavaScript
- **Deployment:** Railway

## Setup locally
```bash
git clone https://github.com/yourusername/peer-tutoring.git
cd peer-tutoring
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```