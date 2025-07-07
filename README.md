#  WatchMate DRF API

A Django REST Framework-based backend API , my first learning project in DRF for managing streaming platforms, watchlists, and user reviews.

##  Features

- Token Authentication
- CRUD operations for:
  - Streaming Platforms
  - Watchlist Items (Movies/Series)
  - Reviews with user-specific control
- Admin-only access to create/update/delete Platforms & Watchlists
- Pagination, ordering, and filtering support for listings

##  Technologies

- Django 5.x
- Django REST Framework
- SQLite 
- Token Authentication

##  API Endpoints

| Endpoint                                         | Method | Access        | Description                            |
|--------------------------------------------------|--------|---------------|----------------------------------------|
| `/api/account/register/`                         | POST   | Public        | Register new users                     |
| `/api/account/login/`                            | POST   | Public        | Obtain auth token                      |
| `/api/account/logout/`                           | POST   | Authenticated | Logout (invalidate token)             |
| `/api/platforms/`                                | GET    | Public        | List all streaming platforms           |
| `/api/platforms/`                                | POST   | **Admin only**| Create new streaming platform          |
| `/api/platforms/<id>/`                           | GET    | Public        | Retrieve platform by ID                |
| `/api/platforms/<id>/`                           | PUT/DELETE | **Admin only**| Update or delete a platform        |
| `/api/watchlist/`                                | GET    | Public        | List all watchlist items               |
| `/api/watchlist/`                                | POST   | **Admin only**| Create new watchlist item              |
| `/api/watchlist/<id>/`                           | GET    | Public        | Retrieve watchlist item by ID          |
| `/api/watchlist/<id>/`                           | PUT/DELETE | **Admin only**| Update or delete watchlist item    |
| `/api/watchlist/<id>/reviews/`                   | GET    | Public        | View all reviews for a watchlist item  |
| `/api/watchlist/<id>/reviews/`                   | POST   | Authenticated | Create a review (one per user/item)    |
| `/api/reviews/<id>/`                             | GET    | Public        | View single review                     |
| `/api/reviews/<id>/`                             | PUT/DELETE | Review Owner | Update/delete own review           |
| `/api/watchlist/reviews/by-user/?username=<username>` | GET | Public    | Get all reviews by a specific user     |

> ⚠️ **Note:** All POST/PUT/DELETE operations on `platforms` and `watchlist` endpoints are restricted to admin users only.

---

## 🚀 Local Setup (Clone & Run)

```bash
git clone https://github.com/tyb01/watchmate-drf-api.git
cd watchmate-drf-api
python -m venv venv
source venv/bin/activate        # On Windows: venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```
---
##  Running Tests

```bash
python manage.py test
