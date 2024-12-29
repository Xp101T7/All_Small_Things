# Define suspicious APIs and actions to monitor
$suspiciousAPIs = @(
    "CreateRemoteThread",     # Often used in process injection
    "VirtualAllocEx",         # Used to allocate memory in a remote process
    "WriteProcessMemory",     # Used to write code into another process
    "NtQuerySystemInformation", # Used for stealthy process listing
    "ZwTerminateProcess",     # Used to terminate processes
    "SetWindowsHookEx",       # Used for keylogging or hooking processes
    "GetProcAddress",         # Used to locate functions in DLLs dynamically
    "LoadLibrary"             # Loads malicious DLLs
)

# Function to get logs from Sysmon or Windows Event Logs
Function Get-SuspiciousAPILogs {
    # Try to get Sysmon logs first
    try {
        Write-Output "Checking for suspicious Sysmon logs..."
        $sysmonLogs = Get-WinEvent -LogName "Microsoft-Windows-Sysmon/Operational" -FilterXPath "*[System[EventID=10]]" -ErrorAction SilentlyContinue
        foreach ($log in $sysmonLogs) {
            if ($suspiciousAPIs -contains $log.Properties[4].Value) {
                Write-Output "Suspicious API call detected in Sysmon logs:"
                Write-Output $log.Message
            }
        }
    } catch {
        Write-Warning "Sysmon logs not accessible or Sysmon not installed. Continuing with alternative logs..."
    }

    # Fallback to Windows Event Logs (Security logs if elevated, Application logs otherwise)
    try {
        Write-Output "Checking standard Windows Event Logs for suspicious activity..."
        $logName = if (([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)) {
            "Security"
        } else {
            Write-Warning "Not running as Administrator. Using Application logs instead of Security logs."
            "Application"
        }

        $windowsLogs = Get-WinEvent -LogName $logName -ErrorAction SilentlyContinue
        foreach ($log in $windowsLogs) {
            foreach ($api in $suspiciousAPIs) {
                if ($log.Message -like "*$api*") {
                    Write-Output "Suspicious API call detected in Windows Event Logs:"
                    Write-Output $log.Message
                }
            }
        }
    } catch {
        Write-Warning "Unable to access $logName logs. Ensure the script is run with appropriate permissions: $_"
    }
}

# Function to monitor processes for suspicious behavior
Function Monitor-Processes {
    Write-Output "Scanning running processes for potential malicious activity..."
    $processes = Get-Process | Where-Object {
        $_.Modules -match "ntdll.dll" -or $_.Modules -match "kernel32.dll"
    }

    foreach ($process in $processes) {
        try {
            $handles = (Get-Process -Id $process.Id).HandleCount
            if ($handles -gt 1000) { # Arbitrary threshold for high handle count
                Write-Output "Potentially malicious process detected: $($process.Name)"
            }

            # Checking for debug flags or environment variables (with null checks)
            if ($process | Get-Member -Name "StartInfo") { # Ensure StartInfo property exists
                $startInfo = $process.StartInfo
                if ($startInfo.EnvironmentVariables -ne $null -and $startInfo.EnvironmentVariables["DEBUG"] -ne $null) {
                    Write-Output "Process $($process.Name) has suspicious debug flags."
                }
            }
        } catch {
            Write-Warning "Unable to retrieve information for process $($process.Name): $_"
        }
    }
}

# Execute functions
Write-Output "Starting API monitoring script..."
Get-SuspiciousAPILogs
Monitor-Processes
Write-Output "Monitoring complete."
