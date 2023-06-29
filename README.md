# Vision Box User Interface Quality Assessment System
The Vision Box is a Computer-Vision-based system designed to automate testing of screens during the development phases of a User Interface. The physical system consists of an enclosed box to ensure a light-controlled environment for any device introduced and containts an illumination system which can be set manually or automatically through the accompanying Desktop Command-Line application.

The Desktop Application supports the following commands:
- **TESTSTATUS(START)**: Start a testing session
- **TESTSTATUS(END)**: End a testing session
- **FICON**: Find a specific icon or subimage embedded within a larger image
- **COMPIMAGE**: Compare two images for similarity, returning a total similarity score
- **FTEXT**: Find specific Ascii-based text (words, letters, sentences) within the screen
- **SETLIGHT**: Adjust light settings in the Vision Box
- **HELPME**: Display help message and syntax of commands
- **EXAMPLE**: Display examples of command usages

## Usage Example
Imagine you have created a new screen for the UI and have an image called 'test\_screen.png'. You also have an image of an asset you want to look for in that screen. The following example of a test session will look for the asset within the image, compare the device-under-test to the screen reference provided and look for the keyword "network" within the device-under-test:

```
TESTSTATUS(START)

Initializing Hardware

TEST STARTED
[PC] >> FICON("clock.png")
[VB] >> ACK FICON(clock.png)
[PC] >> COMPIMAGE("test_screen.png")
[VB] >> ACK COMPIMAGE(test_screen.png)
[PC] >> FTEXT("network")
[VB] >> ACK FTEXT(network)
[PC] >> TESTSTATUS(END)
[VB] >> ACK TESTSTATUS(END)

Waiting on commands to finish processing...
Test result: PASSED
```


