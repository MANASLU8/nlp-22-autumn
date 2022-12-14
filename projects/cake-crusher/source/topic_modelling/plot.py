import matplotlib.pyplot as plt
import numpy as np

x = [2, 5, 10, 20, 40]
#y = [4899.91, 4700.91, 4755.29, 5122.79, 5804.85]
y = [4944.06, 4759.93, 4687.86, 4887.79, 5765.78]
plt.figure(figsize=(12, 7))
plt.plot(x, y, 'o-r', alpha=0.7, label="topics-perplexity", lw=5, mec='b', mew=2, ms=10)
plt.legend()
plt.grid(True)
plt.show()

#polynomial fit with degree = 4
model = np.poly1d(np.polyfit(x, y, 4))

#add fitted polynomial line to scatterplot
polyline = np.linspace(1, 41)
plt.scatter(x, y)
plt.plot(polyline, model(polyline))
plt.show()

# x = [5, 10, 20]
# y = [6701.77, 5804.85, 5362.12]
# plt.figure(figsize=(12, 7))
# plt.plot(x, y, 'o-r', alpha=0.7, label="perplexity_10_topics-max_iter", lw=5, mec='b', mew=2, ms=10)
# plt.legend()
# plt.grid(True)
# plt.show()
