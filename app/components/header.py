import reflex as rx
from app.states.auth_state import AuthState
from app.states.dashboard_state import DashboardState


def header():
    return rx.el.header(
        rx.el.button(
            rx.icon("menu", class_name="w-6 h-6"),
            on_click=DashboardState.toggle_sidebar,
            class_name="p-2 rounded-md hover:bg-gray-100 md:hidden",
        ),
        rx.el.p(f"Hi, {AuthState.logged_in_user} 👋", class_name="font-semibold"),
        rx.el.div(
            rx.el.select(
                rx.foreach(
                    DashboardState.languages,
                    lambda lang: rx.el.option(lang, value=lang),
                ),
                value=AuthState.language,
                on_change=AuthState.set_language,
                class_name="flex h-10 w-full items-center justify-between rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background placeholder:text-muted-foreground focus:outline-none focus:ring-2 focus:ring-ring focus:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50",
            ),
            class_name="flex items-center gap-4",
        ),
        class_name="sticky top-0 z-10 flex items-center justify-between bg-white/80 backdrop-blur-sm p-4 border-b",
    )