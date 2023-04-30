import React, { createContext, useState } from 'react'
import { Redirect, Route, BrowserRouter as Router } from 'react-router-dom'
import Home from './home.jsx'

export const AppContext = createContext()
const App = () => {
    const [appState, setAppState] = useState({
        sid: null,
    })
    return (
        <AppContext.Provider value={[appState, setAppState]}>
            <Router>
                <Route path="/" component={Home} />
                <Redirect path="*" to="/" />
            </Router>
        </AppContext.Provider>
    )
}

export default App
