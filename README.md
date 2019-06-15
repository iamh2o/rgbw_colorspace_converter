## Requirements

* Python 2.7
  [http://www.python.org](http://www.python.org)

* Processing 2.2.1+ (for simulator only)
  [http://www.processing.org](http://www.processing.org)

There are a few 3rd party python modules that need to be installed:

  * cherrypy
  * pybonjour

Install python modules with *easy_install* (You can also use *pip* if you have a preference)  For example:

    easy_install cherrypy

Don't worry too much if you can't get some of the dependencies to install - you'll still be able to run the software, just with some features missing.  Python and Processing are the most important parts if you just want to write shows.

## Getting Started

First, check out the repository:

	hg clone ssh://hg@bitbucket.org/grgbrn/baaahs2014

The simulator lives in the 'SheepSimulator' directory.  Open the file 'SheepSimulator.pde' in Processing, and run it.

To start the lighting software talking to the simulator:

	python go.py --simulator

You can also specify which show to run by using the name of the show:

    python go.py --simulator MyShow

You can also choose which show is running through the web interface:

[http://localhost:9990/](http://localhost:9990/)

## Writing Shows

See the files in 'doc'

## OSC Control

Lighting can be controlled wirelessly over OSC. We're using [TouchOSC](http://hexler.net/software/touchosc), which is available for [iOS](https://itunes.apple.com/app/touchosc/id288120394) and [Android](https://play.google.com/store/apps/details?id=net.hexler.touchosc_a).  (It costs $4.99, but it's worth it, we promise!)

You'll need to install the app on your phone or tablet, then intall a layout.

	1. Download the TouchOSC Editor from the TouchOSC page (scroll down to 'Downloads') 
	2. Open the show control layout from the baaahs repository (misc/ShowControl.touchosc)
	3. Click 'Sync' in the TouchOSC Editor menubar and follow the on-screen instructions
	
For more details on controlling shows with OSC, check the 'doc' directory in this repository.

## Hardware Support

Communicating with the hardware requires [OLA.](http://www.opendmx.net)

OS X:

    brew install ola --with-python

Debian / Ubuntu:

    sudo apt-get install ola ola-python ola-rdm-tests

## Tips

Trouble installing python dependencies?  Try some of these magic incantations:

OS X:

    pip install --no-use-wheel CherryPy

    pip install setuptools-git
    pip install --allow-external pybonjour pybonjour

Debian / Ubuntu:

    apt-get install libavahi-compat-libdnssd1

    pip install --allow-external pybonjour --allow-unverified pybonjour pybonjour



