from Screen import Screen
from Components.ActionMap import ActionMap
from Components.Label import Label
from Components.Pixmap import Pixmap
from Components.Sources.StaticText import StaticText
from Components.MenuList import MenuList
from enigma import eTimer

class MessageBox(Screen):
	TYPE_YESNO = 0
	TYPE_INFO = 1
	TYPE_WARNING = 2
	TYPE_ERROR = 3
	TYPE_MESSAGE = 4

	def __init__(self, session, text, type=TYPE_YESNO, timeout=-1, close_on_any_key=False, default=True, enable_input=True, msgBoxID=None, picon=None, simple=False, list=[], timeout_default=None):
		self.type = type
		Screen.__init__(self, session)
		self.skinName = ["MessageBox"]
		if self.type == self.TYPE_YESNO:
			self.setTitle(_("Question"))
		elif self.type == self.TYPE_INFO:
			self.setTitle(_("Information"))
		elif self.type == self.TYPE_WARNING:
			self.setTitle(_("Warning"))
		elif self.type == self.TYPE_ERROR:
			self.setTitle(_("Error"))
		else:
			self.setTitle(_("Message"))

		if simple:
			self.skinName="MessageBoxSimple"
		
		self.msgBoxID = msgBoxID

		self["text"] = Label(text)
		self["Text"] = StaticText(text)
		self["selectedChoice"] = StaticText()

		self.text = text
		self.close_on_any_key = close_on_any_key
		self.timeout_default = timeout_default

		self["ErrorPixmap"] = Pixmap()
		self["QuestionPixmap"] = Pixmap()
		self["InfoPixmap"] = Pixmap()
		self["WarningPixmap"] = Pixmap()
		self.timerRunning = False
		self.initTimeout(timeout)

		picon = picon or type
		if picon != self.TYPE_ERROR:
			self["ErrorPixmap"].hide()
		if picon != self.TYPE_YESNO:
			self["QuestionPixmap"].hide()
		if picon != self.TYPE_INFO:
			self["InfoPixmap"].hide()
		if picon != self.TYPE_WARNING:
			self["WarningPixmap"].hide()
		self.title = self.type < self.TYPE_MESSAGE and [_("Question"), _("Information"), _("Warning"), _("Error")][self.type] or _("Message")
		if type == self.TYPE_YESNO:
			if list:
				self.list = list
			elif default == True:
				self.list = [ (_("yes"), True), (_("no"), False) ]
			else:
				self.list = [ (_("no"), False), (_("yes"), True) ]
		else:
			self.list = []
		
		self["list"] = MenuList(self.list)
		if self.list:
			self["selectedChoice"].setText(self.list[0][0])
		else:
			self["list"].hide()

		if enable_input:
			self["actions"] = ActionMap(["MsgBoxActions", "DirectionActions"], 
				{
					"cancel": self.cancel,
					"ok": self.ok,
					"alwaysOK": self.alwaysOK,
					"up": self.up,
					"down": self.down,
					"left": self.left,
					"right": self.right,
					"upRepeated": self.up,
					"downRepeated": self.down,
					"leftRepeated": self.left,
					"rightRepeated": self.right
				}, -1)

		self.onLayoutFinish.append(self.layoutFinished)

	def layoutFinished(self):
		self.setTitle(self.title)

	def autoResize(self):
		desktop_w = enigma.getDesktop(0).size().width()
		desktop_h = enigma.getDesktop(0).size().height()
		count = len(self.list)

		if not self["text"].text:
			textsize = (520, 0)
			listsize = (520, 25*count)
			if self["ErrorPixmap"].visible or self["QuestionPixmap"].visible or self["InfoPixmap"].visible:
				self["list"].instance.move(enigma.ePoint(65, 0))
			else:
				self["list"].instance.move(enigma.ePoint(0, 0))
			self["list"].instance.resize(enigma.eSize(*listsize))

		else:
			textsize = self["text"].getSize()
			if textsize[0] < textsize[1]:
				textsize = (textsize[1],textsize[0]+10)
			if textsize[0] > 520:
				textsize = (textsize[0], textsize[1]+25)
			else:
				textsize = (520, textsize[1]+25)
			listsize = (textsize[0], 25*count)

			self["text"].instance.resize(enigma.eSize(*textsize))
			if self["ErrorPixmap"].visible or self["QuestionPixmap"].visible or self["InfoPixmap"].visible:
				self["text"].instance.move(enigma.ePoint(65, 0))
			else:
				self["text"].instance.move(enigma.ePoint(10, 10))

			if self["ErrorPixmap"].visible or self["QuestionPixmap"].visible or self["InfoPixmap"].visible:
				self["list"].instance.move(enigma.ePoint(65, textsize[1]))
				wsizex = textsize[0]+65
			else:
				self["list"].instance.move(enigma.ePoint(0, textsize[1]))
				wsizex = textsize[0]
			self["list"].instance.resize(enigma.eSize(*listsize))

		wsizey = textsize[1]+listsize[1]
		wsize = (wsizex, wsizey)
		self.instance.resize(enigma.eSize(*wsize))
		self.instance.move(enigma.ePoint((desktop_w-wsizex)/2, (desktop_h-wsizey)/2))	

	def initTimeout(self, timeout):
		self.timeout = timeout
		if timeout > 0:
			self.timer = eTimer()
			self.timer.callback.append(self.timerTick)
			self.onExecBegin.append(self.startTimer)
			self.origTitle = None
			if self.execing:
				self.timerTick()
			else:
				self.onShown.append(self.__onShown)
			self.timerRunning = True
		else:
			self.timerRunning = False

	def __onShown(self):
		self.onShown.remove(self.__onShown)
		self.timerTick()

	def startTimer(self):
		self.timer.start(1000)

	def stopTimer(self):
		if self.timerRunning:
			del self.timer
			self.onExecBegin.remove(self.startTimer)
			self.setTitle(self.origTitle)
			self.timerRunning = False

	def timerTick(self):
		if self.execing:
			self.timeout -= 1
			if self.origTitle is None:
				self.origTitle = self.instance.getTitle()
			self.setTitle(self.origTitle + " (" + str(self.timeout) + ")")
			if self.timeout == 0:
				self.timer.stop()
				self.timerRunning = False
				self.timeoutCallback()

	def timeoutCallback(self):
		print "Timeout!"
		if self.timeout_default is not None:
			self.close(self.timeout_default)
		else:
			self.ok()

	def cancel(self):
		self.close(False)

	def ok(self):
		if self.list:
			self.close(self["list"].getCurrent()[1])
		else:
			self.close(True)

	def alwaysOK(self):
		self.close(True)

	def up(self):
		self.move(self["list"].instance.moveUp)

	def down(self):
		self.move(self["list"].instance.moveDown)

	def left(self):
		self.move(self["list"].instance.pageUp)

	def right(self):
		self.move(self["list"].instance.pageDown)

	def move(self, direction):
		if self.close_on_any_key:
			self.close(True)
		self["list"].instance.moveSelection(direction)
		if self.list:
			self["selectedChoice"].setText(self["list"].getCurrent()[0])
		self.stopTimer()

	def __repr__(self):
		return str(type(self)) + "(" + self.text + ")"
