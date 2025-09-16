import reflex as rx
from app.states.distress_state import DistressState
from app.states.dashboard_state import DashboardState


def distress_button():
    return rx.el.button(
        rx.icon("life-buoy", class_name="w-5 h-5"),
        rx.el.span(
            "Ask for Help",
            class_name=rx.cond(DashboardState.sidebar_open, "", "hidden"),
        ),
        on_click=DistressState.trigger_alert,
        class_name="flex items-center justify-center gap-3 rounded-lg bg-red-500 px-3 py-2 text-white font-semibold transition-all hover:bg-red-600",
    )