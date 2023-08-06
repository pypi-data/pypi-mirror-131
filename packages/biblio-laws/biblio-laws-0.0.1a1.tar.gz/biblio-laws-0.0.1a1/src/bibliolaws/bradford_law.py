import math
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from numpy import arange
from collections.abc import Iterable

class BradfordLaw:
    def __init__(self,data):
        self.data=data
        self.new_data=[]
        self.make_table()

    def aggA(self, end_index):
        sum = 0
        for i in range(end_index + 1):
            sum += self.data[i][0]
        return sum

    def aggAB(self,end_index):
        sum = 0
        for i in range(end_index + 1):
            sum += self.data[i][0] * self.data[i][1]
        return sum

    def make_table(self):
        self.new_data = []
        for idx, ls in enumerate(self.data):
            A = ls[0]
            B = ls[1]
            C = self.aggA( idx)
            D = self.aggAB(idx)
            self.new_data.append([A, B, C, D])
        return self.new_data

    def print_table(self):
        print("A\tB\tC\tD")
        for ls in self.new_data:
            A = ls[0]
            B = ls[1]
            C = ls[2]
            D = ls[3]
            print(f'{A}\t{B}\t{C}\t{D}')

    def zone_analysis(self,total_year=4):
        j1 = 0
        j2 = 0
        j3 = 0
        p1 = 0
        p2 = 0
        p3 = 0
        for ls in self.new_data:
            A = ls[0]
            B = ls[1]
            B_ = B * 1.0 / total_year
            if B_ > 4:
                j1 += A
                p1 += A * B
            elif B_ > 1 and B_ <= 4:
                j2 += A
                p2 += A * B
            elif B_ <= 1:
                j3 += A
                p3 += A * B
        js=[j1,j2,j3]
        ps=[p1,p2,p3]
        zone=['>4','1~4','<=1']

        print("Zone\tNo. Paper/Year\tNo. Journal\tNo. Paper")
        for x in range(3):
            print(f'{x}\t{zone[x]}\t{js[x]}\t{ps[x]}')
        # print(j1, j2, j3)
        # print(p1, p2, p3)

        return [j1,j2,j3],[p1,p2,p3]

    def get_column(self,name):
        index=0
        if name=="A":
            index=0
        elif name=="B":
            index=1
        elif name=="C":
            index=2
        elif name=="D":
            index=3
        list_r=[]
        for ls in self.new_data:
            list_r.append(ls[index])
        return list_r

    def figure_analysis(self, show_figure=True):
        x = []
        y = []
        for ls in self.new_data:
            A = ls[0]
            B = ls[1]
            C = ls[2]
            D = ls[3]
            x.append(math.log(C, math.e))
            y.append(D)
        if show_figure:
            plt.plot(x, y)
            plt.title("Publication distribution based on Bradford's Law")
            plt.xlabel("ln n")
            plt.ylabel("R(n)")
            plt.show()
        return x, y

    def fit_smarikov(self,x,y,maxfev=4000):
        def objective(x,K,q1,q2,b):
            if isinstance(x, Iterable):
                list_y = []
                for xx in x:
                    t = q1 * xx + q2 * math.pow(math.e, -b * xx)
                    if t <= 0:
                        t = 0.001
                    list_y.append(K * math.log(t, math.e))
                return list_y
            else:
                t = q1 * x + q2 * math.pow(math.e, -b * x)
                if t <= 0:
                    t = 0.001
                return K*math.log(t,math.e)

        popt1, _ = curve_fit(objective, x, y, maxfev=maxfev)
        K, q1,q2,b = popt1
        print(popt1)
        y_pred = []
        for xx in x:
            y_pred.append(objective(xx, K,q1,q2,b))
        return y_pred,K,q1,q2,b


    def fit_brookes(self,x,y,c=0,maxfev=4000):

        def objective1(x,a,b):
            if isinstance(x,Iterable):
                list_y=[]
                for xx in x:
                    list_y.append(a*math.pow(xx,b))
                return list_y
            else:
                return a*math.pow(x,b)

        def objective2(x, K, S):
            list_y=[]
            # print(x)
            if isinstance(x, Iterable):
                for xx in x:
                    # print("xx = ",xx)
                    t = xx * 1.0 / S
                    if t <= 0:
                        t = 0.01
                    list_y.append(K * math.log(t, math.e))

                return list_y
            else:
                t = x * 1.0 / S
                if t <= 0:
                    t = 0.01
                return K*math.log(t, math.e)

        split_index=0
        #print("split_index: ",split_index)
        for idx,xx in enumerate(x):
            if xx>c:
                split_index=idx-1
                break

        x1=x[0:split_index]
        x2=x[split_index:]
        #print(x1)
        #print(x2)
        y1=y[0:split_index]
        y2=y[split_index:]
        # 1<=n<c
        popt1, _ = curve_fit(objective1, x1, y1, maxfev=maxfev)
        a, b = popt1
        x1_r=arange(min(x1),max(x1)+1,1)
        y_pred1 = []
        for xx in x1_r:
            y_pred1.append(objective1(xx, a, b))
        # c<=n<=N
        popt2, _ = curve_fit(objective2, x2, y2 ,maxfev=maxfev)
        K, S = popt2
        x2_r = arange(min(x2)-1, max(x2), 1)
        y_pred2 = []
        for xx in x2_r:
            y_pred2.append(objective2(xx, K,S))

        return x1_r,y_pred1,x2_r,y_pred2,a,b,K,S






