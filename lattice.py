import numpy as np
from matplotlib import pyplot as plt
import cv2


class Lattice:
    def __init__(
        self,
        lattice_size,
        beta=0.5,
        spin_interaction=1,
        external_magnetic_field=0,
        bias=0.5,
    ):
        self.lattice_size = lattice_size
        self.beta = beta
        self.spin_interaction = spin_interaction
        self.external_magnetic_field = external_magnetic_field

        self.spins = np.random.choice(
            [-1, 1], size=(self.lattice_size, self.lattice_size), p=[bias, 1 - bias]
        )
        self.magnetization = self.spins.mean()
        self.hamiltonian = self.calculate_hamiltonian(self.spins)

    def calculate_hamiltonian(self, state):
        hamiltonian = 0
        hamiltonian -= np.sum(self.spin_interaction * state * np.roll(state, 1, axis=0))
        hamiltonian -= np.sum(self.spin_interaction * state * np.roll(state, 1, axis=1))

        if self.external_magnetic_field != 0:
            hamiltonian -= self.external_magnetic_field * state.sum()

        return hamiltonian

    def metropolis_hastings(self, steps=1000, display_interval=10):
        step = 0
        while step < steps:
            proposed_spins = self.spins.copy()

            i, j = np.random.randint(self.lattice_size, size=2)
            proposed_spins[i][j] = -1 * proposed_spins[i][j]

            initial_state_energy = self.calculate_hamiltonian(self.spins)
            proposed_state_energy = self.calculate_hamiltonian(proposed_spins)

            if initial_state_energy > proposed_state_energy:
                self.spins = proposed_spins
                self.magnetization = self.spins.mean()
                self.hamiltonian = proposed_state_energy
                step += 1
            elif np.random.random_sample() < np.exp(
                -self.beta * (proposed_state_energy - initial_state_energy)
            ):
                self.spins = proposed_spins
                self.magnetization = self.spins.mean()
                self.hamiltonian = proposed_state_energy
                step += 1

            if step % display_interval == 0:
                self.display_spins()

    def display_spins(self):
        img = np.where(self.spins == 1, 255, 0).astype(np.uint8)
        img = cv2.resize(img, (500, 500), interpolation=cv2.INTER_NEAREST)
        img_color = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)

        frame_height = img_color.shape[0] + 50
        frame_width = img_color.shape[1]
        frame = np.zeros((frame_height, frame_width, 3), dtype=np.uint8)

        frame[0 : img_color.shape[0], :] = img_color

        cv2.putText(
            frame,
            f"Magnetization: {self.magnetization:.2f}",
            (10, img_color.shape[0] + 30),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            (0, 255, 0),
            2,
        )

        cv2.imshow("Lattice", frame)
        cv2.waitKey(1)

    def show_spins(self, img_size):
        plt.figure(figsize=(img_size, img_size))
        plt.imshow(self.spins, cmap="gray", interpolation="none")
        plt.title(f"${self.lattice_size}^2$-Lattice Spin Array", fontsize=2 * img_size)
        plt.axis("off")
        plt.show()


if __name__ == "__main__":

    lattice_size = 100
    lattice = Lattice(lattice_size, beta=0.1, bias=0.5)
    cv2.namedWindow("Lattice", cv2.WINDOW_AUTOSIZE)

    lattice.metropolis_hastings(steps=100000, display_interval=10)
