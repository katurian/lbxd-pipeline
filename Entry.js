import React from "react"

function Entry(props) {
    return (
        <div className="px-6 py-4 border-t border-gray-200">
            <div className="bg-gray-200 ml-6 uppercase bg-blue-500 text-blue-100 font-bold text-3xl px-6 py-4">{props.entry.film.name}</div>
            <div className="italic flex justify-between items-center px-6 py-4 text-sm">{props.entry.whenCreated.substring(0, 10)}</div>
            <div className="border rounded-lg text-md bg-gray-200 mb-8" dangerouslySetInnerHTML={{__html:props.entry.review.text}}/>
        </div>
    )
}

export default Entry