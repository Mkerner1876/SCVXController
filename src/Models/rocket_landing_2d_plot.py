import numpy as np
import matplotlib.pyplot as plt

# vector scaling
attitude_scale = 15
thrust_scale = 0.00002


def my_plot(fig, figures_i):
    ax = fig.add_subplot(111)

    X_i = X[figures_i, :, :]
    U_i = U[figures_i, :, :]
    K = X_i.shape[1]

    ax.set_xlabel('X, east')
    ax.set_ylabel('Y, up')

    ax.plot(X_i[0, :], X_i[1, :], color='lightgrey', zorder=0)

    rx = X_i[0, :]
    ry = X_i[1, :]

    dx = np.sin(X_i[4, :])
    dy = np.cos(X_i[4, :])

    Fx = -np.sin(X_i[4, :] + U_i[0, :]) * U_i[1, :]
    Fy = -np.cos(X_i[4, :] + U_i[0, :]) * U_i[1, :]

    # attitude vector
    ax.quiver(rx, ry, dx, dy, color='blue', width=0.003, scale=attitude_scale, headwidth=1, headlength=0)

    # force vector
    ax.quiver(rx, ry, Fx, Fy, color='red', width=0.002, scale=thrust_scale, headwidth=1, headlength=0)

    ax.set_title("Iteration " + str(figures_i))


def key_press_event(event):
    global figures_i, figures_N

    fig = event.canvas.figure

    if event.key == 'q' or event.key == 'escape':
        plt.close(event.canvas.figure)
        return
    if event.key == 'right':
        figures_i += 1
        figures_i %= figures_N
    elif event.key == 'left':
        figures_i -= 1
        figures_i %= figures_N
    fig.clear()
    my_plot(fig, figures_i)
    plt.draw()


def plot(X_in, U_in, sigma_in):
    global figures_i, figures_N
    figures_N = X_in.shape[0]
    figures_i = figures_N - 1

    global X, U, sigma
    X = X_in
    U = U_in
    sigma = sigma_in

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
