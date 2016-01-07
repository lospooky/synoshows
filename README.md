# SynoShows
SynoShows is a series of scripts for managing the TV Show library on your [Synology](http://www.synology.com) NAS unit(s).

The main functionality is that of automating the renaming of TV Show files downloaded via the Synology's own DownloadStation and sorting it into your existing collection. Additionally, it will send you a [PushBullet](http://www.pushbullet.com) notification when DownloadStation finishes downloading something, TV Show or not. Pretty Neat!

## Installation

### Prerequisites
* DownloadStation on your Synology NAS
* Python 2.7 on your Synology NAS
* Install pip. Quickest way seems to [Download this file](https://raw.githubusercontent.com/pypa/pip/master/contrib/get-pip.py) somewhere on your Syno, and run it with python `python get-pip.py`
* [Tvnamer](https://github.com/dbr/tvnamer) `pip install tvnamer`, an awesome utility to rename tv show files
* [Pushbullet.py](https://github.com/randomchars/pushbullet.py) `pip install pushbullet.py`, excellent Python library for the [PushBullet](http://www.pushbullet.com) services 

### Setup
* Clone the repo somewhere on your Synology `git clone https://github.com/lospooky/synoshows.git`
* Edit `/var/packages/DownloadStation/scripts/start-stop-status` and put a # sign in front of the following line<br>
`rm ${PACKAGE_DIR}/etc/download/settings.json` it should be line 86.<br> This will comment it out, disabling the deletion of DownloadStation's setting file every time it starts.
* Stop, Start, and Stop once again DownloadStation via the Synology Package Manager or by running via shell the `start-stop-status` script we just edited. There now should be a `settings.json` file in `/usr/syno/etc/packages/DownloadStation/download`
* Edit `settings.json` to set it to run our script every time DownloadStation completes a download task.<br> Typically the script will be SynoShows' `dl_complete.py` 
  *`"script-torrent-done-enabled": true`, line 57
  *`"script-torrent-done-filename": "/complete/path/to/script.py"`, line 58
* Set the correct permissions for the SynoShows script files, user access, being able to be executed, etc..
* Restart DownloadStation
* To check everything is working smoothly, set DownloadStation's `settings.json` to run `dl_complete_triggercheck.py`. Each time this script runs, it will write a line to the text file specified inside.

## Configuration
<p>
To configure SynoShows, edit the settings.json in its own main folder. 
* `pushbulletkey` has to be set to your own PushBullet API Key (Access Token). Get one from your Pushbullet [Account Settings](https://www.pushbullet.com/#settings/account). It's required to correctly send the PushBullet notifications.
* `tvnamerconfig_path` specifies the configuration file tvnamer will use when invoked by the SynoShows scripts. I have included the one I personally use, you are welcome to use any of your liking.
* `live` provides the configuration for use on live usage, when downloading real shows.
* `test` provides convenience, separate configuration parameters to use when testing out functionality, [more below](#testing).
</p>

<p>
The parameters for the two operating configurations are:
* `filetypes` is the list of filetypes (extensions) that will be treated as Tv Show files.
* `downloadPath` is the directory where DownloadStation is set to download your Show files.
* `pathAsInDb` should be the same as `downloadPath` but without starting or trailing slashes, e.g. `path/to/my/directory`. It's how the path appears in the internal Synology PostgreSQL database.
* `destinationPath` is an intermediate directory the SynoShows scripts will move the show files to, useful to have in case something goes wrong with the renaming process, i.e. thetvdb goes down...
* `archivePath` is the final root path the show files will be moved to, it should be the main, indexed, directory for your shows.
* `mockDbFile` is a txt file that will be used to generate mock files during testing, a sample one is provided. **Test configuration only** 
</p>

## Operations
The workflow of the Synoshows scripts can be summarized as follows:
* When DownloadStation completes a download, the main script `dl_complete.py` is invoked.
* The builtin Synology PostgreSQL database is queried for the DownloadStation task queue.
* Any completed task whose path is `downloadPath` and whose type matches `filetypes` will be treated as a Tv Show file, other completed downloads will be detected as well.
* Tv Show files will be moved to `destinationPath`  and the DownloadStation queue will be cleared.
* `tvnamer` will be invoked on all files in `destinationPath`, using the specified `tvnamerconfig_path` configuration. Show files will be now renamed.
* Successfully identified (and renamed) Show files will be finally moved to `archivePath/showname/showseason/` and they will be added to the Synology Media Index Database (VideoStation, ... ). The Show's proper name and season are identified via `tvnamer` output.
* Finally, you will get a PushBullet notification for the completed downloads. You will be notified about both completed TV Shows and other types of download.

### Testing
I have provided a couple relatively hassle-free test scripts. They are useful for troubleshooting potential issues.
Also, their aim is to help you find a configuration setup of your liking and more generally to assist you with tweaking my scripts to your liking. Have fun!

* `test_pushbullet.py` is a very simple script to verify everything is in order with PushBullet functionality. API key, note content, etc...
* `test_dl_complete_mockdata.py` instead allows you to test the whole processing stack without requiring any actual download to complete on your Synology NAS.<br>
It takes the list of filenames specified in `mockDbFile` and it will generate matching `.txt` files in its own (test configuration) `downloadPath` as well as a fake DownloadStation queue referring to these files. From there everything will proceed as with live processing except that the scripts are set to process `.txt` files. These files will of course not be added to the Synology Media Index. Be sure to specify test configuration paths somewhere else than your actual path to avoid confusion and/or interference!

### Other Functions
Sometimes, the Synology Media Index ends up having orphan entries: database entries whose referred file is not there anymore. Run `util_remove_orphans.sh` or `util_sanitize_mediadb.py` to get rid of those orphans.
