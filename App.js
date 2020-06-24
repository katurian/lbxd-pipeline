import React from "react"
import Entry from "./Entry"
import entryData from "./reviews"

function App() {
    const entryComponents = entryData.map(item => <Entry key={item.id} entry={item}/>)
    return (
        <div>
            {entryComponents}
        </div>
    )
}

export default App