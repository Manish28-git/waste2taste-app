Waste2Taste 🍲
Waste2Taste is a full-stack web application designed to combat food waste by connecting food donors with those in need. Built with a Flask backend and a dynamic HTML/CSS/JavaScript frontend, this platform allows users to post surplus food items, which can then be viewed and claimed by others in the community.

✨ Features
User Authentication: Secure user registration and login system using JWT (JSON Web Tokens).

Role-Based Access Control: Distinct roles for Donors (who can create posts) and Receivers (who can claim posts).

Food Posting: Donors can create detailed posts for surplus food, including descriptions, quantity, location, and an expiry time.

View & Claim: Users can browse all available (unclaimed and unexpired) food posts. Logged-in users can claim an item with a single click.

Donor Dashboard: A personal dashboard for donors to view the status of their posts (Available/Claimed) and delete them.

Receiver Dashboard: A personal dashboard for receivers to view a history of all the items they have successfully claimed.

Automated Cleanup: A background scheduler automatically removes posts from the database once they have expired.

User Profiles: Users can add and update additional profile information like their full name and default location.

🛠️ Tech Stack
Backend: Flask, Flask-SQLAlchemy, Flask-JWT-Extended

Database: SQLite (for development)

Frontend: HTML, Tailwind CSS, Vanilla JavaScript

Background Jobs: APScheduler

🚀 Getting Started
Follow these instructions to get a local copy of the project up and running for development and testing.

Prerequisites
Make sure you have the following installed on your system:

Python 3.10+

pip (Python package manager)

Git

Installation & Setup
Clone the repository:

git clone https://github.com/your-username/waste2taste-app.git
cd waste2taste-app

Create and activate a virtual environment:

# For Windows
python -m venv venv
venv\Scripts\activate

# For macOS/Linux
python3 -m venv venv
source venv/bin/activate

Install the required dependencies:

pip install -r requirements.txt

Run the application:

python app.py

The application will start on http://127.0.0.1:5000. The first time you run it, a waste2taste.db database file will be created automatically.