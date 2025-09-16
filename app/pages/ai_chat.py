import reflex as rx
from app.states.chat_state import ChatState, ChatMessage
from app.states.dashboard_state import DashboardState
from app.components.sidebar import sidebar
from app.components.header import header


def message_bubble(message: ChatMessage):
    return rx.el.div(
        rx.el.p(message.message),
        class_name=rx.cond(
            message.role == "user",
            "bg-blue-500 text-white self-end",
            "bg-gray-200 text-gray-800 self-start",
        ),
        style={
            "border_radius": "1rem",
            "padding": "0.5rem 1rem",
            "max_width": "70%",
            "margin_bottom": "0.5rem",
        },
    )


def ai_chat():
    return rx.el.div(
        sidebar(),
        rx.el.main(
            header(),
            rx.el.div(
                rx.el.div(
                    rx.el.h1(
                        "Chat with Serenity AI", class_name="text-2xl font-bold mb-4"
                    ),
                    rx.el.div(
                        rx.foreach(ChatState.current_chat, message_bubble),
                        class_name="flex flex-col gap-2 p-4 h-[70vh] overflow-y-auto border rounded-lg bg-white",
                    ),
                    rx.el.form(
                        rx.el.input(
                            name="user_message",
                            placeholder="Type your message...",
                            class_name="flex-grow h-10 w-full rounded-md border bg-transparent px-3 py-2 text-sm shadow-sm transition-colors focus-visible:outline-none focus-visible:ring-1",
                            key=ChatState.current_user_message,
                        ),
                        rx.el.button(
                            rx.icon("send", class_name="w-5 h-5"),
                            type="submit",
                            class_name="inline-flex items-center justify-center whitespace-nowrap rounded-md text-sm font-medium transition-colors text-white shadow bg-blue-500 hover:bg-blue-600 h-10 px-4 py-2",
                        ),
                        on_submit=ChatState.send_message,
                        reset_on_submit=True,
                        class_name="flex items-center gap-2 mt-4",
                    ),
                    class_name="p-6",
                ),
                class_name="flex-1 overflow-y-auto",
            ),
            class_name=rx.cond(
                DashboardState.sidebar_open,
                "transition-all ml-0 md:ml-64",
                "transition-all ml-0 md:ml-16",
            ),
        ),
        class_name="font-['Inter'] bg-gray-50 min-h-screen text-gray-800",
    )