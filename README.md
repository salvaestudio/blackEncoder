# blackEncoder
Video encoder written in Python and based on ffmpeg and PyQt4

What differentiates this video encoder from others is that I have created it for very specific uses.
They are presets that I frequently use in which I automatically add a few black frames in front of and behind the video and I use a certain codecs of video and audio and insert a certain TC.

It is tested in linux and works well.

Pending improvements:

- Optimize the code.
- Use exceptions (try - except) to throw errors.
- Progress bar. Currently it passes fast to 99% and it is waiting to finish the process to go to 100% and close. I have not connected the progress bar with the ffmpeg action.
- Make a Swift version for Mac compiling the application with ffmpeg included.

![screenshot](https://k61.kn3.net/8/B/C/9/E/D/077.png)


