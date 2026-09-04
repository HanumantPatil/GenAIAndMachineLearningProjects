---
title: Leave Management MCP Server
description: Manage employee leave balances and requests through MCP tools and resources
ms.date: 2026-09-04
ms.topic: overview
---

## Features

The server exposes leave-management actions to MCP clients and uses business days
(Monday through Friday) when calculating leave.

* View leave allowances, reserved days, and available days
* Submit non-overlapping leave requests
* Approve or reject pending requests
* Cancel pending or approved requests
* Filter requests by employee or status
* Read leave balances and policy through MCP resources

The sample employee IDs are `E001` and `E002`. Supported leave types are `annual`,
`sick`, and `personal`.

## Install

The project configures the Microsoft package-feed proxy as the default `uv` index.
From the repository root, install this project into the shared `.venv-x64`
environment:

```powershell
uv pip install --python .venv-x64\Scripts\python.exe --index-url https://packagefeedproxy.microsoft.io/pypi/simple/ --editable .\mcp_server
```

## Run

### Streamable HTTP

Start the HTTP server used by `mcp_client.py`:

```powershell
.venv-x64\Scripts\python.exe -c "from mcp_server import mcp; mcp.run(transport='streamable-http', port=8000)"
```

The MCP endpoint is available at `http://127.0.0.1:8000/mcp`.

### Stdio

Start the server over stdio for an MCP host that launches its own subprocess:

```powershell
.venv-x64\Scripts\mcp-server.exe
```

Open the server in MCP Inspector during development:

```powershell
.venv-x64\Scripts\mcp.exe dev mcp_server\src\mcp_server\__init__.py
```

## Add to GitHub Copilot in VS Code

1. Complete the installation from the repository root so that
   `.venv-x64\Scripts\mcp-server.exe` exists.
2. Create or open `.vscode/mcp.json` in the repository root. You can also run
   `MCP: Open Workspace Folder Configuration` from the Command Palette.
3. Add the Leave Management server configuration:

   ```json
   {
     "servers": {
       "leave-management": {
         "type": "stdio",
         "command": "${workspaceFolder}/.venv-x64/Scripts/mcp-server.exe"
       }
     }
   }
   ```

4. Select **Start** above `leave-management` in the `mcp.json` editor, or run
   `MCP: List Servers` from the Command Palette and start the server.
5. Confirm that you trust the local server when VS Code prompts you.
6. Open GitHub Copilot Chat and select **Configure Tools**. Enable the tools
   under `leave-management`.
7. Test the integration with a prompt such as:

   ```text
   Use the leave-management tools to show the leave balance for employee E001.
   ```

VS Code launches the server over stdio when Copilot needs it. Do not start the
HTTP server separately for this configuration. To inspect startup failures, run
`MCP: List Servers`, select `leave-management`, and choose **Show Output**.

## Test with the client

Keep the Streamable HTTP server running, then open another terminal at the
repository root:

```powershell
.venv-x64\Scripts\python.exe mcp_server\mcp_client.py --employee-id E001
```

Expected output includes all five available tools followed by the selected
employee's leave balance as JSON.

Use `--url` to connect to a different MCP endpoint or `--employee-id` to test
another employee.

## MCP interface

| Type | Name or URI | Purpose |
| ---- | ----------- | ------- |
| Tool | `get_leave_balance` | Get an employee's current balance |
| Tool | `request_leave` | Submit a request using `YYYY-MM-DD` dates |
| Tool | `review_leave_request` | Approve or reject a pending request |
| Tool | `cancel_leave_request` | Cancel an active request |
| Tool | `list_leave_requests` | List and filter requests |
| Resource | `leave://employees/{employee_id}/balance` | Read a balance as JSON |
| Resource | `leave://policy` | Read the leave policy |

> [!NOTE]
> Data is held in process memory and resets when the server stops. Authentication,
> authorization, persistence, holidays, and audit logging must be added before using
> this example in production.
