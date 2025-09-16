import reflex as rx
from app.states.auth_state import AuthState
from app.database import (
    get_db,
    Report as ReportModel,
    TherapistRequest as TherapistRequestModel,
)


class ReportState(rx.State):
    @rx.event
    async def submit_user_report(self, form_data: dict):
        auth_state = await self.get_state(AuthState)
        if not auth_state.is_authenticated:
            return rx.toast.error("You must be logged in to submit a report.")
        if not all(
            (form_data.get(key) for key in ["reported_pseudonym", "reason", "details"])
        ):
            return rx.toast.error("All fields are required.")
        reporter_pseudonym = auth_state.current_user_data.get("pseudonym")
        if not reporter_pseudonym:
            return rx.toast.error(
                "Could not identify reporter. Please complete your profile."
            )
        with get_db() as db:
            new_report = ReportModel(
                reporter_pseudonym=reporter_pseudonym,
                reported_pseudonym=form_data["reported_pseudonym"],
                reason=form_data["reason"],
                details=form_data["details"],
            )
            db.add(new_report)
            db.commit()
        return rx.toast.success(
            "Report submitted successfully. Our team will review it shortly."
        )

    @rx.event
    async def submit_therapist_request(self, form_data: dict):
        auth_state = await self.get_state(AuthState)
        if not auth_state.is_authenticated or not auth_state.logged_in_user_id:
            return rx.toast.error("You must be logged in to request a therapist.")
        if not all((form_data.get(key) for key in ["urgency", "details"])):
            return rx.toast.error("All fields are required.")
        pseudonym = auth_state.current_user_data.get("pseudonym")
        with get_db() as db:
            new_request = TherapistRequestModel(
                user_id=auth_state.logged_in_user_id,
                pseudonym=pseudonym,
                urgency=form_data["urgency"],
                details=form_data["details"],
            )
            db.add(new_request)
            db.commit()
        return rx.toast.success(
            "Request for a therapist submitted. We will be in touch soon."
        )