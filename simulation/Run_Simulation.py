import pandas as pd
from .Functions_Sim import COI, pipethickness, Internal_ligament, External_ligament, PR_TTR_OK, PR_OR_TTR, Surface_Interaction, Height_Correction, Zone_Critere_Acceptation, Rejection, excavation_length, Repair_CutOut, AC_Table
from .Project import AUT_Project


class Results_Simulation:
    def __init__(self, Project : AUT_Project):
        self.Project = Project
        #self.Project.Acceptance_Tables()
        #self.Acceptance = Acceptance
        
    def Run_COI(self):
        Run_COI = [COI(type_of_indication) for type_of_indication in self.Project.AUT_indication['indication_type']]
        return Run_COI

    def Run_Truethick(self):
        Run_Truethick = [pipethickness(TrueWT, self.Project.Weld_configuration) for TrueWT in self.Project.AUT_indication['true_wt']]
        return Run_Truethick

    def Run_IL(self):
        Run_IL= [Internal_ligament(WT, Depth) for WT, Depth in zip(self.Run_Truethick(), self.Project.get_depth())]
        return Run_IL
    def Run_EL(self):
        Run_EL=[External_ligament(depth, Height) for depth, Height in zip(self.Project.get_depth(), self.Project.get_height())]
        return Run_EL
    def Run_PR_OR_TTR(self):
        Run_PR_OR_TTR = [PR_OR_TTR(IL, self.Project.Repair_data['Minumum value of internal ligament for partial repair (mm)'].values) for IL in
         self.Run_IL()]
        return Run_PR_OR_TTR
    def Run_Surface_Interaction(self):
        Run_Surface_Interaction = [Surface_Interaction(IL, EL, Height) for IL, EL, Height in
                             zip(self.Run_IL(), self.Run_EL(), self.Project.get_height())]
        return Run_Surface_Interaction

    def Run_Height_Correction(self):
        Run_Height_Correction=[Height_Correction(Surface_Interection, Height, IL, Depth) for
                          Surface_Interection, Height, IL, Depth in
                          zip(self.Run_Surface_Interaction(), self.Project.get_height(), self.Run_IL(), self.Project.get_depth())]
        return Run_Height_Correction

    def Run_Zone_AC_Planar(self):
        Run_Zone_AC_Planar= [Zone_Critere_Acceptation(COI, Surface_Interaction, Depth, WT) for COI, Surface_Interaction, Depth, WT in zip(self.Run_COI(), self.Run_Surface_Interaction(), self.Project.get_depth(), self.Run_Truethick())]
        return Run_Zone_AC_Planar

    def Run_Rejection(self):
        Run_Rejection= [Rejection(Height_Corrected, Length, AC_Table(Zone_AC, COI,self.Project.Por_acceptance, self.Project.CP_acceptance, self.Project.Concavity_Sagging_acceptance, self.Project.Planar_acceptance), Zone_AC) for Height_Corrected, Length, Zone_AC, COI in zip(self.Run_Height_Correction(), self.Project.get_length(), self.Run_Zone_AC_Planar(), self.Run_COI())]
        return Run_Rejection 

    def Run_Excavation_Lengt(self):
        Run_Excavation_Length = [excavation_length(Length, Depth, self.Project.Repair_data['Min excavation length at bottom excavation (mm)'].iloc[0]) for Length, Depth in zip(self.Project.get_length(), self.Project.get_depth())]
        return Run_Excavation_Length

    def Run_PR_TTR_OK(self):
        Run_PR_TTR_OK=[PR_TTR_OK(PRTTR, excavation_length, self.Project.Repair_data['Max excavation length at OD for PR (% pipe circumference)'].iloc[0], self.Project.Repair_data['Max excavation length at OD for TTR (% pipe circumference)'].iloc[0], self.Project.Weld_configuration['OD_inch'].iloc[0]) for PRTTR, excavation_length in zip(self.Run_PR_OR_TTR(), self.Run_Excavation_Lengt())]
        return Run_PR_TTR_OK
    def Run_Repair_CutOut(self):
        Run_Repair_CutOut = [Repair_CutOut(PR_TTR_OK, Rejection, COI) for PR_TTR_OK, Rejection, COI in zip(self.Run_PR_TTR_OK(), self.Run_Rejection(),self.Run_COI())]
        return Run_Repair_CutOut

    def Simulation_Data(self):
        Data_tuples = list(zip(self.Run_COI(), self.Run_Truethick(), self.Run_IL(), self.Run_EL(), self.Run_PR_OR_TTR(), self.Run_Surface_Interaction(), self.Run_Height_Correction(), self.Run_Zone_AC_Planar(), self.Run_Rejection(), self.Run_Excavation_Lengt(), self.Run_PR_TTR_OK(), self.Run_Repair_CutOut()))
        Simulation_Data = pd.DataFrame(Data_tuples, columns=['COI', 'True_Thickness', 'IL', 'EL', 'PR_OR_TTR', 'Surface_Interaction', 'Height_Correction', 'Zone_AC', 'Rejection', 'Excavation_Length', 'PR_TTR_OK', 'Repair_CutOut'])
        return Simulation_Data


