class TwilioWhatsAppAdapterSettings:
    def __init__(
            self,
            account_sid: str,
            auth_token: str,
            phone_number: str,
            endpoint_url: str
    ):
        self.account_sid = account_sid
        self.auth_token = auth_token
        self.phone_number = phone_number
        self.endpoint_url = endpoint_url

    def is_valid(self) -> bool:
        if (
                len(self.account_sid) == 0 or
                len(self.auth_token) == 0 or
                len(self.phone_number) == 0 or
                len(self.endpoint_url) == 0
        ):
            return False

        # if not self.phone_number.startsWith('whatsapp:'):
        # self.phone_number = 'whatsapp:' + self.phone_number

        return True
