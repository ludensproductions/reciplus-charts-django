import json

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from django.template.loader import render_to_string

from apps.chat.consts import MESSAGE_TEMPLATE, MessageTypes


class ChatConsumer(WebsocketConsumer):
    """WebSocket consumer that implements a simple broadcast chat using Django Channels.

    This consumer:
    - Accepts WebSocket connections.
    - Adds each connection to a shared channel layer group.
    - Receives JSON-encoded messages from clients.
    - Renders each message server-side into HTML.
    - Broadcasts the rendered HTML to all connected clients.

    The consumer is designed to work well with HTMX, where messages are
    sent as JSON and the server returns pre-rendered HTML fragments
    instead of raw data.

    Attributes:
        group_name (str): Name of the channel layer group used to
            broadcast chat messages to all connected clients.
    """

    def connect(self):
        """Handles a new WebSocket connection.

        When a client connects:
        - A fixed broadcast group name is assigned.
        - The client's channel is added to the group.
        - The WebSocket connection is accepted.

        This allows all connected clients to receive messages broadcast
        to the group.

        Side Effects:
            - Registers the channel in the channel layer group.
            - Opens the WebSocket connection.

        """
        user = self.scope["user"]

        if not user or user.is_anonymous or not user.is_authenticated or not user.is_active:
            self.close(code=4401)
            return

        self.group_name = "chat_broadcast"

        async_to_sync(self.channel_layer.group_add)(
            self.group_name,
            self.channel_name,
        )

        self.accept()

    def disconnect(self, close_code):
        """Handles WebSocket disconnection.

        Removes the client's channel from the broadcast group to prevent
        further messages from being sent to a closed connection.

        Args:
            close_code (int): WebSocket close code provided by the client
                or server.
        """
        async_to_sync(self.channel_layer.group_discard)(
            self.group_name,
            self.channel_name,
        )

    def receive(self, text_data):
        """Handles incoming messages from the WebSocket client.

        Expects JSON-formatted text data with a `message` field.
        Empty or whitespace-only messages are silently ignored.

        For valid messages:
        - The message is rendered into an HTML fragment using a Django
          template.
        - The rendered HTML is broadcast to all clients in the group.

        Args:
            text_data (str): JSON-encoded message payload received over
                the WebSocket connection.

        Expected JSON format:
            {
                "message": "<user message>"
            }
        """
        # HTMX sends form-encoded data
        data = json.loads(text_data)

        message = ""

        try:
            message = data.get("message", "").strip()
        except json.JSONDecodeError:  # silently ignore when text_data isn't a valid json
            return

        if not message:
            return  # silently ignore empty messages

        html = render_to_string(
            template_name=MESSAGE_TEMPLATE,
            context={"message": message},
        )

        async_to_sync(self.channel_layer.group_send)(
            self.group_name,
            {
                "type": MessageTypes.CHAT_MESSAGE.value,
                "html": html,
            },
        )

    def chat_message(self, event):
        """Receives broadcast chat events from the channel layer.

        This method is invoked automatically by Django Channels when a
        message with type `chat.message` is sent to the group.

        It forwards the pre-rendered HTML directly to the WebSocket
        client.

        Args:
            event (dict): Event payload sent by the channel layer.
                Expected to contain:
                - "html" (str): Rendered HTML fragment representing the
                  chat message.
        """
        self.send(text_data=event["html"])
