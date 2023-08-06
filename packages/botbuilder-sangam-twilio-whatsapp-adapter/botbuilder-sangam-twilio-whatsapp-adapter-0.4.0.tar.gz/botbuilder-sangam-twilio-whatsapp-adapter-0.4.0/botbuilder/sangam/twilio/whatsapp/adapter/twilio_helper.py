from typing import Dict
from aiohttp.web_request import Request
from aiohttp.web_response import Response
from botbuilder.schema import Activity
from .twilio_message import TwilioMessage
from .twilio_whatsapp_adapter_settings import TwilioWhatsAppAdapterSettings
import urllib.parse
from twilio.request_validator import RequestValidator
import re

class TwilioHelper:
    @staticmethod
    def parse_activity(
            settings: TwilioWhatsAppAdapterSettings,
            activity: Activity) -> TwilioMessage:

        activity.text = TwilioHelper.text_format_change(activity.text)
        # activity.channel_data =

        message = TwilioMessage()
        message.body = activity.text
        message.message = activity.text
        message.from_user = settings.phone_number
        message.to_user = activity.from_property.id

        if activity.attachments:
            attachment = activity.attachments[0]
            if attachment.content_type == "application/json":
                geo_location = attachment.content
                if 'type' in geo_location and geo_location['type'] == 'GeoCoordinates':
                    if 'coordinates' in geo_location:
                        if attachment.name is not None:
                            geo_name = attachment.name
                        else:
                            geo_name = ""

                        geo = geo_location['coordinates']
                        geo_info = f"geo:{geo['Latitude']} , {geo['Longitude']} , {geo_name}"
                        message.persistent_action = geo_info
            elif attachment.content_url is not None:
                message.media_url = attachment.content_url
            else:
                print("TwilioWhatsAppAdapter.parseActivity(): Attachment ignored. Attachment without contentUrl is "
                      "not supported")

            if message.body is None and message.media_url is None:
                raise Exception("TwilioWhatsAppAdapter.parseActivity(): An activity text or attachment with contentUrl "
                                "must be specified.")
        return message

    # convert the text to whatsapp's formatting (remove all the html related tags)
    @staticmethod
    def text_format_change(format_text: str) -> str:
        if format_text:
            clean = re.compile('<.*?>')
            format_text = re.sub(clean, '', format_text)
        return format_text

    @staticmethod
    def query_string_to_dictionary(query: str) -> Dict:
        """
        Converts a query string to a dictionary with key-value pairs.
        :param query: The query string to convert.
        :type query: str
        :return: A dictionary with the query values.
        :rtype: :class:`typing.Dict`
        """

        values = {}

        if not query:
            return values

        pairs = query.replace("+", "%20").split("&")

        for pair in pairs:
            key_value = pair.split("=")
            key = key_value[0]
            value = urllib.parse.unquote(key_value[1])

            values[key] = value

        return values

    @staticmethod
    def response(code : int, body: str = None, encoding: str = None) -> Request:
        response = Response(status=code)
        if body:
            response.content_type = "text/plain"
            response.body = body.encode(encoding=encoding if encoding else "utf-8")
        return response

    # Need to check this function
    # @staticmethod
    # def twilio_validate(setting: TwilioWhatsAppAdapterSettings, signature) -> bool:
    #     validator = RequestValidator(setting.auth_token)
    #     return validator.validate(setting.endpoint_url, "", signature)
