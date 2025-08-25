# DEV1002 Assessment 3: Commercial Aviation Management System API

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

Despite the fact that each flight number is techincally unique, which would not violate 3NF, they do still contain an identifier in them at the start of the sequence in the form of letters, for example 'AA292' would be an American Airlines flight, due to the 'AA', and 'QF123' would be a Qantas flight, due to the 'QF'.  To avoid any possibility of causing any normalisation issues, the feedback was taken on board, and the issues addressed by creating another table labeled 'Airline'.  Much like the inclusion of further attributes for the 'Flight' table, the same was done here, with some of the new attributes including: fleet size, number of destinations, etc.

### Feedback Received

__Feedback Lot 3:__  

The third lot of feedback received came during the testing stage of the project.  When testing to see the how the system catches errors, the user felt that some error messages were fairly vague, while others were quite specific.  They suggested that the experience would feel better overall if the majority of the messages were personalised, or at least consistent with one style or the other.

### Response & Implementation

In response to the feedback, although the error handling was working as intended,  the advice was taken on board.  Yes it was preventing the API from crashing, but vague responses made it difficult for users to know what criteria to follow.  Given that, the error messages provided were revised and made more specific to the situation the error was made in.  Once these changes were made, the existence of a global error handling module seemed unnecessary, defeating the purpose of it's intention.  While potentially helpful for catching errors that could slip through, since the handling within the module reflected near identically to those within the controllers, 'error_handlers.py' was essentially dead code.  Given this, the decision to remove it entirely was made.  

### Changes Made



__Prior to Feedback Lot 1 & 2:__  

[Initial Normalised Relational Data Model](Diagrams_&_Images/Initial%20Relational%20Data%20Model.jpg)

__After Feedback Lot 1 & 2:__  

[Final Normalised Relational Data Model](Diagrams_&_Images/Normalised%20Relational%20Data%20Model.jpg)

__Prior to Feedback Lot 3:__  

[Global Error Handling Inclusion](https://github.com/GVasing/DEV1002_Assessment_3/commit/020bfd4a8d55de9db8fc5597b7e6c57f97fdd6e1#diff-d0e01cbea78a1a341b483bef4a75cb230879a9034afb80bd810f5828c0cb1b2d).  Here we can see in the commit the inclusion of a 'error_handlers.py' file.

__After Feedback Lot 3:__  

[Global Error Handling Removal](https://github.com/GVasing/DEV1002_Assessment_3/commit/2efbc0ef89b088f3f523aeef9eb4276086bd3358#diff-d0e01cbea78a1a341b483bef4a75cb230879a9034afb80bd810f5828c0cb1b2d).  Here we can see in the commit the removal of the 'error_handlers.py' file.

Screenshots of revised error messages to be more personalised can be found [here](Diagrams_&_Images/Screenshots).

## Features



## Endpoints

<h1>API Endpoints Reference</h1>

<table>
  <thead>
    <tr>
      <th>Endpoint</th>
      <th>Methods</th>
      <th>Rule</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>airline.create_airline</td>
      <td>POST</td>
      <td>/airlines/</td>
    </tr>
    <tr>
      <td>airline.delete_airline</td>
      <td>DELETE</td>
      <td>/airlines/&lt;int:airline_id&gt;</td>
    </tr>
    <tr>
      <td>airline.get_airlines</td>
      <td>GET</td>
      <td>/airlines/</td>
    </tr>
    <tr>
      <td>airline.get_an_airline</td>
      <td>GET</td>
      <td>/airlines/&lt;int:airline_id&gt;</td>
    </tr>
    <tr>
      <td>airline.update_airline</td>
      <td>PATCH, PUT</td>
      <td>/airlines/&lt;int:airline_id&gt;</td>
    </tr>
    <tr>
      <td>airport.create_airport</td>
      <td>POST</td>
      <td>/airports/</td>
    </tr>
    <tr>
      <td>airport.delete_airport</td>
      <td>DELETE</td>
      <td>/airports/&lt;int:airport_id&gt;</td>
    </tr>
    <tr>
      <td>airport.get_airports</td>
      <td>GET</td>
      <td>/airports/</td>
    </tr>
    <tr>
      <td>airport.get_an_airport</td>
      <td>GET</td>
      <td>/airports/&lt;int:airport_id&gt;</td>
    </tr>
    <tr>
      <td>airport.update_airport</td>
      <td>PATCH, PUT</td>
      <td>/airports/&lt;int:airport_id&gt;</td>
    </tr>
    <tr>
      <td>booking.create_booking</td>
      <td>POST</td>
      <td>/bookings/</td>
    </tr>
    <tr>
      <td>booking.delete_booking</td>
      <td>DELETE</td>
      <td>/bookings/&lt;int:booking_id&gt;</td>
    </tr>
    <tr>
      <td>booking.get_a_booking</td>
      <td>GET</td>
      <td>/bookings/&lt;int:booking_id&gt;</td>
    </tr>
    <tr>
      <td>booking.get_bookings</td>
      <td>GET</td>
      <td>/bookings/</td>
    </tr>
    <tr>
      <td>booking.update_booking</td>
      <td>PATCH, PUT</td>
      <td>/bookings/&lt;int:booking_id&gt;</td>
    </tr>
    <tr>
      <td>flight.create_flight</td>
      <td>POST</td>
      <td>/flights/</td>
    </tr>
    <tr>
      <td>flight.delete_flight</td>
      <td>DELETE</td>
      <td>/flights/&lt;int:flight_id&gt;</td>
    </tr>
    <tr>
      <td>flight.get_a_flight</td>
      <td>GET</td>
      <td>/flights/&lt;int:flight_id&gt;</td>
    </tr>
    <tr>
      <td>flight.get_flights</td>
      <td>GET</td>
      <td>/flights/</td>
    </tr>
    <tr>
      <td>flight.update_flight</td>
      <td>PATCH, PUT</td>
      <td>/flights/&lt;int:flight_id&gt;</td>
    </tr>
    <tr>
      <td>location.create_location</td>
      <td>POST</td>
      <td>/locations/</td>
    </tr>
    <tr>
      <td>location.delete_location</td>
      <td>DELETE</td>
      <td>/locations/&lt;int:location_id&gt;</td>
    </tr>
    <tr>
      <td>location.get_a_location</td>
      <td>GET</td>
      <td>/locations/&lt;int:location_id&gt;</td>
    </tr>
    <tr>
      <td>location.get_locations</td>
      <td>GET</td>
      <td>/locations/</td>
    </tr>
    <tr>
      <td>location.update_location</td>
      <td>PATCH, PUT</td>
      <td>/locations/&lt;int:location_id&gt;</td>
    </tr>
    <tr>
      <td>passenger.create_passenger</td>
      <td>POST</td>
      <td>/passengers/</td>
    </tr>
    <tr>
      <td>passenger.delete_passenger</td>
      <td>DELETE</td>
      <td>/passengers/&lt;int:passenger_id&gt;</td>
    </tr>
    <tr>
      <td>passenger.get_a_passenger</td>
      <td>GET</td>
      <td>/passengers/&lt;int:passenger_id&gt;</td>
    </tr>
    <tr>
      <td>passenger.get_passengers</td>
      <td>GET</td>
      <td>/passengers/</td>
    </tr>
    <tr>
      <td>passenger.update_passenger</td>
      <td>PATCH, PUT</td>
      <td>/passengers/&lt;int:passenger_id&gt;</td>
    </tr>
    <tr>
      <td>plane.create_plane</td>
      <td>POST</td>
      <td>/planes/</td>
    </tr>
    <tr>
      <td>plane.delete_plane</td>
      <td>DELETE</td>
      <td>/planes/&lt;int:plane_id&gt;</td>
    </tr>
    <tr>
      <td>plane.get_a_plane</td>
      <td>GET</td>
      <td>/planes/&lt;int:plane_id&gt;</td>
    </tr>
    <tr>
      <td>plane.get_planes</td>
      <td>GET</td>
      <td>/planes/</td>
    </tr>
    <tr>
      <td>plane.update_plane</td>
      <td>PATCH, PUT</td>
      <td>/planes/&lt;int:plane_id&gt;</td>
    </tr>
    <tr>
      <td>staff.create_staff</td>
      <td>POST</td>
      <td>/staffs/</td>
    </tr>
    <tr>
      <td>staff.delete_staff</td>
      <td>DELETE</td>
      <td>/staffs/&lt;int:staff_id&gt;</td>
    </tr>
    <tr>
      <td>staff.get_a_staff_member</td>
      <td>GET</td>
      <td>/staffs/&lt;int:staff_id&gt;</td>
    </tr>
    <tr>
      <td>staff.get_staff</td>
      <td>GET</td>
      <td>/staffs/</td>
    </tr>
    <tr>
      <td>staff.update_staff</td>
      <td>PATCH, PUT</td>
      <td>/staffs/&lt;int:staff_id&gt;</td>
    </tr>
  </tbody>
</table>

## Acknowledgements

- https://www.flightconnections.com  
- https://www.planespotters.net