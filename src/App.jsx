import { useState } from 'react'
import map from './assets/Map_RTS.jpg'
import Schedule from './Schedule'
import Events from './Events'
import './App.css'

function App() {
  const [count, setCount] = useState(0)
  let screen;
  if(count == 0){
    screen = <img src={map} className="mapDefault" alt="Default Map" />;
  } else if(count == 1){
    screen = <Schedule/>
  } else if(count == 2){
    screen = <Events/>
  }
  return (
    <>
      <div>
        {screen}
      </div>
      <div className="card">
        <button onClick={() => setCount(0)}>
          Home
        </button>
        <button onClick={() => setCount(1)}>
          Schedule
        </button>
        <button onClick={() => setCount(2)}>
          Events
        </button>
      </div>
    </>
  )
}

export default App
