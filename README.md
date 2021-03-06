#Ticket Booker

This Django app presents a simple UI for booking seat where each user can book only one ticket.

The system handles concurrent booking of the same seat by accepting the first user's request who booked the seat.

Preview of app can be seen at https://aakash-ticket-booking.herokuapp.com

## Installation Steps
```buildoutcfg
1. python3 -m venv env
2. source env/bin/activate
3. pip install -r requirements.txt
4. python manage.py migrate
5. python manage.py collectstatic --no-input
```

## Running the app locally
Run the following command to start the app server locally

`python manage.py runserver`

### Running test cases locally

Unit test cases can be executed locally using the following command

`python manage.py test`