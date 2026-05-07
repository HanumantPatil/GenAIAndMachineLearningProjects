import numpy as np
import pandas as pd
from pathlib import Path

def gradient_descent(x, y, lr=0.01, epochs=3000):
    m, b = 0.0, 0.0  # Initialize parameters
    # SCALING x and y with min-max Scaling
    x_scaled = (x - np.min(x)) / (np.max(x) - np.min(x))
    y_scaled = (y - np.min(y)) / (np.max(y) - np.min(y))

    for epoch in range(epochs):
        y_pred = m * x_scaled + b  # Predicted values
        error =  y_scaled - y_pred  # Error
        cost = np.mean(error ** 2)  # Mean Squared Error
        dm = -2* np.mean(x_scaled * error)  # Gradient w.r.t m
        db = -2 * np.mean(error)  # Gradient w.r.t b
        b -= db * lr  # Update b
        m -= dm * lr
        if epoch % 100 == 0:
            print(f"m: {m:.4f}, b: {b:.4f}, Epoch {epoch}, Cost: {cost:.4f}")
    
    # Scale back the Coefficients to original scale
    x_min, x_max = np.min(x), np.max(x)
    y_min, y_max = np.min(y), np.max(y)
    b_original = b * (y_max - y_min) + y_min - m * (y_max - y_min) * x_min / (x_max - x_min)
    m_original = m * (y_max - y_min) / (x_max - x_min)
    return m_original, b_original

if __name__ == "__main__":

    # # Example data
    # x = np.array([1, 2, 3, 4, 5])
    # y = np.array([5, 7, 9, 11, 13])
    # # Run gradient descent
    # gradient_descent(x, y)

    data_file = Path(__file__).resolve().parent / "home_prices.csv"
    df = pd.read_csv(data_file)
    x = df["area_sqr_ft"].to_numpy()
    y = df["price_lakhs"].to_numpy()
    m, b = gradient_descent(x, y)

    print(f"Final parameters: m = {m}, b = {b}")
