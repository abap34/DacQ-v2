from streamlit.web.server.websocket_headers import _get_websocket_headers



def get_username():
    headers = _get_websocket_headers()
    user = headers.get("X-Forwarded-User")
    if user is None:
        user = "Unkown"
    return user