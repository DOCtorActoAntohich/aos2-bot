# Emi

## How to run

Clone this repository and go to the root folder.

Create a copy of `sample.env` named `.env` and adjust values as you see fit.

While keeping the game open in the background, execute `python -m emi` in console.
To stop, press `Ctrl+C`.

## Issues

#### Screen borders

The window should NOT clip with physical screen borders, otherwise some parts of the window won't update.

#### Foreground window

The window _has to_ be in foreground (active) for inputs to work.

AoS2 really (really) wants you to use DirectInput.
However, you cannot directly send simulated keystrokes to the game's window when it's in background.
The workaround was implemented,
but just in case your system does something unexpected,
you've been warned.