import logging
import os
import cgi
import datetime
import wsgiref.handlers
import time

from google.appengine.ext import db
from google.appengine.api import users
from google.appengine.ext import webapp
from django.utils import simplejson  

#################################################
#
# Data Model
#
#################################################
class Players(db.Model):
    udid = db.StringProperty()
    username = db.StringProperty()
    date = db.DateTimeProperty(auto_now_add=True)
    lastUpdate = db.DateTimeProperty(auto_now=True)
    score = db.IntegerProperty(default=0)
    
    # Custom model method to return all model properties
    def to_dict(self):
        return dict([(p, unicode(getattr(self, p))) for p in self.properties()])

#################################################
#
# Get the scores
#
#################################################
class GetScores(webapp.RequestHandler):
    def get(self):
        
        # Dump the entire database back as JSON
        players = Players.all()
        self.response.out.write(simplejson.dumps([p.to_dict() for p in players]))
        
        # Do some logic on the server side and return manually
        '''players = db.GqlQuery("SELECT * Players")        
        self.response.out.write('<html><body>')    
        self.response.out.write('Current Time: %s' % time.strftime("%a, %d %b %Y %X UTC<br>", time.gmtime()))
        for player in players:
            self.response.out.write('Username: %s Unique Devices: %s<br>' % player.username,player.udid)
        '''

#################################################
#
# Post the scores
#
#################################################
class PostScores(webapp.RequestHandler):
    def post(self):

        # Log the the request information
        logging.debug(self.request)
        
        # Test if new player or returning player
        welcomeBack = 0
        uniqueId = self.request.get('udid')
        
        # Update a player
        query = db.GqlQuery("SELECT * FROM Players WHERE udid = :1",uniqueId)
        for result in query:
            result.lastUpdate = datetime.datetime.now()
            result.score = int(self.request.get('score'))
            result.put()
            welcomeBack == 1
        
        # Create a new player 
        if welcomeBack == 0:
            player = Players()
            player.lastUpdate = datetime.datetime.now()
            player.udid = self.request.get('udid')
            player.score = int(self.request.get('score'))
            player.username = self.request.get('username')
            player.put()