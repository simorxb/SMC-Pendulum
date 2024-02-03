import matplotlib.pyplot as plt
import pycollimator as collimator

# Load token for Collimator from file
token_file = open("token.txt", 'r')
token = token_file.read()

# Load model from Collimator
project_uuid = "221181d1-4494-4cf8-a58a-61345a7aa14c"
collimator.set_auth_token(token, project_uuid)
model = collimator.load_model("Pendulum - Sliding Mode Control")

# Create array of mass values for robustness analysis
m_V = [0.1, 0.5, 1.2]

# Create array of results
res_V = []

# Simulate for each mass value and store results in res_V
for m in m_V:
    sim = collimator.run_simulation(model, parameters = {'m': m, 'W':1.3,'lambda_':2.5, "tau_d":0.1})
    res = sim.results.to_pandas()
    res_V.append(res)

# Create figure
plt.figure()

# Plot response for each mass value and setpoint in 1st subplot
plt.subplot(2, 1, 1)

for idx in range(len(m_V)):
    plt.plot(res_V[idx].index, res_V[idx]["Pendulum.Theta"], label=f"Response - Mass = {m_V[idx]} kg")

plt.plot(res_V[0].index, res_V[0]["Setpoint_Filter.out_0"], "--", label="Setpoint")
plt.xlabel("Time [s]")
plt.ylabel("Theta [deg]")
plt.legend()
plt.grid()

# Plot controller output for each mass value
plt.subplot(2, 1, 2)

for idx in range(len(m_V)):
    plt.plot(res_V[idx].index, res_V[idx]["Adder_3.out_0"], label=f"Tau - Mass = {m_V[idx]} kg")

plt.xlabel("Time [s]")
plt.ylabel("Tau [Nm]")
plt.legend()
plt.grid()

# Show plots
plt.show()