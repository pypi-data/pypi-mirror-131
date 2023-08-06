class TwilioMessage:
    def __init__(self):
        self._to_user = ""
        self._from_user = ""
        self._message = ""
        self._persistent_action = ""
        self._body = ""
        self._persistent_action = ""
        self._media_url = ""

    @property
    def to_user(self):
        return self._to_user

    @to_user.setter
    def to_user(self, to: str):
        self._to_user = to

    @property
    def from_user(self):
        return self._from_user

    @from_user.setter
    def from_user(self, from_user: str):
        self._from_user = from_user

    @property
    def message(self):
        return self._message

    @message.setter
    def message(self, message: str):
        self._message = message

    @property
    def persistent_action(self):
        return self._persistent_action

    @persistent_action.setter
    def persistent_action(self, persistent: str):
        self._persistent_action = persistent

    @property
    def body(self):
        return self._body

    @body.setter
    def body(self, message_body: str):
        self._body = message_body

    @property
    def persistent_action(self):
        return self._persistent_action

    @persistent_action.setter
    def persistent_action(self, action: str):
        self._persistent_action = action

    @property
    def media_url(self):
        return self._media_url

    @media_url.setter
    def media_url(self, media: str):
        self._media_url = media
