import reflex as rx
from app.states.report_state import ReportState
from app.components.sidebar import sidebar
from app.components.header import header
from app.states.dashboard_state import DashboardState


def reports():
    return rx.el.div(
        sidebar(),
        rx.el.main(
            header(),
            rx.el.div(
                rx.el.h1(
                    "Report Misconduct or Request a Therapist",
                    class_name="text-3xl font-bold text-gray-800",
                ),
                rx.el.p(
                    "Your feedback is confidential and helps us maintain a safe community.",
                    class_name="text-gray-500 mt-1 mb-8",
                ),
                rx.el.div(
                    rx.el.div(
                        rx.el.h2(
                            "Report Misconduct", class_name="text-2xl font-bold mb-4"
                        ),
                        rx.el.form(
                            rx.el.div(
                                rx.el.label(
                                    "User Pseudonym You Are Reporting",
                                    class_name="text-sm font-medium",
                                ),
                                rx.el.input(
                                    name="reported_pseudonym",
                                    placeholder="e.g. AngryPanda23",
                                    required=True,
                                    class_name="w-full mt-1 p-2 border rounded-md",
                                ),
                                class_name="mb-4",
                            ),
                            rx.el.div(
                                rx.el.label(
                                    "Reason for Report",
                                    class_name="text-sm font-medium",
                                ),
                                rx.el.select(
                                    "Harassment",
                                    "Spam",
                                    "Inappropriate Content",
                                    "Other",
                                    name="reason",
                                    placeholder="Select a reason",
                                    required=True,
                                    class_name="w-full mt-1 p-2 border rounded-md",
                                ),
                                class_name="mb-4",
                            ),
                            rx.el.div(
                                rx.el.label(
                                    "Details", class_name="text-sm font-medium"
                                ),
                                rx.el.textarea(
                                    name="details",
                                    placeholder="Provide as much detail as possible...",
                                    required=True,
                                    class_name="w-full mt-1 p-2 border rounded-md h-24",
                                ),
                                class_name="mb-6",
                            ),
                            rx.el.button(
                                "Submit Report",
                                type="submit",
                                class_name="w-full bg-red-500 text-white font-semibold py-2 px-4 rounded-lg hover:bg-red-600",
                            ),
                            on_submit=ReportState.submit_user_report,
                            reset_on_submit=True,
                        ),
                        class_name="p-6 bg-white rounded-xl border shadow-sm",
                    ),
                    rx.el.div(
                        rx.el.h2(
                            "Request a Therapist", class_name="text-2xl font-bold mb-4"
                        ),
                        rx.el.form(
                            rx.el.div(
                                rx.el.label(
                                    "Urgency", class_name="text-sm font-medium"
                                ),
                                rx.el.select(
                                    "Low",
                                    "Medium",
                                    "High",
                                    name="urgency",
                                    placeholder="Select urgency level",
                                    required=True,
                                    class_name="w-full mt-1 p-2 border rounded-md",
                                ),
                                class_name="mb-4",
                            ),
                            rx.el.div(
                                rx.el.label(
                                    "Details of Your Request",
                                    class_name="text-sm font-medium",
                                ),
                                rx.el.textarea(
                                    name="details",
                                    placeholder="Briefly describe what you'd like to talk about...",
                                    required=True,
                                    class_name="w-full mt-1 p-2 border rounded-md h-32",
                                ),
                                class_name="mb-6",
                            ),
                            rx.el.button(
                                "Request Therapist",
                                type="submit",
                                class_name="w-full bg-blue-500 text-white font-semibold py-2 px-4 rounded-lg hover:bg-blue-600",
                            ),
                            on_submit=ReportState.submit_therapist_request,
                            reset_on_submit=True,
                        ),
                        class_name="p-6 bg-white rounded-xl border shadow-sm",
                    ),
                    class_name="grid md:grid-cols-2 gap-8",
                ),
                class_name="p-6",
            ),
            class_name=rx.cond(
                DashboardState.sidebar_open,
                "transition-all ml-0 md:ml-64",
                "transition-all ml-0 md:ml-16",
            ),
        ),
        class_name="font-['Inter'] bg-gray-50 min-h-screen text-gray-800",
    )