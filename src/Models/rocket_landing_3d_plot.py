import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import art3d

figures_i = 0

# vector scaling
thrust_scale = 0.00002
attitude_scale = 20


def key_press_event(event):
    global figures_i
    fig = event.canvas.figure

    if event.key == 'q' or event.key == 'escape':
        plt.close(event.canvas.figure)
        return

    if event.key == 'right':
        figures_i = (figures_i + 1) % figures_N
    elif event.key == 'left':
        figures_i = (figures_i - 1) % figures_N

    fig.clear()
    my_plot(fig, figures_i)
    plt.draw()


def my_plot(fig, figures_i):
    ax = fig.add_subplot(111, projection='3d')

    X_i = X[figures_i, :, :]
    U_i = U[figures_i, :, :]
    K = X_i.shape[1]

    ax.set_xlabel('X, east')
    ax.set_ylabel('Y, north')
    ax.set_zlabel('Z, up')

    for k in range(K):
        rx, ry, rz = X_i[1:4, k]
        qw, qx, qy, qz = X_i[7:11, k]

        CBI = np.array([
            [1 - 2 * (qy ** 2 + qz ** 2), 2 * (qx * qy + qw * qz), 2 * (qx * qz - qw * qy)],
            [2 * (qx * qy - qw * qz), 1 - 2 * (qx ** 2 + qz ** 2), 2 * (qy * qz + qw * qx)],
            [2 * (qx * qz + qw * qy), 2 * (qy * qz - qw * qx), 1 - 2 * (qx ** 2 + qy ** 2)]
        ])

        dx, dy, dz = np.dot(np.transpose(CBI), np.array([0., 0., 1.]))
        Fx, Fy, Fz = np.dot(np.transpose(CBI), U_i[:, k])

        # attitude vector
        ax.quiver(rx, ry, rz, dx, dy, dz, length=attitude_scale, arrow_length_ratio=0.0, color='blue')

        # thrust vector
        ax.quiver(rx, ry, rz, -Fx, -Fy, -Fz, length=thrust_scale, arrow_length_ratio=0.0, color='red')

    scale = X_i[3, 0]
    ax.auto_scale_xyz([-scale / 2, scale / 2], [-scale / 2, scale / 2], [0, scale])

    pad = plt.Circle((0, 0), 20, color='lightgray')
    ax.add_patch(pad)
    art3d.pathpatch_2d_to_3d(pad)

    ax.set_title("Iteration " + str(figures_i))
    ax.plot(X_i[1, :], X_i[2, :], X_i[3, :], color='lightgrey')
    ax.set_aspect('equal')

def plot(X_in, U_in, sigma_in):
    global figures_N
    figures_N = X_in.shape[0]
    figures_i = figures_N - 1

    global X, U
    X = X_in
    U = U_in

    fig = plt.figure(figsize=(10, 12))
    my_plot(fig, figures_i)
    cid = fig.canvas.mpl_connect('key_press_event', key_press_event)
    plt.show()


if __name__ == "__main__":
    import os

    base_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(base_dir)  # This is the actual project root
    trajectory_path = os.path.join(project_root, 'output', 'trajectory')

    if os.path.isdir(trajectory_path):
        folders = os.listdir(trajectory_path)
        if folders:
            folder_number = str(int(max(folders))).zfill(3)
        else:
            folder_number = "000"
    else:
        print(f"Directory does not exist: {trajectory_path}")
        os.makedirs(trajectory_path)
        folder_number = "000"

    folder_path = os.path.join(trajectory_path, folder_number)

    X_in = np.load(os.path.join(folder_path, "X.npy"))
    U_in = np.load(os.path.join(folder_path, "U.npy"))
    sigma_in = np.load(os.path.join(folder_path, "sigma.npy"))

    plot(X_in, U_in, sigma_in)