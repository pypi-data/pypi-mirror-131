from botbuilder.schema import Activity, ActivityTypes, ConversationAccount, ChannelAccount, Attachment
from datetime import datetime


class TwilioActivity:
    def __init__(self, params) -> None:
        self.activity = self.create_activity(params)
        self.activity.conversation = self.create_conversation(params)
        self.activity.from_property = self.create_from_channel_account(params)
        self.activity.recipient = self.create_recipient_channel_account(params)

        attachment = self.find_attachment(params)
        if attachment is not None and len(attachment) > 0:
            self.activity.attachments = attachment

        self.activity.type = self.TwilioActivityType(params['SmsStatus'])

    @staticmethod
    def create_activity(params) -> Activity:
        activity = Activity()
        activity.channel_id = 'twilio'
        activity.timestamp = datetime.now()
        activity.id = params['SmsMessageSid']
        activity.text = params['Body']
        activity.channel_data = 'messages'
        activity.local_timezone = 'null'
        activity.caller_id = 'null'
        activity.service_url = 'null'
        activity.listen_for = 'null'
        activity.label = params['SmsMessageSid']
        activity.value_type = 'null'
        return activity

    @staticmethod
    def create_from_channel_account(params) -> ChannelAccount:
        from_property = ChannelAccount()
        from_property.id = params['From']
        from_property.name = 'null'
        return from_property

    @staticmethod
    def create_recipient_channel_account(reqDict) -> ChannelAccount:
        recipient = ChannelAccount()
        recipient.id = reqDict['To']
        recipient.name = 'null'
        return recipient

    @staticmethod
    def create_conversation(reqDict) -> ConversationAccount:
        conversation = ConversationAccount()
        conversation.id = reqDict['From']
        conversation.is_group = False
        conversation.conversation_type = 'null'
        conversation.tenant_id = 'null'
        conversation.name = 'null'
        return conversation

    @staticmethod
    def TwilioActivityType(message: str) -> str:
        activity_type = ""
        message_type = message.lower()
        if message_type == 'sent':
            activity_type = 'messageSent'
        elif message_type == 'received':
            activity_type = ActivityTypes.message
        elif message_type == 'delivered':
            activity_type = 'messageDelivered'
        elif message_type == 'read':
            activity_type = 'messageRead'
        return activity_type

    def find_attachment(self, reqDict) -> list[Attachment]:
        media_attachment = self.media_content_type_attachments(reqDict)
        location_attachment = self.geo_location(reqDict)

        Attachments = []

        if media_attachment is not None:
            Attachments = media_attachment
        if location_attachment is not None:
            Attachments.append(location_attachment)

        return Attachments

    @staticmethod
    def media_content_type_attachments(reqDict):
        Attachments = []
        media_count = int(reqDict['NumMedia'])
        if media_count > 0:
            for i in range(media_count):
                attachment = Attachment()
                attachment.content_type = reqDict['MediaContentType' + str(i)]
                attachment.content_url = reqDict['MediaUrl' + str(i)]
                Attachments.append(attachment)
            return Attachments
        else:
            return None

    @staticmethod
    def geo_location(params) -> None:
        if 'Latitude' in params and 'Longitude' in params:
            location = Attachment()
            if params['Latitude'] is not None and params['Longitude'] is not None:
                geo_location = {'type': 'GeoCoordinates', 'coordinates': {}}
                geo_location['coordinates']['Latitude'] = float(params['Latitude'])
                geo_location['coordinates']['Longitude'] = float(params['Longitude'])
                if params['Latitude'] is not None:
                    location.name = params['Address']
                else:
                    location.name = 'null'

                location.content_type = 'application/json'
                location.content = geo_location
                return location
        else:
            return None
