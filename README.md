# Job & Internship Application Tracker

**Job & Internship Application Tracker** is a full-stack Django web application designed to help students manage and track job and internship applications. Users can add applications, view details and deadlines, mark applications as completed using AJAX without reloading the page, and delete applications.

---

## 🚀 Features

- **Add Job & Internship Applications**: Easy-to-use HTML form to submit new applications with company name, role title, details, and application deadlines.
- **View Applications Dashboard**: Overview of all tracked applications with live statistics counters (Total, Pending, Completed).
- **Track Deadlines**: Clear display of deadlines formatted in `DD-MM-YYYY`.
- **Mark Completed via AJAX**: Instant status updates from *Pending* to *Completed* using JavaScript `fetch()` without reloading the web page.
- **Delete Applications**: Remove applications from both the SQLite database and the UI dynamically.
- **CSRF Protection**: Native Django CSRF token integration across form submissions and AJAX requests.
- **Responsive & Modern UI**: Built with CSS3 dark mode aesthetics, glassmorphism cards, Google Fonts (`Inter` & `Outfit`), and FontAwesome icons.

---

## 🛠️ Technologies Used

- **Backend**: Python 3.11, Django 5.2 (MVT Pattern)
- **Database**: SQLite3
- **Frontend**: HTML5, CSS3 (Modern Flex/Grid Layout & Custom Theme), JavaScript (Fetch API / AJAX)
- **Version Control**: Git / GitHub

---

## ⚙️ Installation & Setup Instructions

### Prerequisites
- Python 3.10+ installed
- Git installed

### 1. Clone the Repository
```bash
git clone https://github.com/greeshma1376/Job_Application_Tracker.git
cd Job_Application_Tracker
```

### 2. Create and Activate Virtual Environment (Optional but recommended)
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/macOS
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install django
```

### 4. Apply Database Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

---

## 💻 How to Run the Project

Run the Django development server:

```bash
python manage.py runserver
```

Open your browser and navigate to:
```
http://127.0.0.1:8000/
```

---

## 📸 Screenshots Section

### Main Dashboard & Application List
![Main Dashboard](docs/screenshots/dashboard.png)

### Add Application Form
![Add Application Form](docs/screenshots/add_application.png)

### AJAX Completion & Deletion
![AJAX Completion](docs/screenshots/ajax_completion.png)

---

## 📝 License
This project is created for practical examination and educational purposes.
