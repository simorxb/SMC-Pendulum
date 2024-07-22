import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
import pycollimator as collimator

# Load token for Collimator from file
token_file = open("token.txt", 'r')
token = token_file.read()

# Load model from Collimator
project_uuid = "221181d1-4494-4cf8-a58a-61345a7aa14c"
collimator.set_auth_token(token, project_uuid)
model = collimator.load_model("Pendulum - Sliding Mode Control")

# Create array of mass values for robustness analysis
m_V = [0.5]

# Create array of results
res_V = []

# Simulate for each mass value and store results in res_V
for m in m_V:
    sim = collimator.run_simulation(model, parameters={'m': m, 'W': 1.3, 'lambda': 2.5, "tau_d": 0.1})
    res = sim.results.to_pandas()
    res_V.append(res)

# Extract time and theta values
time = res_V[0].index
theta = res_V[0]["Pendulum.Theta"]
setpoint = res_V[0]["Setpoint_Filter.out_0"]
tau = res_V[0]["Adder_3.out_0"]

# Create figure
fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(8, 12))

# Initialize plots
line1, = ax1.plot([], [], label="Response - Mass = 0.5 kg")
setpoint_line, = ax1.plot([], [], "--", label="Setpoint")
line2, = ax2.plot([], [], label="Tau - Mass = 0.5 kg")

pendulum_line, = ax3.plot([], [], 'o-', lw=2)
ax3.set_xlim(-1.1, 1.1)
ax3.set_ylim(-1.1, 1.1)
ax3.set_aspect('equal', adjustable='box')
ax3.grid()

# Animation initialization function
def init():
    ax1.set_xlim(0, max(time))
    ax1.set_ylim(min(theta)-10, max(theta)+30)
    ax1.set_xlabel("Time [s]")
    ax1.set_ylabel("Theta [deg]")
    ax1.legend()
    ax1.grid()
    
    ax2.set_xlim(0, max(time))
    ax2.set_ylim(min(tau)-1, max(tau)+4)
    ax2.set_xlabel("Time [s]")
    ax2.set_ylabel("Tau [Nm]")
    ax2.legend()
    ax2.grid()
    
    pendulum_line.set_data([], [])
    return line1, setpoint_line, line2, pendulum_line

# Animation update function
def update(frame):
    line1.set_data(time[:frame], theta.iloc[:frame])
    setpoint_line.set_data(time[:frame], setpoint.iloc[:frame])
    line2.set_data(time[:frame], tau.iloc[:frame])

    # Update pendulum plot
    x = np.sin(np.radians(theta.iloc[frame]))
    y = -np.cos(np.radians(theta.iloc[frame]))
    pendulum_line.set_data([0, x], [0, y])
    
    return line1, setpoint_line, line2, pendulum_line

# Create animation
ani = animation.FuncAnimation(fig, update, frames=len(time), init_func=init, blit=True, interval=10)

# Show plots
plt.show()