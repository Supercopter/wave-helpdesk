# classes module

# Creates the two classes required to store waves in the datastore

from google.appengine.ext import db

# Dicts: An easy way of remembering numbers.
MAINWAVE_TYPES = {'main':1, 'index':2, 'button':3}
USERWAVE_TYPES = {'question':1, 'discussion':2}

class MainWave(db.Model):
  # Used to fetch the wave if necessary in future
  wave_id = db.StringProperty(required=True)
  wavelet_id = db.StringProperty(required=True)

  # Used if/when the index needs rebuilt
  title = db.StringProperty(required=False)

  # Allows determination of the purpose of the wave.
  wave_type = db.IntegerProperty(required=True)


class UserWave(db.Model):
  # Used to fetch the wave if necessary in future
  wave_id = db.StringProperty(required=True)
  wavelet_id = db.StringProperty(required=True)
  
  # Used if/when the index needs rebuilt
  title = db.StringProperty(required=True)
  
  # Allows determination of the purpose of the wave.
  wave_type = db.IntegerProperty(required=True)

  # Pairs a question wave to an appropriate discussion wave.
  discussionwave = db.ReferenceProperty(required=False)

  # Used should I ever want to do some statistics to find out#
  # top users etc. 
  reported_by = db.StringProperty(required=False)
