import { useState } from 'react'
import axios from 'axios'
import WeatherCard from './components/WeatherCard.jsx'

export default function App() {
  const [city, setCity] = useState('')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')
  const [weather, setWeather] = useState(null)

  async function fetchWeather() {
    const trimmed = city.trim()
    if (!trimmed) {
      setError('Please enter a city name')
      setWeather(null)
      return
    }
    setLoading(true)
    setError('')
    try {
      const res = await axios.get(`http://127.0.0.1:5000/weather`, {
        params: { city: trimmed }
      })
      setWeather(res.data)
    } catch (e) {
      if (e.response && e.response.status === 404) {
        setError('City not found')
      } else {
        setError('Failed to fetch weather')
      }
      setWeather(null)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="app-container">
      <div className="card">
        <h1 className="title">Mini Weather App</h1>
        <div className="controls">
          <input
            type="text"
            placeholder="Enter city name"
            value={city}
            onChange={(e) => setCity(e.target.value)}
            onKeyDown={(e) => { if (e.key === 'Enter') fetchWeather() }}
            className="input"
          />
          <button className="button" onClick={fetchWeather} disabled={loading}>
            {loading ? 'Loading…' : 'Get Weather'}
          </button>
        </div>

        {error && <p className="error">{error}</p>}
        {weather && !error && (
          <div className="result">
            <WeatherCard city={weather.city} temperature={weather.temperature} description={weather.description} />
            {weather.advice && (
              <div className="advice">
                <h3 style={{marginTop: '16px'}}>Advice</h3>
                <div className="advice-sections">
                  <div className="advice-card flip-card">
                    <div className="flip-card-inner">
                      <div className="flip-card-front">
                        <strong>Dressing</strong>
                        <p style={{color: '#64748b'}}>Hover to see details</p>
                      </div>
                      <div className="flip-card-back">
                        <strong>Dressing</strong>
                        <p>{weather.advice.dressing}</p>
                      </div>
                    </div>
                  </div>
                  <div className="advice-card flip-card">
                    <div className="flip-card-inner">
                      <div className="flip-card-front">
                        <strong>Drinks</strong>
                        <p style={{color: '#64748b'}}>Hover to see details</p>
                      </div>
                      <div className="flip-card-back">
                        <strong>Drinks</strong>
                        <p>{weather.advice.drinks}</p>
                      </div>
                    </div>
                  </div>
                  <div className="advice-card flip-card">
                    <div className="flip-card-inner">
                      <div className="flip-card-front">
                        <strong>Cautions</strong>
                        <p style={{color: '#64748b'}}>Hover to see details</p>
                      </div>
                      <div className="flip-card-back">
                        <strong>Cautions</strong>
                        <ul>
                          {(weather.advice.cautions || []).map((c, i) => (
                            <li key={i}>{c}</li>
                          ))}
                        </ul>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  )
}



