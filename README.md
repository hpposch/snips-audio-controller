# snips-audio-controller

This is a very early version of a snips audio controller.
The main aim of this code is to fade down the volume of all audio inputs during snips is talking and when snips is finished to set it back to it's old value.

As said above the code is a very early version and it is more of quick proof of concept.
So don't wonder if it is a bit dirty ;)

Anyway i hope it can help you with your project.

Just to note, i use a third party script from: https://github.com/GeorgeFilipkin/pulsemixer/
This is needed to control all my pulseaudio sinks.

HAVE FUN!



# Getting Started

```
git clone https://github.com/hpposch/snips-audio-controller.git
cd snips-audio-controller
python snipsAudioController.py
```

I also placed a example for a systemd service inside the source folder so you can copy that file


# ATTENTION!!!
All paths inside this python script are hardcode an will not match your system so you have to change them manually.
