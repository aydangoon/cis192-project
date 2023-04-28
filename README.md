## Spotify Matchmaker

### Overview

I want to create a web app that allows spotify users to compare their music taste
compatibility. The criteria for compatibility will be based on users top artists,
genres, albums, etc. A user will be able to send another user a link to the site,
and once the other user has joined, the page will update with relevant information
about their music taste compatibility. It will display interesting metrics, such as
both users top genres over time, difference in their genre or artist variance, etc.

The backend will be entirely python. For the frontend I wil use svelte.

Additional features I could include are:

- group compatibility, i.e. compatability page for more than 2 users
- interactive ui, but this would be through js frameworks like `charts.js`

### Class Definition

I will likely need a class for user Spotify data. The class will have methods
for cleaning and parsing the data as well as methods for getting certain data features.
Internally, the data will be stored with a pandas dataframe.

### First Party Module

- `json`: To parse responses and format requests for the Spotify API.

### Third Party Modules

- `flask`: web framework for the app's backend. Picking this because it is beginner-friendly
  and well documented.
- `numpy`: to easily manipulate and organize metrics data to be sent to the frontend.
- `pandas`: to store spotify-authenticated users who have pending, or completed match invites
  as well as the compatibility results of those matches.
