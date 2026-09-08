from collections import defaultdict
from datetime import date
from typing import TYPE_CHECKING, TypedDict

if TYPE_CHECKING:
    from .schemas import LeaveApplyRequest
elif __package__:
    from .schemas import LeaveApplyRequest
else:
    from schemas import LeaveApplyRequest


class LeaveHistoryRecord(TypedDict):
    history_id: int
    emp_id: str
    leave_date: date
    request_id: int


class LeaveRecord(TypedDict):
    balance: int
    history: list[LeaveHistoryRecord]


class LeaveManager:
    def __init__(self) -> None:
        self.employee_leaves: defaultdict[str, LeaveRecord] = defaultdict(
            lambda: {"balance": 20, "history": []}
        )

    def add_employee(self, employee_id: str) -> None:
        if employee_id in self.employee_leaves:
            raise ValueError(f"Employee ID '{employee_id}' already exists.")
        self.employee_leaves[employee_id] = {"balance": 20, "history": []}

    def get_leave_balance(self, employee_id: str) -> str:
        data = self.employee_leaves.get(employee_id)
        if data:
            return f"{employee_id} has {data['balance']} leave days remaining."
        return "Employee ID not found."

    def apply_leave(self, req: LeaveApplyRequest) -> str:
        employee_id = req.emp_id
        if employee_id not in self.employee_leaves:
            return "Employee ID not found."
        requested = len(req.leave_dates)
        leave_record = self.employee_leaves[employee_id]
        available = leave_record["balance"]
        if available < requested:
            return f"Insufficient leave balance: requested {requested}, available {available}."
        all_history = [
            history
            for record in self.employee_leaves.values()
            for history in record["history"]
        ]
        request_id = max((history["request_id"] for history in all_history), default=0) + 1
        next_history_id = max(
            (history["history_id"] for history in leave_record["history"]),
            default=0,
        ) + 1
        leave_record["balance"] -= requested
        leave_record["history"].extend(
            {
                "history_id": next_history_id + index,
                "emp_id": employee_id,
                "leave_date": leave_date,
                "request_id": request_id,
            }
            for index, leave_date in enumerate(req.leave_dates)
        )
        return (f"Leave applied for {requested} day(s). Remaining balance: "
                f"{leave_record['balance']}")

    def get_leave_history(self, employee_id: str) -> str:
        data = self.employee_leaves.get(employee_id)
        if data:
            dates = [
                history["leave_date"].strftime("%B %d, %Y")
                for history in data["history"]
            ]
            return f"Leave history for {employee_id}: {', '.join(dates)}."
        return "Employee ID not found."


if __name__ == "__main__":
    lm = LeaveManager()
    lm.add_employee("E004")
    print(lm.get_leave_balance("E004"))