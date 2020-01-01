Scope
=====
This is going to be a simple ray tracer in python. Supported objects:
* spheres
* floor
* walls
* sky
* shadows
* lights

Spheres, floor, and walls can be mirrors.
Floor and walls can be checkered.
Spheres, floor, and walls can have color.

Colored/checkered mirrors are not supported.

It's okay for rendering to work for a couple of seconds.
But strive for sub-second latency.

After implementation I'll compare it with "Raytracing in a weekend" and implement
"Raytracing in a weekend".


Questions
=========

* ~~What's the true way of managing virtualenvs in python now? pipenv? conda?
  something else?~~
  It was a close call between pipenv and poetry, but let's go with pipenv
  since it's recommended on packaging.python.org. But poetry looks good tool
  with the pyproject.toml support.
* ~~What to use for the visuals? Tkinter? BMP file? Pillow?
  Some other interactive option?~~
  Let's go with Pillow, tkinter looks strange, but anyway I'll hide drawing stuff
  behind the abstraction so it doesn't matter. For now let it be Pillow.
* ~~Is there any use of numpy here?~~
  Probably not, because I want to do the math by myself.
* ~~Should I use Entity-Component-System here (at least for the sake of learning)?~~
  Let's not use it, seems like overkill.
* ~~What are the primitive objects here?~~
  Point, Ray, Sphere, Plane
* ~~What are the primitive operations here?~~
  Intersections, mirror reflections, set_pixel
* ~~How to test it?~~
  Primitive math you can check with the unit tests.
  You can check scenes during development with your eyes.
  You can write etalon output to the file and compare outputs during
  refactorings.
  But unit tests and eye check seem enough here.
* ~~What is the math/terminology for ray?~~
  Looks like start & direction are enough to describe a ray.
  What's a direction? Basically it's either ordered pair of points, 
  or start & direction (delta). Difference is not clear it, so let's 
  go with ordered pair of points as a simpler choice.
  It's a line, ray has extra condition k > 0
  x = x0 + k(x1 - x0) 
  y = y0 + k(y1 - y0) 
  z = z0 + k(z1 - z0) 
* ~~What is the math/terminology for sphere?~~
  x^2 + y^2 + z^2 = r^2
  (x - x0)^2 + (y - y0)^2 + (z - z0)^2 = r^2 
  center (x0; y0; z0) & radius (r) are enough to represent sphere
* What is the math/terminology for floor/wall?
* What is the math for the intersection of ray and floor/wall?
* What is the math for the intersection of ray and sphere?
* What is the math for the floor/wall mirror?
* What is the math for the sphere mirror?
* How to implement checkers on floor/walls?