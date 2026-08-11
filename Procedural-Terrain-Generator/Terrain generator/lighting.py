import numpy as np


class PhongLighting:

    def __init__(self):

        self.light_direction = np.array(
            [0.5, 1.0, 0.8],
            dtype=float
        )

        self.light_direction /= np.linalg.norm(
            self.light_direction
        )

        self.view_direction = np.array(
            [0, 0, 1],
            dtype=float
        )

        self.ambient = 0.35
        self.diffuse_strength = 0.60
        self.specular_strength = 0.35
        self.shininess = 32

    def calculate_intensity(self, normal):

        normal = normal / np.linalg.norm(normal)

        # Ambient
        ambient = self.ambient

        # Diffuse
        diffuse = max(
            np.dot(normal, self.light_direction),
            0
        )

        # Reflection
        reflection = (
            2 * np.dot(
                normal,
                self.light_direction
            ) * normal
            - self.light_direction
        )

        reflection /= np.linalg.norm(reflection)

        # Specular
        specular = max(
            np.dot(
                reflection,
                self.view_direction
            ),
            0
        )

        specular = specular ** self.shininess

        intensity = (
            ambient
            + self.diffuse_strength * diffuse
            + self.specular_strength * specular
        )

        return min(intensity, 1.0)