import { useState } from 'react'
import EventProp from "./EventProp"
import search from './assets/search.png'
function Events(){
    const [val,setVal]=useState("Search")
    function handleChange(e){
        setVal(e.target.value)
    }

    let [SchoolEvents, setSchoolEvents] = useState([
        ["Move in ..", "7:00", "10:00", "NULL"],
        ["Kickball ..", "3:00", "5:00", "NULL"],
        ["UF vs FSU", "7:30", "11:00", "Ben Hill Griffin Stadium"]
    ]);
    

    return(
        <>
        <div>
            <input onChange={(e) =>handleChange(e)} type="text" value={val}/>
            <button>
                <img src={search} style={{ width: "20px", height: "20px" }}/>
            </button>
        </div>
        <div>{SchoolEvents.map(Ev=><li><EventProp title={Ev[0]} start={Ev[1]} end={Ev[2]} location={Ev[3]}/></li>)}</div>
        </>
    )
}
export default Events