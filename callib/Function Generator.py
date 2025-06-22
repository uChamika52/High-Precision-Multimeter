import numpy as np
import matplotlib.pyplot as plt

def parse_input(data):
    """
    Parses the input in the form 'x --> y' into two lists: x and y.
    """
    x_values = []
    y_values = []
    for line in data.splitlines():
        if ',' in line:
            x, y = line.split(',')
            x_values.append(float(x.strip()))
            y_values.append(float(y.strip()))
    return np.array(x_values), np.array(y_values)

# Input values as a multiline string
input_data = """
12.19,10.8
21.2,20.48
31.79,30.66
40.09,40.38
50.5,50.05
61,60.25
71.09,70.91
80.69,80.53
90.59,90.26
100.69,100.52
110.30,110.23
120.40,120.85
130.03,130.09
141,140.80
150.5,150.48
160.69,160.22
169.90,170.43
179.5,180.16
189.10,190.80
199.19,200.02
210.19,210.4
219.19,220.1
230.19,231.8
239.5,241.5
250.5,250.7
258.68,260.5
270.10,271.8
279.10,281.6
288.10,290.3
300.79,300.2
308.39,310.5
318.5,320.2
328.10,330.1
337.70,340.1
349.20,350.6
358.20,360.7
370.29,370.8
377.60,380.5
388.29,389.9
399.29,400.5
409.70,410.2
417.5,420.5
429.89,430.7
439.79,440.0
457.10,460.6
466.5,469.7
479.60,480.5
487.29,490.2
500.29,500.6
510.89,510.5
519.70,520
525.29,529.8
536.59,540.3
550.29,550.9
557.40,560
567.02,571.5
576.79,580.5
588.90,590.5
599.79,601.3
608.09,609.9
615.09,620.8
624.7,630.1
637.40,639.6
646.90,649.4
653.7,660.5
664.7,670.8
675.09,681.0
685.79,692
696.5,700.2
707.79,708.4
714.59,719.9
725.29,731.2
733.5,740.1
748.5,749
753.79,753.7
767.79,772.1
780.40,781.5
784.29,791.2
793.90,800.7
808.59,810.5
814.5,820.9
823.29,830.9
833.79,841.4
847.59,851.5
861.5,862.5
862.90,869.7
881.29,882.2
887.79,889.7
898.5,900.8
903.9,908.5
911,919.6
922.59,931.1
933.90,942.5
939.40,950.5
947.5,957.9
959.7,970
972.5,981.8
980.09,990
998.90,1002.3
"""

# Parse the input
x, y = parse_input(input_data)

# Fit a polynomial (adjust the degree as necessary)
degree = 3  # Change this to 2 or higher for nonlinear relationships
coefficients = np.polyfit(x, y, degree)

# Create the polynomial function
polynomial = np.poly1d(coefficients)

# Display the polynomial function
print("Fitted Polynomial Function:")
print(polynomial)

# Evaluate the polynomial at the input points
y_fitted = polynomial(x)

# Plot the data and the polynomial
plt.scatter(x, y, color='blue', label='Original Data')
plt.plot(x, y_fitted, color='red', label=f'Fitted Polynomial (Degree {degree})')
plt.xlabel('Input (x)')
plt.ylabel('Output (y)')
plt.legend()
plt.title('Polynomial Fit')
plt.grid(True)
plt.show()