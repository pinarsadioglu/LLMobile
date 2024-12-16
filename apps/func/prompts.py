# the prompts defined here will be changed after finalized the project. It's just like a placeholder for now.
#ONLY output a JSON in the specified format in below. No comments, no explanations. Only a JSON. Only return valid JSON in the format below. No explanations, comments, different JSON or other content should appear in the output.

MANIFESTXML = """
Here is your task. You are an Android application security expert. I just shared with you an AndroidManifest.xml file at the end of this prompt. Analyse it for security. Give me real vulnerabilities and eliminate false positives ones. I shared a sample of JSON response with you. Your response align with the sample. Print only vulnerability scan's results. No error, No additional information.

{file_content}


"""
a = """    {{
        "vulnerabilities": [
            {{"id":1, "Description": "<vulnerability description>", "Proof":"<regarding data,code snippet or any prof>", "Severity": "<Severity based on CVSS>", "Remediation":"<Remediation or Suggested Fix>"}},
            {{"id":2, "Description": "<vulnerability description>", "Proof":"<regarding data,code snippet or any prof>", "Severity": "<Severity based on CVSS>", "Remediation":"<Remediation or Suggested Fix>"}},
            {{"id":3, "Description": "<vulnerability description>", "Proof":"<regarding data,code snippet or any prof>", "Severity": "<Severity based on CVSS>", "Remediation":"<Remediation or Suggested Fix>"}}
        ]
    }}"""

STRINGSXML = """
ONLY output a JSON in the specified format in below. No comments, no explanations. Only a JSON. Only return valid JSON in the format below. No explanations, comments, different JSON or other content should appear in the output.
You are an Android application security expert. I just shared with you an strings.xml file at the end of this prompt and analyse it and tell me which information is sensitive. don't forget eliminate false positives ones. 

{file_content}

"""


DUMMY = """


    A shared 2 responses example, and the JSON response that you generate should be like these.

    RESPONSE EXAMPLE 1:
    {{
        "vulnerabilities": [
            {{"id":1, "Description": "<vulnerability description>", "Proof":"<regarding data,code snippet or any prof>", "Severity": "<Severity based on CVSS>", "Remediation":"<Remediation or Suggested Fix>"}},
            {{"id":2, "Description": "<vulnerability description>", "Proof":"<regarding data,code snippet or any prof>", "Severity": "<Severity based on CVSS>", "Remediation":"<Remediation or Suggested Fix>"}},
            {{"id":3, "Description": "<vulnerability description>", "Proof":"<regarding data,code snippet or any prof>", "Severity": "<Severity based on CVSS>", "Remediation":"<Remediation or Suggested Fix>"}}
        ]
    }}

    RESPONSE EXAMPLE 2:
    {{
        "vulnerabilities": [
            {{"id":1, "Description": "<vulnerability description>", "Proof":"<regarding data,code snippet or any prof>", "Severity": "<Severity based on CVSS>", "Remediation":"<Remediation or Suggested Fix>"}},
            {{"id":2, "Description": "<vulnerability description>", "Proof":"<regarding data,code snippet or any prof>", "Severity": "<Severity based on CVSS>", "Remediation":"<Remediation or Suggested Fix>"}},
            {{"id":3, "Description": "<vulnerability description>", "Proof":"<regarding data,code snippet or any prof>", "Severity": "<Severity based on CVSS>", "Remediation":"<Remediation or Suggested Fix>"}},
            {{"id":4, "Description": "<vulnerability description>", "Proof":"<regarding data,code snippet or any prof>", "Severity": "<Severity based on CVSS>", "Remediation":"<Remediation or Suggested Fix>"}},
            {{"id":5, "Description": "<vulnerability description>", "Proof":"<regarding data,code snippet or any prof>", "Severity": "<Severity based on CVSS>", "Remediation":"<Remediation or Suggested Fix>"}}
        ]
    }}

"""

OWASP_M1 = """I have the content of an Android file that may potentially contain sensitive information. 
        Please review the content below and identify any instances of improper credential usage, 
        hardcoded secrets,apikeys, tokens or any sensitive data that should not be present in the code. 
        Specifically, look for the following issues: 
        Hardcoded API keys or tokens, Sensitive credentials (usernames, passwords), 
        Secrets stored in plaintext, Any other information that could lead to security vulnerabilities related to credential usage.
        Important: I do not want any false positives; please ensure a high level of accuracy in your analysis.
        File Content:
        {file_content}"""


OWASP_M2 = """You are to act as a security/vulnerability file reviewer for a decompiled Android APK. 
        List **only** the file names that should be reviewed for security vulnerabilities. 
        Do not add any explanations, opinions, or additional text. 
        The response should contain **only** file names in plain text, one per line, and nothing else. 
        Exclude irrelevant files like images, or documentation. No comments or descriptions of the files. 
        You can avoid file names including color, drawable,material,draw."""

OWASP_M3 = """You are to act as a security/vulnerability expert for a decompiled Android APK. List **only** the  applicable security vulnerabilities that should be reviewed for with aligned with OWASP top 10 mobile vulnerability 2024. 
        I have the content of an Android file: {file_content}""".strip()