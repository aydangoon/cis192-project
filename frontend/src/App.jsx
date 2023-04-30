import React, { createContext, useEffect, useState } from 'react'
import {
    Redirect,
    Switch,
    Route,
    BrowserRouter as Router,
} from 'react-router-dom'
import Home from './home.jsx'
import Match from './match.jsx'

export const AppContext = createContext()
const App = () => {
    const [appState, setAppState] = useState({
        sid: sessionStorage.getItem('sid'),
    })
    useEffect(() => {
        const sid = sessionStorage.getItem('sid')
        if (sid !== null) {
            setAppState({ sid })
        }
    }, [])
    useEffect(() => {
        sessionStorage.setItem('sid', appState.sid)
    }, [appState.sid])
    return (
        <AppContext.Provider value={[appState, setAppState]}>
            <Router>
                <Switch>
                    <Route path="/match/:match_id" component={Match} />
                    <Route exact path="/" component={Home} />
                    <Route
                        path="*"
                        compontent={() => <Redirect path="*" to="/" />}
                    />
                </Switch>
            </Router>
        </AppContext.Provider>
    )
}

export default App
