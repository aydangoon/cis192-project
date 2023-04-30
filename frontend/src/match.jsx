import { useParams } from 'react-router-dom'
import ReactCountryFlag from 'react-country-flag'
import { useContext, useEffect, useState } from 'react'
import { AppContext } from './App'
import api from './api'

const Match = () => {
    const { match_id } = useParams()
    let interval
    // states "invalid", "waiting", "generating", "done"
    const [state, setState] = useState(null)
    const [data, setData] = useState(null)
    const [appContext, setAppContext] = useContext(AppContext)

    const getData = async () => {
        const retrievedData = await api.get_match_data(match_id)
        setState('done')
        console.log('getData() data:', retrievedData)
        setData(retrievedData)
    }
    const getState = async () => {
        const retrievedData = await api.get_match_state(
            appContext.sid,
            match_id
        )
        console.log('getState() data:', retrievedData)
        if (state === null || state !== retrievedData.state) {
            setState(retrievedData.state)
        }
        if (retrievedData.state === 'generating') {
            getData()
            clearInterval(interval)
        }
    }

    useEffect(() => {
        getState()
        interval = setInterval(getState, 5000)
        return () => clearInterval(interval)
    }, [interval])

    if (state === null) {
        return (
            <svg
                className="animate-spin h-5 w-5 mr-3 ..."
                viewBox="0 0 24 24"
            />
        )
    } else if (state === 'invalid') {
        return <div>This match url is invalid.</div>
    } else if (state === 'waiting') {
        return (
            <div className="w-6/12 shadow-md m-4 p-4 mx-auto text-center">
                <div className="inline-block">
                    waiting for other user to join...
                </div>
                <div className="inline-block w-4 h-4 ml-4 border-b-2 border-violet-500 rounded-full animate-spin"></div>
                <br />
                <button
                    className="rounded-md m-4 p-2 bg-gradient-to-r from-violet-400 to-purple-400 text-white"
                    onClick={() =>
                        navigator.clipboard.writeText(
                            `http://localhost:3000/?join=${match_id}`
                        )
                    }
                >
                    Copy Sharable Link to Clipboard
                </button>
            </div>
        )
    }
    return (
        <div className="w-6/12 shadow-md m-4 p-4 mx-auto text-center">
            {data === null ? (
                <>
                    <div className="inline-block">calculating match...</div>
                    <div className="inline-block w-4 h-4 ml-4 border-b-2 border-violet-500 rounded-full animate-spin"></div>
                </>
            ) : (
                <div>
                    <div>
                        <div className="w-100 text-4xl font-bold">
                            {data.host.name} and {data.guest.name} you have a
                            match of {data.match.percentage}%!
                        </div>
                        <div>
                            {data.match.top_artist === 'null' ? (
                                <div>You had no artists in common</div>
                            ) : (
                                <>
                                    the artist that brought you together was{' '}
                                    {data.match.top_artist}
                                </>
                            )}
                        </div>
                        <div>
                            {data.match.top_genre === 'null' ? (
                                <div>You had no genres in common</div>
                            ) : (
                                <>
                                    the top genre you shared was{' '}
                                    {data.match.top_genre}
                                </>
                            )}
                        </div>
                        <div>
                            {data.match.top_track === 'null' ? (
                                <div>You had no songs in common</div>
                            ) : (
                                <>
                                    the song you both loved was{' '}
                                    {data.match.top_track}
                                </>
                            )}
                        </div>
                    </div>
                    <div className="flex justify-around">
                        <div className="w-50">
                            <img
                                className="rounded-full w-[100px] h-[100px] shadow-sm"
                                src={data.host.pfp_url}
                            />
                            <div>
                                {data.host.name}{' '}
                                <ReactCountryFlag
                                    countryCode={data.host.country}
                                />
                            </div>
                        </div>
                        <div className="w-50">
                            <img
                                className="rounded-full w-[100px] h-[100px] shadow-sm"
                                src={data.guest.pfp_url}
                            />
                            <div>
                                {data.guest.name}{' '}
                                <ReactCountryFlag
                                    countryCode={data.guest.country}
                                />
                            </div>
                        </div>
                    </div>
                </div>
            )}
        </div>
    )
}

export default Match
