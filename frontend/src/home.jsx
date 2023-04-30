import { useLocation, useHistory } from 'react-router-dom'
import { AppContext } from './App'
import { useContext, useEffect, useState } from 'react'
import api from './api'
const Home = () => {
    const [appContext, setAppContext] = useContext(AppContext)
    const location = useLocation()
    const history = useHistory()
    const queryParams = new URLSearchParams(location.search)
    const code = queryParams.get('code')
    const join = queryParams.get('join')
    if (join && appContext.sid) history.push(`/match/${join}`)

    const [data, setData] = useState(null)
    const [error, setError] = useState(null)
    const getData = async (sid) => {
        const retrievedData = await api.get_data(sid || appContext.sid)
        console.log(retrievedData)
        setData(retrievedData)
    }

    const connectAccount = async () => {
        const url = await api
            .get_authorize_url()
            .then(({ redirect_url }) => redirect_url)
        if (url === null) {
            setError('Failed to get authorization url')
        } else {
            window.location.href = url
        }
    }

    const authorize = async () => {
        const { sid } = await api.authorize(code)
        console.log(sid)
        if (sid !== null) {
            getData(sid)
            setAppContext({ sid })
        } else {
            setError('Failed to authorize account')
        }
    }

    const createMatch = async () => {
        await api.create_match(appContext.sid).then(({ match_id, error }) => {
            if (error) {
                setError(error)
            } else {
                history.push(`/match/${match_id}`)
            }
        })
    }

    useEffect(() => {
        if (code != null) {
            authorize()
        } else {
            getData()
        }
    }, [])

    return (
        <div className="w-6/12 shadow-md m-4 p-4 mx-auto text-center">
            <h1 className="text-2xl font-bold">Spotify Matchmaker</h1>
            <div>See how compatible you're music tastes are with others!</div>
            {data == null ? (
                <svg
                    className="animate-spin h-5 w-5 mr-3 ..."
                    viewBox="0 0 24 24"
                />
            ) : data.authenticated ? (
                <div className="mt-8">
                    <div>Welcome!</div>
                    <div>to get started, create a new match</div>
                    <button
                        className="rounded-md m-4 p-2 bg-gradient-to-r from-violet-400 to-purple-400 text-white"
                        onClick={createMatch}
                    >
                        Create Match
                    </button>
                </div>
            ) : (
                <button
                    className="rounded-md m-4 p-2 bg-gradient-to-r from-violet-400 to-purple-400 text-white"
                    onClick={connectAccount}
                >
                    Connect your Spotify Account
                </button>
            )}
            {error && <div className="text-red-500">{error}</div>}
        </div>
    )
}

export default Home
