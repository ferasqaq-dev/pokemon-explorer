# PokéExplorer ⚡

A modern, full-featured Pokémon Explorer web application built with Django and Bootstrap 5, powered by the PokeAPI.

## 🚀 Features Implemented

- **Authentication System**: Secure User Registration, Login, and Logout functionality.
- **Interactive Dashboard**: Dynamically fetches and renders the first 20 Pokémon from PokeAPI.
- **Pokémon Search**: Instant backend filtering allowing users to search by name.
- **Sleek Detail Views**: Explore comprehensive stats, base experience, height, weight, and official artwork for each creature.
- **Premium Favorite System**:
  - Seamless **AJAX toggles via Fetch API** (No page refreshes!).
  - Dedicated **"My Favorites" dashboard** with interactive animation removals.
  - Strict database-level integrity constraints to prevent duplicates.
- **Performance Optimizations**: Implemented **Django Local Memory Caching** for API responses to reduce network overhead and ensure blazing-fast load times.
- **Robust Unit Tests**: Automated test suites covering core authentication views and model constraints.

## 🛠️ How to Run Locally

Follow these clear, step-by-step commands to get the project up and running on your local machine:

### 1. Clone the repository

```bash
git clone https://github.com/ferasqaq-dev/pokemon-explorer
```

### 2. Set up the Virtual Environment & Install Dependencies

Ensure your development environment is isolated cleanly before installing core project packages:

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Apply Migrations & Start Server

Set up the SQLite local database schemas and execute the development server:

```bash
python manage.py migrate
python manage.py runserver
```

Once initialized, open your browser and head over to: http://127.0.0.1:8000/

🧪 Running Tests
To trigger the automated test execution suite and verify system logic integrity, run:

```bash
python manage.py test
```
