# ⚽ Top Transfers

A football transfer tracking web application built with Django.

🌐 **Live Demo:** [https://toptransfersbyasadbek.pythonanywhere.com](https://toptransfersbyasadbek.pythonanywhere.com)

---

## 📌 Features

- Browse football clubs by country
- View latest transfers
- Player profiles and statistics
- U-20 players section
- Transfer stats including:
  - TOP-150 accurate predictions
  - Transfer records
  - TOP-50 clubs by expenditure
  - TOP-50 clubs by income
- Tryouts section

---

## 🛠️ Tech Stack

- **Backend:** Django 6.0
- **Database:** SQLite3
- **Frontend:** HTML, CSS, JavaScript
- **Deployment:** PythonAnywhere

---

## 🚀 Local Setup

```bash
# Clone the repository
git clone https://github.com/xamidovasadbekdev-arch/toptransfers.git
cd toptransfers

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
echo "SECRET_KEY=your-secret-key" > .env
echo "DEBUG=True" >> .env

# Run migrations
python manage.py migrate

# Run server
python manage.py runserver
```

---

## 📁 Project Structure

```
toptransfers/
├── config/         # Project settings
├── main/           # Main app (clubs, players, transfers)
├── stats/          # Statistics app
├── templates/      # HTML templates
├── static/         # CSS, JS, images
├── media/          # Uploaded files
└── requirements.txt
```

---

## 👨‍💻 Developer

**Xamidov Asadbek**
- 📧 xamidovasadbek.dev@gmail.com
- 📱 Telegram: [@homiidov](https://t.me/homiidov)
- 📸 Instagram: [@homiidov_](https://www.instagram.com/homiidov_/)
