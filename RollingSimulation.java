public class RollingSimulation {
  static final double g = 9.81;
  public static void main(String[] args) {
    double theta = Math.toRadians(30);
    double m = 1.0;
    double r = 0.1;
    double dt = 0.01;
    double tMax = 5.0;
    double I_solid = (2.0 / 5.0) * m * r * r;
    double I_hollow = (2.0 / 3.0) * m * r * r;
    System.out.println("SOLID SPHERE:");
    simulate(theta, m, r, I_solid, dt, tMax);
    System.out.println("\nHOLLOW SPHERE:");
    simulate(theta, m, r, I_hollow, dt, tMax);
  }
  static void simulate(double theta, double m, double r, double I, double dt, double tMax) {
    double s = 0;
    double v = 0;
    double alpha = 0;
    double omega = 0;
    for (double t = 0; t <= tMax; t += dt) {
      double a = (g * Math.sin(theta)) / (1 + (I / (m * r * r)));
      double v_mid = v + (a * dt / 2);
      double s_mid = s + (v * dt / 2);
      double omega_mid = omega + ((a / r) * dt / 2);
      double alpha_mid = alpha + (omega * dt / 2);
      s = s + v_mid * dt;
      v = v + a * dt;
      alpha = alpha + omega_mid * dt;
      omega = omega + (a / r) * dt;
      System.out.printf("t=%.2f s=%.4f v=%.4f%n", t, s, v);
    }
  }
}