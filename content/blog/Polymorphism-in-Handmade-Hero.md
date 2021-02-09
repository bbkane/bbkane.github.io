+++
title = "Polymorphism in Handmade Hero"
date = 2018-01-12
updated = 2018-01-12
aliases = [ "2018/01/12/Polymorphism-in-Handmade-Hero.html" ]
+++

A while back, while watching [Handmade Hero](https://handmadehero.org/), I
watched Casey demonstrate one way to produce polymorphism without inheritance
(and the vtable pointer dereferencing penalty it carries). He did this by using
a [tagged union](https://en.wikipedia.org/wiki/Tagged_union) to hold the derived
classes, and switching on the tag in the polymorphic method (actually a function
in this case). I've never actually seen this, before, so I want to write up how
it works, and my thoughts on it.

## The Code

Let's start with some includes and definitions:

```cpp
#include <cstdio>
#include <cassert>
#include <cstdint>

constexpr double  PI = 3.14159;

enum color
{
    color_red,
    color_blue
};
```

Now adding the tag part for the tagged union:

```cpp
enum shape_type
{
    shape_rect,
    shape_circle
};
```

Now we create the unique part of each shape:

```cpp
struct rect
{
    int Width, Height;
};

struct circle
{
    int Radius;
};
```

And create the shared part:

```cpp
struct shape
{
    // shared variables
    color Color;

    shape_type ShapeType;
    union
    {
        rect Rect;
        circle Circle;
    };
};
```

Notice that we have the tag (`ShapeType`) and a union of each type.

Let's create some constructors- I'm creating one constructor to initialize the
shared data, and a two more constructors, one for each shape, that call the
shared constructor.

```cpp
void InitShape(shape* Shape, color Color)
{
    Shape->Color = Color;
}

void InitRect(shape* Shape, color Color, int Width, int Height)
{
    InitShape(Shape, Color);
    Shape->ShapeType = shape_rect;
    Shape->Rect.Width = Width;
    Shape->Rect.Height = Height;
}

void InitCircle(shape* Shape, color Color, int Radius)
{
    InitShape(Shape, Color);
    Shape->ShapeType = shape_circle;
    Shape->Circle.Radius = Radius;
}
```

This is a very C-like approach, but it works and it's easy to understand.

Finally, here's the polymorphic function to compute the area of the shape:

```cpp
double Area(shape* Shape)
{
    switch (Shape->ShapeType)
    {
        case shape_rect:
        {
            return Shape->Rect.Width * Shape->Rect.Height;
        }
        case shape_circle:
        {
            return Shape->Circle.Radius * PI;

        }
    }
    assert(0 && "Unknown Shape...");
}
```

Here's an example main:

```cpp
int main()
{
    shape Shape;

    InitRect(&Shape, color_red, 2, 3);
    printf("%f\n", Area(&Shape));
    // 6.000000

    InitCircle(&Shape, color_blue, 4);
    printf("%f\n", Area(&Shape));
    // 12.566360
}
```

## Conclusions

I think this is an interesting approach. These are some knee-jerk reactions too
it that may or may not be well thought out...

### Pros

- It's straightforward approach means it's very easy to see how these structs
  are laid out in memory. No hidden vtables to worry about here...
- Likewise, because you're doing the work of the compiler, it compiles very
  quickly.
- There's no vtable, so no cache misses- the class's members are always right
  next to each other.
- No magic

### Cons

- No interfaces. `grep -ir <class_name> src/` might be your best bet to see what
  the class does, and that's if the developer names everything to be friendly to
  that approach.
- Every data member is laid out in memory, so every object of type `Shape` will
  be the same size. If one derived `Shape` has particularly large data members,
  all `Shape`s will pay the penalty.
- I think the use of `union` subverts RAII.
- It's hard to extend. If you want to add a new shape, you must add a new
  member to the enum, create a new Init function, and modify all polymorphic
  functions that you care about. It's easy to imagine an undisciplined developer
  messing up case in that function that worked before.
- No extensibility without source access.

Despite all of those cons, I still think this approach is really readable and I
like the potential speed gains. If this is a project where I didn't really need
RAII, I was the only developer, and my classes were roughly the same size, I'd
probably use it.

## Resources

Here are some particularly noteworthy resources on polymorphism in C++ that feel
like they belong here:

- [Handmade Hero episodes](https://hero.handmade.network/episode/code) :
  Unfortunately I don't recall the exact episode he demonstrates this on
- [CppCon 2017: Louis Dionne “Runtime Polymorphism: Back to the
  Basics”](https://www.youtube.com/watch?v=gVGtNFg4ay0) : This dude talks a lot
  about memory layout and inheritance. He invented a compile-time template
  langaage called [dyno](https://github.com/ldionne/dyno) to manipulate it
- [Better Code: Runtime Polymorphism - Sean
  Parent](http://www.youtube.com/watch?v=QGcVXgEVMJg) : Sean Parent talks about
  polymorphism. To be honest, I haven't watched this one yet, but he's usually
  pretty good.
