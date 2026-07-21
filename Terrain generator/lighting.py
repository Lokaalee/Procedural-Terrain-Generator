import numpy as np

class PhongLighting:

    def __init__(self):

        # Direction of the sun
        self.light_direction = np.array([0.5, 1.0, 0.8])
        self.light_direction /= np.linalg.norm(self.light_direction)

        # Camera direction
        self.view_direction = np.array([0, 0, 1])

        # Lighting strengths
        self.ambient = 0.35
        self.diffuse_strength = 0.65
        self.specular_strength = 0.30
        self.shininess = 32

    def calculate_intensity(self, normal):

        normal = normal / np.linalg.norm(normal)

        # Ambient
        ambient = self.ambient

        # Diffuse
        diffuse = max(np.dot(normal, self.light_direction), 0)

        # Reflection
        reflect = (
            2 * np.dot(normal, self.light_direction) * normal
            - self.light_direction
        )

        reflect /= np.linalg.norm(reflect)

        specular = max(np.dot(reflect, self.view_direction), 0)
        specular = specular ** self.shininess

        intensity = (
            ambient
            + self.diffuse_strength * diffuse
            + self.specular_strength * specular
        )

        return min(intensity, 1.0)