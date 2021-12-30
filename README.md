LED Firework
==============

This counts down to midnight by slowly filling a SK6812 LED-strip with blue instead of red. When the strip is full it will play a simple "fireworks" animation.

This was originally meant to be run on an ESP32 using uPython but it turned out that it wasnt QUITE powerfull enough to provide a good FPS without some code-optimization or re-writing it in C and due to time-constraints it was easier to just run it on a Raspberry Pi instead.
