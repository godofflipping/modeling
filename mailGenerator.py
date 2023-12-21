import numpy as np

sampleList = [1, 2, 3]
randomNumberList = np.random.choice(sampleList, 10000, p=[0.80, 0.15, 0.05])

with open('mail_10000.txt', 'w') as file:
    for number in randomNumberList:
        file.write(str(number) + " ")