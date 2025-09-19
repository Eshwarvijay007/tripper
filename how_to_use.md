# 🚀 Naomi.ai - Setup & Run Guide

A complete AI-powered travel planning application with React frontend and FastAPI backend.

## 📋 Prerequisites

Before running the application, ensure you have:

- **Node.js** (v16 or higher) - [Download here](https://nodejs.org/)
- **Python** (3.8 or higher) - [Download here](https://python.org/)
- **npm** (comes with Node.js)
- **pip** (comes with Python)

## 🏗️ Project Structure

```
tripper/
├── app/                    # FastAPI Backend
│   ├── main.py            # Main backend application
│   ├── requirements.txt   # Python dependencies
│   └── ...
├── tripplanner/           # React Frontend
│   ├── package.json       # Node.js dependencies
│   ├── src/               # React components
│   └── ...
├── venv/                  # Python virtual environment
└── HOW_TO_RUN.md         # This file
```

## 🚀 Quick Start (Development Mode)

### Method 1: Run Frontend & Backend Separately (Recommended)

This method provides hot-reloading for both frontend and backend during development.

#### Step 1: Setup Backend

```bash
# Navigate to project root
cd /Users/eshwar/eshwarhq/tripper

# Create and activate Python virtual environment (if not already created)
python3 -m venv venv
source venv/bin/activate

# Install Python dependencies
pip install -r app/requirements.txt
```

#### Step 2: Setup Frontend

```bash
# Navigate to frontend directory
cd /Users/eshwar/eshwarhq/tripper/tripplanner

# Install Node.js dependencies (if not already installed)
npm install
```

#### Step 3: Start the Application

**Terminal 1 - Start Backend:**
```bash
cd tripper
source venv/bin/activate
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**Terminal 2 - Start Frontend:**
```bash
cd tripplanner
npm run dev
```

#### Step 4: Access the Application

- **Frontend (Main App)**: http://localhost:3000/
- **Backend API**: http://localhost:8000/
- **API Documentation**: http://localhost:8000/docs

## 🎯 Method 2: Production-like Setup (Single Port)

If you prefer to serve everything from one port (like in production):

#### Step 1: Build Frontend

```bash
cd tripplanner
npm run build
```

#### Step 2: Configure Backend to Serve Frontend

```bash
cd tripper
export FRONTEND_DIST="/tripper/tripplanner/dist"
source venv/bin/activate
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

#### Step 3: Access the Application

- **Complete App**: http://localhost:8000/
- **API Documentation**: http://localhost:8000/docs

## ⚙️ Environment Configuration

### Backend Configuration

The backend loads environment variables from `.env` files. Key variables:

```bash
# Optional API Keys for full functionality
BOOKING_RAPIDAPI_KEY=your_booking_api_key
BOOKING_RAPIDAPI_HOST=your-host-key
GOOGLE_PLACES_API_KEY=your_google_places_key
GEMINI_API_KEY=your_gemini_api_key
```

### Frontend Configuration

The frontend uses `.env` file in the `tripplanner/` directory:

```bash
# API connection (already configured)
VITE_API_BASE=http://localhost:8000

# Google Maps integration
VITE_GOOGLE_MAPS_API_KEY=your_google_maps_key
```

## 🛠️ Useful Commands

### Backend Commands

```bash
# Activate virtual environment
source venv/bin/activate

# Install/update dependencies
pip install -r app/requirements.txt

# Run with auto-reload
uvicorn app.main:app --reload

# Run on specific host/port
uvicorn app.main:app --host 0.0.0.0 --port 8080

# Check health endpoint
curl http://localhost:8000/api/healthz
```

### Frontend Commands

```bash
# Install dependencies
npm install

# Start development server
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview

# Lint code
npm run lint
```

## 🔍 Troubleshooting

### Common Issues

#### Port Already in Use
If you get "port already in use" errors:

```bash
# Find process using port 8000
lsof -i :8000

# Kill the process (replace PID with actual process ID)
kill -9 <PID>

# Or use different ports
uvicorn app.main:app --port 8001  # Backend
npm run dev -- --port 3001       # Frontend
```

#### Python Virtual Environment Issues
```bash
# Deactivate current environment
deactivate

# Remove existing venv and recreate
rm -rf venv
python3 -m venv venv
source venv/bin/activate
pip install -r app/requirements.txt
```

#### Node.js Dependencies Issues
```bash
# Clear npm cache and reinstall
rm -rf node_modules package-lock.json
npm cache clean --force
npm install
```

#### Frontend-Backend Connection Issues
1. Ensure backend is running on port 8000
2. Check `tripplanner/.env` has correct `VITE_API_BASE=http://localhost:8000`
3. Verify CORS settings in backend allow frontend origin

## 📱 Features Available

### ✅ Working Features
- **Landing Page**: Complete TripPlanner.ai clone
- **AI Chat Interface**: Layla AI conversation system
- **Trip Planning**: Interactive trip creation workflow
- **Responsive Design**: Mobile and desktop optimized
- **Real-time Communication**: Frontend ↔ Backend API integration

### 🔧 API Integrations (Require Keys)
- **Google Places**: POI and location search
- **Booking.com**: Hotel search and booking
- **Google Gemini**: AI trip planning and chat
- **Google Maps**: Interactive map display

## 📚 API Endpoints

Key backend endpoints you can test:

- `GET /api/healthz` - Health check
- `POST /api/chat/messages` - Send chat message
- `GET /api/chat/stream/{conversation_id}` - Stream chat responses
- `POST /api/search/hotels` - Search hotels
- `POST /api/search/flights` - Search flights
- `POST /api/search/poi` - Search points of interest

## 🚀 Deployment

### Development
Use Method 1 (separate frontend/backend) for active development.

### Production
Use Method 2 (single port) or deploy frontend/backend separately:

- **Frontend**: Deploy `tripplanner/dist/` to any static hosting (Vercel, Netlify, etc.)
- **Backend**: Deploy FastAPI app to cloud platforms (Railway, Heroku, AWS, etc.)

## 📞 Support

If you encounter issues:

1. Check that all dependencies are installed
2. Verify ports 3000 and 8000 are available
3. Ensure Python virtual environment is activated
4. Check browser console for frontend errors
5. Check terminal logs for backend errors

---

**Happy Trip Planning! ✈️🗺️**

*Last updated: $(date '+%Y-%m-%d')*
