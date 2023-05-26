# REAL TIME VISUALIZATION OF COVID STATISTICS OF WORLD AND NEPAL
## Introduction
 The purpose to this project is to real time visualize the covid statistics of world and Nepal. The data has been taken from the Worldometer site. Here the data are updated on frequents runs and get visualized in terms of pie-chart and in the form of heatmap in the world map. Also, the user can get the tabular data statistics of all countries of the world.


## Scope and Application
The scope and application of the project would involve developing a web-based application that provides real-time visualization of COVID-19 statistics for the world and Nepal. The project can cater to various stakeholders, including:
  1.  General Public: The application can serve as a reliable source of information for the general public. It allows them to access up-to-date COVID-19 statistics, understand the current situation, and make informed decisions regarding their health and safety measures.

   2. Health Professional and Researcher: The project can assist healthcare professionals and researchers in monitoring the spread of COVID-19, analyzing trends, and making data-driven decisions.


## How to use this project locally?
You can clone this branch and use it right now using the steps given below.  

### Building Locally
It is best to use python **virtualenv** tool to build locally and use Python 3.10.6 and pip 23.1.2:  
> virtualenv venv  
> source venv/bin/activate  
> git clone https://github.com/RochakSedai/Covid_Visualization.git

Then you navigate to the base directory of the project and install the requirements in your vitual environment  
> pip install -r requirements.txt  

And finally you make migration to the database, create a super user, and run the server  
> python manage.py makemigrations  
>python manage.py migrate  
> python manage.py createsuperuser  
> python manage.py runserver  

<b>P.S:<i>  It might get time when showing the visualization in the Map.</i></b><br>  
## Developed by:
- Rochak Sedai
