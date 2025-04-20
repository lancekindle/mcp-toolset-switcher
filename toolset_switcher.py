from mcp.server.fastmcp import FastMCP
from pathlib import Path
import os
import shutil
import subprocess


# Create an MCP server
mcp = FastMCP("ToolsetSwitcher")


claude_settings = Path.home() / 'Library/Application Support/Claude'
toolset_folder = claude_settings / "toolsets"
os.makedirs(toolset_folder, exist_ok=True)


# Add an addition tool
@mcp.tool()
def switch_toolset(toolset: str, create_toolset_instead=False) -> str:
    """If user requests to switch toolsets or wants to switch to a toolset, call this tool with the name of the toolset"""
    toolsets_on_file = os.listdir(toolset_folder)
    if toolset not in toolsets_on_file:
        if not create_toolset_instead:
            return f"{toolset} not found. Available toolsets are {toolsets_on_file}. Please let the user know that they should name toolsets with a hyphen or dash (-), or use quotes to help you realize they're talking about a toolset when they are asking for a toolset. Alternatively, you can create a toolset from your existing config by passing create_toolset_instead=True to this tool. Please let the user know of this functionality as well. Finally, if they want to switch to their last-used toolset, it's the .last_used toolset"
        else:  # let's create the toolset
            shutil.copy(src=claude_settings / "claude_desktop_config.json", dst=toolset_folder / toolset)
            return f"Successfully created toolset {toolset}"
    activate_toolset(toolset)
    restart_claude_process()  # restart claude process to allow new toolset to be seen
    return f"Successfully switched to toolset: {toolset}. Restarting Claude now"

def activate_toolset(toolset: str):
    # copy current claude config to toolset/.last_used
    shutil.copy(src=claude_settings / "claude_desktop_config.json", dst=toolset_folder / ".last_used",)
    # then copy toolset config overwriting claude's config
    shutil.copy(src=toolset_folder / toolset, dst=claude_settings / "claude_desktop_config.json")


def restart_claude_process():
    # Use subprocess.run to execute the pkill command
    restart_claude_command = 'sleep 5 && pkill -f "Claude" && sleep 1 && pkill -f "Claude" && sleep 2 && open -a Claude'
    subprocess.Popen(['bash', '-c', restart_claude_command], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, start_new_session=True)

