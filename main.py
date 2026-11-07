import numpy as np
import matplotlib.pyplot as plt

# Parameters
A = 10
B = 25
C = 8 / 3
dt = 0.001
t0 = 0
t_end = 30
x0, y0, z0 = 1.0, 1.0, 1.0

# Lorenz derivatives
def derivatives(x, y, z):
    dxdt = A * y - A * x
    dydt = -x * z + B * x - y
    dzdt = x * y - C * z
    return dxdt, dydt, dzdt

# Time steps
steps = int((t_end - t0) / dt)

# Euler Method
def euler(x0, y0, z0, steps, dt):
    x, y, z = x0, y0, z0
    xs, zs = [x], [z]
    for _ in range(steps):
        dx, dy, dz = derivatives(x, y, z)
        x += dt * dx
        y += dt * dy
        z += dt * dz
        xs.append(x)
        zs.append(z)
    return np.array(xs), np.array(zs)

# Midpoint Method
def midpoint(x0, y0, z0, steps, dt):
    x, y, z = x0, y0, z0
    xs, zs = [x], [z]
    for _ in range(steps):
        dx1, dy1, dz1 = derivatives(x, y, z)
        xm = x + 0.5 * dt * dx1
        ym = y + 0.5 * dt * dy1
        zm = z + 0.5 * dt * dz1
        dx2, dy2, dz2 = derivatives(xm, ym, zm)
        x += dt * dx2
        y += dt * dy2
        z += dt * dz2
        xs.append(x)
        zs.append(z)
    return np.array(xs), np.array(zs)

# RK4 Method
def rk4(x0, y0, z0, steps, dt):
    x, y, z = x0, y0, z0
    xs, zs = [x], [z]
    for _ in range(steps):
        k1x, k1y, k1z = derivatives(x, y, z)

        k2x, k2y, k2z = derivatives(
            x + 0.5*dt*k1x, y + 0.5*dt*k1y, z + 0.5*dt*k1z)

        k3x, k3y, k3z = derivatives(
            x + 0.5*dt*k2x, y + 0.5*dt*k2y, z + 0.5*dt*k2z)

        k4x, k4y, k4z = derivatives(
            x + dt*k3x, y + dt*k3y, z + dt*k3z)

        x += (dt / 6) * (k1x + 2*k2x + 2*k3x + k4x)
        y += (dt / 6) * (k1y + 2*k2y + 2*k3y + k4y)  # düzeltildi
        z += (dt / 6) * (k1z + 2*k2z + 2*k3z + k4z)
        xs.append(x)
        zs.append(z)
    return np.array(xs), np.array(zs)

# Solve
euler_x,   euler_z   = euler(x0, y0, z0, steps, dt)
mid_x,     mid_z     = midpoint(x0, y0, z0, steps, dt)
rk4_x,     rk4_z     = rk4(x0, y0, z0, steps, dt)

# Plot
fig, axes = plt.subplots(1, 3, figsize=(18, 6))
fig.suptitle("Lorenz Attractor  —  z(x)  phase plot\n"
             f"A={A}, B={B}, C={C:.4f}, dt={dt}, IC: (1,1,1)",
             fontsize=14, fontweight='bold')

methods = [
    ("Euler",    euler_x,   euler_z,   "#e74c3c"),
    ("Midpoint", mid_x,     mid_z,     "#2ecc71"),
    ("RK4",      rk4_x,     rk4_z,     "#3498db"),
]

for ax, (name, xs, zs, color) in zip(axes, methods):
    ax.plot(xs, zs, lw=0.4, color=color, alpha=0.85)
    ax.set_title(name, fontsize=13, fontweight='bold')
    ax.set_xlabel("x", fontsize=11)
    ax.set_ylabel("z", fontsize=11)
    ax.grid(True, linestyle='--', alpha=0.4)
    ax.tick_params(labelsize=9)

plt.tight_layout()
plt.savefig("lorenz_phase_plot.png", dpi=150, bbox_inches='tight')
plt.show()
print("Plot saved.")