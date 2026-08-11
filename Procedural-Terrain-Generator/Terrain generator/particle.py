import random


class Particle:

    def __init__(self, x, y, z):

        self.x = x
        self.y = y
        self.z = z

        self.velocity = random.uniform(
            0.02,
            0.08
        )

        self.life = random.uniform(
            2,
            5
        )

    def update(self, dt):

        self.y -= self.velocity * dt

        self.life -= dt

        if self.life <= 0:

            self.y = 10

            self.life = random.uniform(
                2,
                5
            )


class ParticleSystem:

    def __init__(self, count=100):

        self.particles = []

        for _ in range(count):

            particle = Particle(
                random.uniform(-20, 20),
                random.uniform(5, 15),
                random.uniform(-20, 20)
            )

            self.particles.append(
                particle
            )

    def update(self, dt):

        for particle in self.particles:

            particle.update(dt)