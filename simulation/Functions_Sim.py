"""
This script aims to determine if an indication is rejected or not.
"""

import pandas as pd
import numpy as np
import math

"""
Modifying pandas parameters just to have a better view of the dataframe printing
"""
pd.options.display.float_format = '{:,.2f}'.format
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)

FORBIDDEN_LIST = ['BT', 'COPPER INC.', 'CRACK', 'DISBONDING', 'LAMINATION']
PLANAR_LIST = ['LOF', ' LOF', 'LOF ', 'CL', 'LOP', 'LORF', 'IU', 'ME', 'EU', 'SLAG', 'LCP', 'Slag']
CONCAVITY_LIST = ['RC', 'Concavity']
SAGGING_LIST = ['SAGGING', 'Sagging']
POR_LIST = ['POR']
CP_LIST = ['CP']

PLANAR_STR = 'Planar'
CLUSTERP_STR = 'ClusterP'
POROSITY_STR = 'Porosity'
FORBIDDEN_STR = 'Forbidden'
CONCAVITY_STR = 'Concavity'
SAGGING_STR = 'Sagging'
LAMINATION_STR = 'LAMINATION'
CP_STR = 'CP'
POR_STR = 'POR'

ROOT_INT_STR = 'root int'
CAP_INT_STR = 'cap int'
NO_STR = 'no'
PLANAR_INDICATIONS_KEY = 'Planar indications'
CONCAVITY_SAGGING_KEY = 'Concavity and sagging'
PARAMETERS_KEY = 'parameters'
MAX_HEIGHT_KEY = 'max_height'
MAX_LENGTH_KEY = 'max_length'

def COI(type_of_indication):
    if type_of_indication in POR_LIST:
        return POROSITY_STR
    else:
        if type_of_indication in CP_LIST:
            return CLUSTERP_STR
        else:
            if type_of_indication in CONCAVITY_LIST:
                return CONCAVITY_STR
            else:
                if type_of_indication in FORBIDDEN_LIST:
                    return FORBIDDEN_STR
                else:
                    if type_of_indication in PLANAR_LIST:
                        return PLANAR_STR
                    else:
                        if type_of_indication in SAGGING_LIST:
                            return SAGGING_STR
        return 'Nature not identified'

def pipethickness(TrueWT, df_weld_configuration):
    if TrueWT is None:
        return df_weld_configuration['WT (mm)']
    else:
        return TrueWT

def Internal_ligament(WT, Depth):
    return WT - Depth

def External_ligament(Depth, Height):
    return Depth - Height

def PR_OR_TTR(Internal_Ligament, Min_lig_repair):
    if (Internal_Ligament < Min_lig_repair):
        return 'TTR'
    else:
        return 'PR'

def Surface_Interaction(IL, EL, Height):
    if IL == 0 or (IL < (Height / 2)):
        return ROOT_INT_STR
    else:
        if EL == 0 or (EL < (Height / 2)):
            return CAP_INT_STR
        else:
            return 'Not Interactive'

def Height_Correction(Surface_interaction, Height, IL, Depth):
    if Surface_interaction == ROOT_INT_STR:
        return Height + IL
    else:
        if Surface_interaction == CAP_INT_STR:
            return Depth
        else:
            return Height

def Zone_Critere_Acceptation(COI, Surface_Interaction, Depth, WT):
    if COI in CONCAVITY_LIST:
        return 0 #"NA"
    else:
        if Surface_Interaction == ROOT_INT_STR:
            return 0
        else:
            if Surface_Interaction == CAP_INT_STR:
                return 1
            else:
                if Depth > (7 / 8) * WT:
                    return 2
                else:
                    if Depth > (6 / 8) * WT:
                        return 3
                    else:
                        if Depth > (5 / 8) * WT:
                            return 4
                        else:
                            if Depth > (4 / 8) * WT:
                                return 5
                            else:
                                if Depth > (3 / 8) * WT:
                                    return 6
                                else:
                                    if Depth > (2 / 8) * WT:
                                        return 7
                                    else:
                                        if Depth > (1/8) * WT:
                                            return 8
                                        else:
                                            return 9


def AC_Table(Zone_AC, COI, df_por_acceptance, df_CP_acceptance, df_Concavity_Sagging_acceptance,df_planar_acceptance):
    if COI == POROSITY_STR:
        return df_por_acceptance.iloc[:, 2*Zone_AC:2*Zone_AC + 2]
    else:
        if COI == CLUSTERP_STR:
            return df_CP_acceptance.iloc[:, 2*Zone_AC:2*Zone_AC + 2]
        else:
            if COI == CONCAVITY_STR:
                return df_Concavity_Sagging_acceptance.iloc[:, :2]
            else:
                if COI == SAGGING_STR:
                    return df_Concavity_Sagging_acceptance.iloc[:, 2:4]
                else:
                    if COI == PLANAR_STR:
                        return df_planar_acceptance.iloc[:, 2*Zone_AC:2*Zone_AC + 2]
                    else:
                        if COI == FORBIDDEN_STR:
                            return pd.DataFrame({'A': [FORBIDDEN_STR]},
                                                index=['a1'])
                        else:
                            return 'Nothing'

def Rejection(Height_Corrected, Length, AC_Table, Zone_AC):
    
    if type(AC_Table) is str:
        AC_Table = pd.DataFrame({'A': [FORBIDDEN_STR]},
                                                index=['a1'])
        return FORBIDDEN_STR
    if str(AC_Table.iloc[:1,:1].values) in FORBIDDEN_STR:
        return 'Rejected'
    else:
        if Height_Corrected > (AC_Table.iloc[:1,:1].values):
            return 'Rejected'
        else:
            if Length > AC_Table.iloc[9:,1:].values:
                return 'Rejected'
            else:
                for index in range (2, len(AC_Table)+1):
                    if ( Height_Corrected > AC_Table.iloc[index-1:index,:]['max_height'+str(Zone_AC)].values and Length > AC_Table.iloc[index-2:index-1,:]['max_length'+str(Zone_AC)].values ):
                        return 'Rejected'
                    else:
                        return 'Accepted'

"""
Maintenant que les indications sont classees rejetees ou acceptees il faut determiner si on peut reparer ou non les defauts
Pour cela on utilise la meme methode qu'auparavant:
-Calcul de la longueur d excavation minimale necessaire a la reparation & comparaison avec la longueur maximale autorisee
cette longueur depend de la variable PRTTR. La longueur max autorisee est dans 'Repair_data'. Sachant que dans tous les cas la longueur minimale d'excavation doit respectee
celle dans 'Repair_data'

-Ensuite si la repair est autorisee ou non on definie si la soudure est "Repair" ou "CutOut"

-La COI = 'Forbidden' implique un CutOut systematique

"""
def excavation_length(length,depth, Min_excavation_length):
    return max(length, Min_excavation_length) + 2*depth

def PR_TTR_OK(PRTTR, excavation_length, PR_Max_length, TTR_Max_length, OD):
    if PRTTR == 'PR':
        if excavation_length < PR_Max_length * OD * math.pi * 25.4:
            return 'PROK'
        else:
            return 'PRNOTOK'
    else:
        if PRTTR == 'TTR':
            if excavation_length < TTR_Max_length * OD * math.pi * 25.4:
                return 'TTROK'
            else:
                return 'TTRNOTOK'

def Repair_CutOut(PR_TTR_OK, Rejection, COI):
    if COI in FORBIDDEN_STR or COI == 'Nature not identified':
        return 'CutOut'
    else:
        if Rejection == 'Accepted':
            return Rejection
        else:
            if PR_TTR_OK == 'PROK':
                return 'Repair_as_PR'
            else:
                if PR_TTR_OK == 'TTROK':
                    return 'Repair_as_TTR'
                else:
                    return 'CutOut'
