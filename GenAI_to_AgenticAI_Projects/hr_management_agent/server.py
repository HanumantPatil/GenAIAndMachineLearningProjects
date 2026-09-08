"""MCP server for the HR assistant."""

import argparse

from HRMS.employee_manager import EmployeeManager
from HRMS.leave_manager import LeaveManager
from HRMS.meeting_manager import MeetingManager
from HRMS.ticket_manager import TicketManager

from mcp.server import MCPServer
from HRMS.schemas import EmployeeCreate
from utils import seed_services

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