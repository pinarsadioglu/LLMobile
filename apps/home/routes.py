# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from apps.home import blueprint
from flask import render_template, request, g, make_response
from flask_login import login_required
from jinja2 import TemplateNotFound

from werkzeug.utils import secure_filename
from flask import jsonify
from apps.func.checks import is_apk, decompile_apk, generate_apk_id
import threading
import os
from apps import db
from flask import current_app
import json

#from apps import db
from apps.authentication.models import Vulns

@blueprint.route('/index')
@login_required
def index():

    return render_template('home/index.html', segment='index')


@blueprint.route('/<template>')
@login_required
def route_template(template):

    try:

        if not template.endswith('.html'):
            template += '.html'

        # Detect the current page
        segment = get_segment(request)

        # Serve the file (if exists) from app/templates/home/FILE.html
        return render_template("home/" + template, segment=segment)

    except TemplateNotFound:
        return render_template('home/page-404.html'), 404

    except:
        return render_template('home/page-500.html'), 500


@blueprint.route('/upload', methods=['POST'])
@login_required
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            return jsonify({"message": "The file could not be uploaded."}), 400

        file = request.files.get('file')
        if file and file.filename != '':
            # APK dosyası olup olmadığını kontrol et
            if not is_apk(file):
                return jsonify({"message": "The file you tried to upload is not a valid APK file."}), 400

            # Dosyayı güvenli hale getir
            filename = secure_filename(file.filename)
            # current_app ile app.config['UPLOAD_FOLDER'] değerine eriş
            file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)

            # Dosyayı kaydet
            file.seek(0)  # Dosya göstergesini başa al
            file.save(file_path)

            

            # APK decompile etme işlemi
            apk_id = generate_apk_id()
            output_dir = os.path.join(current_app.config['UPLOAD_FOLDER'], filename[:-4])
            threading.Thread(target=decompile_apk, args=(file_path, output_dir, apk_id)).start()
     
            #decompile_apk(file_path, output_dir)
            #threading.Thread(target=decompile_apk, args=(file_path, current_app.config['UPLOAD_FOLDER'])).start()

            # Yanıtı oluştur ve çerez ayarla
            
            response = make_response(jsonify({"message": f'{filename} has been successfully uploaded. Once the analysis is complete, you will receive a notification'}))
            response.set_cookie('apk_id', apk_id, max_age=60*60*24*7)
            return response
        else:
            return jsonify({"message": "Please upload a valid APK file."}), 400

    return render_template('home/upload.html')


@blueprint.route('/manifest-analysis.html', methods=['GET'])
@login_required
def manifest_analysis():
    manifest_vulns = Vulns.query.with_entities(Vulns.manifestxml, Vulns.apk_name).filter_by(apk_id = request.cookies.get('apk_id')).first()
    if manifest_vulns:
        return render_template('home/manifest-analysis.html', vulns=manifest_vulns, apk_name=manifest_vulns.apk_name)
    else:
        return render_template('home/manifest-analysis.html', vulns=None, apk_name=None)


@blueprint.route('/secrets-scan.html', methods=['GET'])
@login_required
def stringsxml_analysis():
    #strings_secret = Vulns.query.all()
    strings_secret = Vulns.query.with_entities(Vulns.secrets_scan, Vulns.apk_name).filter_by(apk_id = request.cookies.get('apk_id')).first()
    if strings_secret:
        return render_template('home/secrets-scan.html', vulns=strings_secret, apk_name=strings_secret.apk_name)
    else:
        return render_template('home/secrets-scan.html', vulns=None, apk_name=None)

@blueprint.route('/source-code-scan.html', methods=['GET'])
@login_required
def scan_source_code():
    vulns = Vulns.query.with_entities(Vulns.source_code_scan, Vulns.apk_name).filter_by(apk_id = request.cookies.get('apk_id')).first()
    print(vulns)
    if vulns and vulns.source_code_scan:
        vulns_to_json = json.loads(vulns.source_code_scan)
        return render_template('home/source-code-scan.html', vulns=vulns_to_json, apk_name=vulns.apk_name)
    else:
        return render_template('home/source-code-scan.html', vulns=None, apk_name=None)



@blueprint.route('/scans.html', methods=['GET'])
@login_required
def finished_scans():
    apk_names = Vulns.query.with_entities(Vulns.apk_id, Vulns.apk_name, Vulns.date_created).all()
    return render_template('home/scans.html', apks=apk_names)


@blueprint.route('/delete-scan/<string:apk_id>', methods=['POST'])
@login_required
def delete_scan(apk_id):
    try:
        # Veriyi silme işlemi
        vulns = Vulns.query.filter_by(apk_id=apk_id).first()
        if vulns:
            db.session.delete(vulns)
            db.session.commit()
            return jsonify({"message": "Scan başarıyla silindi!"}), 200
        else:
            return jsonify({"message": "Veri bulunamadı!"}), 404
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": f"Bir hata oluştu: {str(e)}"}), 500

# Helper - Extract current page name from request
def get_segment(request):
    try:
        segment = request.path.split('/')[-1]
        if segment == '':
            segment = 'index'

        return segment

    except:
        return None
