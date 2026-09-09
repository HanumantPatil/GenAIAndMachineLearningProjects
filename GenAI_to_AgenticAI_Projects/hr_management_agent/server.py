"""MCP server for the HR assistant."""

import argparse
from datetime import date, datetime

from HRMS.employee_manager import EmployeeManager
from HRMS.leave_manager import LeaveManager
from HRMS.meeting_manager import MeetingManager
from HRMS.ticket_manager import TicketManager

from mcp.server import MCPServer
from HRMS.schemas import EmployeeCreate, LeaveApplyRequest, MeetingCreate, TicketCreate
from utils import seed_services

# Initialize the MCP server and seed the HRMS services.
mcp = MCPServer("MS-HR-Assist")

employee_manager = EmployeeManager()
leave_manager = LeaveManager()
ticket_manager = TicketManager()
meeting_manager = MeetingManager()
seed_services(employee_manager, leave_manager, meeting_manager, ticket_manager)
# Tools
# resources (knowledge)
# prompts

@mcp.tool()
def add_employee(name: str, manager_id: str | None, email: str) -> str:
    """Add a new employee to the  HRMS system.
    Args:
        name (str): The name of the employee.
        manager_id (str | None): The ID of the manager, if any.
        email (str): The email address of the employee.

    Returns:
        str: A message indicating the result of the operation.
    """
    emp = EmployeeCreate(
        emp_id=employee_manager.get_next_emp_id(),
        name=name,
        manager_id=manager_id,
        email=email
    )
    employee_manager.add_employee(emp)
    return f"Employee {name} added successfully."

@mcp.tool()
def get_employee_details(name: str) -> dict | None:
    """Get the details of an employee by name.
    Args:
        name (str): The name of the employee.

    Returns:
        dict | None: A dictionary containing the employee's details if found, otherwise None.
    """
    matches = employee_manager.search_employee_by_name(name)
    if not matches:
        return None
    emp_id = matches[0]
    emp = employee_manager.get_employee_details(emp_id)
    return emp

@mcp.tool()
def send_email(to: str, subject: str, body: str) -> str:
    """Send an email to the specified recipient.
    Args:
        to (str): The recipient's email address.
        subject (str): The subject of the email.
        body (str): The body of the email.

    Returns:
        str: A message indicating the result of the operation.
    """
    # Implement the email sending logic here.
    return f"Email sent to {to} with subject '{subject}'."
@mcp.tool()
def create_ticket(emp_id: str, item: str, reason: str) -> str:
    """
    Create a new ticket for an employee.
    
    Args:
        emp_id (str): The ID of the employee.
        item (str): The item for which the ticket is being created.
        reason (str): The reason for the ticket.

    Returns:
        str: A message indicating the result of the operation.
    """
    ticket_req = TicketCreate(       
        emp_id=emp_id,
        item=item,
        reason=reason
    )
    ticket_manager.create_ticket(ticket_req)
    return f"Ticket for item '{item}' created successfully."

@mcp.tool()
def schedule_meeting(
    emp_id: str,
    meeting_dt: datetime,
    topic: str,
) -> str:
    """
    Schedule a meeting for an employee.
    
    Args:
        emp_id (str): The ID of the employee.
        meeting_dt (datetime): The date and time of the meeting.
        topic (str): The topic of the meeting.

    Returns:
        str: A message indicating the result of the operation.
    """
    meeting_req = MeetingCreate(
        emp_id=emp_id,
        meeting_dt=meeting_dt,
        topic=topic,
    )
    meeting_manager.schedule_meeting(meeting_req)
    return (
        f"Meeting scheduled for employee '{emp_id}' "
        f"on {meeting_dt}: {topic}."
    )

@mcp.tool()
def apply_for_leave(emp_id: str, start_date: list[date]) -> str:
    """
    Apply for leave for an employee.
    
    Args:
        emp_id (str): The ID of the employee.
        start_date (list[datetime]): The start dates of the leave.

    Returns:
        str: A message indicating the result of the operation.
    """
    leave_req = LeaveApplyRequest(
        emp_id=emp_id,
        leave_dates=start_date,
    )
    leave_manager.apply_leave(leave_req)
    return (
        f"Leave applied for employee '{emp_id}' "
        f"from {start_date}."
    )
@mcp.prompt("onboard_new_employee")
def onboard_new_employee(employee_name: str, manager_name: str | None) -> str:
    """Onboard a new employee by adding them to the HRMS system and sending a welcome email.
    Args:
        employee_name (str): The name of the employee.
        manager_name (str | None): The name of the manager, if any.

    Returns:
        str: A message indicating the result of the operation.
    """
    return f"""
    Onboarding a new employee with the following details:
    Employee Name: {employee_name}
    Manager Name: {manager_name}
    steps to follow:
    1. Add the employee to the HRMS system.
    2. Send a welcome email to the employee with their login credentials.(Format: "Hello {employee_name}, your login credentials are ...")
    3. Notify the manager about the new employee onboarding.
    4. Raise tickets for new laptops or other necessary equipment for the employee.
    5. Schedule an introductory meeting for the new employee with their manager.
"""
def create_parser() -> argparse.ArgumentParser:
    """Create the command-line parser for MCP transport settings."""
    parser = argparse.ArgumentParser(description="Run the HR management MCP server.")
    parser.add_argument(
        "--transport",
        choices=("stdio", "streamable-http"),
        default="stdio",
        help="MCP transport to use (default: stdio).",
    )
    parser.add_argument("--host", default="127.0.0.1", help="HTTP bind host.")
    parser.add_argument("--port", type=int, default=8000, help="HTTP bind port.")
    parser.add_argument("--path", default="/mcp", help="Streamable HTTP endpoint path.")
    return parser


def main() -> None:
    """Run the MCP server with the selected transport."""
    args = create_parser().parse_args()
    if args.transport == "streamable-http":
        mcp.run(
            "streamable-http",
            host=args.host,
            port=args.port,
            streamable_http_path=args.path,
        )
        return

    mcp.run("stdio")


if __name__ == "__main__":
    main()