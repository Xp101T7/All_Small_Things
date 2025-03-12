## Azure Admin Added 

Validate the event by confirming the timestamp and verifying its source.
Identify the account that performed the addition and check its recent activity.
Review the IP address, device details, and geolocation associated with the event.
Verify whether the addition aligns with approved change requests or administrative tasks.
Investigate any abnormal login patterns or privilege escalations during the same timeframe.
If unauthorized, remove the added privilege, reset credentials, and initiate a security incident response.
Document findings, escalate if necessary, and monitor for continued suspicious activity.



• Azure AD Audit Logs (track group membership changes, admin role assignments).
• Azure AD Sign-In Logs (check recent login activity, IP addresses, MFA usage).
• Privileged Identity Management (monitor privileged role assignments and just-in-time access).
• Azure Sentinel (centralize and correlate security data, view custom alerts).
• Microsoft Defender for Cloud Apps (investigate suspicious cloud activity and anomalous behavior).
• Azure Activity Logs (review administrative actions across resources).


Go to Azure AD Audit Logs:

In the Azure Portal, navigate to Azure Active Directory > Audit Logs.
Filter the logs by Operation: “Add eligible member to role in PIM.”
Open the Relevant Event:

Look for log entries where the operationName is “Add eligible member to role” and resultDescription is “Completed permanent.”
Click on the event to view its details.
Check the targetResources Field:

Inside the event details (often shown in JSON), look under targetResources.
The displayName or id in targetResources indicates the specific Azure AD role or resource (e.g., “Global Administrator”) the admin was added to.
Review additionalDetails:

This section may show additional info such as:
AssignmentType: whether it’s an Eligible or Active assignment.
AssignmentDuration: whether it’s Temporary or Permanent.
Confirm if this was a permanent role assignment or a time-bound eligible assignment.
Cross-Reference with Privileged Identity Management (PIM):

Go to Azure AD > Privileged Identity Management > Audit History.
Filter for role assignments to see who was added and any associated justifications or approval workflows.
Verify Who Performed the Action:

Under the initiatedBy or similar property, identify the user account or service principal that initiated the addition.
Examine their sign-in logs for IP, MFA usage, and potential anomalies.
By focusing on these fields and steps, you’ll see which admin was added, to which role, and who did it, helping confirm whether it was an approved action or a suspicious privilege escalation.