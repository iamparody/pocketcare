import reflex as rx
from app.states.peer_chat_state import PeerChatState
from app.states.auth_state import AuthState
from app.components.sidebar import sidebar
from app.components.header import header
from app.states.dashboard_state import DashboardState


def waiting_view():
    return rx.el.div(
        rx.el.h2("Finding a Peer...", class_name="text-2xl font-bold"),
        rx.el.p(
            "We're connecting you with someone to talk to.",
            class_name="text-gray-600 mt-2",
        ),
        rx.el.div(rx.spinner(class_name="w-8 h-8 text-blue-500"), class_name="my-8"),
        rx.el.p(f"Your position in queue: {PeerChatState.queue_position}"),
        rx.el.button(
            "Cancel Request",
            on_click=PeerChatState.cancel_request,
            class_name="mt-6 bg-red-500 text-white font-semibold py-2 px-4 rounded-lg hover:bg-red-600",
        ),
        class_name="flex flex-col items-center justify-center h-full p-6 text-center",
    )


def chat_interface():
    return rx.el.div(
        rx.el.h1("Peer Chat", class_name="text-3xl font-bold text-gray-800 mb-4"),
        rx.el.div(
            rx.foreach(
                PeerChatState.current_chat_messages,
                lambda msg: rx.el.div(
                    rx.el.p(msg["message"], class_name="text-sm"),
                    class_name=rx.cond(
                        msg["pseudonym"] == AuthState.current_user_data["pseudonym"],
                        "bg-blue-500 text-white p-3 rounded-lg self-end max-w-md",
                        "bg-gray-200 text-gray-800 p-3 rounded-lg self-start max-w-md",
                    ),
                ),
            ),
            class_name="flex flex-col gap-4 p-4 h-[60vh] overflow-y-auto border rounded-lg bg-white mb-4",
            id="chat-box",
            on_mount=rx.call_script(
                "document.getElementById('chat-box').scrollTop = document.getElementById('chat-box').scrollHeight"
            ),
        ),
        rx.el.form(
            rx.el.input(
                name="message",
                placeholder="Type your message...",
                class_name="flex-grow p-2 border rounded-l-lg",
            ),
            rx.el.button(
                "Send",
                type="submit",
                class_name="bg-blue-500 text-white font-semibold px-4 py-2 rounded-r-lg",
            ),
            on_submit=PeerChatState.send_peer_message,
            reset_on_submit=True,
            class_name="flex w-full",
        ),
        rx.el.button(
            "Leave Chat",
            on_click=PeerChatState.leave_chat,
            class_name="mt-4 bg-red-500 text-white font-semibold py-2 px-4 rounded-lg hover:bg-red-600 w-full",
        ),
        class_name="h-full flex flex-col p-6",
    )


def idle_view():
    return rx.el.div(
        rx.el.h2("Talk to a Peer", class_name="text-2xl font-bold"),
        rx.el.p(
            "Connect anonymously with another member of the community for support.",
            class_name="text-gray-600 mt-2 max-w-md",
        ),
        rx.el.button(
            "Request Support",
            on_click=PeerChatState.request_support,
            class_name="mt-8 bg-blue-500 text-white font-bold py-3 px-6 rounded-lg hover:bg-blue-600 text-lg",
        ),
        class_name="flex flex-col items-center justify-center h-full p-6 text-center",
    )


def peer_chat():
    return rx.el.div(
        sidebar(),
        rx.el.main(
            header(),
            rx.el.div(
                rx.match(
                    PeerChatState.queue_status,
                    ("idle", idle_view()),
                    ("waiting", waiting_view()),
                    ("matched", chat_interface()),
                    rx.el.div("Loading..."),
                ),
                class_name="flex-1",
            ),
            class_name=rx.cond(
                DashboardState.sidebar_open,
                "transition-all ml-0 md:ml-64 flex flex-col h-screen",
                "transition-all ml-0 md:ml-16 flex flex-col h-screen",
            ),
        ),
        class_name="font-['Inter'] bg-gray-50 min-h-screen text-gray-800",
        on_mount=rx.cond(PeerChatState.in_chat, PeerChatState.poll_messages, rx.noop()),
    )