import javax.swing.*;
import java.awt.*;
public class StringSimulation extends JPanel {
    static final int N = 100;
    static final double L = 1.0;
    static final double T = 1.0;
    static final double rho = 1.0;
    static final double c = Math.sqrt(T / rho);
    static final double dx = L / N;
    static final double dt = 0.0001;
    double[] u = new double[N + 1];
    double[] v = new double[N + 1];
    public StringSimulation() {
        for (int i = 0; i <= N; i++) {
            u[i] = Math.sin(Math.PI * i * dx / L);
            v[i] = 0.0;
        }
        u[0] = 0.0; u[N] = 0.0;
        Timer timer = new Timer(16, e -> {
            for (int s = 0; s < 10; s++) step();
            repaint();
        });
        timer.start();
    }
    void step() {
        double[] a = computeAcceleration(u);
        double[] uMid = new double[N + 1];
        double[] vMid = new double[N + 1];
        for (int i = 1; i < N; i++) {
            vMid[i] = v[i] + 0.5 * dt * a[i];
            uMid[i] = u[i] + 0.5 * dt * v[i];
        }
        double[] aMid = computeAcceleration(uMid);
        for (int i = 1; i < N; i++) {
            v[i] = v[i] + dt * aMid[i];
            u[i] = u[i] + dt * vMid[i];
        }
        u[0] = 0.0; u[N] = 0.0;
        v[0] = 0.0; v[N] = 0.0;
    }
    double[] computeAcceleration(double[] u) {
        double[] a = new double[N + 1];
        for (int i = 1; i < N; i++) {
            a[i] = c * c * (u[i + 1] - 2 * u[i] + u[i - 1]) / (dx * dx);
        }
        return a;
    }
    @Override
    protected void paintComponent(Graphics g) {
        super.paintComponent(g);
        Graphics2D g2 = (Graphics2D) g;
        g2.setRenderingHint(RenderingHints.KEY_ANTIALIASING, RenderingHints.VALUE_ANTIALIAS_ON);
        int width = getWidth();
        int height = getHeight();
        int midY = height / 2;
        double scaleX = (double) width / N;
        double scaleY = height / 3.0;
        g2.setColor(Color.BLACK);
        g2.drawLine(0, midY, width, midY);
        g2.setColor(Color.BLUE);
        g2.setStroke(new BasicStroke(2));
        for (int i = 0; i < N; i++) {
            int x1 = (int) (i * scaleX);
            int y1 = (int) (midY - u[i] * scaleY);
            int x2 = (int) ((i + 1) * scaleX);
            int y2 = (int) (midY - u[i + 1] * scaleY);
            g2.drawLine(x1, y1, x2, y2);
        }
    }
    public static void main(String[] args) {
        JFrame frame = new JFrame("String Simulation");
        StringSimulation sim = new StringSimulation();
        frame.add(sim);
        frame.setSize(800, 400);
        frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        frame.setVisible(true);
    }
}