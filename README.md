# 📻 Radio Nabra (راديو نبرة)

A modern, bilingual web platform built specifically for podcast streaming and digital journalism. Designed with a focus on user experience, lightning-fast performance, and elegant aesthetics.

## ✨ Key Features
* **Super Premium UI/UX:** Fully customized interface with a seamless, animated Dark/Light mode toggle.
* **Optimized Performance:** Utilizes Tailwind CSS CLI for a purged, minimal CSS footprint (Zero render-blocking scripts).
* **Media-Rich Content:** Dedicated sections for reading articles and streaming podcast episodes.
* **Fully Responsive:** Flawless experience across desktop, tablet, and mobile devices with a custom animated mobile drawer.

## 🛠️ Tech Stack
* **Backend:** Python 3, Django
* **Frontend:** HTML5, Tailwind CSS (CLI built), Vanilla JavaScript
* **Database:** SQLite (Development) / Ready for PostgreSQL (Production)

## 📸 Screenshots
*(Add a screenshot of the Light Mode here)*
*(Add a screenshot of the Dark Mode here)*

## 🚀 How to Run Locally

```bash
# 1. Clone the repository
git clone [https://github.com/yourusername/radionabra.git](https://github.com/yourusername/radionabra.git)

# 2. Create and activate a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows use: .\venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run the Tailwind CLI (In a separate terminal)
npx @tailwindcss/cli -i ./static/css/input.css -o ./static/css/output.css --watch

# 5. Run the development server
python manage.py runserver