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