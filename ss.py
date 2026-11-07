import numpy as np
import matplotlib.pyplot as plt


def simulate_orbits():
    G = 6.6743e-11
    M_s = 1.989e30
    M_z = 5.972e24
    M_k = 7.347e22
    R_ZS = 1.5e11
    R_ZK = 3.844e8

    v_earth = np.sqrt(G * M_s / R_ZS)
    v_moon_rel = np.sqrt(G * M_z / R_ZK)

    pos_z = np.array([R_ZS, 0.0])
    pos_k = np.array([R_ZS + R_ZK, 0.0])
    vel_z = np.array([0.0, v_earth])
    vel_k = np.array([0.0, v_earth + v_moon_rel])

    dt = 3600
    days = 365
    t_max = days * 24 * 3600
    n_steps = int(t_max / dt)

    earth_path = np.zeros((n_steps, 2))
    moon_path = np.zeros((n_steps, 2))

    def get_accelerations(p_z, p_k):
        r_z_norm = np.linalg.norm(p_z)
        r_k_norm = np.linalg.norm(p_k)
        r_kz = p_k - p_z
        r_kz_norm = np.linalg.norm(r_kz)

        a_z = (-G * M_s * p_z / (r_z_norm ** 3)) + (G * M_k * r_kz / (r_kz_norm ** 3))
        a_k = (-G * M_s * p_k / (r_k_norm ** 3)) - (G * M_z * r_kz / (r_kz_norm ** 3))
        return a_z, a_k

    for i in range(n_steps):
        earth_path[i] = pos_z
        moon_path[i] = pos_k

        a_z, a_k = get_accelerations(pos_z, pos_k)

        pos_z_mid = pos_z + vel_z * (dt / 2)
        vel_z_mid = vel_z + a_z * (dt / 2)
        pos_k_mid = pos_k + vel_k * (dt / 2)
        vel_k_mid = vel_k + a_k * (dt / 2)

        a_z_mid, a_k_mid = get_accelerations(pos_z_mid, pos_k_mid)

        pos_z = pos_z + vel_z_mid * dt
        vel_z = vel_z + a_z_mid * dt
        pos_k = pos_k + vel_k_mid * dt
        vel_k = vel_k + a_k_mid * dt

    visual_scale = 40
    rel_moon_pos = moon_path - earth_path
    scaled_moon_path = earth_path + (rel_moon_pos * visual_scale)

    plt.figure(figsize=(10, 10))
    scale_units = 1e9

    plt.plot(earth_path[:, 0] / scale_units, earth_path[:, 1] / scale_units, 'b-', label='Earth Path')
    plt.plot(scaled_moon_path[:, 0] / scale_units, scaled_moon_path[:, 1] / scale_units, 'r--',
             label=f'Moon Path (Scaled x{visual_scale})')
    plt.plot(0, 0, 'yo', markersize=15, label='Sun')

    plt.title(f"Heliocentric View: Moon's Trajectory relative to Sun ({days} days)")
    plt.xlabel('X Position (10^6 km)')
    plt.ylabel('Y Position (10^6 km)')
    plt.legend()
    plt.grid(True)
    plt.axis('equal')
    plt.show()


if __name__ == "__main__":
    simulate_orbits()