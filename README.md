🏗️ MGNREGA Insight (CivicView Dashboard)
Empowering citizens with data transparency for rural employment initiatives
🧩 Overview

MGNREGA Insight (CivicView Dashboard) is a public web platform designed to make MGNREGA (Mahatma Gandhi National Rural Employment Guarantee Act) data more understandable and accessible to every citizen.

While the Government of India provides MGNREGA statistics through APIs, the data is often raw and difficult to interpret. This platform simplifies that, allowing users to explore district-level performance metrics, visualized insights, and key comparisons in an intuitive interface.

The project aims to promote data-driven transparency and citizen awareness about rural employment schemes.

🌟 Key Features

📊 District Performance Dashboard:
Displays detailed metrics for each district — including work demand, person-days generated, fund utilization, and employment trends.

🌐 Data Visualization:
Interactive charts and graphs that help citizens quickly interpret government data.

🔎 Search & Filter System:
Filter data by state, district, time period, or performance indicators.

📅 Monthly Updates via Open APIs:
Automatically fetches real-time data from the official MGNREGA API for the selected month.

📱 Responsive Web App:
Optimized for both desktop and mobile devices, ensuring accessibility for all users.

💡 Future-Ready Architecture:
Modular backend and component-based frontend for easy scalability and feature expansion.

🧠 Use Case & Impact

Citizens:
Understand how well your district is performing under MGNREGA, in a simple and visual format.

Administrators & Researchers:
Gain analytical insights into fund usage, job card generation, and demand patterns.

Students & Developers:
Learn how real-world government data can be accessed, cleaned, and visualized.

⚙️ Tech Stack
Layer	Technologies Used
Frontend	React.js, Tailwind CSS, Chart.js / Recharts
Backend	Django REST Framework
Database	PostgreSQL / SQLite (dev mode)
Containerization	Docker, Docker Compose
Background Tasks	Celery + Redis (for scheduled API syncs)
Version Control	Git & GitHub
🧱 System Architecture

The platform follows a modular and scalable architecture:

Frontend:

Built using React + Tailwind CSS for a smooth and dynamic experience.

Consumes REST APIs for live data rendering.

Backend (Django + DRF):

Handles authentication, API integration, and data persistence.

Fetches and structures MGNREGA data into user-friendly models.

Database:

Stores processed data locally for efficient access and faster loading.

Background Scheduler (Celery):

Periodically refreshes data from government APIs to ensure the dashboard is always updated.

Containerized Deployment:

Fully Dockerized to ensure consistent setup across environments.

🧭 How to Use
For General Users

Visit the hosted application (link coming soon).

Select your State and District from the dropdown.

Instantly view performance metrics, charts, and insights.

Optionally compare different months or districts.

For Developers (Local Setup)

Clone the repository

git clone https://github.com/<your-username>/mgnrega-insight.git
cd mgnrega-insight


Build and run containers

docker-compose up --build


Access the web app at

http://localhost:8000

🧩 API Integration

The platform connects to the Government of India’s MGNREGA Open Data API.

Data fetched includes metrics such as:

Total person-days generated

Total households employed

Fund allocation and expenditure

Gender-wise work participation

APIs are parsed, validated, and cached to ensure smooth visualizations.

🚀 Future Enhancements

Add AI-based anomaly detection for fund misuse or irregular patterns.

Introduce Geo-visualization maps to show spatial patterns in employment.

Add User Authentication for saved dashboards and custom alerts.

Implement Offline Data Mode for rural users with limited connectivity.

Enable Public Data Export (CSV, PDF) for researchers and policymakers.
