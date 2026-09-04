"""MCP server for managing employee leave requests and balances."""

from dataclasses import dataclass
from datetime import date, timedelta
from itertools import count
import json
from typing import Literal

from mcp.server import MCPServer

LeaveType = Literal["annual", "sick", "personal"]
RequestStatus = Literal["pending", "approved", "rejected", "cancelled"]


@dataclass(frozen=True)
class Employee:
    """An employee and their yearly leave allowances."""

    employee_id: str
    name: str
    allowances: dict[LeaveType, int]


@dataclass
class LeaveRequest:
    """A submitted employee leave request."""

    request_id: str
    employee_id: str
    leave_type: LeaveType
    start_date: date
    end_date: date
    days: int
    reason: str
    status: RequestStatus = "pending"
    reviewed_by: str | None = None
    review_comment: str = ""


EMPLOYEES: dict[str, Employee] = {
    "E001": Employee(
        employee_id="E001",
        name="Asha Patil",
        allowances={"annual": 20, "sick": 10, "personal": 5},
    ),
    "E002": Employee(
        employee_id="E002",
        name="Ravi Kumar",
        allowances={"annual": 18, "sick": 10, "personal": 4},
    ),
}
LEAVE_REQUESTS: dict[str, LeaveRequest] = {}
REQUEST_NUMBERS = count(1)
ACTIVE_STATUSES = {"pending", "approved"}

mcp = MCPServer(
    "Leave Management",
    instructions=(
        "Manage employee leave balances and requests. Employee IDs available in "
        "this demo are E001 and E002. Dates must use YYYY-MM-DD."
    ),
)


def _get_employee(employee_id: str) -> Employee:
    try:
        return EMPLOYEES[employee_id.upper()]
    except KeyError as error:
        raise ValueError(
            f"Unknown employee ID {employee_id!r}. Available IDs: "
            f"{', '.join(EMPLOYEES)}."
        ) from error


def _parse_date(value: str, field_name: str) -> date:
    try:
        return date.fromisoformat(value)
    except ValueError as error:
        raise ValueError(
            f"Invalid {field_name} {value!r}; expected a date in YYYY-MM-DD format."
        ) from error


def _business_days(start_date: date, end_date: date) -> int:
    if end_date < start_date:
        raise ValueError("end_date must be on or after start_date.")

    total_days = (end_date - start_date).days + 1
    return sum(
        1
        for offset in range(total_days)
        if (start_date + timedelta(days=offset)).weekday() < 5
    )


def _serialize_request(request: LeaveRequest) -> dict[str, object]:
    return {
        "request_id": request.request_id,
        "employee_id": request.employee_id,
        "leave_type": request.leave_type,
        "start_date": request.start_date.isoformat(),
        "end_date": request.end_date.isoformat(),
        "days": request.days,
        "reason": request.reason,
        "status": request.status,
        "reviewed_by": request.reviewed_by,
        "review_comment": request.review_comment,
    }


def _balance(employee: Employee) -> dict[str, object]:
    used = {leave_type: 0 for leave_type in employee.allowances}
    for request in LEAVE_REQUESTS.values():
        if request.employee_id == employee.employee_id and request.status in ACTIVE_STATUSES:
            used[request.leave_type] += request.days

    return {
        "employee_id": employee.employee_id,
        "employee_name": employee.name,
        "balances": {
            leave_type: {
                "allowance": allowance,
                "reserved": used[leave_type],
                "available": allowance - used[leave_type],
            }
            for leave_type, allowance in employee.allowances.items()
        },
    }


@mcp.tool()
def get_leave_balance(employee_id: str) -> dict[str, object]:
    """Get yearly leave allowances, reserved days, and available days for an employee."""
    return _balance(_get_employee(employee_id))


@mcp.tool()
def request_leave(
    employee_id: str,
    leave_type: LeaveType,
    start_date: str,
    end_date: str,
    reason: str = "",
) -> dict[str, object]:
    """Submit a leave request using inclusive YYYY-MM-DD dates and business-day totals."""
    employee = _get_employee(employee_id)
    parsed_start = _parse_date(start_date, "start_date")
    parsed_end = _parse_date(end_date, "end_date")
    requested_days = _business_days(parsed_start, parsed_end)
    if requested_days == 0:
        raise ValueError("The requested range must contain at least one business day.")

    for existing_request in LEAVE_REQUESTS.values():
        overlaps = parsed_start <= existing_request.end_date and parsed_end >= existing_request.start_date
        if (
            existing_request.employee_id == employee.employee_id
            and existing_request.status in ACTIVE_STATUSES
            and overlaps
        ):
            raise ValueError(
                f"The dates overlap active request {existing_request.request_id}."
            )

    balance = _balance(employee)
    balances = balance["balances"]
    if not isinstance(balances, dict):
        raise RuntimeError("Leave balance data is unavailable.")
    available = balances[leave_type]["available"]
    if not isinstance(available, int) or requested_days > available:
        raise ValueError(
            f"Insufficient {leave_type} leave: requested {requested_days} day(s), "
            f"available {available}."
        )

    request = LeaveRequest(
        request_id=f"LR-{next(REQUEST_NUMBERS):04d}",
        employee_id=employee.employee_id,
        leave_type=leave_type,
        start_date=parsed_start,
        end_date=parsed_end,
        days=requested_days,
        reason=reason.strip(),
    )
    LEAVE_REQUESTS[request.request_id] = request
    return _serialize_request(request)


@mcp.tool()
def review_leave_request(
    request_id: str,
    approved: bool,
    reviewer: str,
    comment: str = "",
) -> dict[str, object]:
    """Approve or reject a pending leave request as a manager."""
    try:
        request = LEAVE_REQUESTS[request_id.upper()]
    except KeyError as error:
        raise ValueError(f"Unknown leave request {request_id!r}.") from error
    if request.status != "pending":
        raise ValueError(
            f"Request {request.request_id} is {request.status} and cannot be reviewed."
        )
    if not reviewer.strip():
        raise ValueError("reviewer must not be empty.")

    request.status = "approved" if approved else "rejected"
    request.reviewed_by = reviewer.strip()
    request.review_comment = comment.strip()
    return _serialize_request(request)


@mcp.tool()
def cancel_leave_request(request_id: str, employee_id: str) -> dict[str, object]:
    """Cancel an employee's pending or approved leave request."""
    employee = _get_employee(employee_id)
    try:
        request = LEAVE_REQUESTS[request_id.upper()]
    except KeyError as error:
        raise ValueError(f"Unknown leave request {request_id!r}.") from error
    if request.employee_id != employee.employee_id:
        raise ValueError(f"Request {request.request_id} does not belong to {employee.employee_id}.")
    if request.status not in ACTIVE_STATUSES:
        raise ValueError(
            f"Request {request.request_id} is {request.status} and cannot be cancelled."
        )

    request.status = "cancelled"
    return _serialize_request(request)


@mcp.tool()
def list_leave_requests(
    employee_id: str | None = None,
    status: RequestStatus | None = None,
) -> list[dict[str, object]]:
    """List leave requests, optionally filtered by employee ID and request status."""
    normalized_employee_id = None
    if employee_id is not None:
        normalized_employee_id = _get_employee(employee_id).employee_id

    return [
        _serialize_request(request)
        for request in LEAVE_REQUESTS.values()
        if (normalized_employee_id is None or request.employee_id == normalized_employee_id)
        and (status is None or request.status == status)
    ]


@mcp.resource("leave://employees/{employee_id}/balance")
def leave_balance_resource(employee_id: str) -> str:
    """Return an employee's current leave balance as JSON."""
    return json.dumps(_balance(_get_employee(employee_id)), indent=2)


@mcp.resource("leave://policy")
def leave_policy_resource() -> str:
    """Return the leave policy used by this demonstration server."""
    return (
        "Leave is counted on Monday through Friday. Pending and approved requests "
        "reserve balance. Requests must not overlap and require manager review."
    )


def main() -> None:
    """Run the MCP server over the default stdio transport."""
    mcp.run()
