import { useState } from 'react'
import EventProp from "./EventProp"

function Schedule(){
    let [classEvents, setClassEvents] = useState([
        ["CAP5100", "10:40", "11:30", "NULL"],
        ["CDA5636", "3:00", "4:55", "NULL"],
        ["EEL3111C", "4:05", "4:55", "New Engineering Building"]
    ]);
    
    return(
        <>
        <button onClick={() => setClassEvents([...classEvents, ["Empty", "00:00", "00:00", "NULL"]])}>
            Create New Class Event
        </button>
        <div>{classEvents.map(Ev=><li><EventProp title={Ev[0]} start={Ev[1]} end={Ev[2]} location={Ev[3]}/></li>)}</div>
        </>
    )
}

export default Schedule
