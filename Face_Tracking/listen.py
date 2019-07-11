from pubnub.pubnub import PubNub, SubscribeListener  
from pubnub.callbacks import SubscribeCallback 
from pubnub.enums import PNStatusCategory  
from pubnub.pnconfiguration import PNConfiguration  


pnconfig = PNConfiguration() 

pnconfig.subscribe_key = "sub-c-bab9dc6c-912f-11e9-9769-e24cdeae5ee1" 
pnconfig.publish_key = "pub-c-14a2c33b-ff74-4bb7-8139-ff46eed621cc" 

pubnub = PubNub(pnconfig)

 
def ListenMessage():
	my_listener = SubscribeListener()

	pubnub.add_listener(my_listener)
 
	pubnub.subscribe().channels('awesomeChannel').execute()
	my_listener.wait_for_connect()
	print('connected')
	result = my_listener.wait_for_message_on('awesomeChannel')
	keep_goin = True
	print ("starting to listen")
	while keep_goin:
	
		print(result.message)
		result = my_listener.wait_for_message_on('awesomeChannel')
		if result.message == "bye":
			keep_goin = False
ListenMessage()
 
print('unsubscribed')
