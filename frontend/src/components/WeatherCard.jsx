export default function WeatherCard({ city, temperature, description }) {
  return (
    <div className="flip-card">
      <div className="flip-card-inner">
        <div className="flip-card-front weather-card">
          <h2 className="city">{city}</h2>
          <div className="temp">{typeof temperature === 'number' ? `${temperature.toFixed(1)} °C` : 'N/A'}</div>
          <div className="desc" style={{textTransform: 'none'}}>Hover to see details</div>
        </div>
        <div className="flip-card-back weather-card">
          <h2 className="city">Conditions</h2>
          <div className="desc" style={{textTransform: 'none'}}>{description}</div>
        </div>
      </div>
    </div>
  )
}



