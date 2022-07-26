from calendar import c, month
from lib2to3.pgen2.pgen import generate_grammar
from ossaudiodev import control_names
from statistics import mode
from warnings import warn_explicit
# from this import d
from flask import (
    Blueprint, current_app, flash, g, redirect, render_template, request, url_for, Flask
)
from werkzeug.exceptions import abort

from flaskr.db import get_db
# import datetime
import pandas as pd
from flaskr.insert_data import get_score
import sys
from werkzeug.utils import secure_filename
import os
import random
from model import generate_training_info, pred_one, pred_samples, training_model
# import requests
import flask
import json
import re


bp = Blueprint('main_page', __name__, template_folder='templates', static_folder='static')

UPLOAD_FOLDER = './uploads'
ALLOWED_EXTENSIONS = {'xlsx', 'xls', 'csv', 'tsv'}
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@bp.route('/')
def homepage():
    # return render_template('layout.html')
    return render_template('mainpage.html')

@bp.route('/training')
def training():
    db = get_db()
    bad_samples = db.execute("SELECT * FROM sample_all_info WHERE Judge = 'NO'").fetchall()
    bad_num = len(bad_samples)
    print(bad_num)
    good_samples = db.execute("SELECT * FROM sample_all_info WHERE Judge = 'YES' LIMIT %d" % (5000-bad_num)).fetchall()
    print(len(good_samples))
    col_names = good_samples[0].keys()
    data = {}
    for col in col_names:
        data[col] = []
        for Raw in bad_samples+good_samples:
            data[col].append(Raw[col])
    df = pd.DataFrame(data)
    print(df)
    training_info = generate_training_info(df)
    # print(training_info)
    # url = 'http://%s/insert_model_info' % request.host
    # print(url)
    _ = insert_model_info(training_info)
    result = training_model(df,training_info['model_name'])
    _ = update_model_info(result)
    # print(result)
    db.close()
    return "finishingggggggg"

@bp.route('/models_page')
def models_page():
    db = get_db()
    table_data = db.execute('select * from models_info').fetchall()
    table_info = db.execute('PRAGMA table_info(models_info)').fetchall()
    col_names = [x[1] for x in table_info][:-1]
    db.close()
    data = []
    for d in table_data:
        data.append([d[col] for col in col_names])
    perform_in_1w = []
    for d in table_data:
        if d['perform_in_1w'] == '-':
            perform_in_1w.append(d['perform_in_1w'])
        else:
            d = json.loads(d['perform_in_1w'])
            bad_num = len([1 for i in d['preds'] if i == 0])
            good_num = len(d['preds']) - bad_num
            # perform_in_1w.append("rejected: {}, accept: {}".format(bad_num, good_num))
            perform_in_1w.append("{}/{}".format(bad_num, good_num))
    return render_template('models_page.html', col_names=col_names, data=data, perform_in_1w=perform_in_1w, zip=zip)

@bp.route('/dotplot/<data>')
def dotplot(data):
    pred_res = json.loads(data)
    pred_res["yesno"] = []
    for y, n in zip(pred_res['probas_yes'], pred_res['probas_no']):
        if y <= n:
            pred_res["yesno"].append([y, n])
    rest_num = 200 - len(pred_res["yesno"])
    for y, n in zip(pred_res['probas_yes'], pred_res['probas_no']):
        if y > n and rest_num > 0:
            rest_num -= 1
            pred_res["yesno"].append([y, n])
    # print(pred_res["yesno"])
    return render_template('dotplot.html', pred_res=pred_res["yesno"])

# @bp.route('/insert_model_info', methods=['POST'])
def insert_model_info(post_form):
    form = post_form
    print("========================================")
    db_insert_model = get_db()
    table_info = db_insert_model.execute('PRAGMA table_info(models_info)').fetchall()
    col_names = [x[1] for x in table_info][1:-2]
    sql_code = '''INSERT INTO models_info ({col_names}) VALUES ({values})'''.format(col_names=",".join(col_names), values=",".join(['?'] * len(col_names)))
    print(sql_code)
    db_insert_model.execute(sql_code, [form[x] for x in col_names])
    db_insert_model.commit()
    # db_insert_model.close()
    # 这里和下面的update不close是因为他们都在training函数中运行，如果前面有close后面的db就没法操作了，修改变量名也没有办法，后面需要找方法解决
    return "OK--modelinfo"

def update_model_info(update_info):
    db_update = get_db()
    sql = "UPDATE models_info SET valid_set_perform = '{valid_v}', perform_in_1w = '{w_v}', training_status = '{train_v}' WHERE model_name = '{model_v}'".format(
                valid_v=update_info['valid_set_perform'], w_v=update_info['perform_in_1w'], train_v=update_info['training_status'], model_v=update_info['model_name'])
    print(sql)
    db_update.execute(sql)
    db_update.commit()
    # db_update.close()
    return "Done"

@bp.route('/update_current_model', methods=['POST'])
def update_current_model():
    ids_info = request.form['select_ids']
    current_id = re.findall(r'<div.*?>(.*?)</div>', ids_info)[0]
    # print(current_id)
    db = get_db()
    raws = db.execute("SELECT * FROM models_info WHERE current_model = 1").fetchall()
    if len(raws) > 0:
        for raw in raws:
            db.execute("UPDATE models_info SET current_model = 0 WHERE id = {}".format(raw['id']))
    db.execute("UPDATE models_info SET current_model = 1 WHERE id = {}".format(current_id))
    db.commit()
    db.close()
    return "done"  
    

@bp.route('/remove_models', methods=['POST'])
def remove_models():
    # ids = request.form['select_ids'].split(',')
    ids = re.findall(r'<div.*?>(.*?)</div>', request.form['select_ids'])
    # print(ids)
    db = get_db()
    for id in ids:
        db.execute('DELETE FROM models_info WHERE id = {id}'.format(id=id))
    db.commit()
    db.close()
    print("=============\nremove ids:{}\n==============".format(",".join(ids)))
    return "OK"

@bp.route('/ceshi')
def ceshi():
    # return render_template("ceshi.html")
    # url = 'http://localhost:5000/insert_model_info'
    form = {
        "model_name": "RFC_4432_1658673253",
        "features": "json的字符串形式",
        "base_model_name": "RF_model",
        "valid_set_perform": "00000000000000",
        "perform_in_1w": "h",
        "training_status": "Done",
        "use_data_ids":"json的字符串形式"
    }
    # r = requests.post(url=url, data=form)
    update_model_info(form)
    return "OK"

@bp.route('/show_data_demo')
def show_data_demo():
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
    train_flag = 0
    if len(df[df['Judge'] == 'NO']) > 0:
        train_flag = 1
    print(df)
    insert_data_func('_', file_type='_', df_input=df)
    return train_flag
    

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
    train_flag = insert_from_execl(col_name, data)
    return {"insert_status": 1, "train_flag": train_flag}


@bp.route('/predict_samples', methods=['POST'])
def predict_samples():
    db = get_db()
    current_model_name = db.execute("SELECT * FROM models_info WHERE current_model == 1;").fetchone()['model_name']
    db.close()
    current_model_path = "model/{}.model".format(current_model_name)
    col_name = json.loads(request.form['col_arr'])
    data = json.loads(request.form['data'])
    pred_res = pred_samples(col_name, data, model_path=current_model_path)
    return pred_res

@bp.route('/predict_result_page/<pred_res>')
def predict_result_page(pred_res):
    res = json.loads(pred_res)
    print(res)
    print("=======")
    res["yesno"] = []
    for y, n in zip(res['probas_yes'], res['probas_no']):
        res["yesno"].append([y, n])
    return render_template('dotplot.html', pred_res=res["yesno"])


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
    current_model_name = db.execute("SELECT * FROM models_info WHERE current_model == 1;").fetchone()['model_name']
    db.close()
    current_model_path = "model/{}.model".format(current_model_name)
    pred, probas = pred_one(raw, current_model_path)
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