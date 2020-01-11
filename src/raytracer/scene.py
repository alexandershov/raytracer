from __future__ import annotations

import multiprocessing
import time
from dataclasses import dataclass
from typing import List
from typing import Tuple

import numpy as np

from raytracer import geometry
from raytracer.color import Color
from raytracer.image import Image
from raytracer.material import Material
from raytracer.material import Mirror


@dataclass(frozen=True)
class Body:
    figure: geometry.Figure
    material: Material


@dataclass(frozen=True)
class Scene:
    bodies: List[Body]

    camera: geometry.Point
    lights: List[geometry.Point]

    width: int
    height: int

    def __iter__(self):
        return iter(self.bodies)

    def render(self):
        started_at = time.time()
        img = Image(self.width, self.height)
        points = self._screen_points()
        num_processes = 6
        with multiprocessing.Pool(processes=num_processes) as pool:
            chunks = _get_chunks(points, num_processes)
            for colored in pool.map(self._get_colors, chunks):
                for point, color in colored:
                    img.set_pixel(
                        int(geometry.get_x(point)), int(geometry.get_y(point)), color
                    )
        duration = time.time() - started_at
        print(f"rendering took {duration:.3f} seconds")
        img.show()

    def _get_colors(
            self, points: List[geometry.Point]
    ) -> List[Tuple[geometry.Point, Color]]:
        result = []
        for point in points:
            color = Color(26, 108, 171)
            ray = geometry.make_ray(self.camera, point)
            excluded_ids = set()
            for _ in range(5):
                intersections = []
                for body in self:
                    if id(body) in excluded_ids:
                        continue
                    for p in body.figure.intersections(ray):
                        intersections.append((p, body))
                if intersections:
                    p, body = min(
                        intersections,
                        key=lambda p_body: np.linalg.norm(p_body[0] - ray.point),
                    )
                    if isinstance(body.material, Mirror):
                        # TODO: catch exception here
                        ray = ray.mirror(body.figure.perpendicular(p))
                        excluded_ids = {id(body)}
                        continue
                    color = body.material.get_color(p) * self._lightning_coeff(p)
                break
            result.append((point, color))
        return result

    def _lightning_coeff(self, p: geometry.Point) -> float:
        coeffs = []
        for light in self.lights:
            in_the_shadow = False
            segment = geometry.make_line_segment(p, light)
            for body in self:
                for intersections in body.figure.intersections(segment):
                    if np.linalg.norm(intersections - p) > 1:
                        in_the_shadow = True
            if in_the_shadow:
                coeffs.append(0.5)
                continue
            d = np.linalg.norm(light - p)
            cutoff = 800
            if d > cutoff:
                coeffs.append(cutoff / d)
            else:
                coeffs.append(1)
        if not coeffs:
            return 1
        return max(coeffs)

    def _screen_points(self) -> List[geometry.Point]:
        return [
            geometry.make_point(x, y, 0)
            for x in range(0, self.width)
            for y in range(0, self.height)
        ]


def _get_chunks(seq: list, n: int) -> List[list]:
    chunks = []
    for i in range(n):
        chunks.append(seq[i::n])
    return chunks
