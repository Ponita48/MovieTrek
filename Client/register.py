import wx
import wx.xrc
import hashlib
import requests
import json

###########################################################################
## Class RegisterFrame
###########################################################################

class RegisterFrame ( wx.Frame ):
	
	def __init__( self, parent ):
		wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = u"Register", pos = wx.DefaultPosition, size = wx.Size( -1,-1 ), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )
		
		self.SetSizeHintsSz( wx.DefaultSize, wx.DefaultSize )
		
		bSizer1 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.Container = wx.Panel( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		linearLayout = wx.BoxSizer( wx.VERTICAL )
		
		gridLayout = wx.GridSizer( 0, 2, 0, 0 )
		
		self.unameText = wx.StaticText( self.Container, wx.ID_ANY, u"Username", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.unameText.Wrap( -1 )
		gridLayout.Add( self.unameText, 0, wx.ALL|wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.unameBox = wx.TextCtrl( self.Container, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		gridLayout.Add( self.unameBox, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.pwdText = wx.StaticText( self.Container, wx.ID_ANY, u"Password", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.pwdText.Wrap( -1 )
		gridLayout.Add( self.pwdText, 0, wx.ALL|wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.pwdBox = wx.TextCtrl( self.Container, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.TE_PASSWORD )
		gridLayout.Add( self.pwdBox, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.confPwdText = wx.StaticText( self.Container, wx.ID_ANY, u"Confirm Password", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.confPwdText.Wrap( -1 )
		gridLayout.Add( self.confPwdText, 0, wx.ALL|wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.confPwdBox = wx.TextCtrl( self.Container, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.TE_PASSWORD )
		gridLayout.Add( self.confPwdBox, 0, wx.ALL, 5 )
		
		self.emailText = wx.StaticText( self.Container, wx.ID_ANY, u"Email", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.emailText.Wrap( -1 )
		gridLayout.Add( self.emailText, 0, wx.ALL|wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.emailBox = wx.TextCtrl( self.Container, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		gridLayout.Add( self.emailBox, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		
		linearLayout.Add( gridLayout, 0, 0, 5 )
		
		self.btnRegister = wx.Button( self.Container, wx.ID_ANY, u"Register", wx.DefaultPosition, wx.DefaultSize, 0 )
		linearLayout.Add( self.btnRegister, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5 )
		
		
		self.Container.SetSizer( linearLayout )
		self.Container.Layout()
		linearLayout.Fit( self.Container )
		bSizer1.Add( self.Container, 1, wx.EXPAND |wx.ALL, 0 )
		
		
		self.SetSizer( bSizer1 )
		self.Layout()
		bSizer1.Fit( self )
		
		self.Centre( wx.BOTH )
		
		# Connect Events
		self.btnRegister.Bind( wx.EVT_BUTTON, self.btnRegister_click )
	
	def __del__( self ):
		pass
	
	
	# Virtual event handlers, overide them in your derived class
	def btnRegister_click( self, event ):
		uname = self.unameBox.GetValue()
		pwd = self.pwdBox.GetValue()
		conf = self.confPwdBox.GetValue()
		email = self.emailBox.GetValue()

		if len(uname) < 6:
			wx.MessageBox('Username must be at least 6 character', 'MovieTrek Register', wx.OK | wx.ICON_WARNING)
		elif len(pwd) < 6:
			wx.MessageBox('Password must be at least 6 character', 'MovieTrek Register', wx.OK | wx.ICON_WARNING)
		elif "@" not in email or "." not in email:
			wx.MessageBox('Email format didn\'t match', 'MovieTrek Register', wx.OK | wx.ICON_WARNING)
		elif pwd != conf:
			wx.MessageBox('Password didn\'t match', 'MovieTrek Register', wx.OK | wx.ICON_WARNING)
		else:
			data = {
				'username' : uname,
				'password' : pwd,
				'email' : email
			}
			req = requests.post('http://localhost:5000/api/register', data=data)
			ret_val = json.loads(json.dumps(req.json()))
			print(ret_val)
			if ret_val['status'] == 1:
				wx.MessageBox('Successfully Registered!', 'MovieTrek Register', wx.OK | wx.ICON_INFORMATION)
				self.Close()
			elif ret_val['status'] == 2:
				wx.MessageBox('Username already taken!', 'MovieTrek Register', wx.OK | wx.ICON_WARNING)
			elif ret_val['status'] == 0:
				wx.MessageBox('An Error has occured, please try again later', 'MovieTrek Register', wx.OK | wx.ICON_WARNING)
