+++
title = "Saving YouTube Playlists to Android"
date = 2016-09-25
updated = 2017-08-13
aliases = [ "2016/09/25/Saving-YouTube-Playlists-to-Android.html" ]
+++

I use the following method to update the songs on my Android phone:

- Change to the correct directory

```bash
cd ~/Music/YouTube
```

- Use [youtube-dl](https://github.com/rg3/youtube-dl) to download my songs playlist.
This [answer](http://askubuntu.com/questions/673442/downloading-youtube-playlist-with-youtube-dl-skipping-existing-files) on askubuntu was very helpful

```bash
youtube-dl --download-archive downloaded.txt \
    --no-post-overwrites \
    --max-downloads 10 \
    -ciwx \
    --audio-format mp3 \
    -o "%(title)s.%(ext)s" \
    <playlist-url>
```

- Start [SSHelper](http://arachnoid.com/android/SSHelper/) on my Android

- Use `rsync` to push the songs (your Android's IP will probably be different, just check the output from SSHelper)

```bash
rsync -rvh --progress --stats  -e 'ssh -p 2222' . 192.168.1.66:/sdcard/Music/
```
