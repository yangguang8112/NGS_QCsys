import pickle
import numpy as np



features = ['_100X_Coverage_pct', 'MODERATE_impact_INDEL', 'SNP_in_dbSNP', 'chr1_AveDepth_X', 'TotalBases_Gb', 'SV_Whamg_Number', 'SNP_in_gnomAD_exomes', 'chr21_AveDepth_X', 'Heterozygous_SNP', 'Read1_G_pct', 'Het_Hom', 'INDEL_Number', 'HIGH_impact_INDEL', 'SV_xTea_Number', '_1X_Coverage_pct', 'SV_lumpy_Number', 'Clean_data_Raw_data_pct', 'CNV_CNVnator_DUP_Length', 'Novel_SNP', 'Homozygous_SNP', '_20X_Coverage_pct', 'SV_manta_Anno_Number', 'INDEL_in_TOPMed', 'chr18_AveDepth_X', 'chr8_AveDepth_X', 'LOW_impact_INDEL', '_80X_Coverage_pct', 'MODIFIER_impact_INDEL', 'chrX_AveDepth_X', 'Read2_G_pct', 'Sd_Depth_Norm_Distribution', 'SV_lumpy_Anno_Number', 'Read2_T_pct', 'SV_delly_Anno_Number', 'chr11_AveDepth_X', 'Read1_Q30_pct', 'SNP_in_1KGP3', 'MODERATE_impact_SNP', 'INDEL_in_dbSNP', 'SV_manta_Number', 'chr10_AveDepth_X', 'chr22_AveDepth_X', 'Novel_INDEL', 'Read1_T_pct', 'Sd_Autosome_Depth', 'CNV_CNVnator_Number', '_50X_Coverage_pct', 'LOW_impact_SNP', 'Read1_Q20_pct', 'SV_MELT_Number', 'chr13_AveDepth_X', 'chr5_AveDepth_X', 'chr4_AveDepth_X', 'chr14_AveDepth_X', '_10X_Coverage_pct', 'Read2BaseDiversity_GC_pct', 'Read2_C_pct', 'HIGH_impact_SNP', 'SNP_in_gnomAD_genomes', 'SNP_in_ChinaMAP', 'GC_pct', 'INDEL_in_ChinaMAP', 'Read2_Q30_pct', 'Read2BaseDiversity_AT_pct', 'UniqueRate_pct', 'chr7_AveDepth_X', 'Read1BaseDiversity_AT_pct', 'MappingRate_pct', 'chr19_AveDepth_X', 'SdCoverage', '_40X_Coverage_pct', 'Max_N_content_pct', '_5X_Coverage_pct', 'AveDepth_X', 'SV_xTea_Anno_Number', 'Read1_C_pct', 'AveInsertSize', 'chr12_AveDepth_X', 'INDEL_in_1KGP3', 'chr17_AveDepth_X', 'Homozygous_INDEL', '_60X_Coverage_pct', '_70X_Coverage_pct', 'CNV_CNVnator_Anno_Number', 'CNV_CNVnator_DEL_Length', 'chr16_AveDepth_X', 'contamination_pct', 'Read2_A_pct', 'SV_MELT_Anno_Number', 'SdInsertSize', 'chr2_AveDepth_X', 'Range_Autosome_Depth_X', 'SNP_in_TOPMed', 'Read1_A_pct', 'chr6_AveDepth_X', 'Read2_Q20_pct', 'INDEL_in_gnomAD_genomes', 'Read1BaseDiversity_GC_pct', '_90X_Coverage_pct', 'chr3_AveDepth_X', '_30X_Coverage_pct', 'SNP_Number', 'chrM_AveDepth_X', 'INDEL_in_gnomAD_exomes', 'DuplicateRate_pct', 'Heterozygous_INDEL', 'SV_Whamg_Anno_Number', 'Ti_Tv', 'TotalReads_Mb', 'SV_delly_Number', 'chr9_AveDepth_X', 'chr15_AveDepth_X', 'MODIFIER_impact_SNP', 'chrY_AveDepth_X', 'MismatchRate_pct', 'chr20_AveDepth_X']
MODEL_PATH = 'model/RFC_for11611.model'





def pred_one(one_sample, model_path=MODEL_PATH):
    with open(model_path, "rb") as f:
        clf = pickle.load(f)
    data = [one_sample[k] for k in features]
    data = np.array(data).reshape(1, -1)
    preds = clf.predict(data)
    probas = clf.predict_proba(data)
    return preds, probas