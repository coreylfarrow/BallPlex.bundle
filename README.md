BallPlex
========
Plex plugin for [Ballstreams.com](http://www4.ballstreams.com/assist/categories/13/api+discussion/4232/APP+BallPlex)

Original author:  FredenFromSweden / Mark Freden 

## Installation
1. You need to install Plex Media Server before you can use this plugin.
2. Download the latest version of BallPlex [here](https://github.com/kevcenteno/BallPlex/archive/v0.4.zip)
3. Unzip and rename the folder from `BallPlex-0.4` to `BallPlex.bundle`
4. Move the `BallPlex.bundle` folder from step 3 into the Plex Media Server, Plug-ins folder:
  * Mac: `~/Library/Application Support/Plex Media Server/Plug-ins/`
  * Windows: `C:\Users\<your user>\AppData\Local\Plex Media Server\Plug-ins`
  * Linux: `(Installation Directory)/Application Support/Plex Media Server/Plug-ins/`
  
## Known Issues
* Live streams doesn't work on Plex Web Client, and possibly other devices.  This is due to the use of HLS streams.

## Release Log
#### Version .04 - Dec 4, 2014
* On Demand streams: Add "Home Feed" or "Away Feed" to game title as appropriate
* On Demand streams: Use MP4 streams instead of HLS; should improve compatibility on devices (tested on Plex Web Client)
