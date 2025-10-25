# CivicView Frontend

React-based frontend for the MGNREGA Performance Dashboard.

## Tech Stack

- **React 18** - UI library
- **React Router** - Client-side routing
- **Axios** - HTTP client for API requests
- **Chart.js + react-chartjs-2** - Data visualization
- **Vite** - Build tool and dev server
- **React Icons** - Icon library

## Project Structure

```
frontend/
├── src/
│   ├── components/       # Reusable UI components
│   │   ├── Header/
│   │   ├── Footer/
│   │   ├── LoadingSpinner/
│   │   ├── ErrorMessage/
│   │   ├── ErrorBoundary/
│   │   ├── StatusBadge/
│   │   └── Card/
│   ├── pages/           # Page components
│   │   ├── Dashboard/   # Main dashboard with district selector
│   │   ├── Historical/  # Performance trends over time
│   │   └── Comparison/  # Multi-district comparison
│   ├── services/        # API service layer
│   │   └── api.js       # Axios client matching Django backend
│   ├── utils/           # Utility functions
│   │   └── helpers.js   # Formatters, helpers
│   ├── App.jsx          # Main app component
│   ├── main.jsx         # Entry point
│   └── index.css        # Global styles
├── index.html
├── vite.config.js
└── package.json
```

## API Integration

The frontend is tightly integrated with the Django backend:

### Endpoints Used

- `GET /api/health/` - System health check
- `GET /api/districts/` - List all districts
- `GET /api/districts/:id/` - District details
- `GET /api/districts/:id/summary/` - Performance summary
- `GET /api/districts/:id/history/` - Historical trends
- `POST /api/compare/` - Compare multiple districts

### Data Flow

1. **API Service** (`src/services/api.js`) - Axios client with interceptors
2. **Page Components** - Fetch data using API service
3. **UI Components** - Display formatted data
4. **Utilities** - Format numbers, dates, currency (Indian format)

## Features

### 1. Dashboard
- District selector with state filter and search
- Real-time performance summary
- Color-coded status indicators (Good/Average/Poor)
- Comparison to previous month

### 2. Historical Trends
- Line charts for performance metrics
- Configurable time periods (6/12/24/36 months)
- Metric selector (Person Days, Households, Wages, Expenditure)

### 3. District Comparison
- Select up to 5 districts
- Bar charts for visual comparison
- Detailed comparison table
- Multiple metric views

## Setup and Installation

### Prerequisites
- Node.js >= 18.0.0
- npm >= 9.0.0

### Install Dependencies
```bash
cd frontend
npm install
```

### Development Server
```bash
npm run dev
```

The app will run on http://localhost:3000 with API proxy to Django backend at http://localhost:8000

### Build for Production
```bash
npm run build
```

Output will be in `dist/` directory.

### Preview Production Build
```bash
npm run preview
```

## Environment Configuration

### Development
- Vite dev server with HMR
- API proxy to Django backend (configured in `vite.config.js`)
- Source maps enabled

### Production
- Optimized build with code splitting
- Vendor chunks for better caching
- No source maps
- Static assets served by NGINX

## Styling

- **CSS Variables** - Theme colors, spacing, typography
- **Mobile-First** - Responsive design starting from mobile
- **Color-Coded Status** - Matching backend logic
  - Good (Green): >= 80% of state average
  - Average (Amber): 50-79% of state average
  - Poor (Red): < 50% of state average

## Integration with Django

### CORS Configuration
Backend should have CORS headers configured for frontend origin.

### Static Files
In production, React build is served by NGINX:
- `/` - React app (SPA)
- `/api/` - Proxied to Django backend
- `/admin/` - Django admin panel

### Authentication
Currently public - no authentication required for dashboard views.
Admin routes protected by Django authentication.

## Browser Support

- Chrome/Edge (last 2 versions)
- Firefox (last 2 versions)
- Safari (last 2 versions)
- Mobile browsers (iOS Safari, Chrome Mobile)

## Performance

- Code splitting for faster initial load
- Lazy loading for charts
- API response caching (via backend)
- Optimized images and assets
- Debounced search inputs

## Accessibility

- Semantic HTML
- ARIA labels where needed
- Keyboard navigation
- Color contrast compliance
- Responsive text sizes

## Future Enhancements

- Export data to CSV/Excel
- Print-friendly views
- Advanced filtering options
- Map view with geolocation
- Dark mode theme
- Multi-language support
