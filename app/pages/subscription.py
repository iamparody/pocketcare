import reflex as rx
from app.states.subscription_state import SubscriptionState
from app.states.auth_state import AuthState
from app.components.sidebar import sidebar
from app.components.header import header
from app.states.dashboard_state import DashboardState


def feature_item(text: str):
    return rx.el.li(
        rx.icon("check", class_name="w-5 h-5 text-green-500"),
        rx.el.span(text, class_name="text-gray-600"),
        class_name="flex items-center gap-3",
    )


def plan_card(
    plan_name: str, price: str, features: list[str], is_current: bool, plan_type: str
):
    return rx.el.div(
        rx.el.h3(plan_name, class_name="text-xl font-bold"),
        rx.el.p(
            rx.el.span(f"${price}", class_name="text-4xl font-bold"),
            " / month",
            class_name="text-gray-800",
        ),
        rx.el.ul(rx.foreach(features, feature_item), class_name="space-y-3 mt-6 mb-8"),
        rx.el.button(
            rx.cond(is_current, "Current Plan", f"Switch to {plan_name}"),
            on_click=lambda: SubscriptionState.change_plan(plan_type),
            disabled=is_current,
            class_name="w-full py-2 px-4 rounded-lg font-semibold text-white transition-colors "
            + rx.cond(
                is_current,
                "bg-gray-400 cursor-not-allowed",
                "bg-blue-500 hover:bg-blue-600",
            ),
        ),
        class_name="p-6 bg-white rounded-xl border border-gray-200 shadow-sm w-full",
    )


def payment_history_table():
    return rx.el.div(
        rx.el.h2("Payment History", class_name="text-2xl font-bold mb-4"),
        rx.el.div(
            rx.el.table(
                rx.el.thead(
                    rx.el.tr(
                        rx.el.th("Date"),
                        rx.el.th("Amount"),
                        rx.el.th("Plan"),
                        rx.el.th("Status"),
                    )
                ),
                rx.el.tbody(
                    rx.foreach(
                        SubscriptionState.payment_history,
                        lambda payment: rx.el.tr(
                            rx.el.td(payment["date"]),
                            rx.el.td(f"${payment['amount']:.2f}"),
                            rx.el.td(payment["plan"]),
                            rx.el.td(
                                rx.el.span(
                                    payment["status"],
                                    class_name=rx.cond(
                                        payment["status"] == "Paid",
                                        "px-2 py-1 bg-green-100 text-green-800 text-xs font-semibold rounded-full",
                                        "px-2 py-1 bg-red-100 text-red-800 text-xs font-semibold rounded-full",
                                    ),
                                )
                            ),
                        ),
                    )
                ),
                class_name="w-full text-left border-collapse",
            ),
            class_name="overflow-x-auto",
        ),
        class_name="p-6 bg-white rounded-xl border border-gray-200 shadow-sm mt-8",
    )


def subscription():
    return rx.el.div(
        sidebar(),
        rx.el.main(
            header(),
            rx.el.div(
                rx.el.h1(
                    "Subscription & Billing",
                    class_name="text-3xl font-bold text-gray-800",
                ),
                rx.el.p(
                    "Manage your plan and see your payment history.",
                    class_name="text-gray-500 mt-1 mb-6",
                ),
                rx.el.div(
                    rx.el.h2("Current Plan", class_name="text-2xl font-bold mb-4"),
                    rx.cond(
                        AuthState.current_user_data,
                        rx.el.div(
                            rx.el.p(
                                rx.el.span(
                                    AuthState.current_user_data["subscription_plan"],
                                    class_name="font-semibold text-lg",
                                ),
                                rx.el.span(
                                    AuthState.current_user_data[
                                        "subscription_status"
                                    ].capitalize(),
                                    class_name=rx.cond(
                                        AuthState.current_user_data[
                                            "subscription_status"
                                        ]
                                        == "active",
                                        "ml-3 px-2 py-1 bg-green-100 text-green-800 text-xs font-semibold rounded-full",
                                        "ml-3 px-2 py-1 bg-gray-200 text-gray-800 text-xs font-semibold rounded-full",
                                    ),
                                ),
                            ),
                            class_name="p-6 bg-white rounded-xl border border-gray-200 shadow-sm",
                        ),
                        rx.el.p("Loading..."),
                    ),
                ),
                rx.el.div(
                    plan_card(
                        "Basic",
                        "6.99",
                        ["Unlimited AI Chat", "Priority Peer Matching"],
                        AuthState.current_user_data["subscription_plan"] == "Basic",
                        "Basic",
                    ),
                    plan_card(
                        "Plus",
                        "9.99",
                        [
                            "Everything in Basic",
                            "Therapist Booking Discounts",
                            "AI Journaling Assistant",
                        ],
                        AuthState.current_user_data["subscription_plan"] == "Plus",
                        "Plus",
                    ),
                    class_name="grid md:grid-cols-2 gap-8 mt-8",
                ),
                payment_history_table(),
                class_name="p-6",
            ),
            class_name=rx.cond(
                DashboardState.sidebar_open,
                "transition-all ml-0 md:ml-64",
                "transition-all ml-0 md:ml-16",
            ),
        ),
        class_name="font-['Inter'] bg-gray-50 min-h-screen text-gray-800",
        on_mount=SubscriptionState.load_history,
    )