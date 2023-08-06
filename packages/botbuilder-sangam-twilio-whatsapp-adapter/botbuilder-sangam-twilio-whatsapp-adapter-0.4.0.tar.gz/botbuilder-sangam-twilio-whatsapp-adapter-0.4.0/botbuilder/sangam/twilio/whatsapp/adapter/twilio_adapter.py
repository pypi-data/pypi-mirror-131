from abc import ABC
from typing import List, Callable, Awaitable

from aiohttp.web_request import Request
from aiohttp.web_response import Response
from botbuilder.core import BotAdapter, TurnContext
from botbuilder.core.bot_assert import BotAssert
from botbuilder.schema import ResourceResponse, Activity, ActivityTypes, ConversationReference
from botframework.connector.auth import ClaimsIdentity
from twilio.base.exceptions import TwilioRestException
from twilio.rest import Client

from .twilio_helper import TwilioHelper
from .twilio_whatsapp_adapter_settings import TwilioWhatsAppAdapterSettings
from .twilio_activity import TwilioActivity


class TwilioAdapter(BotAdapter, ABC):
    def __init__(self, settings: TwilioWhatsAppAdapterSettings):
        super().__init__()

        if not settings.is_valid():
            raise Exception("TwilioWhatsAppAdapterSettings is failed")

        self.twilio_settings = settings
        try:
            self.client = Client(self.twilio_settings.account_sid, self.twilio_settings.auth_token)
        except TwilioRestException as error:
            value = f"TwilioWhatsAppAdapter.sendActivities() : {error.msg}"
            raise Exception(value)

    async def update_activity(self, context: TurnContext, activity: Activity):
        raise Exception("Method not supported by Twilio WhatsApp API.")

    async def delete_activity(self, context: TurnContext, reference: ConversationReference):
        raise Exception("Method not supported by Twilio WhatsApp API.")

    async def send_activities(
            self, context: TurnContext, activities: List[Activity]
    ) -> List[ResourceResponse]:

        if not context:
            raise Exception("TurnContext is required")
        if not activities:
            raise Exception("List[Activity] is required")

        responses = []
        for activity in activities:
            if activity.type == ActivityTypes.message:
                sid = await self.process_message(activity)
                responses.append(sid)
            elif activity.type == ActivityTypes.delay:
                res = ResourceResponse()
                responses.append(res)
            else:
                res = ResourceResponse()
                responses.append(res)

        return responses

    async def process_message(self, activity) -> str:
        if activity.conversation is None or activity.conversation.id is None:
            raise Exception("TwilioWhatsAppAdapter.sendActivities(): Activity doesn't contain a conversation "
                            "id.")
        message = TwilioHelper.parse_activity(self.twilio_settings, activity)
        try:
            message_instance = self.client.messages.create(
                to=message.from_user,
                from_=message.to_user,
                body=message.message,
                # persistent_action=message.persistent_action,
                # media_url=message.media_url
            )
            return message_instance.sid
        except TwilioRestException as error:
            value = f"TwilioWhatsAppAdapter.sendActivities() : {error.msg}"
            raise Exception(value)

    async def continue_conversation(
            self,
            reference: ConversationReference,
            callback: Callable,
            bot_id: str = None,  # pylint: disable=unused-argument
            claims_identity: ClaimsIdentity = None,  # pylint: disable=unused-argument
            audience: str = None,  # pylint: disable=unused-argument
    ):
        if not reference:
            raise Exception("ConversationReference is required")

        activity = Activity()
        activity.type = ActivityTypes.event
        activity.name = "continue_conversation"
        TurnContext.apply_conversation_reference(activity, reference, True)
        turn_context = TurnContext(activity)
        return self.run_pipeline(turn_context)

    async def process_activity(self, req: Request, res: Response, bot_callable: Callable):
        if not req:
            raise Exception("Request is required")

        auth_header = ""
        if 'X-Twilio-Signature' in req.headers:
            auth_header = req.headers["X-Twilio-Signature"]
        elif 'x-twilio-signature' in req.headers:
            auth_header = req.headers["x-twilio-signature"]

        if len(auth_header) < 0:
            res.status = 401
            return

        if req.body_exists:
            value = await req.read()
            body = value.decode("utf-8")
            twilio_params = TwilioHelper.query_string_to_dictionary(body)

            # validate = TwilioHelper.twilio_validate(self.twilio_settings,auth_header)

            # if validate == False:
            #     res.status = 400
            #     return

            if twilio_params.keys():
                activity = TwilioActivity(twilio_params)
                if activity is not None:
                    context = TurnContext(self, activity.activity)
                    await self.run_pipeline(context, bot_callable)
                    response = TwilioHelper.response(200)
                    return response
                else:
                    raise Exception("create TwilioActivity exception")
            else:
                raise Exception("TwilioWhatsAppAdapter.processActivity(): request read is empty")
        else:
            raise Exception("TwilioWhatsAppAdapter.processActivity(): request read is empty")

    async def run_pipeline(self, context: TurnContext, callback: Callable[[TurnContext], Awaitable] = None):

        BotAssert.context_not_none(context)

        if context.activity is not None:
            try:
                if callback is not None:
                    return await self._middleware.receive_activity_with_status(context, callback)
            except Exception as ex:
                if self.on_turn_error is not None:
                    await self.on_turn_error(context, ex)
                else:
                    raise ex
        else:
            if callback is not None:
                await callback(context)
