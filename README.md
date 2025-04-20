# MCP Toolset Switcher
Call this tool to load different configs into claude_desktop_config.json

You can also use this tool to create a new toolset from the existing claude_desktop_config.json

This isn't super fancy, it's just a fast way to switch between different saved configurations within Claude.

## how to use  (MacOS only for now -- pull requests welcome)
- tell claude "Create a new toolset called xyz"
- Now anytime you can tell claude "switch toolsets to xyz"
- and it should swap claude_desktop_config.json with the xyz config created previously, and then restart claude (necessary for toolset change to be recognized)

## Motivation:
Any MCP tool pollutes your context just a little bit; Claude is told of all available tools before your text input is ever seen.

So the goal here is reduce the context pollution by allowing you to maintain separate toolsets for different types of jobs, such as coding, writing, researching.

## How to install.
- clone this repository
- cd into repo
- uv install
- uv run mcp install toolset_switcher.py


## notes:
Thanks to https://github.com/modelcontextprotocol/python-sdk?tab=readme-ov-file#adding-mcp-to-your-python-project

This was extremely easy to understand and implement. Biggest challenge for me was getting timing right to make Claude restart after the toolset switch.

I purposefully only call this tool a toolset switcher, and don't explicitly advertise (within the tool context that Claude sees) that it can create toolsets. If this tool cannot locate a mentioned toolset, I let claude know that it can be used to create toolsets as well. This is to limit the context pollution for any initial prompt, but allow for that flexibility of creating toolsets. In testing, this seems to work pretty well.
