# BallPlex
# BallStreams.com Plugin for Plex Media Center
# by Mark Freden m@sitticus.com 
# updated by Kevin Centeno @devteno
# Version .04
# Dec 4, 2014

KEY = 'a534012a8ee25958f374263ece97eb27'

TITLE = 'BallPlex .04'
PREFIX = '/video/ballplex'

ART = 'art-default.jpg'
ICON = 'icon-default.png'
LIVE_ICON = ''
ONDEMAND_ICON = ''
TOKEN = ''

TEAM_NAMES = 'teams.json'

TITLE_LIVEGAMES = 'Live Games'
TITLE_ONDEMANDGAMES = 'On Demand'
TITLE_PREFERENCES = 'Preferences'
TITLE_LOGIN = 'Log In'

URL_LOGIN = 'https://api.ballstreams.com/Login'
URL_LIVEGAMES = 'https://api.ballstreams.com/GetLive?token=%s'
URL_ONDEMANDGAMES = 'https://api.ballstreams.com/GetOnDemand?date=%s&token=%s'
URL_ONDEMANDDATES = 'https://api.ballstreams.com/GetOnDemandDates?token=%s'
URL_ONDEMANDSTREAM = 'https://api.ballstreams.com/GetOnDemandStream?id=%s&token=%s'
URL_GAMEOFF = ''
URL_REPO = ''
URL_LOGOREPO = ''
URL_ARENAREPO = ''

# Import urlparse for encodeUrlToken
from urlparse import urlparse

###################################################################################################
def Start():
    ObjectContainer.art = R(ART)
    ObjectContainer.title1 = TITLE
    DirectoryObject.thumb = R(ICON)

    ValidatePrefs()

###################################################################################################
@handler(PREFIX, TITLE, thumb=ICON, art=ART)
def MainMenu():
    oc = ObjectContainer(no_cache=True)

    # Only show menus if TOKEN has been successfully set
    if TOKEN != None:
        oc.add(DirectoryObject(
            key=Callback(LiveGamesMenu),
            title=TITLE_LIVEGAMES,
            thumb=R(LIVE_ICON)
        ))
        oc.add(DirectoryObject(
            key=Callback(OnDemandDatesMenu),
            title=TITLE_ONDEMANDGAMES,
            thumb=R(ONDEMAND_ICON)
        ))

        oc.add(PrefsObject(
            title=TITLE_PREFERENCES)
        )
    else:
        oc.add(PrefsObject(
            title=TITLE_LOGIN)
        )

    return oc

###################################################################################################
def LiveGamesMenu():
    title = TITLE_LIVEGAMES
    url = URL_LIVEGAMES % TOKEN

    oc = ObjectContainer(title2=title, no_cache=True)

    # Loop thru videos array returned from GetLiveGames
    for video in GetLiveGames(url):
        (game_id, title, srcUrl, logo, arena, summary) = video

        # If there was an error, display it
        if game_id == 0:
            return (ObjectContainer(header="Error", message=title))
        else:
            oc.add(GetStream(game_id, title, srcUrl, logo, arena, summary))

    return oc

###################################################################################################
def GetLiveGames(url):
    # Set up our array to return
    videos = []

    # Get data from server
    json = JSON.ObjectFromURL(url)

    if json["status"] == "Success":

        # Get Prefs
        quality = Prefs['quality']

        # Loop thru each to build videos meta
        for video in json['schedule']:

            game_id = video['id']
            awayTeam = ''
            homeTeam = ''
            startTime = ''
            feedType = ''
            ligature = ''
            isPlaying = ''

            # If the game isn't on yet, set to gameoff vid
            if video['isPlaying'] == 0:
                srcUrl = URL_GAMEOFF

            # Set vid quality chosen in prefs
            elif video['isHd'] == '1' and quality == 'High':
                srcUrl = video['hdUrl']
            else:
                srcUrl = video['sdUrl']

            # Set up home and away teams
            if video['awayTeam']: awayTeam = video['awayTeam']
            if video['homeTeam']: homeTeam = video['homeTeam']

            # Set up arena pic name (have to do it before 'vs' gets added)
            arena = R(ICON)

            # Add 'vs' if there is a home and away team
            if homeTeam: ligature = ' @ '

            # Set up logo pic name
            logo = R(ICON)

            # Add playing indicator if game-on (maybe take this out)
            if video['isPlaying'] == 1: isPlaying = ">"

            if video['startTime']: startTime = "Start Time: " + video['startTime']
            if video['period']: startTime = video['period']
            if video['feedType']: feedType = ' - ' + video['feedType']

            # Put the start time in the summary area
            summary = startTime

            # Built the title
            title = isPlaying + getTeamName(awayTeam) + ligature + getTeamName(homeTeam) + feedType

            videos.append([game_id, title, srcUrl, logo, arena, summary])
    else:
        if json["status"] == "Failed":
            videos.append([0, json["msg"], "", "", "", ""])

    return videos

###################################################################################################
def OnDemandDatesMenu():
    oc = ObjectContainer(title2='On Demand Dates', no_cache=True)

    # Read the dates data from the server
    url = URL_ONDEMANDDATES % TOKEN
    json = JSON.ObjectFromURL(url)

    # Make sure there wasn't an error
    if json["status"] == "Success":

        # Loop thru the array of dates return from the server
        for gameDate in json['dates']:

            if gameDate: # Make sure it's not empty
                oc.add(DirectoryObject(
                    key=Callback(OnDemandGamesMenu, gameDate=gameDate),
                    title=FormatDate(gameDate),
                    thumb=R(ONDEMAND_ICON)
                ))
    else:
        # Display the error if there was one
        return (ObjectContainer(header="Error", message=json["msg"]))

    return oc

###################################################################################################
def OnDemandGamesMenu(gameDate):
    title = 'On Demand Games For ' + gameDate
    url = URL_ONDEMANDGAMES % (gameDate, TOKEN)

    oc = ObjectContainer(title2=title, no_cache=True)

    # Loop thru the array return by GetOnDemandGames
    for video in GetOnDemandGames(url):
        (game_id, title, logo, arena, summary) = video

        oc.add(DirectoryObject(
            key=Callback(OnDemandStreamMenu, game_id=game_id, title=title, logo=logo, arena=arena, summary=summary),
            title=title,
            thumb=URL_LOGOREPO + logo,
            art=URL_ARENAREPO + arena,
            summary=summary
        ))

    return oc

###################################################################################################
def OnDemandStreamMenu(game_id, title, logo, arena, summary):
    url = URL_ONDEMANDSTREAM % (game_id, TOKEN)
    game_json = JSON.ObjectFromURL(url)

    # Get Prefs
    quality = Prefs['quality']

    oc = ObjectContainer(title2=title, no_cache=True)

    homeTeam = game_json['homeTeam']
    awayTeam = game_json['awayTeam']

    homeHighlights = game_json['highlights'][0]['homeSrc']
    awayHighlights = game_json['highlights'][0]['awaySrc']
    homeCondensed = game_json['condensed'][0]['homeSrc']
    awayCondensed = game_json['condensed'][0]['awaySrc']
    if game_json['HDstreams'][0]['src']: HD = game_json['HDstreams'][0]['src']
    if game_json['SDstreams'][0]['src']: SD = game_json['SDstreams'][0]['src']

    if homeTeam:
        gameName = "Full Game"
    else:
        gameName = "Watch " + awayTeam

    # Set vid quality chosen in prefs
    if HD and quality == 'High':
        oc.add(GetStream(game_id, gameName, HD, logo, arena, summary, False, True))
    else:
        oc.add(GetStream(game_id, gameName, SD, logo, arena, summary, False, True))

    # If the home and away feeds are the same, don't bother listing both
    if homeCondensed == awayCondensed and homeCondensed != "" and awayCondensed != "":
        oc.add(GetStream(game_id, "Condensed Game", homeCondensed, logo, arena, summary, False, True))
    else:
        if homeCondensed:
            oc.add(GetStream(game_id, homeTeam + " Condensed Game", homeCondensed, logo, arena, summary, False, True))
        if awayCondensed:
            oc.add(GetStream(game_id, awayTeam + " Condensed Game", awayCondensed, logo, arena, summary, False, True))

    if homeHighlights == awayHighlights and homeHighlights != "" and awayHighlights != "":
        oc.add(GetStream(game_id, "Highlights", homeHighlights, logo, arena, summary))
    else:
        if homeHighlights:
            oc.add(GetStream(game_id, homeTeam + " Highlights", homeHighlights, logo, arena, summary, False, True))
        if awayHighlights:
            oc.add(GetStream(game_id, awayTeam + " Highlights", awayHighlights, logo, arena, summary, False, True))

    return oc

###################################################################################################
def GetOnDemandGames(url):
    videos = []

    # Get data from server
    game_json = JSON.ObjectFromURL(url)

    if 'ondemand' in game_json:
        for video in game_json['ondemand']:

            # If there isn't an iStream, don't list it
            if video['isiStream'] == 1:

                game_id = video['id']
                awayTeam = ''
                homeTeam = ''
                summary = ''
                feedType = ''
                ligature = ''

                # Set up home and away teams
                if video['awayTeam']: awayTeam = video['awayTeam']
                if video['homeTeam']: homeTeam = video['homeTeam']

                # Set up arena pic name (have to do it before 'vs' gets added)
                arena = R(ICON)

                # Add 'vs' if there is a home and away team
                if homeTeam: ligature = ' @ '

                # Set up logo pic name
                logo = R(ICON)

                # Add the feedType with a dash
                if video['feedType']: feedType = ' - ' + video['feedType']

                # Built the title
                title = getTeamName(awayTeam) + ligature + getTeamName(homeTeam) + feedType

                videos.append([game_id, title, logo, arena, summary])

    return videos

###################################################################################################
def GetStream(game_id, title1, url, thumb, art, summary, include_container=False, is_mp4=False):
    Log("GetStream Game: " + str([game_id, title1, url, thumb, art, summary]))

    container = Container.MP4
    video_codec = VideoCodec.H264
    audio_codec = AudioCodec.AAC
    audio_channels = 2

    if is_mp4:
        vco = VideoClipObject(
            key=Callback(GetStream, game_id=game_id, title1=title1, url=url, thumb=thumb, art=art, summary=summary,
                         include_container=True, is_mp4=True),
            rating_key=game_id,
            title=title1,
            art=URL_ARENAREPO + art,
            thumb=URL_LOGOREPO + thumb,
            summary=summary,
            items=[
                MediaObject(
                    parts=[
                        PartObject(key=Callback(PlayVideo, url=url))
                    ],
                    container = container,
                    video_codec = video_codec,
                    audio_codec = audio_codec,
                    audio_channels = audio_channels,
                    optimized_for_streaming=True
                )
            ]
        )
    else:
        vco = VideoClipObject(
            key=Callback(GetStream, game_id=game_id, title1=title1, url=url, thumb=thumb, art=art, summary=summary,
                         include_container=True, is_mp4=False),
            rating_key=game_id,
            title=title1,
            art=URL_ARENAREPO + art,
            thumb=URL_LOGOREPO + thumb,
            summary=summary,
            items=[
                MediaObject(
                    optimized_for_streaming=True,
                    parts=[
                        PartObject(key=HTTPLiveStreamURL(url=url))
                    ]
                )
            ]
        )

    if include_container:
        return ObjectContainer(objects=[vco])
    else:
        return vco

@indirect
def PlayVideo(url):
    return IndirectResponse(VideoClipObject, key=url)

###################################################################################################
def ValidatePrefs():
    # When prefs get saved, update Token
    global TOKEN

    TOKEN = GetToken()

    # Assume there was an error
    if TOKEN == None:
        return ObjectContainer(header="Login Error",
                               message="Make sure your username and password are correct.")

###################################################################################################
def GetToken():
    # Get the username and pass from the prefs
    user = Prefs['username']
    password = Prefs['password']

    data = {'username': user, 'password': password, 'key': KEY}

    # Get the token from BS Login API
    try:
        json = JSON.ObjectFromURL(URL_LOGIN, data)
        ## How can I get the HTTP Error and the json? ##

        return json['token']

    except:
        return None

###################################################################################################
def encodeUrlToken(url):
    # Encode the token param so it doesn't fail on 3rd party/web devices

    parsed = urlparse(url)

    encodedToken = String.Quote(parsed[4], True)

    encUrl = parsed[0] + '://' + parsed[1] + parsed[2] + "?" + encodedToken

    return encUrl

###################################################################################################
def FormatDate(theDate):
    # Import date and time modules
    from datetime import date, timedelta
    import time

    # Get and make today and yesterday strings for comparison to theDate
    today = date.today()
    todayStr = today.strftime("%m/%d/%Y")
    yesterday = today - timedelta(1)
    yesterdayStr = yesterday.strftime("%m/%d/%Y")

    # If theDate is today or tomorrow return that
    if theDate == todayStr:
        return "Today"
    elif theDate == yesterdayStr:
        return "Yesterday"
    else:
        # Convert the text to a time obj
        c = time.strptime(theDate, "%m/%d/%Y")

        # Get day item and add suffix
        day = c[2]
        if 4 <= day <= 20 or 24 <= day <= 30:
            suffix = "th"
        else:
            suffix = ["st", "nd", "rd"][day % 10 - 1]

        # Format into a readable format
        formatedDate = time.strftime("%A the %d" + suffix + " of %B, %Y", c)

        # Strip any leading zeros from the day
        formatedDate = formatedDate.replace(' 0', ' ')

        return formatedDate

###################################################################################################
def getTeamName(teamName):
    # Display short or long team name

    useShortNames = Prefs["shortnames"]

    ShortTeams = Resource.Load(TEAM_NAMES, False)
    ShortTeams = JSON.ObjectFromString(ShortTeams)

    if useShortNames == "On":
        teamNameLower = teamName.lower()
        if teamNameLower in ShortTeams:
            return ShortTeams[teamNameLower] # It does so get name
        else:
            return teamName # It doesn't return original

    return teamName