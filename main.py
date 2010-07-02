# main.py

# Imports the modules required for robot operation
from waveapi import robot
from waveapi import events
from waveapi import appengine_robot_runner
# Imports the element module which allows the robot
# to work with elements
from waveapi import element
# Imports the logging module to send debug logs to
# the appengine logger.
import logging
# Imports the appengine datastore module, allowing
# searching of the datastore.
from google.appengine.ext import db
# Imports the local classes module, which model
# the creation of Main Waves & User Waves in
# the datastore
import classes

# "Placeholders" to stop errors
ROOT_WAVE = True
INDEX_WAVE = True
BUTTON_WAVE = True
myRobot = True 

# Gets the "Main Waves" from the datastore
query = db.GqlQuery('SELECT * FROM MainWave')
for i in query:
  if i.wave_type == 1:
    ROOT_WAVE = i
  elif i.wave_type == 2:
    INDEX_WAVE = i
  elif i.wave_type == 3:
    BUTTON_WAVE = i

# Hard Codes the "helpful panel"
PARTICIPANTS = ['wave-helpdesk@googlegroups.com',
                'nat.abbotts@wavewatchers.org',
                'alexandrojv@wavewatchers.org',
                'rivera@wavewatchers.org',
                'mpoole32@googlewave.com',
                'albonono@wavewatchers.org',
                'josh@nunnone.com',
                'pooja@wavewatchers.org',
                'rooneyrox3@googlewave.com',
                'markb@wavewatchers.org',
                'sirdarkstar@googlewave.com',
                'yoann.moinet@wavewatchers.org',
                'tjb654@googlewave.com',
                'rupesh@wavewatchers.org',
                'public@a.gwave.com',]
BUGS = {'no-attachments':{'status':True,
                          'message':'Note: You are not currently able' +
                          ' to include screenshots/gadgets etc. in' +
                          ' the helpdesk, as the helpdesk will delete' +
                          ' them. We are working to allow you to use' +
                          ' attachments.')}

def create_question_wave(q_wave):
  '''Appends the required elements & text to
  make the question wave.'''
  # Sets the title
  q_wave.title = 'New Helpdesk Question'
  # Adds a "Heading 3" element
  q_wave.root_blip.append(element.Line(line_type = 'h3'))
  # Adds some instructions
  q_wave.root_blip.append('Type a summary of ' +
                          'your question in ' +
                          'the box below.\n')
  # Adds an Input element, for people to type
  # their question summary into.
  q_wave.root_blip.append(element.Input('wave-helpdesk:InsertQuestion', ''))
  # Adds another Heading element
  q_wave.root_blip.append(element.Line(line_type = 'h3'))
  # Adds some more instructions
  q_wave.root_blip.append('If you have more detail to add, add it here:\n')
  # Adds a TextArea element, for question detail. TextArea
  # elements expand when more text than fits the box is
  #entered. This behavior does not appear in the Input element.
  q_wave.root_blip.append(element.TextArea('helpdesk/detail', ''))
  # Adds another heading element.
  q_wave.root_blip.append(element.Line(line_type = 'h3'))
  # Adds some more instructions
  q_wave.root_blip.append('Once you are done, click this button:\n')
  # Adds the submit button.
  q_wave.root_blip.append(element.Button('helpdesk-submitquestion',
                                         'Submit Question'))
  # Adds a warning message, if a particular bug hasn't yet been fixed.
  if BUGS['no-attachments']['status'] == True:
    q_wave.root_blip.append('\n\n' + BUGS['no-attachments']['message'])
  return q_wave
      
def OnFormButtonClicked(event, wavelet):
  '''Handles FormButtonClicked events. '''
  # Logs the button name in the appengine logs.
  logging.debug('OnFormButtonClicked Called, Button Name %s' % event.button_name)
  # Assigns the wavelet's operation queue to opQ for easier access.
  opQ = wavelet.get_operation_queue()
  # If the button is the 'new question' button:
  if event.button_name == 'helpdesk-newquestion':
    # Logs that the button is the new question button.
    logging.debug('New Question Wave')
    # Creates a new wave.
    q_wave = myRobot.new_wave(wavelet.domain,
                              participants = [event.modified_by],
                              submit = True)
    # Calls "create_question_wave" on the new wave (see the function above)
    create_question_wave(q_wave)
    # Submits the question wave using the active api.
    myRobot.submit(q_wave)
  # If the button is the helpdesktesting button:
  elif event.button_name == 'helpdesktesting-newquestion':
    # Does the same as above, but the 3 steps are combined into one.
    myRobot.submit(create_question_wave(myRobot.new_wave(wavelet.domain,
                                                         participants = [
                                                           event.modified_by],
                                                         submit=True)))
  # if the button is the 'add me' button on the helpdeskdev wave:
  elif event.button_name == 'helpdesk-dev-add_me':
    # Gets the wave_id
    wave_id_box = event.blip.first(element.Input, name = 'Wave Add')
    # if that was sucsessful:
    if wave_id_box:
      # extracts the wave id from the box.
      wave_id = wave_id_box.value().serialize()['properties']['value']
      # If that was unsucsessful:
      if not wave_id:
        # end running code
        return
    else:
      # end running code
      return
    # tries to find the wavelet_id input box.
    wavelet_id_box = event.blip.first(element.Input, name = 'Wavelet ID')
    # If it found the box:
    if wavelet_id_box:
      # Extract the wavelet id from the box.
      wavelet_id = wavelet_id_box.value().serialize()['properties']['value']
    # if it couldn't find the box: extracts the wavelet id from the wave id.
    else:
      #extract the wavelet id from the wave id
      wavelet_id = wave_id.split('!')[0] + '!conv+root'
    # The following 8 lines attempt to add the person who asked to the wave
    # and make them full access.
    try:
      wavelet.get_operation_queue().wavelet_add_participant(wave_id, wavelet_id, event.modified_by)
    except:
      wavelet.root_blip.append('\nOperation Failed')
    try:
      wavelet.get_operation_queue().wavelet_modify_participant_role(wave_id, wavelet_id, event.modified_by, 'FULL')
    except:
      wavelet.root_blip.append('\nOperation Failed')
  # TODO: Comment from here downwards.
  elif event.button_name == 'helpdesk-dev-add_them':
    wave_id_box = event.blip.first(element.Input, name = 'Wave Add')
    if wave_id_box:
      wave_id = wave_id_box.value().serialize()['properties']['value']
      if not wave_id:
        return
    else:
      return
    wavelet_id_box = event.blip.first(element.Input, name = 'Wavelet ID')
    if wavelet_id_box:
      wavelet_id = wavelet_id_box.value().serialize()['properties']['value']
    else:
      wavelet_id = wave_id.split('!')[0] + '!conv+root'
    who = event.blip.first(element.Input, name = 'User ID')
    if who:
      who = who.value().serialize()['properties']['value']
    else:
      who = event.modified_by
    try:
      wavelet.get_operation_queue().wavelet_add_participant(wave_id, wavelet_id, who)
    except:
      wavelet.root_blip.append('\nOperation Failed')
    try:
      wavelet.get_operation_queue().wavelet_modify_participant_role(wave_id, wavelet_id, who, 'FULL')
    except:
      wavelet.root_blip.append('\nOperation Failed')
  elif event.button_name == 'helpdesk-submitquestion':
    logging.debug('New Question Submitted')
    questionline = event.blip.first(element.Input)
    if questionline:
      question = questionline.value().serialize()['properties']['value']
      
    else:
      question = wavelet.title
    detailbox = event.blip.first(element.TextArea)
    if detailbox:
      detail = detailbox.value().serialize()['properties']['value']
    else:
      detail = ''
    #attachments = {}
    #for e in wavelet.root_blip.elements:
    #  if isinstance(e, element.Attachment):
    #    attachments[e.get('caption')] = e.get('data')
    #logging.debug('No. of attachments: %s' % str(len(attachments)))
    if (question == 'Type a simple version of your question here') or (not question) or (question == 'New Helpdesk Question'):
      wavelet.reply('You need to summarise your question in the question box before submitting.\nIf you are having trouble with the helpdesk, add \'nat.abbotts@wavewatchers.org\' to this wave.')
      return
    wavelet.root_blip.range(0, len(wavelet.root_blip.text) - 1).delete()
    wavelet.title = question
    wavelet.root_blip.append('\n')
    wavelet.root_blip.append(detail)
    #for i in attachments.keys():
    #  wavelet.root_blip.append(element.Attachment(caption = i, data = attachments[i]))
    opQ.wavelet_add_participant(wavelet.wave_id, wavelet.wavelet_id, 'wave-helpdesk@googlegroups.com')
    opQ.wavelet_modify_tag(wavelet.wave_id, wavelet.wavelet_id, 'question')
    d_wave = myRobot.new_wave('googlewave.com',
                              participants = [event.modified_by],
                              submit = True)
    for i in PARTICIPANTS + [event.modified_by]:
      opQ.wavelet_add_participant(d_wave.wave_id, d_wave.wavelet_id, i)
    d_wave.title = "[PUBLIC DISCUSSION] " + question
    opQ.wavelet_modify_tag(d_wave.wave_id, d_wave.wavelet_id, 'discussion')
    d_wave.root_blip.append(wavelet.root_blip.text)
    d_wave.root_blip.append('\n\nOriginal Question Wave', bundled_annotations = [('link/wave', wavelet.wave_id)])
    #for i in attachments.keys():
    #  wavelet.root_blip.append(element.Attachment(caption = i, data = attachments[i]))
    myRobot.submit(d_wave)
    wavelet.reply('''This wave is public read-only (anyone can see it, but only participants can edit). The Helpdesk Team will choose the best answer 
from the discussion wave, once the discussion has finished, and post it here.\n''').append('Go to the full access public Discussion Wave', bundled_annotations = [('link/wave', d_wave.wave_id)])
    index = myRobot.fetch_wavelet(INDEX_WAVE.wave_id, INDEX_WAVE.wavelet_id)
    r = index.reply() ##!
    r.append(element.Line(alignment = element.Line.ALIGN_CENTER))
    r.append(question + '\n')
    r.append(element.Line(alignment = element.Line.ALIGN_CENTER))
    r.append('Question Wave', bundled_annotations = [('link/wave', wavelet.wave_id)])
    r.append(' | ')
    r.append('Discussion Wave', bundled_annotations = [('link/wave', d_wave.wave_id)])
    
    myRobot.submit(index)
    #myRobot.submit(wavelet)
    wavelet.reply('Question Submitted to ').append('The Helpdesk', bundled_annotations=[('link/wave', INDEX_WAVE.wave_id)])
    #myRobot.submit(wavelet)
    #index.submit_with(d_wave)
    rec1 = classes.UserWave(wave_id = d_wave.wave_id,
                            wavelet_id = d_wave.wavelet_id,
                            title = d_wave.title,
                            wave_type = classes.USERWAVE_TYPES['discussion'],
                            reported_by = event.modified_by)
    rec1.put()
    rec2 = classes.UserWave(wave_id = wavelet.wave_id,
                            wavelet_id = wavelet.wavelet_id,
                            title = question,
                            wave_type = classes.USERWAVE_TYPES['question'],
                            discussionwave = rec1,
                            reported_by = event.modified_by)
    rec2.put()

  elif event.button_name == 'helpdesk-setupindex':
    index = myRobot.new_wave('googlewave.com',
                             participants = PARTICIPANTS + [event.modified_by],
                             submit = True)
    for i in PARTICIPANTS:
      opQ.wavelet_add_participant(index.wave_id, index.wavelet_id, i)
    wavelet.participants.set_role('public@a.gwave.com', 'READ_ONLY')
    index.title = '[INDEX] Wave Helpdesk Questions'
    index.root_blip.append('\n\nThis wave is where you will find links to all helpdesk discussions and questions.\n\n')
    #global INDEX_WAVE
    if INDEX_WAVE:
      INDEX_WAVE.delete()
    if ROOT_WAVE:
      index.root_blip.append(element.Line(alignment = element.Line.ALIGN_RIGHT))
      index.root_blip.append('Go To: ', bundled_annotations = [('style/fontSize', '0.9166666666666666em')])
      index.root_blip.append('Main Wave', bundled_annotations = [('style/fontSize', '0.9166666666666666em'), ('link/wave', ROOT_WAVE.wave_id)])
    if BUTTON_WAVE:
      index.root_blip.append(element.Line(alignment = element.Line.ALIGN_RIGHT))
      index.root_blip.append('Post a Question: ', bundled_annotations = [('style/fontSize', '0.9166666666666666em')])
      index.root_blip.append('Helpdesk Question Button', bundled_annotations = [('style/fontSize', '0.9166666666666666em'), ('link/wave', BUTTON_WAVE.wave_id)])
      rec = classes.MainWave(wave_id = index.wave_id,
                           wavelet_id = index.wavelet_id,
                           title = index.title,

                           wave_type = classes.MAINWAVE_TYPES['index'])
    rec.put()
    q_waves = db.GqlQuery('SELECT * FROM UserWave WHERE wave_type = :1', 1)
    for q in q_waves:
      r = index.reply(q.title + '\n')
      r.append(element.Line(alignment = element.Line.ALIGN_CENTER))
      r.append('Question Wave ', bundled_annotations = [('link/wave', q.wave_id)])
      r.append('|')
      r.append(' Discussion Wave', bundled_annotations = [('link/wave', q.discussionwave.wave_id)])
    myRobot.submit(index)
  elif event.button_name == 'helpdesk-setupmain':
    main = myRobot.new_wave('googlewave.com',
                            participants = PARTICIPANTS + [event.modified_by],
                            submit = True)
    for i in PARTICIPANTS + [event.modified_by]:
      opQ.wavelet_add_participant(main.wave_id, main.wavelet_id, i)
    main.title = '[MAIN WAVE] Wave Helpdesk'
    main.root_blip.append('\n\nThe main wave for the helpdesk. It will contain links to our favourite/most useful questions.\n\n')
    main.participants.set_role('public@a.gwave.com', 'READ_ONLY')
    #global ROOT_WAVE
    if ROOT_WAVE:
      ROOT_WAVE.delete()
    if INDEX_WAVE:
      main.root_blip.append(element.Line(alignment = element.Line.ALIGN_RIGHT))
      main.root_blip.append('Go To: ', bundled_annotations = [('style/fontSize', '0.9166666666666666em')])
      main.root_blip.append('Index of Questions', bundled_annotations = [('style/fontSize', '0.9166666666666666em'), ('link/wave', INDEX_WAVE.wave_id)])
    if BUTTON_WAVE:
      main.root_blip.append(element.Line(alignment = element.Line.ALIGN_RIGHT))
      main.root_blip.append('Post a Question: ', bundled_annotations = [('style/fontSize', '0.9166666666666666em')])
      main.root_blip.append('Helpdesk Question Button', bundled_annotations = [('style/fontSize', '0.9166666666666666em'), ('link/wave', BUTTON_WAVE.wave_id)])
    rec = classes.MainWave(wave_id = main.wave_id,
                           wavelet_id = main.wavelet_id,
                           title = main.title,
                           wave_type = classes.MAINWAVE_TYPES['main'])
    rec.put()
    myRobot.submit(main)
  elif event.button_name == 'helpdesk-setupbutton':
    button = myRobot.new_wave('googlewave.com',
                              participants = PARTICIPANTS + [event.modified_by],
                              submit = True)
    for i in PARTICIPANTS + [event.modified_by]:
      opQ.wavelet_add_participant(button.wave_id, button.wavelet_id, i)
    button.title = '[HELPDESK] Use the button on this wave to post a question'
    button.root_blip.append('\n\nClicking the button below will make the helpdesk robot create a new wave for you, where you can ask your question.\n\n')
    button.root_blip.append(element.Line(alignment = element.Line.ALIGN_CENTER))
    button.root_blip.append(element.Button('helpdesk-newquestion', 'Click to ask a question'),
                            bundled_annotations = [('style/color','rgb(51, 127, 229)'),
                                                   ('style/fontWeight', 'bold')])
    button.root_blip.append(element.Line(alignment = element.Line.ALIGN_CENTER))
    button.root_blip.append('Please do not add Robots to this wave - it will get you suspended from being able to use the helpdesk.\n\n')
    #global BUTTON_WAVE
    if BUTTON_WAVE:
      BUTTON_WAVE.delete()
    if ROOT_WAVE:
      button.root_blip.append(element.Line(alignment = element.Line.ALIGN_RIGHT))
      button.root_blip.append('Go To: ', bundled_annotations = [('style/fontSize', '0.9166666666666666em')])
      button.root_blip.append('Main Wave', bundled_annotations = [('style/fontSize', '0.9166666666666666em'), ('link/wave', ROOT_WAVE.wave_id)])
    if INDEX_WAVE:
      button.root_blip.append(element.Line(alignment = element.Line.ALIGN_RIGHT))
      button.root_blip.append('Go To: ', bundled_annotations = [('style/fontSize', '0.9166666666666666em')])
      button.root_blip.append('Index of Questions', bundled_annotations = [('style/fontSize', '0.9166666666666666em'), ('link/wave', INDEX_WAVE.wave_id)])
    rec = classes.MainWave(wave_id = index.wave_id,
                           wavelet_id = index.wavelet_id,
                           title = index.title,
                           wave_type = classes.MAINWAVE_TYPES['button'])
    rec.put()
    myRobot.submit(button)

      
def OnWaveletSelfAdded(event, wavelet):
  logging.debug("OnWaveletSelfAdded")
  if (not wavelet.title) or (wavelet.title == 'Wave Helpdesk'):
    create_question_wave(wavelet)
    return
  elif wavelet.creator != 'nat.abbotts@wavewatchers.org':
    return
  elif 'all@wavewatchers.org' not in wavelet.participants:
    return
  if 'Create Admin Console' in wavelet.title:
    wavelet.title = '[ADMIN CONSOLE] - Wave Helpdesk'
    wavelet.root_blip.append(element.Button('helpdesk-setupindex', 'NEW INDEX WAVE'))
    wavelet.root_blip.append(element.Button('helpdesk-setupmain', 'NEW MAIN WAVE'))
    wavelet.root_blip.append(element.Button('helpdesk-setupbutton', 'NEW BUTTON WAVE'))
  elif 'Add Testing Button' in wavelet.title:
    wavelet.reply().append(element.Button('helpdesktesting-newquestion', 'New Style Question (Test)'))
    return
  elif 'Setup \'Add Me\'' in wavelet.title:
    wavelet.title = 'HelpdeskDev - Add yourself to a wave'
    wavelet.root_blip.append(element.Line('h3', None, 'c'))
    wavelet.root_blip.append('Enter the Wave ID of the wave you want to be added to:\n')
    wavelet.root_blip.append(element.Input(name = 'Wave Add'))
    wavelet.root_blip.append('\n\n')
    wavelet.root_blip.append(element.Line('h3', None, 'c'))
    wavelet.root_blip.append('Enter the Wavelet ID of the wave you want to be added to:\nIf you are\'t sure, leave blank.')
    wavelet.root_blip.append(element.Input(name = 'Wavelet ID'))
    wavelet.root_blip.append('\n\n')
    wavelet.root_blip.append(element.Button('helpdesk-dev-add_me', 'Add Me'))
    wavelet.root_blip.append('\n\nIf you need to add someone else, enter their address here, then click \'Add Them\'\n')
    wavelet.root_blip.append(element.Input(name = 'User ID'))
    wavelet.root_blip.append('\n')
    wavelet.root_blip.append(element.Button('helpdesk-dev-add_them', 'Add Them'))

def OnParticipantsChanged(event, wavelet):
  logging.info('OnParticipantsChanged Called')
  if ('wave-helpdesk@appspot.com' != wavelet.root_blip.creator):
    return
  badAdded = []
  goodRemoved = []
  #q = db.GqlQuery('SELECT * FROM UserWave WHERE wave_id = :1', wavelet.wave_id)
  repBy = []
  #if q:
  #  if q.reported_by:
  #    repby = [q.reported_by]
  for p in event.participants_added:
    if (p.split('@')[1] == 'appspot.com') or (p.split('@')[1] == 'googlewaverobots.com'):
      badAdded.append(p)
      if p in ['wave-helpdesk@appspot.com', 'statusee@appspot.com',]:
        badAdded.remove(p)
  for p in event.participants_removed:
    if p in PARTICIPANTS + repBy:
      goodRemoved.append(p)
  if event.modified_by in PARTICIPANTS + repBy:
    return
  if not (badAdded or goodRemoved):
    return
  for i in badAdded:
    wavelet.participants.set_role(i, 'READ_ONLY')
    logging.debug('%s now read only' % i)
  for i in goodRemoved:
    wavelet.participants.add(i)
    logging.debug('%s was re-added' % i)
  wavelet.participants.set_role(event.modified_by, 'READ_ONLY')

if ROOT_WAVE:
  prof_url = 'https://wave.google.com/wave/waveref/%s/%s' % (ROOT_WAVE.wave_id.split('!')[0], ROOT_WAVE.wave_id.split('!')[1])
else:
  prof_url = 'http://groups.google.com/group/wave-helpdesk'
myRobot = robot.Robot(name = 'HelpDesk(beta)',
                      image_url = 'http://wave-helpdesk.appspot.com/avatar.png',
                      profile_url = prof_url)
myRobot.register_handler(events.FormButtonClicked, OnFormButtonClicked, context = ['ROOT', 'SELF'])
myRobot.register_handler(events.WaveletParticipantsChanged, OnParticipantsChanged, context = 'ROOT')
myRobot.register_handler(events.WaveletSelfAdded, OnWaveletSelfAdded, context = 'ROOT')
try:
  import credentials
except:
  import credentials_template as credentials
if credentials.V_TOKEN:
  myRobot.set_verification_token_info(credentials.V_TOKEN, credentials.S_TOKEN)
if (credentials.KEY) and (credentials.SECRET):
  myRobot.setup_oauth(credentials.KEY, credentials.SECRET)
appengine_robot_runner.run(myRobot, debug=True)
