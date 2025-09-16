import reflex as rx
from typing import TypedDict
import datetime
from app.states.auth_state import AuthState
from app.database import (
    get_db,
    DistressLog,
    Report,
    TherapistRequest,
    User,
    Profile,
    Subscription,
)


class AdminDashboardState(rx.State):
    selected_tab: str = "Distress Reports"
    distress_logs: list[dict] = []
    user_reports: list[dict] = []
    therapist_requests: list[dict] = []
    all_users: list[dict] = []
    user_search: str = ""

    @rx.event
    def set_selected_tab(self, tab_name: str):
        self.selected_tab = tab_name
        return AdminDashboardState.load_data

    @rx.event(background=True)
    async def load_data(self):
        with get_db() as db:
            if self.selected_tab == "Distress Reports":
                logs = (
                    db.query(DistressLog).order_by(DistressLog.timestamp.desc()).all()
                )
                async with self:
                    self.distress_logs = [log.__dict__ for log in logs]
            elif self.selected_tab == "User Reports":
                reports = db.query(Report).order_by(Report.timestamp.desc()).all()
                async with self:
                    self.user_reports = [report.__dict__ for report in reports]
            elif self.selected_tab == "Therapist Requests":
                requests = (
                    db.query(TherapistRequest)
                    .order_by(TherapistRequest.timestamp.desc())
                    .all()
                )
                async with self:
                    self.therapist_requests = [req.__dict__ for req in requests]
            elif self.selected_tab == "User Overview":
                query = db.query(User).join(Profile).join(Subscription)
                if self.user_search:
                    query = query.filter(Profile.pseudonym.contains(self.user_search))
                users = query.order_by(User.created_at.desc()).all()
                user_list = []
                for user in users:
                    user_list.append(
                        {
                            "id": user.id,
                            "pseudonym": user.profile.pseudonym,
                            "subscription_plan": user.subscription.plan_type,
                            "status": user.subscription.status,
                            "join_date": user.created_at.isoformat(),
                            "last_active": "N/A",
                        }
                    )
                async with self:
                    self.all_users = user_list
        yield

    @rx.event
    def set_user_search(self, search: str):
        self.user_search = search
        return AdminDashboardState.load_data

    @rx.event
    def update_distress_status(self, log_id: int, new_status: str):
        with get_db() as db:
            log = db.query(DistressLog).filter(DistressLog.id == log_id).first()
            if log:
                log.status = new_status
                db.commit()
        return AdminDashboardState.load_data

    @rx.event
    def update_report_status(self, report_id: int, new_status: str):
        with get_db() as db:
            report = db.query(Report).filter(Report.id == report_id).first()
            if report:
                report.status = new_status
                db.commit()
        return AdminDashboardState.load_data

    @rx.event
    def update_therapist_request_status(self, request_id: int, new_status: str):
        with get_db() as db:
            req = (
                db.query(TherapistRequest)
                .filter(TherapistRequest.id == request_id)
                .first()
            )
            if req:
                req.status = new_status
                db.commit()
        return AdminDashboardState.load_data