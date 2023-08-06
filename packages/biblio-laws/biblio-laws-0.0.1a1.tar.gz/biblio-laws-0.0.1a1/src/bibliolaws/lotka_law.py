import matplotlib.pyplot as plt
import math
from collections.abc import Iterable
from scipy.optimize import curve_fit

class LotkaLaw:
    def __init__(self,data):
        self.data=data
        self.new_data=[]
        self.make_table()

    def aggC(self,end_index,total_author):
        sum = 0
        for i in range(end_index + 1):
            sum +=  self.data[i][1]*1.0/total_author
        return sum

    def make_table(self):
        self.new_data=[]
        total_author=0
        for ls in self.data:
            total_author+=ls[1]
        for idx,ls in enumerate(self.data):
            A=ls[0]
            B=ls[1]
            C=B*1.0/total_author
            D=self.aggC(idx,total_author)
            self.new_data.append([A,B,C,D])

    def print_table(self):
        print("A\tB\tC\tD")
        for ls in self.new_data:
            A = ls[0]
            B = ls[1]
            C = ls[2]
            D = ls[3]
            print(f'{A}\t{B}\t{round(C,4)}\t{round(D,4)}')

    def fit_with_C(self,x,y,maxfev=4000,C=0.6079):
        def objective(x,a):
            # = e^(ln(C)-a*ln(x))
            if isinstance(x, Iterable):
                list_y = []
                for xx in x:
                    if xx<=0:
                        xx=0.001
                    list_y.append(math.pow(math.e,math.log(C,math.e)-a*math.log(xx,math.e)))
                return list_y
            else:
                if x<=0:
                    x=0.001
                return math.pow(math.e,math.log(C,math.e)-a*math.log(x,math.e))

        popt1, _ = curve_fit(objective, x, y, maxfev=maxfev)
        a = popt1
        print(popt1)
        y_pred = []
        for xx in x:
            y_pred.append(objective(xx, a))
        return y_pred, a,C

    def fit(self,x,y,maxfev=4000):
        def objective(x,a,C):
            # = e^(ln(C)-a*ln(x))
            if isinstance(x, Iterable):
                list_y = []
                for xx in x:
                    if xx<=0:
                        xx=0.001
                    list_y.append(math.pow(math.e,math.log(C,math.e)-a*math.log(xx,math.e)))
                return list_y
            else:
                if x<=0:
                    x=0.001
                return math.pow(math.e,math.log(C,math.e)-a*math.log(x,math.e))

        popt1, _ = curve_fit(objective, x, y, maxfev=maxfev)
        a,C = popt1
        # print(popt1)
        y_pred = []
        for xx in x:
            y_pred.append(objective(xx, a,C))
        return y_pred, a,C

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

    def plot(self,show_figure=True):
        x=[]
        y=[]
        for ls in self.new_data:
            A = ls[0]
            B = ls[1]
            C = ls[2]
            D = ls[3]
            x.append(math.log(A,math.e))
            y.append(math.log(C,math.e))
        if show_figure:
            plt.plot(x,y)
            plt.title("Lotka's Law")
            plt.xlabel("ln (No. Publication)")
            plt.ylabel("ln (Pct. Author)")
            plt.show()
        return x,y
