# Statistics 101

This web page was developed as the Capstone project for [CS50's Web Programming with Python and JavaScript](https://cs50.harvard.edu/web/2020/) course by Harvard OpenCourseWare.

The website is an education resource that explores the basics of statistics. Statistics is a branch of mathematics that pertains to the collection, analysis, interpretation or explanation, and presentation of data. Hosted version is available [here](https://viksil.pythonanywhere.com/statistics101) (it may take a while to load, since it is hosted on pythonanywhere free tier).

Deployed version of the website can be viewed [here](https://viksil.pythonanywhere.com/statistics101).
Video demo can be viewed [here](https://youtu.be/sdl8YkIIXxA).

## Distinctiveness and Complexity

This project employs Django framework in the back end, and HTML, CSS and JavaScript in the front end - the technologies that were covered in the course. As the capstone project it builds upon the material covered in lectures and previous projects adding further complexity and employing new libraries. The following aspects distinguish this capstone project from previous projects: 
* Unlike any of the previous projects, this website is designed to be used as education resource dedicated to the basic concepts of statistics. Each page describes common terminology, provides theoretical basis for concepts, numerical measures (also collectively referred to as "statistics") or graphical representations of statistical data. Most of the theoretical information is sourced from "Statistics for Dummies" book by Dr Deborah Rumsey (2nd Edition, chapters 1 to 7, 16 and 17). The website includes several public data sets to demonstrate statistical calculations and charts. It also allows registered users to upload their own proprietary data sets and apply the same calculations and charting functionality. 

* The website utilises a number of libraries that were not previously introduced by the course material. These include:
    * __Python [pandas](https://pandas.pydata.org/) an [numpy](https://numpy.org/)__ - two of the most popular libraries used for data manipulation. Pandas is widely used for operations on numerical tables and time series. Numpy supports large multi-dimensional arrays and includes high-level mathematical functions to operate on array data.
    * __Python [plotly](https://plotly.com/)__ - an open source charting library for data visualisation. Plotly supports a variety of different graphs and charts that can be embedded into websites and feature interactive elements.
    * __Javascript [MathJax](https://www.mathjax.org/)__ - a display engine that allows rendering of mathematical formulas written in basic TeX notation into user-friendly human-readable format.
    * __Javascript [Dropzone.js](https://www.dropzone.dev/)__ - an open source library that allows for visual drag-and-drop file upload via an HTML interface.

* Asynchronous data processing in the capstone project is done at larger volumes and higher complexity. All interactions the user has with the data is organised asynchronously. The three main asynchronous functionalities that are supported by the website include:
    * __Data retrieval__ - all inbuilt data sets, as well as users' own data sets are stored in SQLite database. The templates in Data Sets section of the website allows users to pull up each dataset by pressing a button that calls an asynchronous function to retrieve, assemble and display the data in a human-freindly format.
    * __Statistics calculations__ - the templates in Statistics section of the website expand upon the dataset retrieval functionality by calculating common statistical measures for each dataset before displaying it to the user.
    * __Graphical visualisation__ - the templates in Charts section of the website utilises Python's plotly library to represent the data as graphs and charts. All charts are invoked by a push of the button in the front end, that sends a request to the back end to construct the charts, convert them to HTML format and return the results asynchronously. This is one of the most calculation intensive part of the website that can take a few minutes to complete, depending on the processor speed, data set size and bandwidth. A placeholder with processing message is displayed to the user while chart is being prepared. Once complete the chart HTML is added to the DOM of the web page from which it was invoked.
    * __File upload__ - users can submit formatted data sets of their own to the website by uploading a .csv file. The file is uploaded via Dropzone.js at which point asynchronous processing of the data takes place. The file is checked for consistency, the data is cleaned, transformed into objects and stored into the website's database.  Once processed, the users' data sets become accessible in the front-end.

* The website structure is based on a global variable that defines the layout of the navigation pane in the front-end and the corresponding url endpoints that are dynamically generated in the back-end. This global variable is initialised when the server is started. All internal links within the website templates reference the navigation pane variable and checks if the particular section/url is present within the variable. Depending on the result of the check the link is either enabled or disabled. This allows pages can be easily taken out of the overall structure for amendments when necessary. Simply commenting out the corresponding line in the global navigation variable will  hide a page from the website navigation pane, exclude it from urls and disable all links to the template across all website.

* Additionally the website utilises Django native logging functionality that was not covered in the course material. Media directory has also been added to provide a directory structure for handling file upload and processing. 



## Project file structure
This section lists all of the relevant files that are included in the capstone project repository and briefly describes the functionality contained in these files. Once the repository is cloned to a local machine, the file structure should contain:

* quant (directory) - contains files that are necessary for Django framework to run a project, most notable of these - settings.py - will contain project wide settings
* statistics101 (directory) - contains all files and directories pertaining to the specific application within a project. These are:
    * directories:
        * logs - will contain log files with debug and warning information. When the server is started two files will spawn in this directory - debugLOG and warningLOG. By default, population of these files is disabled in order to save disk space. Logging can be enabled by uncommenting LOGGERS variable in quant/settings.py before starting the server. 
        * media - will contain a directory structure that is used to store files during the data upload process. Each sub-directory will contain a .gitignore file - this is is necessary to allow an empty directory structure to be uploaded to GitHub.
        * migrations - will contain all files used to build out database structures. These are strictly necessary because the database with inbuilt data sets is distributed as part of the repo. However, if the inbuilt data sets are not desirable for any reason, the database can be removed and rebuilt from scratch by running the following commands consecutivelly: `python manage.py makemigrations statistics101`  and `python manage.py migrate`.
        * static - will contain css, Javascript scripts and images used on the website.
        * templates - will contain all the templates that can be accessed in the front-end of the website.
    * files:
        * \_\_init__.py  - a namespace package is part of Django ecosystem, and its presence of which is necessary for the structural integrity of the project. This file has not been changed and remains empty.  
        * admin.py  - defines the classes and layout for the admin interface.
        * forms.py - defines the forms that are used for user registration and authorisation.
        * globals.py - defines data structures that are used by a majority of templates across the website, such as NAVIGATION_PANE and ALL_SOURCES, as well as utility functions that handle formatting of these data structures.
        * models.py - contains the models that define how the database storage is organised.
        * urls.py - contains definition of all endpoints for the website and specifies view functions that are invoked from specific endpoints.
        * utils_async.py - contains all utilities functions for asynchronous operations on database objects. These functions retrieve data from the database and perform calculations to return either data sets, statistics or charts as responses to requests from the front-end.
        * utils_upload.py - contains all utilities functions that handle data upload to the website's database.
        * utils.py - contains all other non-view functions that are neither asynchronous nor related to file processing.
        * views.py - contains all view functions that are invoked from an endpoint listed in the urls.py file, process requests and serve templates to the front-end user.

* db.sqlite3 - is a persistent database file with inbuilt data.
* manage.py - is a Django framework file that allows interacting with the project.
* README.md - this file.
* requirements.txt - is a file that lists all dependencies that need to be installed for the project to run properly.



## How to run the application

### Requirements and Dependencies

There are no strict hardware requirements for running Django projects, however, given the nature of the project, you will need a screen and processor, graphics card and enough RAM and disk space to handle running the browser of your choice. The size of the project is less than 35MB, but additional requirements to space will imposed by the browser and the operating system.

Software prerequisites for this project are:
* Git - to clone this repo to local directory
* Python with pip - the latest stable version preferred, the project was developed using python 3.11, and has been tested to work on 3.9 and 3.10 as well
* Node.js with npm - the latest stable version preferred, the project was developed using node 18.17.
* a browser of your choice.

_Installation of all the above will differ depending on the operating system. Please check official documentation for available options._

* all packages listed in requirements.txt file

### Setting up the project

Follow these steps to set up the project on a local machine:

1. Create a directory where the project will be contained
2. Git clone this repository into your local directory. The command will differ slightly depending on where the project is found on Github. General console command for cloning a Git repository is: `git clone --branch <branch_name> <URL_to_repo>`. If in doubt, please consult the [documentation](https://git-scm.com/docs/git-clone).
3. In console navigate to the root directory of the project (where __manage.py__ file is located)
4. Run this command to install all pythonic dependencies (this will take several minutes to complete): `pip install -r requirements.txt`
5. Run this command to install bootstrap (this will create several new files and folders in the project directory): `npm install bootstrap`
6. You should be ready to start the server


### Starting the server and viewing the website

In order to start the project, use console to navigate to the directory where the repo was cloned into. This should be the directory where __manage.py__ file is. To start the server execute this command: `python manage.py runserver`.  If successful, you should see a line `Starting development server at http://127.0.0.1:8000/` amongst the output.

The website will now be available on the localhost. Input the following url in the browser to access it: `http://127.0.0.1:8000/statistics101`

