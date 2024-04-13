import matplotlib.pyplot as plt
import numpy as np

actuated = {'queue': 96212, 'speed': 5.869}
ai = {'queue': 57623, 'speed': 7.237}

passengers = [2040, 2190, 2085, 2295, 2415, 2430, 2580, 2460, 2625, 3045, 3285,
              3375, 3255, 3135, 2880, 2880, 2820, 2775, 2925, 2970, 3075, 3015, 3015, 3105]
trucks = [160, 172, 164, 180, 189, 190, 202, 193, 207, 237, 256, 264,
          254, 246, 226, 226, 221, 218, 229, 233, 240, 235, 235, 242,]
buses = [26, 26, 26, 26, 26, 26, 26, 26, 26, 26, 26,
         26, 26, 26, 26, 26, 26, 26, 26, 26, 26, 26, 26, 26,]

y = np.vstack([passengers, trucks, buses])

plt.stackplot(np.arange(0, 12.0, 0.5), y, colors=[
              "#C13A22", "#ff964f", "#56AE57"])
plt.ylabel('vehicles')
plt.xlabel('hours')
plt.show()

# plt.figure(figsize=(3, 5))
# bar = plt.bar(['Actuated System', 'AI System'],
#               [actuated['queue'],
#                ai['queue']],
#               color=["#C13A22", "#56AE57"],
#               width=0.9,
#               )
# plt.title('Total queue length')
# plt.yticks(np.arange(0, 110000, 25000))
# plt.ylabel('vehicles')
# plt.bar_label(bar)
# plt.gcf().savefig('queue length', bbox_inches='tight')
#
# plt.figure(figsize=(3, 5))
# bar = plt.bar(['Actuated System', 'AI System'],
#               [actuated['speed'],
#                ai['speed']],
#               color=["#C13A22", "#56AE57"],
#               width=0.9,
#               )
# plt.title('Mean speed of vehicles')
# plt.yticks(np.arange(0.0, 8.1, 2.0))
# plt.ylabel('m/s')
# plt.bar_label(bar)
# plt.gcf().savefig('mean speed', bbox_inches='tight')
