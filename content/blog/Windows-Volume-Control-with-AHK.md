+++
title = "Windows Volume Control with AHK"
date = 2017-05-13
updated = 2017-07-31
aliases = [ "2017/05/13/Windows-Volume-Control-with-AHK.html" ]
+++

This is some code I use at work to control my laptop's volume and mute it when the I locked the device.
It was born from the frustration I felt when frantically tying to silence my music while my coworkers laughed at me that one time I locked my screen without muting and then removed my earbuds from the headphone jack.

The easiest way to install it is to download AutoHotKey, compile the script into an executable, then place it or a shortcut to it in the Startup folder.

```
; Map Function keys to volume controls
; Useless if your keyboard comes with Volume controls
F6::Send {Volume_Mute}
F7::Send {Volume_Down}
F8::Send {Volume_Up}
```

```
; Mute the sound when the screen locks
; by intercepting the keyboard shortcut Win+L
#l::
SoundGet, is_mute, , Mute
if is_mute = off
    Send {Volume_Mute}
```

