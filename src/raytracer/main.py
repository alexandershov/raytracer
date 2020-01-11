import raytracer.material
from raytracer import geometry
from raytracer import scene
from raytracer.color import Color
from raytracer.color import Palette


def render():
    floor = scene.Body(
        shape=geometry.make_plane(0, 1, 0, -200),
        material=raytracer.material.Monochrome(Color(170, 170, 170)),
    )

    left_wall = scene.Body(
        shape=geometry.make_plane(1, 0, 0, 250),
        material=raytracer.material.Checkered(
            square_width=80,
            lighter=Palette.WHITE,
            darker=Palette.BLACK,
            projection=raytracer.material.Checkered.project_to_local_yz,
        ),
    )

    right_wall = scene.Body(
        shape=geometry.make_plane(1, 0, 0, -350), material=raytracer.material.Mirror(),
    )

    far_wall = scene.Body(
        shape=geometry.make_plane(0, 0, 1, -2000),
        material=raytracer.material.Checkered(
            square_width=80,
            lighter=Palette.WHITE,
            darker=Color(15, 171, 18),
            projection=raytracer.material.Checkered.project_to_local_xy,
        ),
    )

    left_sphere = scene.Body(
        geometry.Sphere(center=geometry.make_point(75, 185, 400), radius=15),
        material=raytracer.material.Monochrome(Palette.GRAY),
    )
    right_sphere = scene.Body(
        geometry.Sphere(center=geometry.make_point(200, 150, 500), radius=50),
        material=raytracer.material.Mirror(),
    )
    left_light = geometry.make_point(0, 0, 400)
    right_light = geometry.make_point(450, 1000, 200)
    camera = geometry.make_point(150, 100, -300)
    bodies = [left_wall, right_wall, far_wall, floor, left_sphere, right_sphere]
    s = scene.Scene(
        bodies=bodies,
        camera=camera,
        lights=[left_light, right_light],
        width=300,
        height=200,
    )
    image = s.render()
    return image


def main():
    render().show()


if __name__ == "__main__":
    main()
