# CivicView - MGNREGA Dashboard 🌾# 🌏 CivicView - MGNREGA Transparency Dashboard## Atomicloops Django Setup



Hey! This is a simple dashboard to check how well the MGNREGA scheme is working across India. Think of it like a report card for government employment programs - but way easier to understand!



## What's This About?> **Empowering Public Accountability Through Data Transparency**### Project-Name : <>



MGNREGA gives jobs to people in rural areas. This dashboard helps anyone see:

- How many jobs were created

- How much money was spentA comprehensive web application for visualizing and analyzing MGNREGA (Mahatma Gandhi National Rural Employment Guarantee Act) performance data across Indian states and districts. Built to promote government transparency and enable citizens to monitor employment guarantee scheme implementation.### 1. Clone the repository

- Which districts are doing well

- Which ones need help



No fancy government websites, no confusing reports - just clean, simple data.---```



## What Can You Do Here?git clone <url>



### 1. Check Your District 📍## 📋 Table of Contentscd <repo-name>

Pick any district from the dropdown and see:

- How many work days were created this monthgit checkout -b dev

- How many families got jobs

- How much wages were paid- [Introduction](#-introduction)```

- How much was spent on materials

- [Features](#-features)

Plus you get a simple badge: Good ✅ / Average 😐 / Poor ❌

- [Technology Stack](#-technology-stack)### 2. Install AWS CLI and configurations as per your os

### 2. See Historical Trends 📊

Want to know if things are getting better or worse? - [Project Structure](#-project-structure)

- Choose any district

- Pick how far back you want to look (6, 12, 24, or 36 months)- [Getting Started](#-getting-started)- [Install AWSCLI](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html)

- See nice charts that show the trends

- [Usage Guide](#-usage-guide)- [Install & Configure AWSCLI](https://medium.com/analytics-vidhya/configure-aws-cli-and-execute-commands-fc16a17b0aa2)

### 3. Compare Districts 🔄

Curious how your district compares to others?- [API Documentation](#-api-documentation)

- Pick multiple districts

- Choose what you want to compare (jobs, wages, etc.)- [Data Model](#-data-model)### 3. Create a new virtualenv and install requirements (Soon will be deprecated)

- See who's doing best and who needs improvement

- [Contributing](#-contributing)

That's it! Simple, right?

- [License](#-license)- [How to install virtualenv](./docs/Install%20Virtaulenv.pdf)

## The Tech Stuff (Don't Worry, It's Easy!)



**Backend:** Django + PostgreSQL (basically a Python website with a database)  

**Frontend:** React + Vite (the pretty interface you see)  ---#### Windows

**Charts:** Chart.js (makes those nice graphs)  



Everything runs in Docker containers, so you don't have to install a million things.

## 🎯 Introduction```

## How to Run This Thing

virtualenv venv

### What You Need

- Docker (it's like a box that runs everything for you)**CivicView** is a public-facing transparency dashboard that provides real-time insights into MGNREGA scheme performance across India. The platform enables citizens, researchers, and policymakers to:.\venv\Scripts\activate

- That's literally it!

pip install -r requirements.txt

### Step 1: Get the Code

```bash- **Monitor Performance**: Track key metrics like person-days generated, wages paid, and household employmentpip install "drf-yasg[validation]"

git clone <your-repo-url>

cd django-boilerplate- **Compare Districts**: Benchmark performance across multiple districts and statespip install git+https://github.com/atomic-loops/atomicloops-django-logger

```

- **Analyze Trends**: View historical data spanning 36 months to identify patterns```

### Step 2: Start Everything

```bash- **Promote Accountability**: Access transparent, up-to-date information on public welfare spending

docker-compose up -d

```#### Linux and Mac OS



Wait a minute... and boom! Backend is running.### Why CivicView?



### Step 3: Set Up the Database```

```bash

docker exec nrega-backend python manage.py migrateMGNREGA is one of the world's largest employment guarantee programs, affecting millions of rural households. CivicView bridges the information gap by:virtualenv venv

```

source venv/bin/activate

### Step 4: Create an Admin Account

```bash✅ **Making data accessible** - Complex government data presented in user-friendly visualizations  pip install -r requirements.txt

docker exec nrega-backend python manage.py shell -c "from users.models import Users; Users.objects.create_superuser(email='admin@civicview.com', password='admin123')"

```✅ **Enabling comparisons** - Side-by-side performance analysis across regions  pip install "drf-yasg[validation]"



Login: `admin@civicview.com` / `admin123`✅ **Tracking trends** - Historical data analysis to measure progress  pip install git+https://github.com/atomic-loops/atomicloops-django-logger



### Step 5: Load Some Data✅ **Supporting decisions** - Data-driven insights for policy improvements  ```

```bash

docker exec nrega-backend python create_sample_data.py

```

---### 4. Download vault file

This creates data for 95 districts across 19 states - 3 years worth!

Note: After downloading please update the vault file with your email credentials.

### Step 6: Start the Frontend

```bash## ✨ Features

cd frontend

npm install

npm run dev

```### 🏠 DashboardA. Initial



### Step 7: Open Your Browser 🎉- **District Selection**: Choose from 95 districts across 19 major Indian states```

Go to: **http://localhost:3001**

- **Key Metrics Cards**: wget -O src/vault.py https://atomicloops-dev.s3.ap-south-1.amazonaws.com/vault.py

That's it! You're done!

  - Person Days Generated```

## What Data Do We Have?

  - Households Employed  

**95 Districts** from these states:

- Andhra Pradesh (5 districts)  - Total Wages PaidWindows

- Assam (5 districts)

- Bihar (5 districts)  - Material Expenditure

- Chhattisgarh (5 districts)

- Gujarat (5 districts)- **Performance Status**: Color-coded badges (Good ≥80%, Average 50-79%, Poor <50%)```

- Haryana (5 districts)

- Jharkhand (5 districts)- **Month-over-Month Comparison**: Track performance changes with percentage indicatorscurl -o src/vault.py https://atomicloops-dev.s3.ap-south-1.amazonaws.com/vault.py

- Karnataka (5 districts)

- Kerala (5 districts)- **Indian Number Formatting**: Values displayed in Lakh/Crore notation```

- Madhya Pradesh (5 districts)

- Maharashtra (5 districts)

- Odisha (5 districts)

- Punjab (5 districts)### 📊 Historical AnalysisB. Latest

- Rajasthan (5 districts)

- Tamil Nadu (5 districts)- **Time Period Selection**: View data for 6, 12, 24, or 36 months

- Telangana (5 districts)

- Uttar Pradesh (5 districts)- **Interactive Charts**: Line and bar charts powered by Chart.js```

- Uttarakhand (5 districts)

- West Bengal (5 districts)- **Trend Visualization**: Identify seasonal patterns and long-term trendswget -O src/vault.py https://atomicloops-dev.s3.ap-south-1.amazonaws.com/vault.py



**36 Months of Data** for each district (November 2022 to October 2025)- **Metric Filtering**: Focus on specific performance indicators```



Total: **3,384 records** of real-looking performance data!



## Quick Links### 🔄 District ComparisonWindows



Once everything's running:- **Multi-District Selection**: Compare up to 10 districts simultaneously

- **Main Dashboard:** http://localhost:3001

- **Backend API:** http://localhost:8000/api/v1/mgnrega/- **Metric-Based Ranking**: Sort by any performance metric```

- **Admin Panel:** http://localhost:8000/admin

- **Cross-State Analysis**: Compare districts from different statescurl -o src/vault.py https://atomicloops-dev.s3.ap-south-1.amazonaws.com/vault.py

## The API (For Nerds 🤓)

- **Visual Charts**: Bar charts for easy performance comparison```

If you want to build something on top of this, here are the endpoints:

- **Comprehensive Table**: Detailed metrics with rank, district, state, and values

```bash

# Get all districtsNote :- Update the urls for Lastest Section when you sync the vault file.

GET /api/v1/mgnrega/districts/

### 🎨 User Experience

# Get one district

GET /api/v1/mgnrega/districts/1/- **Responsive Design**: Works seamlessly on desktop, tablet, and mobile### 5. Initialize Project Setup



# Get district summary for a month- **Error Handling**: Graceful error boundaries with user-friendly messages

GET /api/v1/mgnrega/summary/?district_id=1&year=2025&month=10

- **Loading States**: Clear feedback during data fetching[Setup Email Password](http://165.232.181.62/books/backend-development/page/generate-password-for-automated-e-mail)

# Get historical data

GET /api/v1/mgnrega/history/?district_id=1&from=2024-11&to=2025-10- **Accessibility**: WCAG-compliant color contrasts and semantic HTML



# Compare districts- **Fast Performance**: Optimized API calls and React component rendering[Atomicloops Django Setup](./docs/ProjectSetup.pdf)

GET /api/v1/mgnrega/compare/?district_ids=1,2,3&year=2025&month=10&metric=person_days

```



All responses come in this format:---[Atomicloops Custom Commands with Bash](http://165.232.181.62/books/backend-development/page/django-atomicloops-commands-bash)

```json

{

  "data": { /* your data here */ },

  "error": {},## 🛠️ Technology Stack[Atomicloops Custom Commands python](https://drive.google.com/file/d/1dKK_Eo-7OAAFYTrEtS_N5pQGDLK06Y-a/view?usp=share_link)

  "isSuccess": true

}

```

### Backend### 6. Makemigrations and Create Table

## How the Data Works

- **Django 5.0.4** - Modern Python web framework

We track 4 main things for each district every month:

- **Django REST Framework (DRF)** - RESTful API development```

1. **Person Days** - Total work days given to people

2. **Households** - How many families got work- **PostgreSQL 14** - Robust relational database./run.sh start-dev

3. **Wages** - Money paid to workers (shown in Lakhs/Crores)

4. **Materials** - Money spent on materials for projects- **Redis 7** - Caching and message broker./run.sh interactive-dev



We calculate a **performance status** based on how well they're doing:- **Celery 5.4.0** - Asynchronous task processingpython manage.py makemigrations

- **Good** (80%+): Things are going well! 🎉

- **Average** (50-79%): Doing okay, could be better 😐- **Docker & Docker Compose** - Containerization and orchestrationpython manage.py migrate

- **Poor** (Below 50%): Needs serious improvement 😟

```

## File Structure (Where Everything Lives)

### Frontend

```

django-boilerplate/- **React 18.2.0** - Component-based UI library### 7. Start Server

├── mgnrega/              # Backend code (the API)

│   ├── models.py        # Database structure- **Vite 5.0.8** - Fast build tool with HMR (Hot Module Replacement)

│   ├── views.py         # API endpoints

│   ├── serializers.py   # How data is formatted- **React Router 6.20.0** - Client-side routing```sh

│   └── urls.py          # API routes

│- **Axios 1.6.2** - HTTP client with interceptors./run.sh start-dev

├── frontend/            # Frontend code (what you see)

│   ├── src/- **Chart.js 4.4.0** - Data visualization library```

│   │   ├── pages/      # Dashboard, History, Comparison

│   │   ├── components/ # Reusable pieces- **CSS3** - Modern styling with CSS Grid and Flexbox

│   │   └── services/   # API calls

│   └── package.json### 8. Update and Sync Vault

│

├── create_sample_data.py  # Script that creates fake data### Development Tools

├── docker-compose.yml     # Runs everything

└── README.md             # You are here!- **ESLint** - JavaScript lintingTo Add Secret key add the variable to vault file.

```

- **Docker** - Containerized development environment

## Common Issues

- **Git** - Version control```

**Port already in use?**

```bash./run.sh sync-vault

# Frontend tries 3001 if 3000 is busy

# Backend is on 8000---```

```



**Can't connect to database?**

```bash## 📁 Project Structure### 9. How to add new libraries

# Make sure Docker is running

docker ps  # Should show 6 containersBash scripts

```

``````

**Frontend not loading?**

```bashdjango-boilerplate/./run.sh interactive-dev

cd frontend

npm install  # Install dependencies again├── backend/pip install <package_name>

npm run dev

```│   ├── mgnrega/                 # Main Django apppip freeze > requirements.txt



## Want to Add More Data?│   │   ├── models.py           # Database models (District, Performance, APIStatus)exit



The sample data script (`create_sample_data.py`) is pretty flexible. You can:│   │   ├── views.py            # API views (List, Summary, History, Comparison)./run.sh start-dev

- Add more districts

- Change the date range│   │   ├── serializers.py      # DRF serializers with data transformation```

- Adjust performance patterns

│   │   ├── urls.py             # API route definitionsPython scripts

Just edit the file and run:

```bash│   │   └── admin.py            # Django admin configuration```

docker exec nrega-backend python create_sample_data.py

```│   ├── users/                   # User management appsource venv/bin/activate



## Making Changes│   ├── src/                     # Django project settingspip install <package_name>



1. **Backend changes** - Edit files in `mgnrega/`, Django auto-reloads│   │   ├── settings/           # Environment-specific settingspip freeze > requirements.txt

2. **Frontend changes** - Edit files in `frontend/src/`, Vite auto-reloads

3. **Database changes** - Create migrations:│   │   ├── urls.py             # Root URL configurationpython manage.py run --mode start-dev

   ```bash

   docker exec nrega-backend python manage.py makemigrations│   │   └── wsgi.py             # WSGI application```

   docker exec nrega-backend python manage.py migrate

   ```│   ├── manage.py               # Django management script



## Stopping Everything│   └── requirements.txt        # Python dependenciesTODO:



```bash│Create atomicloops package

docker-compose down

```├── frontend/

│   ├── src/

Want to clear everything and start fresh?│   │   ├── components/         # Reusable React components

```bash│   │   │   ├── Header/         # Navigation header

docker-compose down -v  # -v removes the database too│   │   │   ├── ErrorBoundary/  # Error handling wrapper

```│   │   │   ├── ErrorMessage/   # Error display component

│   │   │   └── LoadingSpinner/ # Loading state indicator

## Cool Features│   │   ├── pages/              # Route-based page components

│   │   │   ├── Dashboard/      # Main dashboard page

- **Indian Number Format**: We show numbers like Indians do (Lakh/Crore, not millions/billions)│   │   │   ├── History/        # Historical trends page

- **Real-time Updates**: Change a district and see data instantly│   │   │   └── Comparison/     # Multi-district comparison page

- **Responsive**: Works on phone, tablet, desktop│   │   ├── services/

- **Error Handling**: If something breaks, you get a friendly message│   │   │   └── api.js          # Axios API client with interceptors

- **Fast**: Data loads quickly even with thousands of records│   │   ├── utils/

│   │   │   └── formatters.js   # Indian number formatting utilities

## Future Ideas│   │   ├── App.jsx             # Root application component

│   │   └── main.jsx            # Application entry point

Some things we could add (feel free to contribute!):│   ├── package.json            # NPM dependencies

- [ ] Map view of districts│   └── vite.config.js          # Vite configuration

- [ ] Download data as Excel/CSV│

- [ ] Compare by state (not just district)├── docker-compose.yml          # Multi-container orchestration

- [ ] Add notifications for poor performance├── Dockerfile                  # Backend container definition

- [ ] Mobile app├── create_sample_data.py       # Sample data generation script

- [ ] More chart types└── README.md                   # This file

```

## Who Made This?

---

Just someone who thought government data should be easier to understand. 

## 🚀 Getting Started

If you want to help make it better, feel free to:

- Report bugs### Prerequisites

- Suggest features

- Submit pull requests- **Docker** (v20.10+)

- Share with others who might find it useful- **Docker Compose** (v2.0+)

- **Git**

## License

### Installation

MIT - Use it however you want!

1. **Clone the repository**

---   ```bash

   git clone <repository-url>

**Questions?** Open an issue on GitHub or email us.   cd django-boilerplate

   ```

**Found a bug?** Let us know! We're constantly improving this.

2. **Start the application**

**Want to contribute?** Awesome! Fork it, make changes, send a pull request.   ```bash

   # Start all Docker containers

---   docker-compose up -d

   ```

Made with ❤️ to help people understand how MGNREGA is really working.

   This will start:

*Because transparency shouldn't be complicated.*   - Backend API (Django) on `http://localhost:8000`

   - PostgreSQL database on port `5432`
   - Redis cache on port `6379`
   - Celery worker for async tasks
   - Celery beat for scheduled tasks
   - Flower (Celery monitoring) on `http://localhost:5555`

3. **Run database migrations**
   ```bash
   docker exec nrega-backend python manage.py migrate
   ```

4. **Create admin user**
   ```bash
   docker exec nrega-backend python manage.py shell -c "from users.models import Users; Users.objects.create_superuser(email='admin@civicview.com', password='admin123'); print('Admin created!')"
   ```

5. **Load sample data**
   ```bash
   docker exec nrega-backend python create_sample_data.py
   ```

   This creates:
   - **95 districts** across 19 major Indian states
   - **3,384 performance records** (36 months × 94 districts)
   - Date range: November 2022 to October 2025

6. **Install frontend dependencies and start dev server**
   ```bash
   cd frontend
   npm install
   npm run dev
   ```

   Frontend will be available at `http://localhost:3001`

### Quick Start (Development)

```bash
# Start backend services
docker-compose up -d

# In a separate terminal, start frontend
cd frontend
npm run dev
```

Visit:
- **Frontend Dashboard**: http://localhost:3001
- **Backend API**: http://localhost:8000/api/v1/mgnrega/
- **Django Admin**: http://localhost:8000/admin (admin@civicview.com / admin123)
- **API Docs**: http://localhost:8000/api/docs/

---

## 📖 Usage Guide

### Accessing the Dashboard

1. **Open the application**  
   Navigate to http://localhost:3001 in your browser

2. **Select a District**  
   Use the dropdown to choose from 95 districts across 19 states:
   - Andhra Pradesh, Assam, Bihar, Chhattisgarh, Gujarat
   - Haryana, Jharkhand, Karnataka, Kerala, Madhya Pradesh
   - Maharashtra, Odisha, Punjab, Rajasthan, Tamil Nadu
   - Telangana, Uttar Pradesh, Uttarakhand, West Bengal

3. **View Key Metrics**  
   The dashboard displays 4 primary metrics:
   - **Person Days**: Total employment days generated
   - **Households**: Number of households employed
   - **Wages**: Total wages paid (in Crores/Lakhs)
   - **Materials**: Material expenditure (in Crores/Lakhs)

4. **Check Performance Status**  
   Color-coded badges indicate performance level:
   - 🟢 **Good** (≥80%): Green badge
   - 🟡 **Average** (50-79%): Yellow badge
   - 🔴 **Poor** (<50%): Red badge

5. **Monitor Month-over-Month Changes**  
   Each metric card shows:
   - Current month value
   - Previous month value
   - Percentage change (↑ increase, ↓ decrease)

### Viewing Historical Trends

1. **Navigate to History Page**  
   Click "Historical Trends" in the navigation menu

2. **Select District and Time Period**  
   - Choose a district from the dropdown
   - Select time range: 6, 12, 24, or 36 months

3. **Analyze Charts**  
   - **Line Chart**: View trends over time
   - **Bar Chart**: Compare monthly performance
   - Hover over data points for exact values

4. **Filter by Metric**  
   Select specific metrics to focus your analysis:
   - Person Days Generated
   - Households Employed
   - Total Wages Paid
   - Material Expenditure

### Comparing Districts

1. **Navigate to Comparison Page**  
   Click "District Comparison" in the navigation menu

2. **Configure Comparison**  
   - **Select Districts**: Choose multiple districts (up to 10)
   - **Choose Metric**: Pick the metric to compare
   - **Set Time Period**: Select month and year

3. **View Results**  
   - **Bar Chart**: Visual comparison of selected districts
   - **Table**: Detailed rankings with:
     - Rank
     - District name
     - State
     - Metric value
     - Color-coded performance status

4. **Interpret Rankings**  
   Districts are automatically ranked from highest to lowest performance for the selected metric

### Using the API (For Developers)

The backend provides a RESTful API for programmatic access:

```bash
# Get all districts
curl http://localhost:8000/api/v1/mgnrega/districts/

# Get district by ID
curl http://localhost:8000/api/v1/mgnrega/districts/1/

# Get district summary for specific month
curl http://localhost:8000/api/v1/mgnrega/summary/?district_id=1&year=2025&month=10

# Get historical data (last 12 months)
curl http://localhost:8000/api/v1/mgnrega/history/?district_id=1&from=2024-11&to=2025-10

# Compare districts
curl http://localhost:8000/api/v1/mgnrega/compare/?district_ids=1,2,3&year=2025&month=10&metric=person_days
```

---

## 🔌 API Documentation

### Base URL
```
http://localhost:8000/api/v1/mgnrega/
```

### Endpoints

#### 1. Health Check
**GET** `/health/`

Check API status.

**Response:**
```json
{
  "data": {
    "status": "ok",
    "timestamp": "2025-10-26T00:00:00Z"
  },
  "error": {},
  "isSuccess": true
}
```

#### 2. List Districts
**GET** `/districts/`

Get paginated list of all districts.

**Query Parameters:**
- `page` (optional): Page number (default: 1)
- `page_size` (optional): Items per page (default: 10)
- `state` (optional): Filter by state name

**Response:**
```json
{
  "data": {
    "count": 95,
    "next": "http://localhost:8000/api/v1/mgnrega/districts/?page=2",
    "previous": null,
    "results": [
      {
        "id": 1,
        "name": "Visakhapatnam",
        "code": "AP-VSK-001",
        "state": "Andhra Pradesh",
        "population": 4290589,
        "lat": "17.6869000",
        "lon": "83.2185000"
      }
    ]
  },
  "error": {},
  "isSuccess": true
}
```

#### 3. Get District Details
**GET** `/districts/{id}/`

Get specific district information.

**Response:**
```json
{
  "data": {
    "id": 1,
    "name": "Visakhapatnam",
    "code": "AP-VSK-001",
    "state": "Andhra Pradesh",
    "population": 4290589,
    "lat": "17.6869000",
    "lon": "83.2185000"
  },
  "error": {},
  "isSuccess": true
}
```

#### 4. Get District Summary
**GET** `/summary/`

Get performance summary for a specific district and month.

**Query Parameters:**
- `district_id` (required): District ID
- `year` (required): Year (YYYY)
- `month` (required): Month (1-12)

**Response:**
```json
{
  "data": {
    "district": {
      "id": 1,
      "name": "Visakhapatnam",
      "state": "Andhra Pradesh"
    },
    "period": "2025-10",
    "metrics": {
      "personDays": 245680,
      "householdsWorked": 28450,
      "totalWages": 122840000.50,
      "materialExpenditure": 61420000.25
    },
    "status": "Good",
    "previousMonth": {
      "personDays": 238920,
      "householdsWorked": 27680,
      "totalWages": 119460000.75,
      "materialExpenditure": 59730000.38
    },
    "changes": {
      "personDays": 2.83,
      "householdsWorked": 2.78,
      "totalWages": 2.83,
      "materialExpenditure": 2.83
    }
  },
  "error": {},
  "isSuccess": true
}
```

#### 5. Get Historical Data
**GET** `/history/`

Get historical performance data for a district.

**Query Parameters:**
- `district_id` (required): District ID
- `from` (required): Start period (YYYY-MM)
- `to` (required): End period (YYYY-MM)

**Response:**
```json
{
  "data": [
    {
      "period": "2024-11",
      "personDays": 235680,
      "householdsWorked": 27340,
      "totalWages": 117840000.50,
      "materialExpenditure": 58920000.25
    },
    {
      "period": "2024-12",
      "personDays": 242150,
      "householdsWorked": 28090,
      "totalWages": 121075000.00,
      "materialExpenditure": 60537500.00
    }
  ],
  "error": {},
  "isSuccess": true
}
```

#### 6. Compare Districts
**GET** `/compare/`

Compare multiple districts for a specific period and metric.

**Query Parameters:**
- `district_ids` (required): Comma-separated district IDs (e.g., "1,2,3")
- `year` (required): Year (YYYY)
- `month` (required): Month (1-12)
- `metric` (required): Metric name (`person_days`, `households_worked`, `total_wages`, `material_expenditure`)

**Response:**
```json
{
  "data": [
    {
      "id": 1,
      "name": "Visakhapatnam",
      "state": "Andhra Pradesh",
      "value": 245680,
      "rank": 1
    },
    {
      "id": 2,
      "name": "Guntur",
      "state": "Andhra Pradesh",
      "value": 238920,
      "rank": 2
    }
  ],
  "error": {},
  "isSuccess": true
}
```

### Response Structure

All API responses follow this format:

```json
{
  "data": {}, // Response data
  "error": {}, // Error details (empty if successful)
  "isSuccess": true // Boolean indicating success/failure
}
```

### Error Handling

**400 Bad Request:**
```json
{
  "data": {},
  "error": {
    "message": "Missing required parameter: district_id",
    "code": "BAD_REQUEST"
  },
  "isSuccess": false
}
```

**404 Not Found:**
```json
{
  "data": {},
  "error": {
    "message": "District not found",
    "code": "NOT_FOUND"
  },
  "isSuccess": false
}
```

**500 Internal Server Error:**
```json
{
  "data": {},
  "error": {
    "message": "An unexpected error occurred",
    "code": "INTERNAL_ERROR"
  },
  "isSuccess": false
}
```

---

## 🗄️ Data Model

### District Model

Represents an Indian district with MGNREGA implementation.

| Field | Type | Description |
|-------|------|-------------|
| `id` | AutoField | Primary key |
| `createdAt` | DateTime | Record creation timestamp |
| `updatedAt` | DateTime | Last update timestamp |
| `name` | CharField(255) | Official district name |
| `code` | CharField(50) | Unique district code (e.g., "AP-VSK-001") |
| `state` | CharField(100) | Indian state name |
| `population` | BigInteger | District population |
| `lat` | Decimal(10,7) | Latitude for geolocation |
| `lon` | Decimal(10,7) | Longitude for geolocation |

**Indexes:** `name`, `state`, `code` (unique)

### Performance Model

Monthly performance metrics for a district.

| Field | Type | Description |
|-------|------|-------------|
| `id` | AutoField | Primary key |
| `createdAt` | DateTime | Record creation timestamp |
| `updatedAt` | DateTime | Last update timestamp |
| `districtId` | ForeignKey | Reference to District |
| `year` | Integer | Year (YYYY, ≥2006) |
| `month` | Integer | Month (1-12) |
| `personDays` | BigInteger | Total person-days of employment |
| `householdsWorked` | BigInteger | Number of households employed |
| `totalWages` | Decimal(15,2) | Total wages paid (INR) |
| `materialExpenditure` | Decimal(15,2) | Total material costs (INR) |

**Unique Constraint:** `(districtId, year, month)`  
**Indexes:** `(districtId, year, month)`, `(year, month)`

### APIStatus Model

Tracks external API call status and health.

| Field | Type | Description |
|-------|------|-------------|
| `id` | AutoField | Primary key |
| `createdAt` | DateTime | Record creation timestamp |
| `updatedAt` | DateTime | Last update timestamp |
| `endpoint` | CharField(255) | API endpoint called |
| `statusCode` | Integer | HTTP status code |
| `responseTime` | Decimal(8,2) | Response time (ms) |
| `isSuccess` | Boolean | Success/failure flag |

---

## 🎨 Key Features Explained

### 1. Indian Number Formatting

Values are formatted according to Indian numbering system:

```javascript
// Lakh (1,00,000)
formatIndianNumber(125000) // "1.25 Lakh"

// Crore (1,00,00,000)
formatIndianNumber(25000000) // "2.50 Crore"

// Thousands
formatIndianNumber(5500) // "5,500"
```

### 2. Performance Status Calculation

Status is calculated based on efficiency ratio:

```python
efficiency = (actual_value / target_value) * 100

if efficiency >= 80:
    status = "Good"
elif efficiency >= 50:
    status = "Average"
else:
    status = "Poor"
```

### 3. Month-over-Month Comparison

Percentage change calculation:

```javascript
change = ((current - previous) / previous) * 100

// Displayed with arrow indicator
// ↑ 5.2% (increase)
// ↓ 3.1% (decrease)
```

### 4. Seasonal Adjustments

Data generation includes realistic seasonal patterns:

```python
# Monsoon months (June-September): -8% activity
# Peak season (October-January): +8% activity
# Regular months: baseline
```

### 5. State-wise Performance Patterns

Sample data includes varied performance levels:

- **Excellent (90%)**: Gujarat, Karnataka, Kerala, Tamil Nadu
- **Good (75%)**: Andhra Pradesh, Haryana, Maharashtra, Punjab, Telangana
- **Average (60%)**: Assam, Chhattisgarh, Madhya Pradesh, Odisha, Uttarakhand, West Bengal
- **Poor (45%)**: Bihar, Jharkhand, Uttar Pradesh
- **Very Poor (30%)**: Rajasthan

---

## 🔧 Configuration

### Environment Variables

Create `.env` file in the project root:

```bash
# Django Settings
DEBUG=True
SECRET_KEY=your-secret-key-here
ALLOWED_HOSTS=localhost,127.0.0.1

# Database
POSTGRES_DB=mgnrega_db
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_HOST=db
POSTGRES_PORT=5432

# Redis
REDIS_URL=redis://redis:6379/0

# Celery
CELERY_BROKER_URL=redis://redis:6379/0
CELERY_RESULT_BACKEND=redis://redis:6379/0

# CORS
CORS_ALLOWED_ORIGINS=http://localhost:3001,http://127.0.0.1:3001
```

### Docker Compose Services

```yaml
services:
  db:          # PostgreSQL database
  redis:       # Redis cache & message broker
  backend:     # Django API server
  celery:      # Async task worker
  celery-beat: # Scheduled task scheduler
  flower:      # Celery monitoring UI
```

---

## 🧪 Testing

### Backend API Testing

```bash
# Run Django tests
docker exec nrega-backend python manage.py test

# Test specific app
docker exec nrega-backend python manage.py test mgnrega

# Run with coverage
docker exec nrega-backend coverage run --source='.' manage.py test
docker exec nrega-backend coverage report
```

### Frontend Testing

```bash
cd frontend

# Run unit tests (if configured)
npm test

# Run linting
npm run lint
```

### Manual API Testing

Use the provided test script:

```bash
docker exec nrega-backend python test_api.py
```

Expected output:
```
✅ 1/6 Health Check: PASSED
✅ 2/6 List Districts: PASSED
✅ 3/6 Get District: PASSED
✅ 4/6 District Summary: PASSED
✅ 5/6 Historical Data: PASSED
✅ 6/6 District Comparison: PASSED

All tests passed! ✅
```

---

## 🚢 Deployment

### Production Deployment

1. **Update settings**
   ```python
   # src/settings/prod.py
   DEBUG = False
   ALLOWED_HOSTS = ['your-domain.com']
   ```

2. **Build frontend**
   ```bash
   cd frontend
   npm run build
   ```

3. **Collect static files**
   ```bash
   docker exec nrega-backend python manage.py collectstatic --noinput
   ```

4. **Use production Docker Compose**
   ```bash
   docker-compose -f docker-compose.yml up -d
   ```

5. **Set up reverse proxy (Nginx)**
   ```nginx
   server {
       listen 80;
       server_name your-domain.com;

       location /api/ {
           proxy_pass http://backend:8000;
       }

       location / {
           root /var/www/frontend/dist;
           try_files $uri $uri/ /index.html;
       }
   }
   ```

---

## 🤝 Contributing

Contributions are welcome! Please follow these guidelines:

1. **Fork the repository**
2. **Create a feature branch**
   ```bash
   git checkout -b feature/amazing-feature
   ```
3. **Commit your changes**
   ```bash
   git commit -m 'Add amazing feature'
   ```
4. **Push to the branch**
   ```bash
   git push origin feature/amazing-feature
   ```
5. **Open a Pull Request**

### Code Style

- **Python**: Follow PEP 8 guidelines
- **JavaScript**: Use ESLint configuration
- **Commits**: Use conventional commit messages

---

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 👥 Authors

**CivicView Development Team**

---

## 🙏 Acknowledgments

- MGNREGA scheme data structure inspired by official government portals
- Chart.js community for excellent visualization library
- Django and React communities for comprehensive documentation
- All contributors who helped improve this project

---

## 📞 Support

For issues, questions, or contributions:

- **GitHub Issues**: [Project Issues](https://github.com/your-repo/issues)
- **Email**: support@civicview.example.com
- **Documentation**: [Full Docs](https://docs.civicview.example.com)

---

## 🗺️ Roadmap

### Planned Features

- [ ] Map-based district visualization
- [ ] Export data to CSV/Excel
- [ ] Advanced filtering and search
- [ ] Mobile native applications
- [ ] Real-time data updates via WebSocket
- [ ] User accounts for saved comparisons
- [ ] PDF report generation
- [ ] Multi-language support
- [ ] Accessibility improvements (WCAG AAA)
- [ ] Machine learning predictions

---

**Made with ❤️ for Public Good**

*Promoting transparency, accountability, and data-driven governance in India's largest employment guarantee scheme.*
