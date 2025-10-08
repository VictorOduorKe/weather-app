# Mini Weather App

A full-stack weather application built with Flask (Python) backend and React (Vite) frontend. The app provides current weather information for any city and offers personalized advice on dressing, drinks, and safety precautions based on weather conditions.

## Features

- 🌤️ **Real-time Weather Data**: Get current weather information for any city worldwide
- 🤖 **AI-Powered Advice**: Smart recommendations for dressing, drinks, and safety precautions
- 🎨 **Modern UI**: Clean, responsive design with interactive weather cards
- 🔄 **Fallback System**: Uses heuristic advice when AI service is unavailable
- 🌍 **CORS Enabled**: Frontend and backend can run on different ports

## Tech Stack

### Backend
- **Flask**: Python web framework
- **Flask-CORS**: Cross-Origin Resource Sharing support
- **Requests**: HTTP library for weather API calls
- **Google Generative AI**: AI-powered weather advice
- **Python-dotenv**: Environment variable management

### Frontend
- **React**: JavaScript UI library
- **Vite**: Fast build tool and development server
- **Axios**: HTTP client for API requests
- **CSS3**: Modern styling with animations

## Prerequisites

Before running the application, ensure you have the following installed:

- **Python 3.8+** (recommended: Python 3.12)
- **Node.js 16+** (recommended: Node.js 18+)
- **npm** or **yarn** package manager

## API Keys Required

You'll need to obtain the following API keys:

1. **OpenWeatherMap API Key**
   - Visit: https://openweathermap.org/api
   - Sign up for a free account
   - Generate an API key

2. **Google AI API Key** (Optional)
   - Visit: https://aistudio.google.com/app/apikey
   - Create a new API key for Google Generative AI
   - Note: The app works without this key using fallback advice

## Installation & Setup

### 1. Clone the Repository

```bash
git clone <your-repository-url>
cd weather-app
```

### 2. Backend Setup

#### Navigate to Backend Directory
```bash
cd backend
```

#### Create Virtual Environment
```bash
python -m venv venv
```

#### Activate Virtual Environment

**On Linux/macOS:**
```bash
source venv/bin/activate
```

**On Windows:**
```bash
venv\Scripts\activate
```

#### Install Dependencies
```bash
pip install -r requirements.txt
```

#### Create Environment File
Create a `.env` file in the backend directory:

```bash
touch .env
```

Add the following content to `.env`:
```env
WEATHER_API_KEY=your_openweathermap_api_key_here
GOOGLE_AI_API_KEY=your_google_ai_api_key_here
GOOGLE_AI_MODEL=gemini-1.5-flash
```

Replace the placeholder values with your actual API keys.

### 3. Frontend Setup

#### Navigate to Frontend Directory
```bash
cd ../frontend
```

#### Install Dependencies
```bash
npm install
```

## Running the Application

### Option 1: Run Both Services Separately

#### Terminal 1 - Start Backend Server
```bash
cd backend
source venv/bin/activate  # On Windows: venv\Scripts\activate
python app.py
```

The backend server will start on `http://127.0.0.1:5000`

#### Terminal 2 - Start Frontend Server
```bash
cd frontend
npm run dev
```

The frontend development server will start on `http://127.0.0.1:5173`

### Option 2: Using Concurrent Commands (Optional)

If you have `concurrently` installed globally, you can run both services with one command:

```bash
# Install concurrently globally
npm install -g concurrently

# From the project root directory
concurrently "cd backend && source venv/bin/activate && python app.py" "cd frontend && npm run dev"
```

## Usage

1. Open your web browser and navigate to `http://127.0.0.1:5173`
2. Enter a city name in the input field
3. Click "Get Weather" or press Enter
4. View the current weather information and personalized advice
5. Hover over the advice cards to see detailed recommendations

## API Endpoints

### GET /weather

Fetches weather information for a specified city.

**Parameters:**
- `city` (required): The name of the city to get weather for

**Example:**
```
GET http://127.0.0.1:5000/weather?city=London
```

**Response:**
```json
{
  "city": "London",
  "temperature": 15.5,
  "description": "partly cloudy",
  "advice": {
    "dressing": "Light coat or sweater; consider a scarf.",
    "drinks": "Water or warm tea; stay hydrated.",
    "cautions": ["Stay aware of changing conditions and local advisories."]
  }
}
```

## Project Structure

```
weather-app/
├── backend/
│   ├── app.py              # Main Flask application
│   ├── requirements.txt    # Python dependencies
│   ├── .env               # Environment variables (create this)
│   ├── venv/              # Virtual environment
│   └── README.md          # Backend-specific documentation
├── frontend/
│   ├── src/
│   │   ├── App.jsx        # Main React component
│   │   ├── main.jsx       # React entry point
│   │   ├── components/
│   │   │   └── WeatherCard.jsx
│   │   └── styles/
│   │       └── index.css
│   ├── index.html         # HTML template
│   ├── package.json       # Node.js dependencies
│   ├── vite.config.js     # Vite configuration
│   └── node_modules/      # Node.js dependencies
└── README.md              # This file
```

## Configuration

### Backend Configuration

The backend can be configured through environment variables:

- `WEATHER_API_KEY`: Your OpenWeatherMap API key (required)
- `GOOGLE_AI_API_KEY`: Your Google AI API key (optional)
- `GOOGLE_AI_MODEL`: AI model to use (default: "gemini-1.5-flash")

### Frontend Configuration

The frontend is configured in `vite.config.js`:

- **Host**: `127.0.0.1` (localhost)
- **Port**: `5173`
- **Backend URL**: `http://127.0.0.1:5000` (hardcoded in App.jsx)

## Troubleshooting

### Common Issues

#### 1. Backend Server Won't Start

**Error**: `ModuleNotFoundError: No module named 'flask'`

**Solution**: Ensure you're in the virtual environment and dependencies are installed:
```bash
cd backend
source venv/bin/activate
pip install -r requirements.txt
```

#### 2. Frontend Can't Connect to Backend

**Error**: `Failed to fetch weather` or CORS errors

**Solutions**:
- Ensure backend is running on port 5000
- Check that Flask-CORS is installed and configured
- Verify the backend URL in `frontend/src/App.jsx`

#### 3. Weather API Errors

**Error**: `Server is not configured with WEATHER_API_KEY`

**Solution**: Create a `.env` file in the backend directory with your OpenWeatherMap API key:
```env
WEATHER_API_KEY=your_actual_api_key_here
```

#### 4. City Not Found

**Error**: `City not found` or `404` response

**Solutions**:
- Check the spelling of the city name
- Try using the full city name (e.g., "New York" instead of "NY")
- Some cities may require country code (e.g., "London, UK")

#### 5. Port Already in Use

**Error**: `Address already in use` or `EADDRINUSE`

**Solutions**:
- Kill processes using the ports:
  ```bash
  # For port 5000 (backend)
  lsof -ti:5000 | xargs kill -9
  
  # For port 5173 (frontend)
  lsof -ti:5173 | xargs kill -9
  ```
- Or change ports in the configuration files

### Environment-Specific Issues

#### Linux/macOS
- Ensure Python 3.8+ is installed
- Use `source venv/bin/activate` to activate virtual environment

#### Windows
- Use `venv\Scripts\activate` to activate virtual environment
- Ensure PowerShell execution policy allows script execution if needed

## Development

### Adding New Features

1. **Backend**: Add new routes in `backend/app.py`
2. **Frontend**: Create new components in `frontend/src/components/`
3. **Styling**: Update `frontend/src/styles/index.css`

### Building for Production

#### Frontend Build
```bash
cd frontend
npm run build
```

The built files will be in the `dist/` directory.

#### Backend Deployment
For production deployment, consider:
- Using a production WSGI server (e.g., Gunicorn)
- Setting up proper environment variables
- Configuring a reverse proxy (e.g., Nginx)

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is open source and available under the [MIT License](LICENSE).

## Support

If you encounter any issues or have questions:

1. Check the troubleshooting section above
2. Search existing GitHub issues
3. Create a new issue with detailed information about your problem

---

**Happy Weather Tracking! 🌤️**
