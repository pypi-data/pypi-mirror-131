import matplotlib.pyplot as plt
import math
from collections.abc import Iterable
from scipy.optimize import curve_fit


class ZipfLaw:
    def __init__(self,data):
        self.data=data
        self.new_data=[]
        self.make_table()

    def make_table(self):
        self.new_data=[]
        for idx,ls in enumerate(self.data):
            A=ls[0]
            B=ls[1]
            C=math.log(A,math.e)
            D=math.log(B,math.e)
            self.new_data.append([A,B,C,D])

    def print_table(self):
        print("A\tB\tC\tD")
        for ls in self.new_data:
            A = ls[0]
            B = ls[1]
            C = ls[2]
            D = ls[3]
            print(f'{A}\t{B}\t{round(C,4)}\t{round(D,4)}')

    def plot(self,show_figure=True):
        x=[]
        y=[]
        for ls in self.new_data:
            A = ls[0]
            B = ls[1]
            C = ls[2]
            D = ls[3]
            x.append(C)
            y.append(D)
        if show_figure:
            plt.plot(x,y)
            plt.title("Zipf's Law")
            plt.xlabel("ln r")
            plt.ylabel("ln f")
            plt.show()
        return x,y

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

    def fit(self,x,y,maxfev=4000):
        b=1
        def objective(x,C):
            # = e^(lnC-ln(r))
            if isinstance(x, Iterable):
                list_y = []
                for xx in x:
                    if xx<=0:
                        xx=0.001
                    list_y.append(math.pow(math.e,math.log(C,math.e)-math.log(xx,math.e)))
                return list_y
            else:
                if x<=0:
                    x=0.001
                return math.pow(math.e,math.log(C,math.e)-math.log(x,math.e))

        popt1, _ = curve_fit(objective, x, y, maxfev=maxfev)
        C = popt1
        print(popt1)
        y_pred = []
        for xx in x:
            y_pred.append(objective(xx, C))
        return y_pred, b,C

    def fit_joss(self,x,y,maxfev=4000):
        def objective(x,b,C):
            # = e^(lnC-b*ln(r))
            if isinstance(x, Iterable):
                list_y = []
                for xx in x:
                    if xx<=0:
                        xx=0.001
                    list_y.append(math.pow(math.e,math.log(C,math.e)-b*math.log(xx,math.e)))
                return list_y
            else:
                if x<=0:
                    x=0.001
                return math.pow(math.e,math.log(C,math.e)-b*math.log(x,math.e))

        popt1, _ = curve_fit(objective, x, y, maxfev=maxfev)
        b,C = popt1
        print(popt1)
        y_pred = []
        for xx in x:
            y_pred.append(objective(xx, b,C))
        return y_pred, b,C

    def fit_mandelbrot(self,x,y,maxfev=4000):
        def objective(x,a,b,C):
            # = e^(lnC-b*ln(r))
            if isinstance(x, Iterable):
                list_y = []
                for xx in x:
                    t=xx+a
                    if t<=0:
                        t=0.001
                    list_y.append(math.pow(math.e,math.log(C,math.e)-b*math.log(t,math.e)))
                return list_y
            else:
                t=x+a
                if t<=0:
                    t=0.001
                return math.pow(math.e,math.log(C,math.e)-b*math.log(t,math.e))

        popt1, _ = curve_fit(objective, x, y, maxfev=maxfev)
        a, b,C = popt1
        print(popt1)
        y_pred = []
        for xx in x:
            y_pred.append(objective(xx,a, b,C))
        return y_pred, a, b,C



