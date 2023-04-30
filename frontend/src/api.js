const setCookie = require('set-cookie')
const url = 'http://localhost:8000/';
exports.get_data = async (sid) => {
    return await fetch(`${url}?sid=${sid}`).then(res => res.json()).catch(err => {
        console.log("Not authorized");
        return { authorized: false}
    })
}

exports.get_authorize_url = async () => {
    return await fetch(url + 'connect_account').then(res => res.json()).catch(err => {
        console.log("Error getting redirect url");
        return { redirect_url: null}
    })
}

exports.authorize = async (code) => {
    return await fetch(`${url}authorize?code=${code}`).then(res => res.json()).catch(err => {
        console.log("Error authorizing");
        return { sid: null }
    })
}

exports.create_match = async (sid) => {
    return await fetch(`${url}create_match?sid=${sid}`).then(res => res.json()).catch(err => {
        console.log("Error creating match");
        return { match_id: null }
    })
}

exports.get_match_state = async (sid, match_id) => {
    return await fetch(`${url}match_state/${match_id}?sid=${sid}`).then(res => res.json()).catch(err => {
        console.log("Error getting match state");
        return { state: null }
    })
}

exports.get_match_data = async (match_id) => {
    /*
    {
        host: {
            name,
            country_code,
            pfp_url
        },
        guest: {
            name,
            country_code,
            pfp_url
        },
        match: {
            percentage,
            top_genre,
            top_artist,
            top_track,
        }
    }  
    */ 
    return await fetch(`${url}match/${match_id}`).then(res => res.json()).catch(err => {
        console.log("Error getting match data");
        return null
    })
}