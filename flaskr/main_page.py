from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, Flask
)
from werkzeug.exceptions import abort

from flaskr.db import get_db
import datetime
import pandas as pd
from flaskr.insert_data import get_score
import sys
from werkzeug.utils import secure_filename
import os
import random
from model import pred_one
# import request
import flask
import json


bp = Blueprint('main_page', __name__, template_folder='templates', static_folder='static')

UPLOAD_FOLDER = './uploads'
ALLOWED_EXTENSIONS = {'xlsx', 'xls', 'csv', 'tsv'}
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@bp.route('/')
def homepage():
    # return render_template('layout.html')
    return render_template('mainpage.html')

@bp.route('/show_data_demo')
def  show_data_demo():
    db = get_db()
    sql_code = '''
    SELECT * FROM sample_all_info LIMIT 5000;
    '''
    demo = db.execute(sql_code).fetchall()
    db.close()
    col_names = demo[0].keys()
    col_names.remove('is_bad')
    col_names.remove('bad_note')
    col_names.remove('created')
    data = []
    for d in demo:
        data.append({col: d[col] for col in col_names})
    posts = {'col_names': col_names, 'data': data}
    return render_template('demo_data_table.html', posts=posts)

@bp.route('/predict')
def predict():
    db = get_db()
    demo = db.execute("SELECT * FROM sample_all_info LIMIT 1").fetchone()
    db.close()
    col_names = demo.keys()
    col_names.remove('is_bad')
    col_names.remove('bad_note')
    col_names.remove('created')
    return render_template('predict.html', col_names=col_names)


def open_excel_file(file_path):
    # 直接打开excel文件还是会有些错误出现
    df = pd.read_excel(file_path,)
    score, note_warning = get_score(df)
    df['Score'] = score
    df['Note_Warning'] = note_warning
    #features = ['Q30 %', 'GC %', 'Max N Content(%)', 'TotalReads(Mb)', 'TotalBases(Gb)', 'Read1_Q20(%)', 'Read2_Q20(%)', 'Read1_Q30(%)', 'Read2_Q30(%)', 'Read1_A(%)', 'Read1_T(%)', 'Read1_G(%)', 'Read1_C(%)', 'Read2_A(%)', 'Read2_T(%)', 'Read2_G(%)', 'Read2_C(%)', 'Read1BaseDiversity_AT(%)', 'Read1BaseDiversity_GC(%)', 'Read2BaseDiversity_AT(%)', 'Read2BaseDiversity_GC(%)', 'Clean data/Raw data(%)', 'MappingRate(%)', 'UniqueRate(%)', 'DuplicateRate(%)', 'MismatchRate(%)', 'AveInsertSize', 'SdInsertSize', 'chr1_AveDepth(X)', 'chr2_AveDepth(X)', 'chr3_AveDepth(X)', 'chr4_AveDepth(X)', 'chr5_AveDepth(X)', 'chr6_AveDepth(X)', 'chr7_AveDepth(X)', 'chr8_AveDepth(X)', 'chr9_AveDepth(X)', 'chr10_AveDepth(X)', 'chr11_AveDepth(X)', 'chr12_AveDepth(X)', 'chr13_AveDepth(X)', 'chr14_AveDepth(X)', 'chr15_AveDepth(X)', 'chr16_AveDepth(X)', 'chr17_AveDepth(X)', 'chr18_AveDepth(X)', 'chr19_AveDepth(X)', 'chr20_AveDepth(X)', 'chr21_AveDepth(X)', 'chr22_AveDepth(X)', 'chrM_AveDepth(X)', 'AveDepth(X)', 'Sd_Autosome_Depth', 'Range_Autosome_Depth(X)', 'Sd_Depth_Norm_Distribution', '1X_Coverage(%)', '5X_Coverage(%)', '10X_Coverage(%)', '20X_Coverage(%)', '30X_Coverage(%)', '40X_Coverage(%)', '50X_Coverage(%)', '60X_Coverage(%)', '70X_Coverage(%)', '80X_Coverage(%)', '90X_Coverage(%)', '100X_Coverage(%)', 'SdCoverage', 'SNP_Number', 'SNP_in_dbSNP', 'SNP_in_1KGP3', 'SNP_in_gnomAD_exomes', 'SNP_in_gnomAD_genomes', 'SNP_in_TOPMed', 'SNP_in_ChinaMAP', 'Novel_SNP', 'Homozygous_SNP', 'Heterozygous_SNP', 'HIGH_impact_SNP', 'MODERATE_impact_SNP', 'LOW_impact_SNP', 'MODIFIER_impact_SNP', 'Het_Hom', 'Ti_Tv', 'INDEL_Number', 'INDEL_in_dbSNP', 'INDEL_in_1KGP3', 'INDEL_in_gnomAD_exomes', 'INDEL_in_gnomAD_genomes', 'INDEL_in_TOPMed', 'INDEL_in_ChinaMAP', 'Novel_INDEL', 'Homozygous_INDEL', 'Heterozygous_INDEL', 'HIGH_impact_INDEL', 'MODERATE_impact_INDEL', 'LOW_impact_INDEL', 'MODIFIER_impact_INDEL', 'CNV_CNVnator_Number', 'CNV_CNVnator_DUP_Length', 'CNV_CNVnator_DEL_Length', 'CNV_CNVnator_Anno_Number', 'SV_lumpy_Number', 'SV_lumpy_Anno_Number', 'SV_delly_Number', 'SV_delly_Anno_Number', 'SV_manta_Number', 'SV_manta_Anno_Number', 'SV_MELT_Number', 'SV_MELT_Anno_Number', 'contamination(%)']
    features = ['sample concentration（ng/μL）', 'Sample Volume（μL）', 'sample basenumber', '>Q30%(total)', 'GC%(total)', 'EstErr%(total)', 'TotalReads(Mb)', 'TotalBases(Gb)', 'Read1_Q20(%)', 'Read2_Q20(%)', 'Read1_Q30(%)', 'Read2_Q30(%)', 'Read1_A(%)', 'Read1_T(%)', 'Read1_G(%)', 'Read1_C(%)', 'Read2_A(%)', 'Read2_T(%)', 'Read2_G(%)', 'Read2_C(%)', 'Read1BaseDiversity_AT(%)', 'Read1BaseDiversity_GC(%)', 'Read2BaseDiversity_AT(%)', 'Read2BaseDiversity_GC(%)', 'Max_N_content(%)', 'GC(%)', 'Clean data/Raw data(%)', 'MappingRate(%)', 'UniqueRate(%)', 'DuplicateRate(%)', 'MismatchRate(%)', 'AveInsertSize', 'SdInsertSize', 'chr1_AveDepth(X)', 'chr2_AveDepth(X)', 'chr3_AveDepth(X)', 'chr4_AveDepth(X)', 'chr5_AveDepth(X)', 'chr6_AveDepth(X)', 'chr7_AveDepth(X)', 'chr8_AveDepth(X)', 'chr9_AveDepth(X)', 'chr10_AveDepth(X)', 'chr11_AveDepth(X)', 'chr12_AveDepth(X)', 'chr13_AveDepth(X)', 'chr14_AveDepth(X)', 'chr15_AveDepth(X)', 'chr16_AveDepth(X)', 'chr17_AveDepth(X)', 'chr18_AveDepth(X)', 'chr19_AveDepth(X)', 'chr20_AveDepth(X)', 'chr21_AveDepth(X)', 'chr22_AveDepth(X)', 'chrX_AveDepth(X)', 'chrY_AveDepth(X)', 'chrM_AveDepth(X)', 'AveDepth(X)', 'Sd_Autosome_Depth', 'Range_Autosome_Depth(X)', 'Sd_Depth_Norm_Distribution', '1X_Coverage(%)', '5X_Coverage(%)', '10X_Coverage(%)', '20X_Coverage(%)', '30X_Coverage(%)', '40X_Coverage(%)', '50X_Coverage(%)', '60X_Coverage(%)', '70X_Coverage(%)', '80X_Coverage(%)', '90X_Coverage(%)', '100X_Coverage(%)', 'SdCoverage', 'SNP_Number', 'SNP_in_dbSNP', 'SNP_in_1KGP3', 'SNP_in_gnomAD_exomes', 'SNP_in_gnomAD_genomes', 'SNP_in_TOPMed', 'SNP_in_ChinaMAP', 'Novel_SNP', 'Homozygous_SNP', 'Heterozygous_SNP', 'HIGH_impact_SNP', 'MODERATE_impact_SNP', 'LOW_impact_SNP', 'MODIFIER_impact_SNP', 'Het_Hom', 'Ti_Tv', 'INDEL_Number', 'INDEL_in_dbSNP', 'INDEL_in_1KGP3', 'INDEL_in_gnomAD_exomes', 'INDEL_in_gnomAD_genomes', 'INDEL_in_TOPMed', 'INDEL_in_ChinaMAP', 'Novel_INDEL', 'Homozygous_INDEL', 'Heterozygous_INDEL', 'HIGH_impact_INDEL', 'MODERATE_impact_INDEL', 'LOW_impact_INDEL', 'MODIFIER_impact_INDEL', 'CNV_CNVnator_Number', 'CNV_CNVnator_DUP_Length', 'CNV_CNVnator_DEL_Length', 'CNV_CNVnator_Anno_Number', 'SV_lumpy_Number', 'SV_lumpy_Anno_Number', 'SV_delly_Number', 'SV_delly_Anno_Number', 'SV_manta_Number', 'SV_manta_Anno_Number', 'SV_MELT_Number', 'SV_MELT_Anno_Number', 'SV_Whamg_Number', 'SV_Whamg_Anno_Number', 'SV_xTea_Number', 'SV_xTea_Anno_Number', 'contamination(%)']
    features += ['is_bad', 'bad_note']
    cols = ['Task list no.', 'sample ID'] + features + ['Score', 'Note_Warning', 'Judge']
    df = df[df['是否交付'] == '是']
    df = df[cols]
    col_name = df.columns.tolist()
    data = df.to_numpy().tolist()
    return col_name, data


def insert_from_execl(col_arr, data):
    df_data = {}
    for i, col in enumerate(col_arr):
        df_data[col] = [x[i] for x in data]
    df = pd.DataFrame(df_data)
    print(df)
    insert_data_func('_', file_type='_', df_input=df)
    return "OK"
    

def insert_data_func(file_path, file_type='xlsx', df_input=None):
    # 直接打开excel文件还是会有些错误出现
    if file_type == 'xlsx':
        df = pd.read_excel(file_path,)
    else:
        df = df_input
    score, note_warning = get_score(df)
    df['Score'] = score
    df['Note_Warning'] = note_warning
    #features = ['Q30 %', 'GC %', 'Max N Content(%)', 'TotalReads(Mb)', 'TotalBases(Gb)', 'Read1_Q20(%)', 'Read2_Q20(%)', 'Read1_Q30(%)', 'Read2_Q30(%)', 'Read1_A(%)', 'Read1_T(%)', 'Read1_G(%)', 'Read1_C(%)', 'Read2_A(%)', 'Read2_T(%)', 'Read2_G(%)', 'Read2_C(%)', 'Read1BaseDiversity_AT(%)', 'Read1BaseDiversity_GC(%)', 'Read2BaseDiversity_AT(%)', 'Read2BaseDiversity_GC(%)', 'Clean data/Raw data(%)', 'MappingRate(%)', 'UniqueRate(%)', 'DuplicateRate(%)', 'MismatchRate(%)', 'AveInsertSize', 'SdInsertSize', 'chr1_AveDepth(X)', 'chr2_AveDepth(X)', 'chr3_AveDepth(X)', 'chr4_AveDepth(X)', 'chr5_AveDepth(X)', 'chr6_AveDepth(X)', 'chr7_AveDepth(X)', 'chr8_AveDepth(X)', 'chr9_AveDepth(X)', 'chr10_AveDepth(X)', 'chr11_AveDepth(X)', 'chr12_AveDepth(X)', 'chr13_AveDepth(X)', 'chr14_AveDepth(X)', 'chr15_AveDepth(X)', 'chr16_AveDepth(X)', 'chr17_AveDepth(X)', 'chr18_AveDepth(X)', 'chr19_AveDepth(X)', 'chr20_AveDepth(X)', 'chr21_AveDepth(X)', 'chr22_AveDepth(X)', 'chrM_AveDepth(X)', 'AveDepth(X)', 'Sd_Autosome_Depth', 'Range_Autosome_Depth(X)', 'Sd_Depth_Norm_Distribution', '1X_Coverage(%)', '5X_Coverage(%)', '10X_Coverage(%)', '20X_Coverage(%)', '30X_Coverage(%)', '40X_Coverage(%)', '50X_Coverage(%)', '60X_Coverage(%)', '70X_Coverage(%)', '80X_Coverage(%)', '90X_Coverage(%)', '100X_Coverage(%)', 'SdCoverage', 'SNP_Number', 'SNP_in_dbSNP', 'SNP_in_1KGP3', 'SNP_in_gnomAD_exomes', 'SNP_in_gnomAD_genomes', 'SNP_in_TOPMed', 'SNP_in_ChinaMAP', 'Novel_SNP', 'Homozygous_SNP', 'Heterozygous_SNP', 'HIGH_impact_SNP', 'MODERATE_impact_SNP', 'LOW_impact_SNP', 'MODIFIER_impact_SNP', 'Het_Hom', 'Ti_Tv', 'INDEL_Number', 'INDEL_in_dbSNP', 'INDEL_in_1KGP3', 'INDEL_in_gnomAD_exomes', 'INDEL_in_gnomAD_genomes', 'INDEL_in_TOPMed', 'INDEL_in_ChinaMAP', 'Novel_INDEL', 'Homozygous_INDEL', 'Heterozygous_INDEL', 'HIGH_impact_INDEL', 'MODERATE_impact_INDEL', 'LOW_impact_INDEL', 'MODIFIER_impact_INDEL', 'CNV_CNVnator_Number', 'CNV_CNVnator_DUP_Length', 'CNV_CNVnator_DEL_Length', 'CNV_CNVnator_Anno_Number', 'SV_lumpy_Number', 'SV_lumpy_Anno_Number', 'SV_delly_Number', 'SV_delly_Anno_Number', 'SV_manta_Number', 'SV_manta_Anno_Number', 'SV_MELT_Number', 'SV_MELT_Anno_Number', 'contamination(%)']
    features = ['sample concentration（ng/μL）', 'Sample Volume（μL）', 'sample basenumber', '>Q30%(total)', 'GC%(total)', 'EstErr%(total)', 'TotalReads(Mb)', 'TotalBases(Gb)', 'Read1_Q20(%)', 'Read2_Q20(%)', 'Read1_Q30(%)', 'Read2_Q30(%)', 'Read1_A(%)', 'Read1_T(%)', 'Read1_G(%)', 'Read1_C(%)', 'Read2_A(%)', 'Read2_T(%)', 'Read2_G(%)', 'Read2_C(%)', 'Read1BaseDiversity_AT(%)', 'Read1BaseDiversity_GC(%)', 'Read2BaseDiversity_AT(%)', 'Read2BaseDiversity_GC(%)', 'Max_N_content(%)', 'GC(%)', 'Clean data/Raw data(%)', 'MappingRate(%)', 'UniqueRate(%)', 'DuplicateRate(%)', 'MismatchRate(%)', 'AveInsertSize', 'SdInsertSize', 'chr1_AveDepth(X)', 'chr2_AveDepth(X)', 'chr3_AveDepth(X)', 'chr4_AveDepth(X)', 'chr5_AveDepth(X)', 'chr6_AveDepth(X)', 'chr7_AveDepth(X)', 'chr8_AveDepth(X)', 'chr9_AveDepth(X)', 'chr10_AveDepth(X)', 'chr11_AveDepth(X)', 'chr12_AveDepth(X)', 'chr13_AveDepth(X)', 'chr14_AveDepth(X)', 'chr15_AveDepth(X)', 'chr16_AveDepth(X)', 'chr17_AveDepth(X)', 'chr18_AveDepth(X)', 'chr19_AveDepth(X)', 'chr20_AveDepth(X)', 'chr21_AveDepth(X)', 'chr22_AveDepth(X)', 'chrX_AveDepth(X)', 'chrY_AveDepth(X)', 'chrM_AveDepth(X)', 'AveDepth(X)', 'Sd_Autosome_Depth', 'Range_Autosome_Depth(X)', 'Sd_Depth_Norm_Distribution', '1X_Coverage(%)', '5X_Coverage(%)', '10X_Coverage(%)', '20X_Coverage(%)', '30X_Coverage(%)', '40X_Coverage(%)', '50X_Coverage(%)', '60X_Coverage(%)', '70X_Coverage(%)', '80X_Coverage(%)', '90X_Coverage(%)', '100X_Coverage(%)', 'SdCoverage', 'SNP_Number', 'SNP_in_dbSNP', 'SNP_in_1KGP3', 'SNP_in_gnomAD_exomes', 'SNP_in_gnomAD_genomes', 'SNP_in_TOPMed', 'SNP_in_ChinaMAP', 'Novel_SNP', 'Homozygous_SNP', 'Heterozygous_SNP', 'HIGH_impact_SNP', 'MODERATE_impact_SNP', 'LOW_impact_SNP', 'MODIFIER_impact_SNP', 'Het_Hom', 'Ti_Tv', 'INDEL_Number', 'INDEL_in_dbSNP', 'INDEL_in_1KGP3', 'INDEL_in_gnomAD_exomes', 'INDEL_in_gnomAD_genomes', 'INDEL_in_TOPMed', 'INDEL_in_ChinaMAP', 'Novel_INDEL', 'Homozygous_INDEL', 'Heterozygous_INDEL', 'HIGH_impact_INDEL', 'MODERATE_impact_INDEL', 'LOW_impact_INDEL', 'MODIFIER_impact_INDEL', 'CNV_CNVnator_Number', 'CNV_CNVnator_DUP_Length', 'CNV_CNVnator_DEL_Length', 'CNV_CNVnator_Anno_Number', 'SV_lumpy_Number', 'SV_lumpy_Anno_Number', 'SV_delly_Number', 'SV_delly_Anno_Number', 'SV_manta_Number', 'SV_manta_Anno_Number', 'SV_MELT_Number', 'SV_MELT_Anno_Number', 'SV_Whamg_Number', 'SV_Whamg_Anno_Number', 'SV_xTea_Number', 'SV_xTea_Anno_Number', 'contamination(%)']
    features += ['is_bad', 'bad_note']
    # sql_features = ["_".join(f.strip().split()).replace('%', 'pct').replace('(', '_').replace(')','').replace('/', '_') for f in features]
    sql_features = ["_".join(f.strip().split()).replace('%', 'pct').replace('(', '_').replace(')','').replace('/', '_').replace('（', '_').replace('）', '_').replace('>', '_gt_').replace('<', '_le_').replace('μ', 'u') for f in features]
    sql_features = [f if not f[0].isdigit() else '_'+f for f in sql_features]
    # cols = ['任务单号', '样本编号'] + features + ['Score', 'Note_Warning', 'Judge']
    cols = ['Task list no.', 'sample ID'] + features + ['Score', 'Note_Warning', 'Judge']
    sql_features = ['task_code', 'sample_code'] + sql_features + ['Score', 'Note_Warning', 'Judge']
    # df = df[df['是否交付'] == '是']
    df = df[cols]
    print(df)
    db = get_db()
    for i in range(df.shape[0]):
        line = df.iloc[i].tolist()
        sql = "INSERT INTO sample_all_info ("
        sql += ",".join(sql_features)
        sql += ') VALUES ('
        sql += ",".join(['?'] * len(line))
        sql += ')'
        # print(sql)
        db.execute(sql,(line))
        db.commit()
    print("===========================INSERT FINISH===========================")

@bp.route('/insert_data')
def insert_data():
    file_path = './PM表-补data.xlsx'
    file_path = '/mnt/c/Users/yangguang2/OneDrive/BGI/质控系统数据/gai_clean_0330-生产质控表格-20220330副本.xlsx'
    insert_data_func(file_path)
    return redirect('/')

@bp.route('/get_words')
# note words
def get_words():
    db = get_db()
    sql = '''
    SELECT id, Note_Warning, Score, Judge  from sample_all_info;
    '''
    res = db.execute(sql).fetchall()
    for r in res:
        if not r['Note_Warning'] or r['Note_Warning'].strip() == '':
            continue
        s_id = r['id']
        note_words = r['Note_Warning'].split('/')
        for n in note_words:
            db.execute(
                'INSERT INTO warning_note_words (sample_table_id, note_warning_word, Score, Judge)'
                ' VALUES (?, ?, ?, ?)',
                (s_id, n, r['Score'], r['Judge'])
            )
            db.commit()
    return "done"


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@bp.route('/upload_page')
def upload_page():
    return render_template('upload_page.html')

@bp.route('/upload_old', methods=['POST'])
def upload_old():
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        flash('No selected file')
        return redirect(request.url)
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        in_file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        insert_data_func(in_file_path)
        df = pd.read_excel(in_file_path)
        sampleids = [str(i) for i in df['sample ID']]
        sampleids = ",".join(sampleids)
        os.system("rm %s" % in_file_path)
        return redirect(url_for('main_page.find_samples', sampleIDs=sampleids))
    return "OK"

@bp.route('/upload', methods=['POST'])
def upload():
    # return "ok"
    file = flask.request.files['file']
    if not file:
        return {"status": "fail"}
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        in_file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        # insert_data_func(in_file_path)
        col_name, data = open_excel_file(in_file_path)
        # print(col_name)
        os.system("rm %s" % in_file_path)
        res = {'col_name': col_name, 'data': data}
        return json.dumps(res)
    return "FAIL"

@bp.route('/insert_excel_data', methods=['POST'])
def insert_excel_data():
    col_name = json.loads(request.form['col_arr'])
    data = json.loads(request.form['data'])
    print("hahhhhhhh!!!!!!!!!!!!!")
    insert_from_execl(col_name, data)
    return "pass"

@bp.route('/find_samples')
def find_samples():
    sampleIDs = request.args.get("sampleIDs")
    sampleID_list = sampleIDs.split(",")
    db = get_db()
    demo = []
    for sampleid in sampleID_list:
        sql_code = '''
                    SELECT * FROM sample_all_info WHERE sample_code == %s;
                   ''' % (sampleid)
        res = db.execute(sql_code).fetchone()
        if res:
            demo.append(db.execute(sql_code).fetchone())
    db.close()
    col_names = demo[0].keys()
    col_names.remove('is_bad')
    col_names.remove('bad_note')
    col_names.remove('created')
    data = []
    for d in demo:
        data.append({col: d[col] for col in col_names})
    posts = {'col_names': col_names, 'data': data}
    return render_template('demo_data_table.html', posts=posts)


#
@bp.route('/go')
def go():
    return "pass"

@bp.route('/phenotypes_page')
def phenotypes_page():
    return "pass"

@bp.route('/random_page')
def random_page():
    db = get_db()
    sql_code = '''
    SELECT id FROM sample_all_info;
    '''
    id_list = db.execute(sql_code).fetchall()
    random_id = random.choice([raw['id'] for raw in id_list])
    del id_list
    raw = db.execute("SELECT * FROM sample_all_info WHERE id == %d;" % random_id).fetchone()
    db.close()
    pred, probas = pred_one(raw)
    pred = pred.tolist()
    probas = probas[0].tolist()
    col_names = raw.keys()
    col_names.remove('is_bad')
    col_names.remove('bad_note')
    col_names.remove('created')
    raw = [{col: raw[col] for col in col_names}]
    res = {'random_sample': raw, "pred": pred, "probas": probas}
    return res

@bp.route('/logout')
def logout():
    return "logout"

@bp.route('/about_page')
def about_page():
    return "about_page"
#

@app.route('/js_call', methods=['GET', 'POST'])
def js_call():  
   print(request.values['ip'])
   print(request.values['text'])
   # to send the command by ssh : os.system("ssh user@host \' restart(command) \' ")  
   return 'ok!!!!'