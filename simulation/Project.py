import pandas as pd
import numpy as np


class AUT_Project:
    def __init__(self, d):
        self.AUT_indication = d['defect_log']
        self.Weld_configuration = d['weld_configuration']
        self.Repair_data = d['repair_data']
        # self.Productivity = pd.read_excel(excel_data_path, sheet_name='productivity')
        #self.ACC_criteria = Acceptance_Tables(pd.read_excel(excel_data_path, sheet_name='project_AC'))
        self.Planar_acceptance = d['PlanarIndicationAcceptanceCriteria']

        self.Concavity_Sagging_acceptance = d['ConcavitySaggingCriteria']

        self.Por_acceptance = d['PorosityCriteria']


        self.CP_acceptance = d['ClusterPorosityCriteria']


        self.Slag_acceptance = d['SlagCriteria']


        self.Other1_acceptance = d['Other1Criteria']


        self.Other2_acceptance = d['Other2Criteria']


        self.Other3_acceptance = d['Other3Criteria']


        self.Other4_acceptance = d['Other4Criteria']


        self.Other5_acceptance = d['Other5Criteria']

    def get_length(self):
        return self.AUT_indication['length'].values.tolist()

    def get_depth(self):
        return self.AUT_indication['depth'].values.tolist()

    def get_height(self):
        return self.AUT_indication['height'].values.tolist()
 
    # def Acceptance_Tables(self):
    #     df = pd.read_excel(self.excel_data_path, sheet_name='project_AC')
    #     Height_Length_col = ['max_height', 'max_length', 'max_height', 'max_length', 'max_height', 'max_length',
    #                          'max_height', 'max_length', 'max_height', 'max_length', 'max_height', 'max_length',
    #                          'max_height', 'max_length', 'max_height', 'max_length', 'max_height', 'max_length',
    #                          'max_height', 'max_length']
    #     self.Planar_acceptance = df.iloc[4:14, 1:21]
    #     self.Planar_acceptance.columns = Height_Length_col
    #
    #     self.Concavity_Sagging_acceptance = df.iloc[19:29, 1:5]
    #
    #     self.Por_acceptance = df.iloc[36:39, 1:21]
    #     self.Por_acceptance.columns = Height_Length_col
    #
    #     self.CP_acceptance = df.iloc[46:49, 1:21]
    #     self.CP_acceptance.columns = Height_Length_col
    #
    #     self.Slag_acceptance = df.iloc[56:59, 1:21]
    #     self.Slag_acceptance.columns = Height_Length_col
    #
    #     self.Other1_acceptance = df.iloc[75:85, 1:21]
    #     self.Other1_acceptance.columns = Height_Length_col
    #
    #     self.Other2_acceptance = df.iloc[92:102, 1:21]
    #     self.Other2_acceptance.columns = Height_Length_col
    #
    #     self.Other3_acceptance = df.iloc[109:119, 1:21]
    #     self.Other3_acceptance.columns = Height_Length_col
    #
    #     self.Other4_acceptance = df.iloc[126:136, 1:21]
    #     self.Other4_acceptance.columns = Height_Length_col
    #
    #     self.Other5_acceptance = df.iloc[143:153, 1:21]
    #     self.Other5_acceptance.columns = Height_Length_col

    def LIST_ACC_Tables(self):
        LIST = [self.Planar_acceptance, self.Concavity_Sagging_acceptance, self.Por_acceptance, self.CP_acceptance,
                self.Slag_acceptance, self.Other1_acceptance, self.Other2_acceptance, self.Other3_acceptance,
                self.Other4_acceptance, self.Other5_acceptance]
        return LIST
    
    """
    Upgrade : Pendant le chargement du cette classe on utilise direct la classe Acceptance_Tables
    def Project_Acceptance_Criteria(self) -> Acceptance_Tables:
        return Acceptance_Tables(self.ACC_criteria)
    """
