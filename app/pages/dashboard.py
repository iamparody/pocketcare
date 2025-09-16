import reflex as rx
from app.states.dashboard_state import DashboardState
from app.components.sidebar import sidebar
from app.components.header import header
from app.components.dashboard_widgets import (
    quick_actions_widget,
    user_status_widget,
    mental_health_tip_widget,
)


def dashboard():
    return rx.el.div(
        sidebar(),
        rx.el.main(
            header(),
            rx.el.div(
                rx.el.div(
                    quick_actions_widget(),
                    user_status_widget(),
                    mental_health_tip_widget(),
                    class_name="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 p-6",
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