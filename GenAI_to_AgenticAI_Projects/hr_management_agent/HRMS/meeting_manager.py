from collections import defaultdict
from typing import TYPE_CHECKING, TypedDict

if TYPE_CHECKING:
    from .schemas import MeetingCancelRequest, MeetingCreate
elif __package__:
    from .schemas import MeetingCancelRequest, MeetingCreate
else:
    from schemas import MeetingCancelRequest, MeetingCreate


class MeetingRecord(TypedDict):
    date: str
    topic: str


class MeetingManager:
    def __init__(self) -> None:
        self.meetings: defaultdict[str, list[MeetingRecord]] = defaultdict(list)

    def schedule_meeting(self, req: MeetingCreate) -> str:
        dt_str = req.meeting_dt.isoformat()
        emp_id = req.emp_id
        if any(m["date"] == dt_str for m in self.meetings[emp_id]):
            raise ValueError(f"Conflict: {emp_id} already has a meeting at {dt_str}.")
        self.meetings[emp_id].append({"date": dt_str, "topic": req.topic})
        return f"Meeting scheduled for {emp_id} on {dt_str} about '{req.topic}'."

    def get_meetings(self, employee_id: str) -> list[MeetingRecord]:
        return sorted(self.meetings.get(employee_id, []), key=lambda m: m["date"])

    def cancel_meeting(self, req: MeetingCancelRequest) -> str:
        emp_id = req.emp_id
        dt_str = req.meeting_dt.isoformat()
        original = list(self.meetings.get(emp_id, []))
        self.meetings[emp_id] = [m for m in original if not (
            m["date"] == dt_str and (req.topic is None or m["topic"] == req.topic)
        )]
        if len(self.meetings[emp_id]) == len(original):
            raise ValueError("No matching meeting to cancel.")
        return f"Canceled meeting for {emp_id} on {dt_str}{f' about {req.topic}' if req.topic else ''}."