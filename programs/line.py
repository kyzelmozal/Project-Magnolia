
import matplotlib.pyplot as plt
from scipy import stats

x = [8, 9, 14, 19, 21, 22, 30]
y = [3, 2, 2, 6, 7, 8, 12]

slope, intercept, r, p, std_err = stats.linregress(x, y)

def myfunc(x):
    return slope * x + intercept

mymodel = list(map(myfunc, x))

print(r ** 2)

plt.figure()
plt.scatter(x, y, marker="o")
plt.plot(x, mymodel)
plt.show(block=True)