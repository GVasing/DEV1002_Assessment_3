# DEV1002_Assessment_3

## About  

The Commercial Aviation Management System RESTful web API server provides comprehensive data management and storage services for commercial aviation operations. Providing endpoints for managing data including passenger records, flight bookings, aircraft fleet information, airport facilities, airline operations, and staff administration, the server allows users to efficiently create, retrieve, update, and manage(delete) data such as passenger info, flight schedules, aircraft specifications, airport terminal information, and staff records. With its SQL base structure ideal for handling complex relationships between passengers, flights, airports, planes, airlines, and staff, this API serves as a reliable solution for aviation industry applications requiring real-time access to comprehensive flight operations data, booking management, and resource tracking capabilities.

### Database Selection

When designing this API, I decided to choose an SQL style DBMS, in particular PostgresSQL.  Other database systems seemed appealing, such as the NoSQL Mongodb.  However, while database scalability will be limited and schema rigidity making future changes more time consuming in comparison, the advantages of SQL for conducting complex queries, data aggregations, and data joins in particular, are more beneficial for this type of application.  Given the server application's detail-oriented nature, with the data analysis a big intention, SQL is ideal for gaining insight from a structured dataset, which this will be.  Furthermore, NoSQL's lack of immediate data consistency and, although admittedly possibly temporary, the potential size of the dataset does not warrant a NoSQL database, meaning SQL would allow for faster performace of operations, and overall, a better suit for this API server.

## Feedback

### Feedback Received

__Feedback Lot 1:__  

The first lot of feedback received mentioned separating the initial travel table into two tables.  One for general flight related details that apply to all passengers, and another that is more passenger specific. i.e. Cabin Class, Meal Ordered, etc.

### Response & Implementation

While on the surface the existence of the 'Travel' table did not violate normalisation rules, the feedback was welcomed, as to have both 'booking' and 'flight' related attributes in the same table felt illogical, and seprating them seemed cleaner.  To address this, the feedback was implemented by creating two seperate tables labeled 'Flight' and 'Booking', with further attributes given to the 'Flight' table, allowing for a more comprehensive collection of data.  Some of the new attributes included: airline, flight code, departure point, etc.

### Feedback Received

__Feedback Lot 2:__  

With the revised Relational Data Model to go off, the second lot of feedback received mentioned the potential for the 'Airline' and 'Flight Code' could be dependent on one another, violating 3NF rules, due to their transitive dependency.

### Response & Implementation

Although each flight number is techincally unique, which would not violate 3NF, they do still contain an identifier in them at the start of the sequence in the form of letters, for example 'AA292' would be an American Airlines flight, due to the 'AA', and 'QF123' would be a Qantas flight, due to the 'QF'.  To avoid any possibility of causing any normalisation issues, the feedback was taken on board, and the issues addressed by creating another table labeled 'Airline'.  Much like the inclusion of further attributes for the 'Flight' table, the same was done here, with some of the new attributes including: fleet size, number of destinations, etc.

### Changes Made

__Prior to feedback:__  

[Initial Normalised Relational Data Model](Diagrams/Initial%20Relational%20Data%20Model.jpg)  

__After feedback:__  

[Final Normalised Relational Data Model](Diagrams/Normalised%20Relational%20Data%20Model.jpg)

## Features

## Acknowledgements

- https://www.flightconnections.com  
- https://www.planespotters.net