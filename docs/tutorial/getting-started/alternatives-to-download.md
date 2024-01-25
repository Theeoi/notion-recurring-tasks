# Alternatives to Downloading the Finished Executable

The easiest way of getting started with this software is to download the included executable files from the releases. However, if you would like to take an alternative route to getting the software on your computer you can. These are your alternatives:

- Install the software to a Python environment
- Build your own executable file

No matter which alternative you choose you must download the source code onto your computer. All options require some computer prowess in navigating a terminal window and executing a few commands. After having followed these steps you should continue the [Getting Started tutorial](index.md#setting-up-your-notion-integration) to set up your Notion database and integration.

## Prerequisites

### Getting the Source Code

The first step is to get the source code and be able to explore it through a terminal window.

The source code is available with every release on the [release page on Github](https://github.com/Theeoi/notion-recurring-tasks/releases). Download the Source code and extract it to an appropriate location.

Open a terminal and navigate to the source code. There are multiple ways of doing this but an easy option is to navigate to the extracted folder in a file explorer, right click in the folder and select 'Open in terminal'. If successful you should be able to to type `ls` and see the contents of the directory.

![ls source](../../assets/img/source-1.PNG)

### Activating a Python Virtual Environment

When installing Python packages it is customary to create what is known as a virtual environment and install the package there. This is done as to seperate this install from interfering with other installed Python packages on your system.

Run the following terminal command in the source code directory `python3.12 -m venv .venv`. If you receive an error it could mean that you do not have the correct version of Python installed. [Install Python 3.12](https://www.python.org/downloads/) and retry the above command.

Having created a the virtual environment we can now activate it using the following commands:

- Windows: `.\.venv\Scripts\activate`
- Linux/macOS: `source .venv/bin/activate`

If successful you should see the name of the virtual environment by the commandline.

![Activate venv](../../assets/img/source-2.PNG)

## Installing the Software from Source

### Installing the Software

Having already activated our virtual environment it is very easy to install the software. Run the following command `python -m pip install .` with the virtual environment activated.

If the install was successful you should be able to run the command `pip list` and see all packages installed in the virtual environment.

![pip list](../../assets/img/install-3.PNG)

### Running the Software

The software is now installed within the virtual environment. Run the script using the command `notion-recurring-tasks` with the virtual environment activated.

![Running the software](../../assets/img/install-4.PNG)

## Building an Executable from Source

### Installing the Software and Development Dependencies

To build your own executable you must install the dependencies required to do so. Having already activated our virtual environment it is very easy to install these dependencies. Run the following command `python -m pip install .[dev]` with the virtual environment activated.

If the install was successful you should be able to run the command `pip list` and see all packages installed in the virtual environment.

![pip list dev](../../assets/img/build-3.PNG)

### Building the Executable

Now we are ready to build our executable. The source code includes a helper script to do the heavy lifting for us. Run the script using:

- Windows: `python .\scripts\build_executable.py`
- Linux/macOS: `python scripts/build_executable.py`

The built executable is created in the `dist` directory. Navigate to it either through the terminal or a file explorer. Run the executable as usual.

![Executable in dist directory](../../assets/img/build-4.PNG)
