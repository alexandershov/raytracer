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
* ~~What is the math/terminology for floor/wall?~~
  Looks like a plane should be ax + by + cz = d
  E.g y = 0 is a floor.
* ~~What is the math for the intersection of ray and floor/wall?~~
  Just put x = x0 + k(x1 - x0) into plane equation and you'll 
  get linear equation with k 
* ~~What is the math for the intersection of ray and sphere?~~
  Just put x = x0 + k(x1 - x0) into sphere equation and you'll get 
  quadratic equation with k 
* ~~How to implement colors?~~
  Thing{figure, material}, thing can return Colorable which have get_color()
* ~~How to implement checkers on floor/walls?~~
  Idea 1: set local x & y for a plane and project point to local coordinates
    I don't like it, but it seems like the most realistic solution to get without
    google. And I don't want to google, I want to learn.
  Idea 2: some wicked function of x, y, z
  Idea 3: project Xs axis onto plane and build a perpendicular on plane - 
    that's no good because you can't project Ox if plane contains Ox
  Idea 4: just get two different points on a plane, that'll be your Ox, then build perpendicular
  Idea 5: any plane can be made as the rotation + shift of Oxy we need to find this rotation
  Actually, after a good night's sleep the simplest way is to have a simple projection
  to Oxy or Oxz in the Material (no plane can be parallel to both of those). 
  There'll be (almost) no math. 
* ~~How to project point to a plane?~~
  On a plane y=ax + b projection of (x0; y0) will be intersection of
  another line y=-x/a + b1 (b1 can be found easily), then you can find intersection 
  of two lines
  In 3d we can choose view where plane is a line and do it, but how to choose this view?
  How to rotate? 
  Maybe just multiplying all a, b, c leads to rotation?
  No at least for by=3, if you change b then it doesn't rotate but just moves up/down
  two vectors are perpendicular if they x1*x2 + y1*y2 + z1*z2 = 0.
  We have 3 points on a plane. And we have a point outside of it.
  We can get system of 3 equations with 3 unknowns. Looks inspiring.
  Also looks like there can be cases 3 equations and 2 unknowns. 
  We can special case it, if x/y/z is constant then solution is trivial.
  So we have a projection, but it's in global coordinates. This is the next question.
* ~~How to convert a point on a plane to local coordinates?~~
  Projection on axis is easy - it's an equation against k.
  Now we have projected point on axis, how to translate it to local coordinates?
  Actually when we projecting point we're finding k, that'll be the coordinate.
  We just need to do it for 2 axis.
* ~~What is the math for the floor/wall mirror?~~
  Let's say we can build a perpendicular vector at the given point of a plane.
  And we can because we can project point to a plane, so reversal vector will be
  perpendicular.
  Then we project the start of our ray to this line. We already have the technology
  for it. When we find projection we find k, we should just double the k and find
  direction of the reflection.
* ~~What is the math for the sphere mirror?~~
  Same as for floor/wall mirror, start building the perpendicular from the center
  to the intersection. The rest is the same.
* ~~Is there a simpler way to build floor/wall mirror?~~
  Since floor/wall is always of the kind z=1 we can determine perpendicular
  without equation just from the common sense.
* ~~Why does raytracing work? There's no rays coming out of your eye in real life~~
  And it looks like camera in your phone can work without inner light.
  Looks like when light goes from the source of light it spreads
  in all directions and when it meets a block it also spreads
  from this block in all directions.
* What there's a need for camera & screen in raytracing?
  Is there a camera & screen in real life?
* How does mirrors work in real life?
* Why we need self.height - 1 in set_pixel?
