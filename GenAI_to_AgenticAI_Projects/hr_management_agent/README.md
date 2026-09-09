---
title: HR Management Agent
description: In-memory HR management example exposed through a Model Context Protocol server
ms.date: 2026-09-09
ms.topic: overview
keywords:
  - model context protocol
  - mcp server
  - human resources
  - python
estimated_reading_time: 7
---

## Overview

The HR Management Agent is an educational Python project that models common HR operations and exposes selected operations as Model Context Protocol (MCP) tools. It seeds in-memory employee, leave, meeting, and equipment-ticket data each time the server starts.

The current MCP server exposes employee creation, employee lookup, simulated email delivery, equipment-ticket creation, meeting scheduling, and leave applications. It also provides an onboarding prompt that coordinates employee creation, notifications, equipment requests, and an introductory meeting.

## Features

* Add an employee with an automatically generated employee ID
* Find employee details by an approximate name match
* Simulate sending an email to an employee
* Create equipment-request tickets for an employee
* Schedule employee meetings with conflict detection
* Apply for one or more leave dates
* Guide employee onboarding with a reusable MCP prompt
* Model manager and direct-report relationships
* Seed sample leave, meeting, and equipment-ticket records
* Validate employee input with Pydantic models
* Serve operations to MCP-compatible clients

## Project Structure

```text
hr_management_agent/
|-- server.py                  # MCP server and exposed tools
|-- utils.py                   # Sample in-memory data generation
|-- Architecture.excalidraw    # Editable architecture diagram
|-- HRMS/
|   |-- __init__.py
|   |-- employee_manager.py    # Employee records and reporting lines
|   |-- leave_manager.py       # Leave balances and history
|   |-- meeting_manager.py     # Employee meeting schedules
|   |-- ticket_manager.py      # Equipment request tickets
|   `-- schemas.py             # Pydantic request and response models
`-- BAK/                       # Archived project files
```

## MCP Tools

| Tool | Parameters | Result |
| --- | --- | --- |
| `add_employee` | `name`, `manager_id`, `email` | Confirmation that the employee was added |
| `get_employee_details` | `name` | The first matching employee record, or `null` |
| `send_email` | `to`, `subject`, `body` | Confirmation that the simulated email was sent |
| `create_ticket` | `emp_id`, `item`, `reason` | Confirmation that the equipment ticket was created |
| `schedule_meeting` | `emp_id`, `meeting_dt`, `topic` | Confirmation with the employee, date and time, and topic |
| `apply_for_leave` | `emp_id`, `start_date` | Confirmation with the employee and requested leave dates |

`manager_id` can be `null`. When supplied, it must identify an employee already present in the in-memory store.

The `send_email` tool is a demonstration stub. It returns a confirmation message but does not connect to an email provider or deliver a message. The `create_ticket`, `schedule_meeting`, and `apply_for_leave` tools store their changes in memory. Supply `meeting_dt` as an ISO 8601 date and time and `start_date` as a list of ISO 8601 dates.

## MCP Prompts

| Prompt | Arguments | Workflow |
| --- | --- | --- |
| `onboard_new_employee` | `employee_name`, `manager_name` | Add the employee, send notifications, raise equipment tickets, and schedule an introductory meeting |

The onboarding prompt gives the client instructions for coordinating the tools. The client must resolve the manager name to an employee ID, supply the new employee's email address, invoke `add_employee`, send employee and manager notifications with `send_email`, raise each required equipment request with `create_ticket`, and arrange the manager introduction with `schedule_meeting`. The prompt does not execute these operations by itself.

## Prerequisites

* Python 3.10 or later
* `uv` or `pip`
* An MCP-compatible client or the MCP Inspector

Dependencies are managed by the repository-level [requirements file](../requirements.txt). The relevant packages are `mcp[cli]` and `pydantic` (installed as an MCP dependency).

## Setup

Run these commands from the repository root in PowerShell:

```powershell
python -m venv .venv-x64
.venv-x64\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

With `uv`, you can use the existing dependency file:

```powershell
uv venv .venv-x64
.venv-x64\Scripts\Activate.ps1
uv pip install -r requirements.txt
```

## Run the Server

### Start with MCP Inspector

Change to the project directory and start the development server:

```powershell
Set-Location hr_management_agent
mcp dev server.py
```

The `mcp dev` command opens the MCP Inspector development workflow. Use the Inspector to verify that all six tools appear and can be invoked. Open the prompts view to confirm that `onboard_new_employee` accepts an employee name and an optional manager name.

### Start with stdio

To use standard input/output transport directly, run:

```powershell
python server.py
```

The process waits for an MCP client on standard input. A blank terminal with no prompt is expected. Stop the server with `Ctrl+C`.

### Start with Streamable HTTP

To expose the server over Streamable HTTP, run:

```powershell
python server.py --transport streamable-http
```

The server listens on `http://127.0.0.1:8000/mcp` by default. Use `--host`, `--port`, and `--path` to override these values.

## Add to GitHub Copilot in VS Code

GitHub Copilot can launch this local stdio server itself. You do not need to start `server.py` in a separate terminal.

1. Create `.vscode/mcp.json` at the repository root.
2. Add the following configuration:

   ```json
   {
     "servers": {
      "hr-management-x64": {
         "type": "stdio",
         "command": "${workspaceFolder}/.venv-x64/Scripts/python.exe",
         "args": ["${workspaceFolder}/hr_management_agent/server.py"],
         "cwd": "${workspaceFolder}/hr_management_agent"
       }
     }
   }
   ```

3. Open the Command Palette with `Ctrl+Shift+P` and run `MCP: List Servers`.
4. Select `hr-management-x64`, select **Start**, and approve the trust prompt after reviewing the command.
5. Open GitHub Copilot Chat with `Ctrl+Alt+I`.
6. Select **Configure Tools** and confirm that the six HR tools are enabled.
7. Ask Copilot to find employee details for Tony Sharma or run the onboarding prompt from the chat prompt picker.

Run `MCP: List Servers` and select **Show Output** to inspect startup errors. If the virtual environment is stored elsewhere, update the `command` value to its Python executable.

## Add to Microsoft 365 Copilot

Microsoft 365 Copilot cannot launch a local stdio process. Copilot Studio currently connects to MCP servers through Streamable HTTP, and its cloud service must be able to reach the endpoint over HTTPS.

> [!IMPORTANT]
> Create or open the agent in [Microsoft Copilot Studio](https://copilotstudio.microsoft.com/), not in Microsoft 365 Copilot Agent Builder. Agent Builder provides knowledge sources and Copilot connectors, but external MCP tools must be configured through the Copilot Studio **Tools** page.

### Expose the local HTTP endpoint

1. Start the server from the `hr_management_agent` directory. The local endpoint is `http://127.0.0.1:8000/mcp`.

  ```powershell
  python server.py --transport streamable-http
  ```

1. Install Microsoft Dev Tunnels on Windows:

   ```powershell
   winget install Microsoft.devtunnel
   ```

1. Sign in and expose the local port:

   ```powershell
   devtunnel user login
   devtunnel host -p 8000
   ```

1. Copy the HTTPS URL printed by Dev Tunnels and append `/mcp`, for example `https://<tunnel-name>-8000.<region>.devtunnels.ms/mcp`.
1. Keep both the HTTP server and tunnel processes running while testing.

The tunnel URL is temporary and is intended only for development. Do not send real employee data through an unauthenticated test endpoint.

### Connect through Copilot Studio

1. Sign in to [Copilot Studio](https://copilotstudio.microsoft.com/) and open or create an agent.
2. Turn on generative orchestration for the agent.
3. Open **Tools**, select **Add a tool**, select **New tool**, and then select **Model Context Protocol**.
4. Enter a server name, description, and the HTTPS `/mcp` URL from Dev Tunnels.
5. Select **None** for authentication only during isolated local testing. Use an API key or OAuth 2.0 before sharing the agent.
6. Select **Create**, create a new connection, and select **Add to agent**.
7. Test the agent with an employee lookup request and confirm the MCP tool invocation succeeds.
8. Publish the agent, then add the **Teams and Microsoft 365 Copilot** channel to make it available in Microsoft 365 Copilot.

Your tenant might require an administrator to approve connectors, agent publishing, or tool access. Power Platform data-loss-prevention policies also apply to MCP connections.

### Optional tenant registration

Organizations can register a remote MCP server through the Agent 365 CLI for centralized review and governance. This preview workflow requires a publicly accessible endpoint and approval in **Microsoft 365 admin center > Agents > Tools > Requests**. A localhost URL cannot be registered.

## Example Requests

After connecting an MCP client, try requests such as:

* Add an employee named Priya Shah with email `priya.shah@atliq.com` and manager ID `E001`
* Find the employee details for Tony Sharma
* Add a department leader without a manager
* Send a welcome email to `priya.shah@atliq.com`
* Raise a laptop ticket for employee `E009`
* Schedule a project introduction for employee `E009` at `2026-09-10T10:00:00`
* Apply for leave for employee `E009` on `2026-09-21` and `2026-09-22`
* Onboard Hanumant Patil reporting to David Wilson
* Onboard H1 P1 under Hanumant Patil, notify the manager, request equipment, and schedule an introductory meeting

The server assigns the next available ID in the `E001` format. Name lookup uses approximate matching and returns the first result.

## Data and Limitations

* All records are stored in memory and disappear when the process stops
* Seeded leave balances and activity records are randomized at startup
* No authentication or authorization is implemented
* Email delivery is simulated and no login credentials are generated or stored
* Employee, ticket, meeting, and leave changes disappear when the server restarts
* Six tools cover employee creation and lookup, simulated email, tickets, meetings, and leave
* The onboarding prompt provides instructions but depends on the client to invoke tools
* The project is intended for local learning and demonstration, not production HR data

## Extending the Agent

To add a capability, define a function in `server.py`, decorate it with `@mcp.tool()`, and delegate the operation to the relevant manager. Reuse the models in `HRMS/schemas.py` for input validation and keep business logic inside the manager classes.

## References

* [Add and manage MCP servers in VS Code](https://code.visualstudio.com/docs/agent-customization/mcp-servers)
* [Connect a Copilot Studio agent to an MCP server](https://learn.microsoft.com/microsoft-copilot-studio/mcp-add-existing-server-to-agent)
* [Create and host a Microsoft Dev Tunnel](https://learn.microsoft.com/azure/developer/dev-tunnels/get-started)
* [Manage agent tools in Microsoft 365](https://learn.microsoft.com/microsoft-365/admin/manage/manage-tools-for-agent)
