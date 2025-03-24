import { useState } from 'react'
import EventProp from "./EventProp"

function Schedule(){
    const [valTitle,setValTitle]=useState("Title")
    const [valStart,setValStart]=useState("Start")
    const [valEnd,setValEnd]=useState("End")
    const [valLoc,setValLoc]=useState("Location")
    const [newEventVisible,setNewEventVisible]=useState(false)

    function handleChangeTitle(e){
        setValTitle(e.target.value)
    }
    function handleChangeStart(e){
        setValStart(e.target.value)
    }
    function handleChangeEnd(e){
        setValEnd(e.target.value)
    }
    function handleChangeLocation(e){
        setValLoc(e.target.value)
    }

    let titleIn,startIn,endIn,locIn,createButt

    let [classEvents, setClassEvents] = useState([
        ["CAP5100", "10:40", "11:30", "NULL"],
        ["CDA5636", "3:00", "4:55", "NULL"],
        ["EEL3111C", "4:05", "4:55", "New Engineering Building"]
    ]);

    if(newEventVisible){
        titleIn = <input onChange={(e) =>handleChangeTitle(e)} type="text" value={valTitle}/>
        startIn = <input onChange={(e) =>handleChangeStart(e)} type="text" value={valStart}/>
        endIn = <input onChange={(e) =>handleChangeEnd(e)} type="text" value={valEnd}/>
        locIn = <input onChange={(e) =>handleChangeLocation(e)} type="text" value={valLoc}/>
        createButt = <button onClick={()=>(setClassEvents([...classEvents, [valTitle, valStart, valEnd, valLoc]]),setNewEventVisible(false))}>
            Create
        </button>
    }else{
        titleIn =<></>
        startIn =<></>
        endIn =<></>
        locIn =<></>
        createButt=<></>
    }
    
    return(
        <>
        <button onClick={() => setNewEventVisible(true)}>
            Create New Class Event
        </button>
        <div>
            {titleIn}
            {startIn}
            {endIn}
            {locIn}
            {createButt}
        </div>

        <div>{classEvents.map(Ev=><li><EventProp title={Ev[0]} start={Ev[1]} end={Ev[2]} location={Ev[3]}/></li>)}</div>
        </>
    )
}

export default Schedule
//setClassEvents([...classEvents, ["Empty", "00:00", "00:00", "NULL"]])