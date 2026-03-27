# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "requests>=2,<3",
#     "mcp>=1.2.0,<2",
# ]
# ///

import sys
import requests
import argparse
import logging
from urllib.parse import urljoin

from mcp.server.fastmcp import FastMCP

DEFAULT_GHIDRA_SERVER = "http://127.0.0.1:8080/"

logger = logging.getLogger(__name__)

mcp = FastMCP("ghidra-mcp")

# Initialize ghidra_server_url with default value
ghidra_server_url = DEFAULT_GHIDRA_SERVER

def safe_get(endpoint: str, params: dict = None) -> list:
    """
    Perform a GET request with optional query parameters.
    """
    if params is None:
        params = {}

    url = urljoin(ghidra_server_url, endpoint)

    try:
        response = requests.get(url, params=params, timeout=5)
        response.encoding = 'utf-8'
        if response.ok:
            return response.text.splitlines()
        else:
            return [f"Error {response.status_code}: {response.text.strip()}"]
    except Exception as e:
        return [f"Request failed: {str(e)}"]

def safe_post(endpoint: str, data: dict | str) -> str:
    try:
        url = urljoin(ghidra_server_url, endpoint)
        if isinstance(data, dict):
            response = requests.post(url, data=data, timeout=5)
        else:
            response = requests.post(url, data=data.encode("utf-8"), timeout=5)
        response.encoding = 'utf-8'
        if response.ok:
            return response.text.strip()
        else:
            return f"Error {response.status_code}: {response.text.strip()}"
    except Exception as e:
        return f"Request failed: {str(e)}"

@mcp.tool()
def list_methods(offset: int = 0, limit: int = 100) -> list:
    """
    List all function names in the program with pagination.
    """
    return safe_get("methods", {"offset": offset, "limit": limit})

@mcp.tool()
def list_classes(offset: int = 0, limit: int = 100) -> list:
    """
    List all namespace/class names in the program with pagination.
    """
    return safe_get("classes", {"offset": offset, "limit": limit})

@mcp.tool()
def decompile_function(name: str) -> str:
    """
    Decompile a specific function by name and return the decompiled C code.
    """
    return safe_post("decompile", name)

@mcp.tool()
def rename_function(old_name: str, new_name: str) -> str:
    """
    Rename a function by its current name to a new user-defined name.
    """
    return safe_post("renameFunction", {"oldName": old_name, "newName": new_name})

@mcp.tool()
def rename_data(address: str, new_name: str) -> str:
    """
    Rename a data label at the specified address.
    """
    return safe_post("renameData", {"address": address, "newName": new_name})

@mcp.tool()
def list_segments(offset: int = 0, limit: int = 100) -> list:
    """
    List all memory segments in the program with pagination.
    """
    return safe_get("segments", {"offset": offset, "limit": limit})

@mcp.tool()
def list_imports(offset: int = 0, limit: int = 100) -> list:
    """
    List imported symbols in the program with pagination.
    """
    return safe_get("imports", {"offset": offset, "limit": limit})

@mcp.tool()
def list_exports(offset: int = 0, limit: int = 100) -> list:
    """
    List exported functions/symbols with pagination.
    """
    return safe_get("exports", {"offset": offset, "limit": limit})

@mcp.tool()
def list_namespaces(offset: int = 0, limit: int = 100) -> list:
    """
    List all non-global namespaces in the program with pagination.
    """
    return safe_get("namespaces", {"offset": offset, "limit": limit})

@mcp.tool()
def list_data_items(offset: int = 0, limit: int = 100) -> list:
    """
    List defined data labels and their values with pagination.
    """
    return safe_get("data", {"offset": offset, "limit": limit})

@mcp.tool()
def search_functions_by_name(query: str, offset: int = 0, limit: int = 100) -> list:
    """
    Search for functions whose name contains the given substring.
    """
    if not query:
        return ["Error: query string is required"]
    return safe_get("searchFunctions", {"query": query, "offset": offset, "limit": limit})

@mcp.tool()
def rename_variable(function_name: str, old_name: str, new_name: str) -> str:
    """
    Rename a local variable within a function.
    """
    return safe_post("renameVariable", {
        "functionName": function_name,
        "oldName": old_name,
        "newName": new_name
    })

@mcp.tool()
def get_function_by_address(address: str) -> str:
    """
    Get a function by its address.
    """
    return "\n".join(safe_get("get_function_by_address", {"address": address}))

@mcp.tool()
def get_current_address() -> str:
    """
    Get the address currently selected by the user.
    """
    return "\n".join(safe_get("get_current_address"))

@mcp.tool()
def get_current_function() -> str:
    """
    Get the function currently selected by the user.
    """
    return "\n".join(safe_get("get_current_function"))

@mcp.tool()
def list_functions() -> list:
    """
    List all functions in the database.
    """
    return safe_get("list_functions")

@mcp.tool()
def decompile_function_by_address(address: str) -> str:
    """
    Decompile a function at the given address.
    """
    return "\n".join(safe_get("decompile_function", {"address": address}))

@mcp.tool()
def disassemble_function(address: str) -> list:
    """
    Get assembly code (address: instruction; comment) for a function.
    """
    return safe_get("disassemble_function", {"address": address})

@mcp.tool()
def set_decompiler_comment(address: str, comment: str) -> str:
    """
    Set a comment for a given address in the function pseudocode.
    """
    return safe_post("set_decompiler_comment", {"address": address, "comment": comment})

@mcp.tool()
def set_disassembly_comment(address: str, comment: str) -> str:
    """
    Set a comment for a given address in the function disassembly.
    """
    return safe_post("set_disassembly_comment", {"address": address, "comment": comment})

@mcp.tool()
def rename_function_by_address(function_address: str, new_name: str) -> str:
    """
    Rename a function by its address.
    """
    return safe_post("rename_function_by_address", {"function_address": function_address, "new_name": new_name})

@mcp.tool()
def set_function_prototype(function_address: str, prototype: str) -> str:
    """
    Set a function's prototype.
    """
    return safe_post("set_function_prototype", {"function_address": function_address, "prototype": prototype})

@mcp.tool()
def set_local_variable_type(function_address: str, variable_name: str, new_type: str) -> str:
    """
    Set a local variable's type.
    """
    return safe_post("set_local_variable_type", {"function_address": function_address, "variable_name": variable_name, "new_type": new_type})

@mcp.tool()
def get_xrefs_to(address: str, offset: int = 0, limit: int = 100) -> list:
    """
    Get all references to the specified address (xref to).
    
    Args:
        address: Target address in hex format (e.g. "0x1400010a0")
        offset: Pagination offset (default: 0)
        limit: Maximum number of references to return (default: 100)
        
    Returns:
        List of references to the specified address
    """
    return safe_get("xrefs_to", {"address": address, "offset": offset, "limit": limit})

@mcp.tool()
def get_xrefs_from(address: str, offset: int = 0, limit: int = 100) -> list:
    """
    Get all references from the specified address (xref from).
    
    Args:
        address: Source address in hex format (e.g. "0x1400010a0")
        offset: Pagination offset (default: 0)
        limit: Maximum number of references to return (default: 100)
        
    Returns:
        List of references from the specified address
    """
    return safe_get("xrefs_from", {"address": address, "offset": offset, "limit": limit})

@mcp.tool()
def get_function_xrefs(name: str, offset: int = 0, limit: int = 100) -> list:
    """
    Get all references to the specified function by name.
    
    Args:
        name: Function name to search for
        offset: Pagination offset (default: 0)
        limit: Maximum number of references to return (default: 100)
        
    Returns:
        List of references to the specified function
    """
    return safe_get("function_xrefs", {"name": name, "offset": offset, "limit": limit})

@mcp.tool()
def list_strings(offset: int = 0, limit: int = 2000, filter: str = None) -> list:
    """
    List all defined strings in the program with their addresses.
    
    Args:
        offset: Pagination offset (default: 0)
        limit: Maximum number of strings to return (default: 2000)
        filter: Optional filter to match within string content
        
    Returns:
        List of strings with their addresses
    """
    params = {"offset": offset, "limit": limit}
    if filter:
        params["filter"] = filter
    return safe_get("strings", params)

@mcp.tool()
def find_xrefs(address: str, offset: int = 0, limit: int = 100) -> list:
    """
    Find all cross-references to and from the given address.

    Combines both inbound (xref-to) and outbound (xref-from) references
    into a single result set for comprehensive reference analysis.

    Args:
        address: Target address in hex format (e.g. "0x1400010a0")
        offset: Pagination offset (default: 0)
        limit: Maximum number of references per direction (default: 100)

    Returns:
        List of cross-references grouped by direction (to/from)
    """
    refs_to = safe_get("xrefs_to", {"address": address, "offset": offset, "limit": limit})
    refs_from = safe_get("xrefs_from", {"address": address, "offset": offset, "limit": limit})
    results = [f"=== References TO {address} ==="]
    results.extend(refs_to)
    results.append(f"=== References FROM {address} ===")
    results.extend(refs_from)
    return results


@mcp.tool()
def search_strings(pattern: str, offset: int = 0, limit: int = 2000) -> list:
    """
    Search for strings matching a regex pattern in the program.

    Args:
        pattern: Regex pattern to match against string content
        offset: Pagination offset (default: 0)
        limit: Maximum number of results (default: 2000)

    Returns:
        List of matching strings with their addresses
    """
    return safe_get("strings", {"offset": offset, "limit": limit, "filter": pattern})


@mcp.tool()
def rename_function_at(address: str, new_name: str) -> str:
    """
    Rename the function located at the specified address.

    Args:
        address: Function address in hex format (e.g. "0x1400010a0")
        new_name: New name to assign to the function

    Returns:
        Confirmation message or error
    """
    return safe_post("rename_function_by_address", {
        "function_address": address,
        "new_name": new_name
    })


@mcp.tool()
def get_data_types(offset: int = 0, limit: int = 100) -> list:
    """
    List all defined data types in the program.

    Retrieves structures, enums, typedefs, and other data type definitions
    from the Ghidra data type manager.

    Args:
        offset: Pagination offset (default: 0)
        limit: Maximum number of data types to return (default: 100)

    Returns:
        List of data type names and categories
    """
    return safe_get("dataTypes", {"offset": offset, "limit": limit})


@mcp.tool()
def get_all_imports(offset: int = 0, limit: int = 100) -> list:
    """
    List all imported functions/symbols in the program.

    Args:
        offset: Pagination offset (default: 0)
        limit: Maximum number of imports to return (default: 100)

    Returns:
        List of imported function names and their library sources
    """
    return safe_get("imports", {"offset": offset, "limit": limit})


@mcp.tool()
def get_all_exports(offset: int = 0, limit: int = 100) -> list:
    """
    List all exported functions/symbols in the program.

    Args:
        offset: Pagination offset (default: 0)
        limit: Maximum number of exports to return (default: 100)

    Returns:
        List of exported symbol names and addresses
    """
    return safe_get("exports", {"offset": offset, "limit": limit})


@mcp.tool()
def get_function_graph(address: str) -> list:
    """
    Get the function call graph for the function at the given address.

    Returns a list of called functions (callees) and calling functions (callers)
    to build a call graph around the target function.

    Args:
        address: Function address in hex format (e.g. "0x1400010a0")

    Returns:
        List of caller and callee relationships for the function
    """
    callers = safe_get("xrefs_to", {"address": address, "offset": 0, "limit": 200})
    callees = safe_get("xrefs_from", {"address": address, "offset": 0, "limit": 200})
    results = [f"=== Call Graph for {address} ==="]
    results.append(f"--- Callers (who calls this function) ---")
    results.extend(callers)
    results.append(f"--- Callees (functions called by this) ---")
    results.extend(callees)
    return results


@mcp.tool()
def decompile_by_name(name: str) -> str:
    """
    Decompile a function by searching for it by name first.

    Searches for a function matching the given name and decompiles it.
    Useful when you know the function name but not its address.

    Args:
        name: Function name or substring to search for

    Returns:
        Decompiled C pseudocode of the matched function
    """
    matches = safe_get("searchFunctions", {"query": name, "offset": 0, "limit": 5})
    if not matches or (len(matches) == 1 and matches[0].startswith("Error")):
        return f"No function found matching '{name}'"
    # Use the first match — attempt direct decompilation by name
    return safe_post("decompile", name)


def main():
    parser = argparse.ArgumentParser(description="MCP server for Ghidra")
    parser.add_argument("--ghidra-server", type=str, default=DEFAULT_GHIDRA_SERVER,
                        help=f"Ghidra server URL, default: {DEFAULT_GHIDRA_SERVER}")
    parser.add_argument("--mcp-host", type=str, default="127.0.0.1",
                        help="Host to run MCP server on (only used for sse), default: 127.0.0.1")
    parser.add_argument("--mcp-port", type=int,
                        help="Port to run MCP server on (only used for sse), default: 8081")
    parser.add_argument("--transport", type=str, default="stdio", choices=["stdio", "sse"],
                        help="Transport protocol for MCP, default: stdio")
    args = parser.parse_args()
    
    # Use the global variable to ensure it's properly updated
    global ghidra_server_url
    if args.ghidra_server:
        ghidra_server_url = args.ghidra_server
    
    if args.transport == "sse":
        try:
            # Set up logging
            log_level = logging.INFO
            logging.basicConfig(level=log_level)
            logging.getLogger().setLevel(log_level)

            # Configure MCP settings
            mcp.settings.log_level = "INFO"
            if args.mcp_host:
                mcp.settings.host = args.mcp_host
            else:
                mcp.settings.host = "127.0.0.1"

            if args.mcp_port:
                mcp.settings.port = args.mcp_port
            else:
                mcp.settings.port = 8081

            logger.info(f"Connecting to Ghidra server at {ghidra_server_url}")
            logger.info(f"Starting MCP server on http://{mcp.settings.host}:{mcp.settings.port}/sse")
            logger.info(f"Using transport: {args.transport}")

            mcp.run(transport="sse")
        except KeyboardInterrupt:
            logger.info("Server stopped by user")
    else:
        mcp.run()
        
if __name__ == "__main__":
    main()

