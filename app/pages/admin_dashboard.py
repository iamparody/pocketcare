import reflex as rx
from app.states.admin_dashboard_state import AdminDashboardState
from app.states.auth_state import AuthState


def admin_sidebar_link(icon: str, text: str, is_active: bool):
    return rx.el.button(
        rx.icon(icon, class_name="w-5 h-5"),
        rx.el.span(text),
        on_click=lambda: AdminDashboardState.set_selected_tab(text),
        class_name=rx.cond(
            is_active,
            "flex items-center gap-3 rounded-lg bg-blue-100 px-3 py-2 text-blue-600 transition-all hover:text-blue-600 w-full text-left",
            "flex items-center gap-3 rounded-lg px-3 py-2 text-gray-700 transition-all hover:text-gray-900 hover:bg-gray-100 w-full text-left",
        ),
    )


def admin_sidebar():
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.icon("shield-check", class_name="h-8 w-8 text-blue-600"),
                rx.el.h1("Admin Panel", class_name="text-xl font-bold"),
                class_name="flex items-center gap-2 font-semibold",
            ),
            rx.el.nav(
                admin_sidebar_link(
                    "siren",
                    "Distress Reports",
                    AdminDashboardState.selected_tab == "Distress Reports",
                ),
                admin_sidebar_link(
                    "file-warning",
                    "User Reports",
                    AdminDashboardState.selected_tab == "User Reports",
                ),
                admin_sidebar_link(
                    "user-plus",
                    "Therapist Requests",
                    AdminDashboardState.selected_tab == "Therapist Requests",
                ),
                admin_sidebar_link(
                    "users",
                    "User Overview",
                    AdminDashboardState.selected_tab == "User Overview",
                ),
                class_name="grid items-start gap-1 mt-6",
            ),
            class_name="flex flex-col gap-4",
        ),
        rx.el.button(
            rx.icon("log-out", class_name="w-5 h-5"),
            rx.el.span("Sign Out"),
            on_click=AuthState.sign_out,
            class_name="mt-auto flex items-center gap-3 rounded-lg px-3 py-2 text-gray-500 transition-all hover:text-gray-900",
        ),
        class_name="fixed inset-y-0 left-0 z-10 flex w-64 flex-col border-r bg-white p-4 transition-all",
    )


def distress_reports_panel():
    return rx.el.div(
        rx.el.h2("Distress Reports", class_name="text-2xl font-bold mb-6"),
        rx.el.table(
            rx.el.thead(
                rx.el.tr(
                    rx.el.th("Pseudonym"),
                    rx.el.th("Timestamp"),
                    rx.el.th("Severity"),
                    rx.el.th("Details"),
                    rx.el.th("Status"),
                    rx.el.th("Actions"),
                )
            ),
            rx.el.tbody(
                rx.foreach(
                    AdminDashboardState.distress_logs,
                    lambda log: rx.el.tr(
                        rx.el.td(log["pseudonym"]),
                        rx.el.td(log["timestamp"].to_string()),
                        rx.el.td(log["severity"]),
                        rx.el.td(log["details"]),
                        rx.el.td(log["status"]),
                        rx.el.td(
                            rx.el.button(
                                "Mark Reviewed",
                                on_click=lambda: AdminDashboardState.update_distress_status(
                                    log["id"], "reviewed"
                                ),
                            )
                        ),
                    ),
                )
            ),
            class_name="w-full text-left border-collapse",
        ),
        class_name="p-6",
    )


def user_reports_panel():
    return rx.el.div(
        rx.el.h2("User Reports", class_name="text-2xl font-bold mb-6"),
        rx.el.table(
            rx.el.thead(
                rx.el.tr(
                    rx.el.th("Reporter"),
                    rx.el.th("Reported"),
                    rx.el.th("Reason"),
                    rx.el.th("Details"),
                    rx.el.th("Timestamp"),
                    rx.el.th("Status"),
                    rx.el.th("Actions"),
                )
            ),
            rx.el.tbody(
                rx.foreach(
                    AdminDashboardState.user_reports,
                    lambda report: rx.el.tr(
                        rx.el.td(report["reporter_pseudonym"]),
                        rx.el.td(report["reported_pseudonym"]),
                        rx.el.td(report["reason"]),
                        rx.el.td(report["details"]),
                        rx.el.td(report["timestamp"].to_string()),
                        rx.el.td(report["status"]),
                        rx.el.td(
                            rx.el.select(
                                rx.el.option("Pending", value="pending"),
                                rx.el.option("Resolved", value="resolved"),
                                default_value=report["status"],
                                on_change=lambda new_status: AdminDashboardState.update_report_status(
                                    report["id"], new_status
                                ),
                            )
                        ),
                    ),
                )
            ),
            class_name="w-full text-left border-collapse",
        ),
        class_name="p-6",
    )


def therapist_requests_panel():
    return rx.el.div(
        rx.el.h2("Therapist Requests", class_name="text-2xl font-bold mb-6"),
        rx.el.table(
            rx.el.thead(
                rx.el.tr(
                    rx.el.th("Pseudonym"),
                    rx.el.th("Details"),
                    rx.el.th("Urgency"),
                    rx.el.th("Timestamp"),
                    rx.el.th("Status"),
                    rx.el.th("Actions"),
                )
            ),
            rx.el.tbody(
                rx.foreach(
                    AdminDashboardState.therapist_requests,
                    lambda req: rx.el.tr(
                        rx.el.td(req["pseudonym"]),
                        rx.el.td(req["details"]),
                        rx.el.td(req["urgency"]),
                        rx.el.td(req["timestamp"].to_string()),
                        rx.el.td(req["status"]),
                        rx.el.td(
                            rx.el.select(
                                rx.el.option("Pending", value="pending"),
                                rx.el.option("Assigned", value="assigned"),
                                rx.el.option("Completed", value="completed"),
                                default_value=req["status"],
                                on_change=lambda new_status: AdminDashboardState.update_therapist_request_status(
                                    req["id"], new_status
                                ),
                            )
                        ),
                    ),
                )
            ),
            class_name="w-full text-left border-collapse",
        ),
        class_name="p-6",
    )


def user_overview_panel():
    return rx.el.div(
        rx.el.h2("User Overview", class_name="text-2xl font-bold mb-6"),
        rx.el.input(
            placeholder="Search by pseudonym...",
            on_change=AdminDashboardState.set_user_search,
            class_name="mb-4 p-2 border rounded-md",
        ),
        rx.el.table(
            rx.el.thead(
                rx.el.tr(
                    rx.el.th("Pseudonym"),
                    rx.el.th("Subscription Plan"),
                    rx.el.th("Status"),
                    rx.el.th("Join Date"),
                    rx.el.th("Last Active"),
                )
            ),
            rx.el.tbody(
                rx.foreach(
                    AdminDashboardState.all_users,
                    lambda user: rx.el.tr(
                        rx.el.td(user["pseudonym"]),
                        rx.el.td(user["subscription_plan"]),
                        rx.el.td(user["status"]),
                        rx.el.td(user["join_date"]),
                        rx.el.td(user["last_active"]),
                    ),
                )
            ),
            class_name="w-full text-left border-collapse",
        ),
        class_name="p-6",
    )


def admin_dashboard():
    return rx.el.div(
        admin_sidebar(),
        rx.el.main(
            rx.match(
                AdminDashboardState.selected_tab,
                ("Distress Reports", distress_reports_panel()),
                ("User Reports", user_reports_panel()),
                ("Therapist Requests", therapist_requests_panel()),
                ("User Overview", user_overview_panel()),
                rx.el.div("Select a tab"),
            ),
            class_name="ml-64",
        ),
        class_name="font-['Inter'] bg-gray-50 min-h-screen text-gray-800",
        on_mount=AdminDashboardState.load_data,
    )