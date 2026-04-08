# URL Shortener - Mini Project Report

## 1. Project Overview
This project is a full-stack **URL Shortener** web application. Its primary goal is to take a long, complicated URL and convert it into a short, easy-to-share link. When a user clicks or navigates to the shortened link, the application intercepts the request and redirects the user to the original long URL. 

The project is structured with a decoupled architecture, separating the backend logic from the frontend user interface, and uses a NoSQL database for storage.

## 2. System Architecture & Components

The system follows a standard Client-Server architecture, containerized for easy deployment, consisting of three main components:

### A. Frontend (Streamlit)
* **File:** `frontend/app.py`
* **Purpose:** Provides the User Interface (UI).
* **Functionality:** 
  * Displays a simple, centralized dashboard (`🔗 URL Shortener`) using Streamlit.
  * Contains a text input for the user to paste their long URL.
  * When the "Shorten URL" button is clicked, it sends a REST API `POST` request (using the `requests` library) to the backend.
  * Displays the resulting generated short URL or an error if the request fails.

### B. Backend Server (FastAPI)
* **Files:** `backend/main.py`, `backend/models.py`, `backend/database.py`
* **Purpose:** Handles the core business logic, random code generation, and URL redirection.
* **Functionality:**
  * **Generation (`POST /shorten`):** Accepts a long URL, validates it using **Pydantic**, and generates a random 6-character alphanumeric short code. It stores the mapping (along with a creation timestamp, expiration date, and click count) in the database.
  * **Redirection (`GET /{short_code}`):** Listens for requests to short links. It looks up the short code in the database. If found, it issues a `302 Redirect` to route the browser to the original long URL. If not found, it returns a `404 Not Found` error.

### C. Database (MongoDB)
* **File:** `backend/database.py`
* **Purpose:** Persistent storage for URL mappings.
* **Functionality:** Uses MongoDB (typically hosted on MongoDB Atlas). It stores documents inside a collection named `urls`.
* **Data Stored:** 
  * `short_code` (e.g., "aB3dE9")
  * `long_url` (The original URL)
  * `created_at` (Timestamp of creation)
  * `expires_at` (Optional expiration metric)
  * `clicks` (Analytics counter - initialized at 0)

## 3. Technology Stack Used

* **Language:** Python 3.9+
* **Backend Framework:** **FastAPI** (Chosen for its high performance, automatic documentation, and native async support).
* **Server Gateway:** **Uvicorn** (Asynchronous ASGI server to run the FastAPI application).
* **Frontend Framework:** **Streamlit** (A Python-based framework ideal for rapidly building data-driven web applications).
* **Database:** **MongoDB** (A NoSQL document database).
* **Database Driver:** **Motor** (`motor-asyncio` - An asynchronous Python driver for MongoDB, ensuring non-blocking operations).
* **Data Validation:** **Pydantic** (Used in `models.py` to enforce that submitted URLs are valid `HttpUrl` formats).
* **Environment Management:** `python-dotenv` (To manage secrets securely).
* **Containerization:** **Docker & Docker Compose** (`Dockerfile` & `docker-compose.yml` to package the frontend and backend into isolated, reproducible containers).

## 4. Flow of Execution (How it works)

1. **User Input:** The user opens the Streamlit frontend UI on port `8501` and pastes a long URL.
2. **API Call:** Streamlit sends a JSON payload to the FastAPI backend over port `8000`.
3. **Code Generation:** FastAPI processes the request, generates a random 6-character string (e.g., `Xy7p2Q`), and saves `{ "short_code": "Xy7p2Q", "long_url": "..." }` into MongoDB using the Motor async client.
4. **Display:** FastAPI responds with the URL `http://your_domain_name/Xy7p2Q`. Streamlit displays this to the user.
5. **Redirection:** If someone pastes `http://your_domain_name/Xy7p2Q` in their browser, the FastAPI backend intercepts `GET /Xy7p2Q`, queries MongoDB for `Xy7p2Q`, retrieves the original URL, and redirects the browser.

## 5. Key Concepts Highlighted

* **Asynchronous Programming:** Utilizing Python's `async/await` syntax extensively (via FastAPI and Motor) to ensure the server can handle multiple requests concurrently without blocking.
* **Microservices Concept:** Decoupling the User Interface (Streamlit container) from the Backend API (FastAPI container).
* **RESTful API Design:** Implementing standard HTTP methods (`POST` for creation, `GET` for fetching/redirecting).
* **Containerization:** Using `docker-compose` allows a developer to spin up the entire multi-service application with a single command (`docker-compose up`).