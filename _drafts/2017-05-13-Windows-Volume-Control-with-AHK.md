---
layout: default
title: Windows Volume Control with AHK
---

This is some code I use at work to control my laptop's volume/muting.
It was born from the fustration felt while frantically tying to silence my music while my coworkers laughed at me.

The easiest way to install it is to download AutoHotKey, compile the script into an executable, then place it or a shortcut to it in the Startup folder.

Of course, if your keyboard has built in volume controls, it's much less useful.

```
; Map Function keys to volume controls
F6::Send {Volume_Mute}
F7::Send {Volume_Down}
F8::Send {Volume_Up}

; Mute the sound when the screen locks
; by intercepting the keyboard shortcut Win+L
#l::
SoundGet, is_mute, , Mute
if is_mute = off
    Send {Volume_Mute}
```
