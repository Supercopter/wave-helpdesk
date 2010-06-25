from google.appengine.ext import db
MAINWAVE_TYPES = {'main':1, 'index':2, 'button':3}
USERWAVE_TYPES = {'question':1, 'discussion':2}
class MainWave(db.Model):
  wave_id = db.StringProperty(required=True)
  wavelet_id = db.StringProperty(required=True)
  title = db.StringProperty(required=False)
  wave_type = db.IntegerProperty(required=True)
class UserWave(db.Model):
  wave_id = db.StringProperty(required=True)
  wavelet_id = db.StringProperty(required=True)
  title = db.StringProperty(required=True)
  wave_type = db.IntegerProperty(required=True)
  discussionwave = db.ReferenceProperty(required=False)
  reported_by = db.StringProperty(required=False)
