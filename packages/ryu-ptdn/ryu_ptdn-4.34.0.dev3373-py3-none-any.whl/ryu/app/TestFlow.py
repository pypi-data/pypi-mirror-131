from ryu.base import app_manager
from ryu.controller import ofp_event
from ryu.controller.handler import CONFIG_DISPATCHER, MAIN_DISPATCHER
from ryu.controller.handler import set_ev_cls
from ryu.ofproto import ofproto_v1_3
from ryu.lib.packet import packet
from ryu.lib.packet import ethernet
from ryu.lib.packet import ether_types

class TestFlow(app_manager.RyuApp):
	OFP_VERSIONS = [ofproto_v1_3.OFP_VERSION]
	
	def __init__(self, *args, **kwargs):
		super(TestFlow,self).__init__(*args, **kwargs)
	
	@set_ev_cls(ofp_event.EventOFPPortDescStatsReply, CONFIG_DISPATCHER)
	def multipart_handler(self, ev):
		with open('/tmp/newtest.txt', 'w') as f:
			f.write('Hello, dkl!')
