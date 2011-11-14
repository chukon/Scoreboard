Scoreboard is a simple google app engine application to showcase a simple way to interface with an iOS application.

** Adding Data From the Command Line **
curl -d udid=1234 -d score=5 http://localhost:8080/postscores/

** Requesting Data in JSON Format **
curl http://localhost:8080/getscores
