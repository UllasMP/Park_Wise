# ParkWise

ParkWise is a simple parking management system for handling vehicle entry, parking slots, exit, payments, and daily parking data.

## Features

- Add vehicle entry
- Automatically assign a parking slot
- Support for two-wheelers and four-wheelers
- Separate parking areas for Gate A and Gate B
- View available, occupied, and blocked slots
- Search a vehicle or ticket at exit
- Calculate parking fees
- Record payments
- View parking dashboard and gate-wise collection
- Block or unblock parking slots

## Tech Stack

- Frontend: React + Vite
- Backend: Django
- Database: SQLite

## Project Structure

```text
parkwise/
├── backend/       # Django API and parking rules
├── frontend/      # React user interface
└── docs/          # Project documentation
Run the Project

BACKEND
--------------------------------------------
cd parkwise/backend
pip install -r requirements.txt
python manage.py migrate
python manage.py seed_data
python manage.py runserver

Frontend
----------------------------------------------
Open another terminal:
cd parkwise/frontend
npm install
npm run dev

Then open the frontend URL shown in the terminal, usually:
http://localhost:5173

Testing
-----------------------------------------------
cd parkwise/backend
python manage.py test

Parking Fee Rules
- Two-wheeler: ₹30 for the first 2 hours
- Four-wheeler: ₹50 for the first 2 hours
- Extra hourly charges apply after 2 hours
- A daily maximum charge is applied for longer stays

Author
Ullas MP
