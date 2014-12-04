BallPlex
========
Plex plugin for [Ballstreams.com](http://www4.ballstreams.com/assist/categories/13/api+discussion/4232/APP+BallPlex)

Original author:  FredenFromSweden / Mark Freden 

## Installation
You need to install Plex Media Server before you can use this plugin.

**If you have a previous version of BallPlex, please remove it before installing an updated version**

1. Download the latest version of BallPlex [here](https://github.com/kevcenteno/BallPlex/archive/v0.4.zip)
2. Extract the `BallPlex-0.4` folder from the zip file and rename this folder to `BallPlex.bundle`
3. Move the `BallPlex.bundle` folder from step 3 into the Plex Media Server, Plug-ins folder:
  * Mac: `~/Library/Application Support/Plex Media Server/Plug-ins/`
  * Windows: `C:\Users\<your user>\AppData\Local\Plex Media Server\Plug-ins`
  * Linux: `(Installation Directory)/Application Support/Plex Media Server/Plug-ins/`
4. Restart Plex Media Server

### Configure
Most devices will allow you to enter your BallStreams username and password from the Log In menu when you go to the BallPlex Channel. If your device does not, you can enter them using the Plex Media Manager. To do this:

1. Choose Media Manager from the Plex menu in your menubar/taskbar or open the Plex Media Server app again.
2. Under Channels, choose BallPlex.
3. Click the "Settings" (gear) icon.
4. Enter your ballstreams account username and password, press "Save" to save
  
## Known Issues
* Live streams don't work on Plex Web Client, and possibly other devices.  This is due to the use of HLS streams.

## Release Log
#### Version .04 - Dec 4, 2014
* On Demand streams: Add "Home Feed" or "Away Feed" to game title as appropriate
* On Demand streams: Use MP4 streams instead of HLS; should improve compatibility on devices (tested on Plex Web Client)
