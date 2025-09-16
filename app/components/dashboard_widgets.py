import reflex as rx
from app.states.auth_state import AuthState
from app.states.dashboard_state import DashboardState


def quick_action_button(icon: str, text: str, color: str, href: str | None = None):
    button_content = rx.fragment(
        rx.icon(icon, class_name="w-6 h-6"),
        rx.el.span(text, class_name="font-semibold"),
    )
    button = rx.el.button(
        button_content,
        class_name=f"flex flex-col items-center justify-center gap-2 p-4 rounded-xl {color} text-white transition-transform hover:scale-105",
    )
    if href:
        return rx.el.a(button, href=href)
    return button


def quick_actions_widget():
    return rx.el.div(
        rx.el.h2("Quick Actions", class_name="text-lg font-bold mb-4"),
        rx.el.div(
            quick_action_button(
                "messages-square", "Peer Chat", "bg-blue-500", href="/peer-chat"
            ),
            quick_action_button(
                "bot", "Chat with AI", "bg-purple-500", href="/ai-chat"
            ),
            quick_action_button(
                "user-plus", "Request Therapist", "bg-green-500", href="/reports"
            ),
            class_name="grid grid-cols-3 gap-4",
        ),
        class_name="p-6 bg-white rounded-xl border border-gray-200 shadow-sm md:col-span-2 lg:col-span-1",
    )


def user_status_widget():
    return rx.el.div(
        rx.el.h2("Your Status", class_name="text-lg font-bold mb-4"),
        rx.cond(
            AuthState.current_user_data,
            rx.el.div(
                rx.el.div(
                    rx.el.p("Pseudonym", class_name="text-sm text-gray-500"),
                    rx.el.p(
                        AuthState.current_user_data.get("pseudonym", "N/A"),
                        class_name="text-xl font-bold",
                    ),
                ),
                rx.el.div(
                    rx.el.p("Subscription", class_name="text-sm text-gray-500"),
                    rx.el.div(
                        AuthState.current_user_data.get("subscription_plan", "N/A"),
                        class_name="px-2 py-1 bg-yellow-200 text-yellow-800 text-xs font-semibold rounded-full w-fit",
                    ),
                ),
                rx.el.div(
                    rx.el.p("Status", class_name="text-sm text-gray-500"),
                    rx.el.div(
                        AuthState.current_user_data.get(
                            "subscription_status", "N/A"
                        ).capitalize(),
                        class_name=rx.cond(
                            AuthState.current_user_data.get("subscription_status")
                            == "active",
                            "px-2 py-1 bg-green-200 text-green-800 text-xs font-semibold rounded-full w-fit",
                            "px-2 py-1 bg-gray-200 text-gray-800 text-xs font-semibold rounded-full w-fit",
                        ),
                    ),
                ),
                class_name="space-y-4",
            ),
            rx.el.div("Loading user data..."),
        ),
        class_name="p-6 bg-white rounded-xl border border-gray-200 shadow-sm",
    )


def mental_health_tip_widget():
    return rx.el.div(
        rx.el.h2("Tip of the Day", class_name="text-lg font-bold mb-4 text-white"),
        rx.el.p(DashboardState.current_tip, class_name="text-white/90"),
        class_name="p-6 bg-teal-500 rounded-xl border border-teal-600 shadow-sm",
    )