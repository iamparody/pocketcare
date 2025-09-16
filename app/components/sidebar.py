import reflex as rx
from app.states.auth_state import AuthState
from app.models.user import UserProfile
from app.states.dashboard_state import DashboardState
from app.components.distress_button import distress_button


def sidebar_link(icon: str, text: str, href: str, is_active: bool):
    return rx.el.a(
        rx.icon(icon, class_name="w-5 h-5"),
        rx.el.span(
            text, class_name=rx.cond(DashboardState.sidebar_open, None, "hidden")
        ),
        href=href,
        class_name=rx.cond(
            is_active,
            "flex items-center gap-3 rounded-lg bg-blue-100 px-3 py-2 text-blue-600 transition-all hover:text-blue-600",
            "flex items-center gap-3 rounded-lg px-3 py-2 text-gray-500 transition-all hover:text-gray-900",
        ),
    )


def sidebar():
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.icon("sun-moon", class_name="h-8 w-8 text-blue-600"),
                rx.el.h1(
                    "Serenity",
                    class_name=rx.cond(
                        DashboardState.sidebar_open, "text-xl font-bold", "hidden"
                    ),
                ),
                class_name="flex items-center gap-2 font-semibold",
            ),
            rx.el.nav(
                sidebar_link("layout-dashboard", "Dashboard", "/", False),
                sidebar_link("user", "Profile", "/profile", False),
                sidebar_link("book-marked", "Journaling", "/journaling", False),
                sidebar_link("gem", "Subscription", "/subscription", False),
                sidebar_link("messages-square", "Peer Chat", "/peer-chat", False),
                sidebar_link("flag", "Report/Request", "/reports", False),
                class_name="grid items-start gap-1",
            ),
            class_name="flex flex-col gap-4",
        ),
        rx.el.div(
            distress_button(),
            rx.el.button(
                rx.icon("log-out", class_name="w-5 h-5"),
                rx.el.span(
                    "Sign Out",
                    class_name=rx.cond(DashboardState.sidebar_open, None, "hidden"),
                ),
                on_click=AuthState.sign_out,
                class_name="flex items-center gap-3 rounded-lg px-3 py-2 text-gray-500 transition-all hover:text-gray-900",
            ),
            class_name="mt-auto flex flex-col gap-4",
        ),
        class_name=rx.cond(
            DashboardState.sidebar_open,
            "fixed inset-y-0 left-0 z-10 flex w-64 flex-col border-r bg-white p-4 transition-all",
            "fixed inset-y-0 left-0 z-10 flex w-16 flex-col items-center border-r bg-white p-4 transition-all",
        ),
    )