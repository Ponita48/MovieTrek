import wx
import wx.xrc
import hashlib
import requests
import json

###########################################################################
## Class LoginFrame
###########################################################################

class LoginFrame ( wx.Frame ):
	
	def __init__( self, parent ):
		wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = wx.EmptyString, pos = wx.DefaultPosition, size = wx.Size( -1,-1 ), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )
		
		self.SetSizeHintsSz( wx.DefaultSize, wx.DefaultSize )
		
		bSizer1 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.m_panel2 = wx.Panel( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer2 = wx.BoxSizer( wx.VERTICAL )
		
		gSizer1 = wx.GridSizer( 0, 2, 0, 0 )
		
		self.unameText = wx.StaticText( self.m_panel2, wx.ID_ANY, u"Username", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.unameText.Wrap( -1 )
		gSizer1.Add( self.unameText, 0, wx.ALL|wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.unameBox = wx.TextCtrl( self.m_panel2, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer1.Add( self.unameBox, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.pwdText = wx.StaticText( self.m_panel2, wx.ID_ANY, u"Password", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.pwdText.Wrap( -1 )
		gSizer1.Add( self.pwdText, 0, wx.ALL|wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.pwdBox = wx.TextCtrl( self.m_panel2, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.TE_PASSWORD )
		gSizer1.Add( self.pwdBox, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		
		bSizer2.Add( gSizer1, 0, 0, 5 )
		
		self.btnLogin = wx.Button( self.m_panel2, wx.ID_ANY, u"Login", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer2.Add( self.btnLogin, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5 )
		
		
		self.m_panel2.SetSizer( bSizer2 )
		self.m_panel2.Layout()
		bSizer2.Fit( self.m_panel2 )
		bSizer1.Add( self.m_panel2, 1, wx.EXPAND |wx.ALL, 0 )
		
		
		self.SetSizer( bSizer1 )
		self.Layout()
		bSizer1.Fit( self )
		
		self.Centre( wx.BOTH )
		
		# Connect Events
		self.btnLogin.Bind( wx.EVT_BUTTON, self.btnLogin_click )
	
	def __del__( self ):
		pass
	
	
	# Virtual event handlers, overide them in your derived class
	def btnLogin_click( self, event ):
		uname = self.unameBox.GetValue()
		pwd = self.pwdBox.GetValue()
		data = {
			'username': uname,
			'password': pwd
		}
		req = requests.post('http://localhost:5000/api/login', data=data)
		ret_val = json.loads(json.dumps(req.json()))
		if ret_val['status'] == 1:
			# Successfully logged in
			file = open("data", "w")
			file.write(str(ret_val["token"]))
			file.close()
			wx.MessageBox('Successfully Logged In!', 'MovieTrek Login', wx.OK | wx.ICON_INFORMATION)
			self.Close()
		elif ret_val['status'] == 0:
			# wrong uname or password
			wx.MessageBox('Incorrect Username or Password', 'MovieTrek Login', wx.OK | wx.ICON_WARNING)
			