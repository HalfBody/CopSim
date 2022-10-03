from simpful import *
import server_req
import server


class Fuzzy():
    def __init__(self, LR_arr, LRF_arr):
        self.FS = FuzzySystem()

        LR_n = TrapezoidFuzzySet(a=0, b=0, c=LR_arr[0], d=LR_arr[1], term = 'n')
        LR_m = TrapezoidFuzzySet(a=LR_arr[2], b=LR_arr[3], c=LR_arr[4], d=LR_arr[5], term = 'm')
        LR_f = TrapezoidFuzzySet(a=LR_arr[6], b=LR_arr[7], c=2, d=2, term = 'f')

        LRF_n = TrapezoidFuzzySet(a=0, b=0, c=LRF_arr[0], d=LRF_arr[1], term = 'n')
        LRF_m = TrapezoidFuzzySet(a=LRF_arr[2], b=LRF_arr[3], c=LRF_arr[4], d=LRF_arr[5], term = 'm')
        LRF_f = TrapezoidFuzzySet(a=LRF_arr[6], b=LRF_arr[7], c=2, d=2, term = 'f')

        self.FS.add_linguistic_variable('L', LinguisticVariable([LR_n, LR_m, LR_f], concept="L_dist", universe_of_discourse=[0,2]))
        self.FS.add_linguistic_variable('LF', LinguisticVariable([LRF_n, LRF_m, LRF_f], concept="Lf_dist", universe_of_discourse=[0,2]))
        self.FS.add_linguistic_variable('F', LinguisticVariable([LRF_n, LRF_m, LRF_f], concept="F_dist", universe_of_discourse=[0,2]))
        self.FS.add_linguistic_variable('RF', LinguisticVariable([LRF_n, LRF_m, LRF_f], concept="RF_dist", universe_of_discourse=[0,2]))
        self.FS.add_linguistic_variable('R', LinguisticVariable([LR_n, LR_m, LR_f], concept="R_dist", universe_of_discourse=[0,2]))

        L = TrapezoidFuzzySet(a=-180, b=-180, c=-30, d=-20, term = 'L')
        LF = TrapezoidFuzzySet(a=-25, b=-20, c=-10, d=-5, term = 'LF')
        F = TriangleFuzzySet(a=-10, b=0, c=10, term='F')
        RF = TrapezoidFuzzySet(a=5, b=10, c=20, d=25, term = 'RF')
        R = TrapezoidFuzzySet(a=20, b=30, c=180, d=180, term = 'R')
        self.FS.add_linguistic_variable('target_angle', LinguisticVariable([L, LF, F, RF, R], concept='angle to target', universe_of_discourse=[-180,180]))

        LS = TrapezoidFuzzySet(a=-2, b=-1.5, c=-1, d=-0.5, term = 'LS')
        LM = TrapezoidFuzzySet(a=-1.5, b=-1, c=-0.5, d=-0, term = 'LM')
        F = TriangleFuzzySet(a=-0.5, b=0, c=0.5, term='F')
        RM = TrapezoidFuzzySet(a=0, b=0.5, c=1, d=1.5, term = 'RM')
        RS = TrapezoidFuzzySet(a=0.5, b=1, c=1.5, d=2, term = 'RS')
        self.FS.add_linguistic_variable('angle', LinguisticVariable([LS, LM, F, RM, RS], concept='turn angle', universe_of_discourse=[-45,45]))

        slow = TriangleFuzzySet(a=1, b=1.5, c=2, term='slow')
        normal = TriangleFuzzySet(a=2.5, b=3, c=3.5, term='normal')
        self.FS.add_linguistic_variable('speed', LinguisticVariable([slow, normal], concept='speed', universe_of_discourse=[0,3]))

        rules = []
        rules.append('IF (L IS n) THEN (angle IS RM)')
        rules.append('IF (LF IS n) THEN (angle IS RM)')
        rules.append('IF (RF IS n) THEN (angle IS LM)')
        rules.append('IF (R IS n) THEN (angle IS LM)')
        rules.append('IF (L IS n) AND (LF IS n) AND (F IS n) THEN (angle IS RS)')
        rules.append('IF (LF IS n) AND (F IS n) THEN (angle IS RS)')
        rules.append('IF (R IS n) AND (RF IS n) AND (F IS n) THEN (angle IS LS)')
        rules.append('IF (RF IS n) AND (F IS n) THEN (angle IS LS)')
        rules.append('IF (L IS n) AND (LF IS n) THEN (angle IS RS)')
        rules.append('IF (R IS n) AND (RF IS n) THEN (angle IS LS)')

        rules.append('IF (target_angle IS L) THEN (angle IS LS)')
        rules.append('IF (target_angle IS LF) THEN (angle IS LM)')
        rules.append('IF (target_angle IS R) THEN (angle IS RS)')
        rules.append('IF (target_angle IS RF) THEN (angle IS RM)')
        rules.append('IF (target_angle IS F) THEN (angle IS F)')

        rules.append('IF (LF IS n) AND (RF IS n) AND (target_angle IS LF) THEN (angle IS LM)')
        rules.append('IF (LF IS n) AND (RF IS n) AND (target_angle IS RF) THEN (angle IS RM)')
        rules.append('IF (LF IS n) AND (RF IS n) AND (target_angle IS L) THEN (angle IS LS)')
        rules.append('IF (LF IS n) AND (RF IS n) AND (target_angle IS R) THEN (angle IS RS)')
        rules.append('IF (LF IS n) AND (L IS n) AND (target_angle IS L) THEN (angle IS LS)')
        rules.append('IF (RF IS n) AND (R IS n) AND (target_angle IS R) THEN (angle IS RS)')
        rules.append('IF (LF IS n) AND (RF IS n) AND (target_angle IS F) THEN (angle IS LS)')

        rules.append('IF (LF IS n) THEN (speed IS slow)')
        rules.append('IF (RF IS n) THEN (speed IS slow)')
        rules.append('IF (L IS n) AND (LF IS n) AND (RF IS n) THEN (speed IS slow)')
        rules.append('IF (R IS n) AND (LF IS n) AND (RF IS n) THEN (speed IS slow)')

        rules.append('IF (target_angle IS L) THEN (speed IS slow)')
        rules.append('IF (target_angle IS LF) THEN (speed IS normal)')
        rules.append('IF (target_angle IS R) THEN (speed IS slow)')
        rules.append('IF (target_angle IS RF) THEN (speed IS normal)')
        rules.append('IF (target_angle IS F) THEN (speed IS normal)')

        self.FS.add_rules(rules)


    def get_lidar_data(self, sim):
        lidar_data = sim.get_lidar_data()
        r, rf, f, lf, l = [], [], [], [], []
        
        for i in range(len(lidar_data)):
            if i >= 114 and i < 205:
                r.append(lidar_data[i])
            elif i >= 205 and i < 296:
                rf.append(lidar_data[i])
            elif i >= 296 and i < 387:
                f.append(lidar_data[i])
            elif i >= 387 and i < 478:
                lf.append(lidar_data[i])
            elif i >= 479 and i < 570:
                l.append(lidar_data[i])

        r_temp, rf_temp, f_temp, lf_temp, l_temp = [], [], [], [], []

        for i in range(len(r)):
            if 0.0 < r[i] <= 1.5:
                r_temp.append(r[i])
            else:
                r_temp.append(1.5)
            if 0.0 < rf[i] <= 1.5:
                rf_temp.append(rf[i])
            else:
                rf_temp.append(1.5)
            if 0.0 < l[i] <= 1.5:
                l_temp.append(l[i])
            else:
                l_temp.append(1.5)
            if 0.0 < lf[i] <= 1.5:
                lf_temp.append(lf[i])
            else:
                lf_temp.append(1.5)
            if 0.0 < f[i] <= 1.5:
                f_temp.append(f[i])
            else:
                f_temp.append(1.5)

        l_data = min(l_temp)
        lf_data = min(lf_temp)
        f_data = min(f_temp)
        rf_data = min(rf_temp)
        r_data = min(r_temp)

        return [l_data, lf_data, f_data, rf_data, r_data]
        
        
    def fuz_log(self, lidar_data, target_angle, sim):
        lidar_data = self.get_lidar_data(sim)

        self.FS.set_variable("L", lidar_data[0])
        self.FS.set_variable("LF", lidar_data[1])
        self.FS.set_variable("F", lidar_data[2])
        self.FS.set_variable("RF", lidar_data[3])
        self.FS.set_variable("R", lidar_data[4])
        self.FS.set_variable("target_angle", target_angle)

        #server_req.print_to_console(f'Lidar data: {lidar_data[0]}, {lidar_data[1]}, {lidar_data[2]}, {lidar_data[3]}, {lidar_data[4]}\n')

        return self.FS.Mamdani_inference(['angle', 'speed'])
