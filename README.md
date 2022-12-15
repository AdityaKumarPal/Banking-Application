# Banking-Application

*This project helps to understand how the frontend as well as backend of a banking website can be done. The frontend is made by using HTML and CSS and the backend is made by flask. The main challenge which I faced is to understand how it actually going to work. I also want to add some additional features later.*

**Creating database for the project: **
*Rather than this project, you must have MySQL database installed in your computer. Create a database inside it as "abi_project" and make 2 different tables(one for user details and another for all the transactions going to happen) inside it whose commands are shown below.*
- create table users(Name varchar(50) not null unique, Gender varchar(6) not null, DOB date not null, Email varchar(50) not null, Mobile varchar(13) not null primary key, Password varchar(50) not null, Confirm_Password varchar(50) not null);
- create table transactions(Transaction varchar(20), Transferred varchar(15), Cash int, mobile varchar(10), Date_Time timestamp default CURRENT_TIMESTAMP, foreign key(mobile) references users(Mobile));

**Install the following dependencies: **
Create a virtual environment for your project and fullfill the requirements of it as mentioned in the "requirement.txt" file of this repository.

**To run the file scraping.py, do: **
- python3 scraping.py
- Open it in any of your browser
- And you're done ✌️
