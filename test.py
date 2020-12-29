import matplotlib.pyplot as plt

x = ("Jan","Feb","Mar","Apr","Mai")
y = (1,2,3,4,5)

plt.bar(x,y,align='center') # A bar chart
plt.xlabel('Bins')
plt.ylabel('Frequency')

plt.show()