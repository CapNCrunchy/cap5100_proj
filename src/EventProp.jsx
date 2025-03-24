import {useState} from 'react'
import './EventProp.css'

function EventProp(props){
    const [selected, setSelected] = useState(false);

    return(
        <div class="eventContainer">
        <div class="infoContainer">
            <p1 class="info" id="infoTitle">
                {props.title} {props.start} - {props.end}
            </p1>
            <p1 class="info" id="infoLoc">
                {props.location}
            </p1>
        </div>
        
        <button 
            onClick={() => setSelected(!selected)}
            style={{
            padding: "10px 20px",
            fontSize: "16px",
            borderRadius: "8px",
            border: "none",
            cursor: "pointer",
            backgroundColor: selected ? "#4CAF50" : "#ccc",
            color: selected ? "white" : "black",
        }}
        >
        {selected ? "Selected" : "Not Selected"}
        </button>

        

        </div>
    )
}

export default EventProp