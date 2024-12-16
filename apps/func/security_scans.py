from apps.func import prompts
from apps.func import llm
from apps import db, create_app
from flask import Flask, render_template, request
from apps.authentication.models import Vulns
from apps.config import config_dict
from flask_migrate import Migrate
import os
from apps.func import checks


# WARNING: Don't run with debug turned on in production!
DEBUG = (os.getenv('DEBUG', 'False') == 'True')

# The configuration
get_config_mode = 'Debug' if DEBUG else 'Production'

try:

    # Load the configuration using the default values
    app_config = config_dict[get_config_mode.capitalize()]

except KeyError:
    exit('Error: Invalid <config_mode>. Expected values [Debug, Production] ')

app = create_app(app_config)
Migrate(app, db)

def initialize_ai(file_path, apk_id):
    print("chaggpt has been started!")
    client = llm.ChatGPTClient(file_path)
    with app.app_context():
        manifest_analysis(client, file_path, apk_id)
        secret_scan_stringsxml(client, file_path, apk_id)
        source_code_scan(client, file_path, apk_id)
    

def manifest_analysis(client, file_path, apk_id):
    manifest = "/resources/AndroidManifest.xml"
    apk_name = os.path.basename(file_path)

    with open(file_path[:-4]+manifest, "r") as u:
        manifestxml = u.read().splitlines()

    prompt = prompts.MANIFESTXML.format(file_content=manifestxml)

    #print("Prompt", prompt)
    manifestxml_results = client.get_response(prompt)

    #print("PROMPT: ", prompt)
    #print("GPT Response:", manifestxml_results)

    vuln = Vulns(
        apk_name=apk_name,
        apk_id=apk_id,
        manifestxml=manifestxml_results
    )


    db.session.add(vuln)
    db.session.commit()

def secret_scan_stringsxml(client, file_path,apk_id):
    stringsxml_path = "/resources/res/values/strings.xml"
    apk_name = os.path.basename(file_path)

    with open(file_path[:-4]+stringsxml_path, "r") as u:
        stringsxml_content = u.read().splitlines()

    prompt = prompts.STRINGSXML.format(file_content=stringsxml_content)

    #print("Prompt", prompt)
    stringsxml_results = client.get_response(prompt)

    #print("PROMPT: ", prompt)
    #print("GPT Response:", stringsxml_results)

    vuln = Vulns.query.filter_by(apk_id=apk_id).first()
    vuln.secrets_scan = stringsxml_results

    db.session.commit()

def source_code_scan(client, file_path, apk_id):
    print("source_code_scan started!")
    code_scan_results = checks.run_semgrep(file_path)

    vuln = Vulns.query.filter_by(apk_id=apk_id).first()
    vuln.source_code_scan = code_scan_results
    db.session.commit()

def cryptographic_issues():
    pass
