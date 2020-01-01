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
* What to use for the visuals? Tkinter? BMP file? Pillow?
  Some other interactive option?
* ~~Is there any use of numpy here?~~
  Probably not, because I want to do the math by myself.
* Should I use Entity-Component-System here (at least for the sake of learning)?
* What are the primitive objects here?
* What are the primitive operations here?
* How to implement checkers on floor/walls?
* ~~How to test it?~~
  Primitive math you can check with the unit tests.
  You can check scenes during development with your eyes.
  You can write etalon output to the file and compare outputs during
  refactorings.
  But unit tests and eye check seem enough here.
* What is the math/terminology for ray?
  Looks like start & direction are enough to describe a ray.
* ~~What is the math/terminology for sphere?~~
  x^2 + y^2 + z^2 = r^2
  center & radius are enough for the sphere
* What is the math/terminology for floor/wall?
* What is the math for the intersection of ray and floor/wall?
* What is the math for the intersection of ray and sphere?
* What is the math for the floor/wall mirror?
* What is the math for the sphere mirror?
