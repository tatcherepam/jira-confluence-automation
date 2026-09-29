$ErrorActionPreference = "Stop"

$script:SupportedProtocolVersions = @(
    "2025-11-25",
    "2025-03-26",
    "2024-11-05"
)

function Send-JsonRpcMessage {
    param([hashtable]$Message)

    $json = ConvertTo-Json -InputObject $Message -Depth 32 -Compress
    [Console]::Out.WriteLine($json)
    [Console]::Out.Flush()
}

function Send-JsonRpcResult {
    param(
        [object]$Id,
        [object]$Result
    )

    Send-JsonRpcMessage @{ jsonrpc = "2.0"; id = $Id; result = $Result }
}

function Send-JsonRpcError {
    param(
        [object]$Id,
        [int]$Code,
        [string]$Message
    )

    Send-JsonRpcMessage @{
        jsonrpc = "2.0"
        id = $Id
        error = @{ code = $Code; message = $Message }
    }
}

function Get-EchoTool {
    return @{
        name = "echo"
        description = "Return the provided message unchanged."
        inputSchema = @{
            type = "object"
            properties = @{
                message = @{
                    type = "string"
                    description = "The text to return."
                }
            }
            required = @("message")
        }
    }
}

while ($null -ne ($line = [Console]::In.ReadLine())) {
    if ([string]::IsNullOrWhiteSpace($line)) {
        continue
    }

    try {
        $request = ConvertFrom-Json -InputObject $line -ErrorAction Stop
    }
    catch {
        Send-JsonRpcError -Id $null -Code -32700 -Message "Parse error"
        continue
    }

    $hasId = $request.PSObject.Properties.Name -contains "id"
    $requestId = $request.id
    $method = [string]$request.method

    $shouldExit = $false
    switch ($method) {
        "initialize" {
            $requestedVersion = [string]$request.params.protocolVersion
            if ($script:SupportedProtocolVersions -contains $requestedVersion) {
                $protocolVersion = $requestedVersion
            }
            else {
                $protocolVersion = $script:SupportedProtocolVersions[0]
            }

            $result = @{
                protocolVersion = $protocolVersion
                capabilities = @{ tools = @{ listChanged = $false } }
                serverInfo = @{ name = "echo-windows"; version = "1.0.0" }
            }

            if ($hasId) {
                Send-JsonRpcResult -Id $requestId -Result $result
            }
        }
        "notifications/initialized" {
        }
        "ping" {
            if ($hasId) {
                Send-JsonRpcResult -Id $requestId -Result @{}
            }
        }
        "tools/list" {
            if ($hasId) {
                Send-JsonRpcResult -Id $requestId -Result @{ tools = @((Get-EchoTool)) }
            }
        }
        "tools/call" {
            if (-not $hasId) {
                continue
            }

            if ([string]$request.params.name -ne "echo") {
                Send-JsonRpcError -Id $requestId -Code -32602 -Message "Unknown tool"
                continue
            }

            $arguments = $request.params.arguments
            $messageProperty = $null
            if ($null -ne $arguments) {
                $messageProperty = $arguments.PSObject.Properties["message"]
            }

            if ($null -eq $messageProperty -or $messageProperty.Value -isnot [string]) {
                Send-JsonRpcResult -Id $requestId -Result @{
                    content = @(@{ type = "text"; text = "The echo tool requires a string 'message' argument." })
                    isError = $true
                }
                continue
            }

            Send-JsonRpcResult -Id $requestId -Result @{
                content = @(@{ type = "text"; text = $messageProperty.Value })
            }
        }
        "shutdown" {
            if ($hasId) {
                Send-JsonRpcResult -Id $requestId -Result $null
            }
        }
        "exit" {
            $shouldExit = $true
        }
        default {
            if ($hasId) {
                Send-JsonRpcError -Id $requestId -Code -32601 -Message "Method not found"
            }
        }
    }

    if ($shouldExit) {
        break
    }
}
