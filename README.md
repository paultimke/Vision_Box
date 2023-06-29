# Vision Box User Interface Quality Assessment System
The Vision Box is a Computer-Vision-based system designed to automate testing of screens during the development phases of a User Interface. The physical system consists of an enclosed box to ensure a light-controlled environment for any device introduced and containts an illumination system which can be set manually or automatically through the accompanying Desktop Command-Line application.

All commands supported by the Dekstop application can be displayed using the HELPME command. Some of the main commands for a testing session are:
- **FICON**: Find a specific icon or subimage embedded within a larger image
- **COMPIMAGE**: Compare two images for similarity, returning a total similarity score
- **FTEXT**: Find specific Ascii-based text (words, letters, sentences) within the screen

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
The images used on the above session were the following:
<img width="780" alt="images_dut" src="https://github.com/paultimke/Vision_Box/assets/87957114/f629eb5c-71e6-4745-8412-0bf6ae271fb7">

After the test, the following output images and log file will be produced:
<p float="left">
  <img width="150" alt="ficon_out" src="https://github.com/paultimke/Vision_Box/assets/87957114/cae11482-e7bf-4f8a-89f9-cc89fcd9d3b0">
  <img width="153" alt="ftext_out" src="https://github.com/paultimke/Vision_Box/assets/87957114/13115623-219c-4977-9bd8-3c2a840fddca">
</p>

```
VISION BOX LOG FILE
Vision Box software version 0.1.0
Starting light level: 0
Verbose Output enabled: True

TIMESTAMP              #  who  DESCRIPTION
[2023-06-29-00-27-40]  1 [PC]  TESTSTATUS(START)
[2023-06-29-00-27-43]  2 [PC]  FICON(clock.png)
[2023-06-29-00-27-54]  3 [VB]  FICON PASSED
[2023-06-29-00-27-54]  4 [VB]  FICON Number of objects detected: 1
[2023-06-29-00-27-56]  6 [PC]  COMPIMAGE(test_screen.png)
[2023-06-29-00-27-56]  7 [VB]  COMPIMAGE Structural similarity: 0.81
[2023-06-29-00-27-58]  8 [VB]  COMPIMAGE Image text similarity: 0.9
[2023-06-29-00-27-58]  9 [VB]  COMPIMAGE PASSED
[2023-06-29-00-28-01]  10 [PC]  FTEXT(network)
[2023-06-29-00-28-04]  11 [VB]  FTEXT PASSED
[2023-06-29-00-28-04]  12 [VB]  FTEXT Number of times the text 'network' was found: 1
[2023-06-29-00-28-06]  14 [PC]  TESTSTATUS(END)
[2023-06-29-00-28-06]  15 [VB]  
PASSED
```



