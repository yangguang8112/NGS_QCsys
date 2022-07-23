import sys
import pandas as pd
from flaskr.db import get_db

def get_score(df):
    # features = ['数据量', 'Q30 %', 'GC %', 'Max N Content(%)', 'TotalReads(Mb)', 'TotalBases(Gb)', 'Read1_Q20(%)', 'Read2_Q20(%)', 'Read1_Q30(%)', 'Read2_Q30(%)', 'Read1_A(%)', 'Read1_T(%)', 'Read1_G(%)', 'Read1_C(%)', 'Read2_A(%)', 'Read2_T(%)', 'Read2_G(%)', 'Read2_C(%)', 'Read1BaseDiversity_AT(%)', 'Read1BaseDiversity_GC(%)', 'Read2BaseDiversity_AT(%)', 'Read2BaseDiversity_GC(%)', 'Max_N_content(%)', 'GC(%)', 'Clean data/Raw data(%)', 'EqualReads', 'ReferenceVersion', 'MappingRate(%)', 'UniqueRate(%)', 'DuplicateRate(%)', 'MismatchRate(%)', 'AveInsertSize', 'SdInsertSize', 'chr1_AveDepth(X)', 'chr2_AveDepth(X)', 'chr3_AveDepth(X)', 'chr4_AveDepth(X)', 'chr5_AveDepth(X)', 'chr6_AveDepth(X)', 'chr7_AveDepth(X)', 'chr8_AveDepth(X)', 'chr9_AveDepth(X)', 'chr10_AveDepth(X)', 'chr11_AveDepth(X)', 'chr12_AveDepth(X)', 'chr13_AveDepth(X)', 'chr14_AveDepth(X)', 'chr15_AveDepth(X)', 'chr16_AveDepth(X)', 'chr17_AveDepth(X)', 'chr18_AveDepth(X)', 'chr19_AveDepth(X)', 'chr20_AveDepth(X)', 'chr21_AveDepth(X)', 'chr22_AveDepth(X)', 'chrM_AveDepth(X)', 'AveDepth(X)', 'Sd_Autosome_Depth', 'Range_Autosome_Depth(X)', 'Sd_Depth_Norm_Distribution', '1X_Coverage(%)', '5X_Coverage(%)', '10X_Coverage(%)', '20X_Coverage(%)', '30X_Coverage(%)', '40X_Coverage(%)', '50X_Coverage(%)', '60X_Coverage(%)', '70X_Coverage(%)', '80X_Coverage(%)', '90X_Coverage(%)', '100X_Coverage(%)', 'SdCoverage', 'SNP_Number', 'SNP_in_dbSNP', 'SNP_in_1KGP3', 'SNP_in_gnomAD_exomes', 'SNP_in_gnomAD_genomes', 'SNP_in_TOPMed', 'SNP_in_ChinaMAP', 'Novel_SNP', 'Homozygous_SNP', 'Heterozygous_SNP', 'HIGH_impact_SNP', 'MODERATE_impact_SNP', 'LOW_impact_SNP', 'MODIFIER_impact_SNP', 'Het_Hom', 'Ti_Tv', 'INDEL_Number', 'INDEL_in_dbSNP', 'INDEL_in_1KGP3', 'INDEL_in_gnomAD_exomes', 'INDEL_in_gnomAD_genomes', 'INDEL_in_TOPMed', 'INDEL_in_ChinaMAP', 'Novel_INDEL', 'Homozygous_INDEL', 'Heterozygous_INDEL', 'HIGH_impact_INDEL', 'MODERATE_impact_INDEL', 'LOW_impact_INDEL', 'MODIFIER_impact_INDEL', 'CNV_CNVnator_Number', 'CNV_CNVnator_DUP_Length', 'CNV_CNVnator_DEL_Length', 'CNV_CNVnator_Anno_Number', 'SV_lumpy_Number', 'SV_lumpy_Anno_Number', 'SV_delly_Number', 'SV_delly_Anno_Number', 'SV_manta_Number', 'SV_manta_Anno_Number', 'SV_MELT_Number', 'SV_MELT_Anno_Number', 'contamination(%)']
    # features = [i for i in features if i not in ['数据量', 'EqualReads', 'ReferenceVersion']]
    features = ['sample concentration（ng/μL）', 'Sample Volume（μL）', 'sample basenumber', '>Q30%(total)', 'GC%(total)', 'EstErr%(total)', 'TotalReads(Mb)', 'TotalBases(Gb)', 'Read1_Q20(%)', 'Read2_Q20(%)', 'Read1_Q30(%)', 'Read2_Q30(%)', 'Read1_A(%)', 'Read1_T(%)', 'Read1_G(%)', 'Read1_C(%)', 'Read2_A(%)', 'Read2_T(%)', 'Read2_G(%)', 'Read2_C(%)', 'Read1BaseDiversity_AT(%)', 'Read1BaseDiversity_GC(%)', 'Read2BaseDiversity_AT(%)', 'Read2BaseDiversity_GC(%)', 'Max_N_content(%)', 'GC(%)', 'Clean data/Raw data(%)', 'MappingRate(%)', 'UniqueRate(%)', 'DuplicateRate(%)', 'MismatchRate(%)', 'AveInsertSize', 'SdInsertSize', 'chr1_AveDepth(X)', 'chr2_AveDepth(X)', 'chr3_AveDepth(X)', 'chr4_AveDepth(X)', 'chr5_AveDepth(X)', 'chr6_AveDepth(X)', 'chr7_AveDepth(X)', 'chr8_AveDepth(X)', 'chr9_AveDepth(X)', 'chr10_AveDepth(X)', 'chr11_AveDepth(X)', 'chr12_AveDepth(X)', 'chr13_AveDepth(X)', 'chr14_AveDepth(X)', 'chr15_AveDepth(X)', 'chr16_AveDepth(X)', 'chr17_AveDepth(X)', 'chr18_AveDepth(X)', 'chr19_AveDepth(X)', 'chr20_AveDepth(X)', 'chr21_AveDepth(X)', 'chr22_AveDepth(X)', 'chrX_AveDepth(X)', 'chrY_AveDepth(X)', 'chrM_AveDepth(X)', 'AveDepth(X)', 'Sd_Autosome_Depth', 'Range_Autosome_Depth(X)', 'Sd_Depth_Norm_Distribution', '1X_Coverage(%)', '5X_Coverage(%)', '10X_Coverage(%)', '20X_Coverage(%)', '30X_Coverage(%)', '40X_Coverage(%)', '50X_Coverage(%)', '60X_Coverage(%)', '70X_Coverage(%)', '80X_Coverage(%)', '90X_Coverage(%)', '100X_Coverage(%)', 'SdCoverage', 'SNP_Number', 'SNP_in_dbSNP', 'SNP_in_1KGP3', 'SNP_in_gnomAD_exomes', 'SNP_in_gnomAD_genomes', 'SNP_in_TOPMed', 'SNP_in_ChinaMAP', 'Novel_SNP', 'Homozygous_SNP', 'Heterozygous_SNP', 'HIGH_impact_SNP', 'MODERATE_impact_SNP', 'LOW_impact_SNP', 'MODIFIER_impact_SNP', 'Het_Hom', 'Ti_Tv', 'INDEL_Number', 'INDEL_in_dbSNP', 'INDEL_in_1KGP3', 'INDEL_in_gnomAD_exomes', 'INDEL_in_gnomAD_genomes', 'INDEL_in_TOPMed', 'INDEL_in_ChinaMAP', 'Novel_INDEL', 'Homozygous_INDEL', 'Heterozygous_INDEL', 'HIGH_impact_INDEL', 'MODERATE_impact_INDEL', 'LOW_impact_INDEL', 'MODIFIER_impact_INDEL', 'CNV_CNVnator_Number', 'CNV_CNVnator_DUP_Length', 'CNV_CNVnator_DEL_Length', 'CNV_CNVnator_Anno_Number', 'SV_lumpy_Number', 'SV_lumpy_Anno_Number', 'SV_delly_Number', 'SV_delly_Anno_Number', 'SV_manta_Number', 'SV_manta_Anno_Number', 'SV_MELT_Number', 'SV_MELT_Anno_Number', 'SV_Whamg_Number', 'SV_Whamg_Anno_Number', 'SV_xTea_Number', 'SV_xTea_Anno_Number', 'contamination(%)']
    # df = df[df['是否交付'] == '是']
    df = df[features]
    # na filter
    real_df = df[df.isnull().sum(axis=1) < 10]
    real_df = (real_df - real_df.mean()) / real_df.std()
    real_df = (real_df - real_df.median()).abs()
    # note top 1%
    note = []
    quan_99_df = real_df > real_df.quantile(0.99)
    for i in quan_99_df.index:
        note.append("/".join(quan_99_df.columns[quan_99_df.loc[i]]))
    # score
    score = len(features) + 20 - real_df.sum(axis=1)
    real_df['note'] = note
    return score, real_df['note']

if __name__ == "__main__":
    file_path = sys.argv[1]
    df = pd.read_excel(file_path,)
    score, note_warning = get_score(df)
    df['Score'] = score
    df['Note_Warning'] = note_warning
    cols = ['任务单号', '样本编号', 'Q30 %', 'GC %', 'Max N Content(%)', 'Score', 'Note_Warning']
    df = df[cols]
    db = get_db()
    for line in df.loc:
        line = line.tolist()
        db.execute(
            'INSERT INTO sample_all_info (task_code, sample_code, q30, gc, max_n)'
            ' VALUES (?, ?, ?, ?, ?)',
            (line)
        )
        db.commit()
