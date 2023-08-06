from meili_sdk.websockets.client import MeiliWebsocketClient


def open_handler():
    print("Websocket is opened")


def on_close():
    print("WS CLOSED")


def on_error(*_):
    print("error has occurred")


client = MeiliWebsocketClient(
    "77b971e8f47e421045d384558059c31679b4b6ca",
    override_host="wss://development.meilirobots.com",
    fleet=True,
    open_handler=open_handler,
    close_handler=on_close,
    error_handler=on_error,
)

client.add_vehicle("2eb03045cbc640fdbd2181ab60387b7a")
client.run()
