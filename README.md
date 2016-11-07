# ACTLabs WebTESS

WebTESS is the webified version of TESS or Text Evaluation Software System, originally developed by Rick Meisner.

**WebTESS** provides you with an interface wherein you insert a passage to evaluate, and get back numerous statistics regarding the passage. Graphical Visualization of some statistics is also available. 

WebTESS currently has two hosted websites:  
1. http://webtess.actlabs.org  
2. http://webtess-dev.actlabs.org

The first one, is the live version, which should only contain stable code, and be completely tested.  
The second is the dev version, which may contain additional features not yet implemented in the live version, and may also be in an untested state.  

Both websites offer basic authorization. You will not be able to access them unless you enter the correct credentials.  

  
  
# Features

## 1. Visualization
The application provides the option to view graphs based on the data generated. The application includes various kinds of graphs such as line graphs, bar graphs, pie graphs, donut graphs etc. These graphs were implemented using **angular-chart.js** charting library, which provides easy to use methods of drawing charts using AngularJS. The angular-chart.js is itself based on Chart.js  

## 2. Google Analytics
The web application has been setup with Google Analytics. This provides a lot of data regarding the users of the application. The data includes, but is not limited to : Location of the user, Operating System of the user, Internet Provider of the user, Device that is used, Active users etc.  

## 3. Database Support
The application has been integrated with Amazon DynamoDB (Part of AWS). It has been used to store all the passages that the user inputs. Its programmed to not allow any duplicate entries. It doesn't store any of the computed data, as it can be recomputed at any time.  

  

  
  
# Run on Local Machine

To run the website on your local machine:

### 1. Pre-requisites
Make sure that python is installed in your Operating System.  
Next you install pip. 

**On Mac/Linux:**
Run the following command in terminal :
`sudo easy_install pip`

**On Windows:**
Download [get-pip.py](https://bootstrap.pypa.io/get-pip.py) to a folder on your computer. Open a command prompt window and navigate to the folder containing get-pip.py. Then run python get-pip.py. This will install pip.


### (Optional) 2. Set up Virtual Environment - Recommended
a. First download the virtual environment python module by running the command `pip install virtualenv`  
b. Next, create the virtual environment which will hold all the project files by running `virtualenv <name>`
     This creates a folder called `<name>`.  
c. Go into the newly created folder `cd <name>`  
d. Now in order to activate the virtual environment, run the command `source bin/activate`

You may deactivate this by entering `deactivate` in the command line.


### 3. Clone the Repository
There are two ways to do this:  

The first one is to download the zip, directly from the Downloads page. Next extract the contents of the zip file, inside the virtualenv `<name>`.

The second method requires git to be installed and configured on your machine. Once you're in the virtual environment folder, run the following command in the terminal 

```
git clone https://{username}@bitbucket.org/actlabs/actlabs-webtess.git
```

You'll now have a copy of the repository in the directory `<name>`


### 4. Install Dependencies
a. Ensure that your virtual environment is activated and cd into the folder `webtess`.  
b. You can directly install all dependencies to your virtual environment by running the command `pip install -r requirements.txt` in the terminal window.  


### 5. Run
Next you run the application by entering `python application.py` in the terminal window.  
Windows users will have to run `path/to/python/python.exe application.py` in the command prompt.  If you want to simply type python.exe you must add python.exe to your PATH environmental variable.

You will see a message in the terminal, saying 'Running on http://127.0.0.1:5000/ (Press Ctrl+C to quit)'

You can then visit the above address on your local browser to visit the website. 


