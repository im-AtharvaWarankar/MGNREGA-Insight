# 🌏 CivicView - MGNREGA Transparency Dashboard

> **Empowering Public Accountability Through Data Transparency**

A comprehensive web application for visualizing and analyzing MGNREGA (Mahatma Gandhi National Rural Employment Guarantee Act) performance data across Indian states and districts. Built to promote government transparency and enable citizens to monitor employment guarantee scheme implementation.

---

## 📋 Table of Contents

- [Introduction](#-introduction)
- [Features](#-features)
- [Technology Stack](#-technology-stack)
- [Getting Started](#-getting-started)
- [Usage Guide](#-usage-guide)
- [API Documentation](#-api-documentation)
- [Contributing](#-contributing)

---

## 🎯 Introduction

MGNREGA (Mahatma Gandhi National Rural Employment Guarantee Act) is one of India's largest social security schemes, guaranteeing 100 days of wage employment to rural households. **CivicView** makes MGNREGA data accessible, transparent, and actionable for:

- **Citizens**: Monitor scheme implementation in their districts
- **Researchers**: Analyze employment trends across regions
- **Policy Makers**: Identify underperforming areas needing intervention
- **Civil Society**: Promote accountability in government programs

### What Makes CivicView Different?

✅ **Simple & Intuitive** - No technical knowledge required  
✅ **Real-time Insights** - Track current month performance  
✅ **Historical Analysis** - View trends over 36 months  
✅ **District Comparison** - Benchmark multiple regions  
✅ **Performance Indicators** - Clear ratings (Good/Average/Poor)

---

## ✨ Features

### 1. 📍 District Dashboard
- View current month performance for any district
- Key metrics: Person-days, Households worked, Wages paid, Material expenditure
- Performance rating with clear visual indicators

### 2. 📊 Historical Trends
- Analyze 6, 12, 24, or 36 months of historical data
- Interactive charts showing employment trends
- Month-over-month comparison

### 3. 🔄 District Comparison
- Compare multiple districts side-by-side
- Benchmark performance across states
- Identify best practices and underperforming regions

### 4. 🗺️ Multi-State Coverage
Currently tracking **40 districts** across **8 major states**:
- Uttar Pradesh
- Maharashtra  
- Bihar
- West Bengal
- Madhya Pradesh
- Rajasthan
- Tamil Nadu
- Karnataka

---

## 🛠️ Technology Stack

### Backend
- **Django 5.0.4** - Python web framework
- **Django REST Framework** - API development
- **PostgreSQL 14** - Database
- **Redis 7** - Caching & task queue
- **Celery** - Asynchronous task processing

### Frontend
- **React 18** - UI library
- **Vite 5** - Build tool & dev server
- **Recharts** - Data visualization
- **Axios** - HTTP client

### Infrastructure
- **Docker & Docker Compose** - Containerization
- **Nginx** - Web server & reverse proxy

---

## 🚀 Getting Started

### Prerequisites

- **Docker** & **Docker Compose** (recommended)
- OR: Python 3.12+, PostgreSQL 14+, Redis 7+, Node.js 18+

### Quick Start with Docker (Recommended)

1. **Clone the repository**
   ```bash
   git clone https://github.com/your-username/civicview-mgnrega.git
   cd civicview-mgnrega
   ```

2. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env and update with your settings (especially DJANGO_SECRET_KEY)
   ```

3. **Start all services**
   ```bash
   docker-compose up -d
   ```

4. **Run database migrations**
   ```bash
   docker exec nrega-backend python manage.py migrate
   ```

5. **Create sample data** (40 districts with 36 months of performance data)
   ```bash
   docker exec nrega-backend python create_sample_data.py
   ```

6. **Create admin user**
   ```bash
   docker exec -it nrega-backend python manage.py createsuperuser
   ```

7. **Access the application**
   - **Frontend Dashboard**: http://localhost:3000
   - **Backend API**: http://localhost:8000/api/
   - **Django Admin**: http://localhost:8000/admin
   - **API Documentation**: http://localhost:8000/swagger/

### Manual Setup (Without Docker)

<details>
<summary>Click to expand manual installation steps</summary>

#### Backend Setup

1. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up PostgreSQL database**
   ```bash
   createdb nrega_db
   ```

4. **Configure environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your database credentials and secret key
   ```

5. **Run migrations**
   ```bash
   python manage.py migrate
   ```

6. **Create sample data**
   ```bash
   python create_sample_data.py
   ```

7. **Start Redis** (in separate terminal)
   ```bash
   redis-server
   ```

8. **Start Celery worker** (in separate terminal)
   ```bash
   celery -A src worker -l info
   ```

9. **Start development server**
   ```bash
   python manage.py runserver
   ```

#### Frontend Setup

1. **Navigate to frontend directory**
   ```bash
   cd frontend
   ```

2. **Install dependencies**
   ```bash
   npm install
   ```

3. **Start development server**
   ```bash
   npm run dev
   ```

4. **Access frontend**: http://localhost:3000

</details>

---

## 📖 Usage Guide

### Viewing District Performance

1. Open the dashboard at http://localhost:3000
2. Select a district from the dropdown menu
3. View current month metrics:
   - Person-days generated
   - Households provided work
   - Total wages paid
   - Material expenditure
4. Check the performance badge (Good ✅ / Average 😐 / Poor ❌)

### Analyzing Historical Trends

1. Navigate to the **History** page
2. Select a district from the dropdown
3. Choose time period (6, 12, 24, or 36 months)
4. Analyze trends through interactive line charts
5. Observe seasonal patterns and long-term improvements

### Comparing Districts

1. Go to the **Comparison** page
2. Select multiple districts (2-5 districts recommended)
3. Choose metrics to compare:
   - Person-days
   - Households worked
   - Total wages
   - Material expenditure
4. Review side-by-side bar charts
5. Identify best performers and underperforming regions

---

## 🔌 API Documentation

### Base URL
```
http://localhost:8000/api/
```

### Endpoints

#### Health Check
```http
GET /api/health/
```
Returns system health status, database & Redis connectivity.

**Response:**
```json
{
  "data": {
    "status": "ok",
    "database": true,
    "redis": true,
    "timestamp": "2025-10-26T00:00:00Z"
  }
}
```

#### List Districts
```http
GET /api/districts/?limit=100
```
Returns paginated list of all districts.

**Response:**
```json
{
  "data": {
    "count": 40,
    "results": [
      {
        "id": 1,
        "name": "Lucknow",
        "code": "UP-LKO-001",
        "state": "Uttar Pradesh",
        "population": 4589838
      }
    ]
  }
}
```

#### District Details
```http
GET /api/districts/{id}/
```
Returns detailed information for a specific district including current month performance.

#### District Performance History
```http
GET /api/districts/{id}/performance-history/?months=12
```
Returns performance data for the last N months.

**Parameters:**
- `months` (optional): Number of months to retrieve (default: 12, max: 36)

#### Compare Districts
```http
POST /api/compare/
Content-Type: application/json

{
  "districtIds": [1, 2, 3],
  "months": 6
}
```
Returns comparison data for multiple districts over specified time period.

**Full Interactive API Documentation**: http://localhost:8000/swagger/

---

## 📊 Data Model

### District Model
```python
{
  "id": Integer,
  "name": String,
  "code": String (unique),
  "state": String,
  "population": Integer,
  "createdAt": DateTime,
  "updatedAt": DateTime
}
```

### Performance Model
```python
{
  "id": Integer,
  "districtId": ForeignKey(District),
  "year": Integer,
  "month": Integer,
  "personDays": Integer,
  "householdsWorked": Integer,
  "totalWages": Decimal,
  "materialExpenditure": Decimal,
  "createdAt": DateTime,
  "updatedAt": DateTime
}
```

---

## 🤝 Contributing

We welcome contributions! Here's how you can help:

1. **Fork the repository**
2. **Create a feature branch**
   ```bash
   git checkout -b feature/amazing-feature
   ```
3. **Make your changes**
   - Add new features
   - Fix bugs
   - Improve documentation
4. **Commit with meaningful messages**
   ```bash
   git commit -m 'Add: Feature to export district reports'
   ```
5. **Push to your fork**
   ```bash
   git push origin feature/amazing-feature
   ```
6. **Open a Pull Request**

### Development Guidelines

- **Python**: Follow PEP 8 style guide
- **JavaScript/React**: Use ESLint and Prettier
- **Commits**: Write clear, concise commit messages
- **Tests**: Add tests for new features
- **Documentation**: Update README and API docs

---

## 🔒 Security Note

⚠️ **Important**: Never commit sensitive credentials to the repository!

- Use `.env` file for secrets (already in `.gitignore`)
- Generate a new `DJANGO_SECRET_KEY` for production
- Change default database passwords
- Keep AWS credentials private

---

## 📄 License

This project is licensed under the MIT License - free to use, modify, and distribute.

---

## 🙏 Acknowledgments

- MGNREGA official data structure and guidelines
- Built to promote transparency in public welfare schemes
- Inspired by India's Right to Information Act (RTI)

---

## 📧 Support & Contact

- **Issues**: [Report bugs or request features](https://github.com/your-username/civicview-mgnrega/issues)
- **Discussions**: [Join community discussions](https://github.com/your-username/civicview-mgnrega/discussions)

---

**Made with ❤️ for transparency in governance**
