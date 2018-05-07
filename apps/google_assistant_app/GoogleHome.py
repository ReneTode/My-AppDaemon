#################################################################################################
#                                                                                               #
#  Rene Tode ( hass@reot.org )                                                                  #
#  2017/5/2 Germany                                                                             #
#
#  I used the code from the example from google assistant SDK.                                  #
#  https://developers.google.com/assistant/sdk/prototype/getting-started-pi-python/run-sample   #
#  and i created an Appdaemon App from it to connect it to Home assistant.                      #
#  args:                                                                                        #
#    - activation_boolean = input_boolean.google_assistant (create this boolean in HA)          #
#                                                                                               #
#  install the google assistant in the same environment as appdaemon                            #
#  edit the line with sys.path to match the directory where your google assistant is installed  #
#                                                                                               #
#################################################################################################

import appdaemon.appapi as appapi
import datetime
import time
import os.path
import click

from google.assistant.embedded.v1alpha1 import embedded_assistant_pb2
from google.rpc import code_pb2

import sys
sys.path.append('/home/pi/googlehome/lib/python3.4/site-packages/googlesamples/assistant')
import assistant_helpers
import audio_helpers
import auth_helpers
import common_settings

class GoogleHome(appapi.AppDaemon):

  def initialize(self):
    self.ASSISTANT_API_ENDPOINT = 'embeddedassistant.googleapis.com'
    self.END_OF_UTTERANCE = embedded_assistant_pb2.ConverseResponse.END_OF_UTTERANCE
    self.DIALOG_FOLLOW_ON = embedded_assistant_pb2.ConverseResult.DIALOG_FOLLOW_ON
    self.CLOSE_MICROPHONE = embedded_assistant_pb2.ConverseResult.CLOSE_MICROPHONE
    api_endpoint=self.ASSISTANT_API_ENDPOINT
    credentials=os.path.join(click.get_app_dir(common_settings.ASSISTANT_APP_NAME), common_settings.ASSISTANT_CREDENTIALS_FILENAME)
    verbose=False
    self.audio_sample_rate=common_settings.DEFAULT_AUDIO_SAMPLE_RATE
    self.audio_sample_width=common_settings.DEFAULT_AUDIO_SAMPLE_WIDTH
    self.audio_iter_size=common_settings.DEFAULT_AUDIO_ITER_SIZE
    self.audio_block_size=common_settings.DEFAULT_AUDIO_DEVICE_BLOCK_SIZE
    self.audio_flush_size=common_settings.DEFAULT_AUDIO_DEVICE_FLUSH_SIZE
    self.grpc_deadline=common_settings.DEFAULT_GRPC_DEADLINE

    # Load credentials.
    try:
        creds = auth_helpers.load_credentials(credentials, scopes=[common_settings.ASSISTANT_OAUTH_SCOPE])
    except Exception as e:
        self.error('Error loading credentials: %s', e)
        self.error('Run auth_helpers to initialize new OAuth2 credentials.')
        return

    # Create gRPC channel
    grpc_channel = auth_helpers.create_grpc_channel(api_endpoint, creds, ssl_credentials_file="", grpc_channel_options="")
    self.log('Connecting to google')
    # Create Google Assistant API gRPC client.
    self.assistant = embedded_assistant_pb2.EmbeddedAssistantStub(grpc_channel)

    # Configure audio source and sink.
    self.audio_device = None
    self.audio_source = self.audio_device = (self.audio_device or audio_helpers.SoundDeviceStream(sample_rate=self.audio_sample_rate, sample_width=self.audio_sample_width, block_size=self.audio_block_size, flush_size=self.audio_flush_size))
    self.audio_sink = self.audio_device = (self.audio_device or audio_helpers.SoundDeviceStream(sample_rate=self.audio_sample_rate, sample_width=self.audio_sample_width, block_size=self.audio_block_size, flush_size=self.audio_flush_size))

    # Create conversation stream with the given audio source and sink.
    self.conversation_stream = audio_helpers.ConversationStream(source=self.audio_source, sink=self.audio_sink, iter_size=self.audio_iter_size)
    self.conversation_state_bytes = None
    self.volume_percentage = 70

    self.listen_state(self.startGH,self.args["activation_boolean"],new="on")        
    self.log("App started. now listening to Homeassistant input")
     
  def startGH(self, entity, attribute, old, new, kwargs):

    wait_for_user = False
    while not wait_for_user:
      self.conversation_stream.start_recording()
      self.log('Recording audio request.')

      def gen_converse_requests():
        converse_state = None
        if self.conversation_state_bytes:
            converse_state = embedded_assistant_pb2.ConverseState( conversation_state=self.conversation_state_bytes)
        config = embedded_assistant_pb2.ConverseConfig(audio_in_config=embedded_assistant_pb2.AudioInConfig(encoding='LINEAR16', sample_rate_hertz=int(self.audio_sample_rate)), audio_out_config=embedded_assistant_pb2.AudioOutConfig(encoding='LINEAR16', sample_rate_hertz=int(self.audio_sample_rate), volume_percentage=self.volume_percentage), converse_state=converse_state)
        yield embedded_assistant_pb2.ConverseRequest(config=config)
        for data in self.conversation_stream:
           yield embedded_assistant_pb2.ConverseRequest(audio_in=data)

      def iter_converse_requests():
        for c in gen_converse_requests():
            assistant_helpers.log_converse_request_without_audio(c)
            yield c
        self.conversation_stream.start_playback()

      for resp in self.assistant.Converse(iter_converse_requests(), self.grpc_deadline):
        assistant_helpers.log_converse_response_without_audio(resp)
        if resp.error.code != code_pb2.OK:
            self.error('server error: ' + resp.error.message)
            return
        if resp.event_type == self.END_OF_UTTERANCE:
            self.log('End of audio request detected')
            self.conversation_stream.stop_recording()
        if resp.result.spoken_request_text:
            self.log('Transcript of user request: ' + resp.result.spoken_request_text)
            self.log('Playing assistant response.')
        if len(resp.audio_out.audio_data) > 0:
            self.conversation_stream.write(resp.audio_out.audio_data)
        if resp.result.spoken_response_text:
            self.log('Transcript of TTS response (only populated from IFTTT): ' + resp.result.spoken_response_text)
        if resp.result.conversation_state:
            conversation_state_bytes = resp.result.conversation_state
        if resp.result.volume_percentage != 0:
            volume_percentage = resp.result.volume_percentage
            self.log('Volume should be set to ' + str(volume_percentage))
        if resp.result.microphone_mode == self.DIALOG_FOLLOW_ON:
            wait_for_user = False
            self.log('Expecting follow-on query from user.')
        elif resp.result.microphone_mode == self.CLOSE_MICROPHONE:
            wait_for_user = True
            self.log("Closing the microphone now.")
      self.log('Finished playing assistant response.')
      self.conversation_stream.stop_playback()
    self.turn_off(entity)

  def terminate():
    self.conversation_stream.close()

