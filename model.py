import pickle
import re
import numpy as np
import pandas as pd



features = ['_100X_Coverage_pct', 'MODERATE_impact_INDEL', 'SNP_in_dbSNP', 'chr1_AveDepth_X', 'TotalBases_Gb', 'SV_Whamg_Number', 'SNP_in_gnomAD_exomes', 'chr21_AveDepth_X', 'Heterozygous_SNP', 'Read1_G_pct', 'Het_Hom', 'INDEL_Number', 'HIGH_impact_INDEL', 'SV_xTea_Number', '_1X_Coverage_pct', 'SV_lumpy_Number', 'Clean_data_Raw_data_pct', 'CNV_CNVnator_DUP_Length', 'Novel_SNP', 'Homozygous_SNP', '_20X_Coverage_pct', 'SV_manta_Anno_Number', 'INDEL_in_TOPMed', 'chr18_AveDepth_X', 'chr8_AveDepth_X', 'LOW_impact_INDEL', '_80X_Coverage_pct', 'MODIFIER_impact_INDEL', 'chrX_AveDepth_X', 'Read2_G_pct', 'Sd_Depth_Norm_Distribution', 'SV_lumpy_Anno_Number', 'Read2_T_pct', 'SV_delly_Anno_Number', 'chr11_AveDepth_X', 'Read1_Q30_pct', 'SNP_in_1KGP3', 'MODERATE_impact_SNP', 'INDEL_in_dbSNP', 'SV_manta_Number', 'chr10_AveDepth_X', 'chr22_AveDepth_X', 'Novel_INDEL', 'Read1_T_pct', 'Sd_Autosome_Depth', 'CNV_CNVnator_Number', '_50X_Coverage_pct', 'LOW_impact_SNP', 'Read1_Q20_pct', 'SV_MELT_Number', 'chr13_AveDepth_X', 'chr5_AveDepth_X', 'chr4_AveDepth_X', 'chr14_AveDepth_X', '_10X_Coverage_pct', 'Read2BaseDiversity_GC_pct', 'Read2_C_pct', 'HIGH_impact_SNP', 'SNP_in_gnomAD_genomes', 'SNP_in_ChinaMAP', 'GC_pct', 'INDEL_in_ChinaMAP', 'Read2_Q30_pct', 'Read2BaseDiversity_AT_pct', 'UniqueRate_pct', 'chr7_AveDepth_X', 'Read1BaseDiversity_AT_pct', 'MappingRate_pct', 'chr19_AveDepth_X', 'SdCoverage', '_40X_Coverage_pct', 'Max_N_content_pct', '_5X_Coverage_pct', 'AveDepth_X', 'SV_xTea_Anno_Number', 'Read1_C_pct', 'AveInsertSize', 'chr12_AveDepth_X', 'INDEL_in_1KGP3', 'chr17_AveDepth_X', 'Homozygous_INDEL', '_60X_Coverage_pct', '_70X_Coverage_pct', 'CNV_CNVnator_Anno_Number', 'CNV_CNVnator_DEL_Length', 'chr16_AveDepth_X', 'contamination_pct', 'Read2_A_pct', 'SV_MELT_Anno_Number', 'SdInsertSize', 'chr2_AveDepth_X', 'Range_Autosome_Depth_X', 'SNP_in_TOPMed', 'Read1_A_pct', 'chr6_AveDepth_X', 'Read2_Q20_pct', 'INDEL_in_gnomAD_genomes', 'Read1BaseDiversity_GC_pct', '_90X_Coverage_pct', 'chr3_AveDepth_X', '_30X_Coverage_pct', 'SNP_Number', 'chrM_AveDepth_X', 'INDEL_in_gnomAD_exomes', 'DuplicateRate_pct', 'Heterozygous_INDEL', 'SV_Whamg_Anno_Number', 'Ti_Tv', 'TotalReads_Mb', 'SV_delly_Number', 'chr9_AveDepth_X', 'chr15_AveDepth_X', 'MODIFIER_impact_SNP', 'chrY_AveDepth_X', 'MismatchRate_pct', 'chr20_AveDepth_X']
MODEL_PATH = 'model/RFC_for11611.model'
SEED = 2022
cvFolds = 2

def pred_one(one_sample, model_path=MODEL_PATH):
    with open(model_path, "rb") as f:
        clf = pickle.load(f)
    data = [one_sample[k] for k in features]
    data = np.array(data).reshape(1, -1)
    preds = clf.predict(data)
    probas = clf.predict_proba(data)
    return preds, probas

def pred_samples(raw_col_names, data, model_path=MODEL_PATH):
    with open(model_path, "rb") as f:
        clf = pickle.load(f)
    col_name = ["_".join(f.strip().split()).replace('%', 'pct').replace('(', '_').replace(')','').replace('/', '_').replace('（', '_').replace('）', '_').replace('>', '_gt_').replace('<', '_le_').replace('μ', 'u') for f in raw_col_names]
    col_name = [f if not f[0].isdigit() else '_'+f for f in col_name]
    df_data = {}
    for index, col in enumerate(col_name):
        df_data[col] = []
        for d in data:
            df_data[col].append(d[index])
    df = pd.DataFrame(df_data)
    # print(df)
    input_data = df[features]
    input_data.fillna(0)
    # input_data = StandardScaler().fit_transform(input_data)
    print(input_data)
    preds = clf.predict(input_data)
    probas = clf.predict_proba(input_data)
    probas_NO = probas[:, 0]
    probas_YES = probas[:, 1]
    # print(probas)
    res = {'sample_id': df['sample_ID'].tolist(), 'preds': preds.tolist(), 'probas_yes': probas_YES.tolist(), 'probas_no': probas_NO.tolist()}
    # print(res)
    return res


def pred_11611_samples(model):
    clf = model
    DATA_FILE = './uploads/PQC_11611.process.xls'
    df = pd.read_table(DATA_FILE)
    col_name = ["_".join(f.strip().split()).replace('%', 'pct').replace('(', '_').replace(')','').replace('/', '_').replace('（', '_').replace('）', '_').replace('>', '_gt_').replace('<', '_le_').replace('μ', 'u') for f in df.columns]
    col_name = [f if not f[0].isdigit() else '_'+f for f in col_name]
    df.columns = col_name
    df = df[features]
    new_df = StandardScaler().fit_transform(df)
    new_df = df.fillna(0)
    preds = clf.predict(new_df)
    probas = clf.predict_proba(new_df)
    df['preds'] = preds
    df['probas_no'] = probas[:, 0]
    df['probas_yes'] = probas[:, 1]
    res_df = df[['preds', 'probas_no', 'probas_yes']]
    print(res_df)
    res = {'preds': res_df['preds'].tolist(), 'probas_no': res_df['probas_no'].tolist(), 
           'probas_yes': res_df['probas_yes'].tolist(), 'bad_samples_index': list(res_df[res_df['preds'] == 0].index)}
    return res


import random
import time
import json
import warnings
warnings.filterwarnings("ignore")
# import project utils
# import seqQscorer.utils.Exceptions as myExceptions
# import seqQscorer.utils.utils as utils
import model_utils.utils as utils
# import seqQscorer.utils.parser as parser
# import seqQscorer.utils.custom_metrics as cm

from sklearn.model_selection import cross_validate, StratifiedKFold
from sklearn.metrics import roc_auc_score, precision_recall_curve, auc, precision_score, recall_score, f1_score, accuracy_score

from collections import Counter

from imblearn.over_sampling import SMOTE
from sklearn.preprocessing import StandardScaler

def generate_training_info(data_df):
    df = data_df
    best_clf = 'RFC'
    model_name = "{best_clf}_{sample_num}_{time}".format(best_clf=best_clf, 
                                                         sample_num=df.shape[0],
                                                         time=int(time.time()))
    return {
        'model_name': model_name,
        'features': json.dumps(features),
        'base_model_name': best_clf,
        'valid_set_perform': '-',
        'perform_in_1w': '-',
        'training_status': 'Training',
        'use_data_ids': json.dumps(df['id'].tolist())
    }



def training_model(data_df, model_name):
    df = data_df
    col_name = ["_".join(f.strip().split()).replace('%', 'pct').replace('(', '_').replace(')','').replace('/', '_').replace('（', '_').replace('）', '_').replace('>', '_gt_').replace('<', '_le_').replace('μ', 'u') for f in df.columns]
    col_name = [f if not f[0].isdigit() else '_'+f for f in col_name]
    df.columns = col_name
    label_count = Counter(df['Judge'])
    label_dict = {'YES': 1, 'WARN': 1, 'NO': 0}
    df['label'] = [label_dict[i] for i in df['Judge']]
    print(Counter(df['label']))

    yes_index = df[df['label'] == 1].index.tolist()
    # warn_index = df[df['label'] == 1].index.tolist()
    no_index = df[df['label'] == 0].index.tolist()
    train_yes = random.sample(yes_index, int(len(yes_index) * 1))
    # train_warn = random.sample(warn_index, int(len(warn_index) * 0.8))
    train_no = random.sample(no_index, int(len(no_index) * 1))

    train_index = train_yes +  train_no
    test_index = list(set(df.index.tolist()) - set(train_index))
    train_df = df.loc[train_index]
    test_df = df.loc[test_index]

    best_clf = 'RFC'
    parameters = {"criterion": "entropy", "max_depth": None, "max_features": "auto", "n_estimators": 1000}
    clf = utils.get_clf_algos()[best_clf]
    if not best_clf in ['GNB','KNN']:
        parameters['random_state'] = SEED
    clf_setup = clf.set_params(**parameters)

    # model_name = "{best_clf}_{sample_num}_{time}".format(best_clf=best_clf, 
    #                                                      sample_num=df.shape[0],
    #                                                      time=int(time.time()))
    model_file_path = 'model/%s.model' % model_name
    labels = train_df['label']
    # label_map = dict( zip( train_df['Sample'], labels ) )
    y = np.array(labels)
    input_data = train_df[features]
    input_data = StandardScaler().fit_transform(input_data)
    X = np.array(input_data)
    print('Input data has %d samples and %d features.'%(input_data.shape))
    print('Fraction of positive labels: %.2f'%(np.mean(y)))
    # training the model
    print('Training and cross-validating the model now...')
    stratifiedFold = StratifiedKFold(n_splits=cvFolds, random_state=SEED, shuffle=True)

    cv_auROC = []
    cv_auPRC = []

    # collect important evaluation measures during the grid search to 
    # provide more information about which decision threshold to use
    metrics = {}
    metrics['Precision'] = dict( (dt, []) for dt in range(1,10) )
    metrics['Recall']    = dict( (dt, []) for dt in range(1,10) )
    metrics['F1']        = dict( (dt, []) for dt in range(1,10) )
    metrics['Accuracy']  = dict( (dt, []) for dt in range(1,10) )

    smo = SMOTE(random_state=42)
    X_smo, y_smo = smo.fit_resample(X, y)
    X, y = X_smo, y_smo
    print(Counter(y))
    for train, test in stratifiedFold.split(X, y):
        model = clf_setup.fit(X[train],y[train])
        
        probas = model.predict_proba(X[test])
        
        auROC = roc_auc_score(y[test], probas[:,1])
        prec, rec, dts = precision_recall_curve(y[test], probas[:,1], pos_label=1)
        auPRC = auc(rec, prec)
        
        cv_auROC.append(auROC)
        cv_auPRC.append(auPRC)
        
        # for the different DTs
        for dt in range(1,10):
            threshold = float(dt) / 10.0
            y_pred = [1 if prob > threshold else 0 for prob in probas[:,1]]
            
            metrics['Precision'][dt] = precision_score(y[test], y_pred) 
            metrics['Recall'][dt] = recall_score(y[test], y_pred)
            metrics['F1'][dt] = f1_score(y[test], y_pred)
            metrics['Accuracy'][dt] = accuracy_score(y[test], y_pred)
    
    print('The cross-validated performance metrics are:')
    print('\tauROC: %.3f'%np.mean(cv_auROC))
    print('\tauPRC: %.3f'%np.mean(cv_auPRC))
    print('')
    print('See also more metrics for different decision thresholds:')

    header = ['Decision Threshold:']
    header += list( map(lambda x: '%.1f'%(float(x)/10.0), range(1,10) ))
    table = [ header ]
    metrics_res = {}
    for metric in metrics:
        row = [metric]
        row += [ '%.3f'%(np.mean(metrics[metric][dt])) for dt in range(1,10) ]
        table.append(row)
        tmp = [np.mean(metrics[metric][dt]) for dt in range(1,10)]
        metrics_res[metric] = sum(tmp) / len(tmp)
    utils.print_nice_table(table)
    # print(metrics_res)

    # train again all all samples, then serialize
    model = clf_setup.fit(X,y)
    pickle.dump(model, open(model_file_path, 'wb'))
    perform_in_1w = pred_11611_samples(model)
    return {
        'model_name': model_name,
        'features': json.dumps(features),
        'base_model_name': best_clf,
        'valid_set_perform': json.dumps(metrics_res),
        'perform_in_1w': json.dumps(perform_in_1w),
        'training_status': 'Done',
        'use_data_ids': json.dumps(df['id'].tolist())
    }

