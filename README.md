# Cinema RDBMS (Python + MySQL)

A cinema booking system demonstrating relational database design, SQL joins,
and CRUD operations using Python and MySQL.

## Features
- Relational schema (movies, screens, showtimes, bookings)
- Primary & foreign keys
- SQL JOIN queries
- REST API built with Flask

## Schema Overview

Movie ───< Showtime >─── Screen  
              |  
              v  
           Booking  

## Tech Stack
- Python
- MySQL
- Flask
- SQL

## Setup (Local)

1. Create database and user in MySQL
2. Load `schema.sql`
3. Install dependencies from `requirements.txt`
4. Run `app.py`

## Credits
- Author: Franklin Okoth Agina
