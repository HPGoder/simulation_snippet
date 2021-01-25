import pandas as pd
import numpy as np


class AUT_Project:
    def __init__(self, d):
        self.AUT_indication = d['defect_log']
        self.Weld_configuration = d['weld_configuration']
        self.Repair_data = d['repair_data']
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
 
    def LIST_ACC_Tables(self):
        LIST = [self.Planar_acceptance, self.Concavity_Sagging_acceptance, self.Por_acceptance, self.CP_acceptance,
                self.Slag_acceptance, self.Other1_acceptance, self.Other2_acceptance, self.Other3_acceptance,
                self.Other4_acceptance, self.Other5_acceptance]
        return LIST
