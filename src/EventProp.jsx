import {useState} from 'react'

function EventProp(props){
    const [selected, setSelected] = useState(false);

    return(
        <>
        <p1>
            {props.title} 
        </p1>
        <p1>
            {props.start} - {props.end} 
        </p1>
        
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
        <p1>
            {props.location}
        </p1>
        </>
    )
}

export default EventProp