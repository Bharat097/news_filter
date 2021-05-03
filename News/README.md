# News Filter

## Install Dependencies

pip install -r requirements.txt


## Setup Database

python manage.py db init  
python manage.py db migrate  
python manage.py db upgrade  


## Run Server

python manage.py runserver


## To send E-mail with image of COVID API Response

Configure Sender's Email and Password in .env file

### Note
 * In current implementation, there are some fixis required.
    * Right now, any user can access all the things available
    * Single user can do vote multiple times and right now no details is stored about who has submitted which vote. (this needs improvement)
    * For fetching new news and sending notifications, right now I have started threads in backgroung on ready hook of app config (may be there could some better ways of this..) and at perticular interval it will fetch news (dont cares about duplicate news as there is no such things provided by api to get only new news.) and also sends notification mail to subscrined uses with link to submit theie vote.
    * For storing news, we may use in memory db/messaging queue/kafka pub-sub. these are my thoughts by whcih we may do it quite efficiently. but need to check and investigate.

    * At end, I tried to make it as per my understanding and knowledge, but there can be different implementation approach.