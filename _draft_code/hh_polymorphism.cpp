#include <cstdio>
#include <cassert>
#include <cstdint>

#define PI 3.14159

enum color
{
    color_red,
    color_blue
};

enum shape_type
{
    shape_type_first = 0x1000000,
    shape_rect,
    shape_circle
};

// So, uh, can I have RAII out of this?

struct rect
{
    int X, Y;
};

struct circle
{
    int Radius;
};

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

void InitShape(shape* Shape, color Color)
{
    Shape->Color = Color;
}

void InitRect(shape* Shape, color Color, int X, int Y)
{
    InitShape(Shape, Color);
    Shape->ShapeType = shape_rect;
    Shape->Rect.X = X;
    Shape->Rect.Y = Y;
}

void InitCircle(shape* Shape, color Color, int Radius)
{
    InitShape(Shape, Color);
    Shape->ShapeType = shape_circle;
    Shape->Circle.Radius = Radius;
}


float Area(shape* Shape)
{
    switch (Shape->ShapeType)
    {
        case shape_rect:
        {
            return Shape->Rect.X * Shape->Rect.Y;
        } break;
        case shape_circle:
        {
            return Shape->Circle.Radius * PI;

        } break;
        default:
            assert(0);
    }
}


int main()
{
    shape Shape;

    InitRect(&Shape, color_red, 2, 3);
    printf("%f\n", Area(&Shape));

    InitCircle(&Shape, color_blue, 4);
    printf("%f\n", Area(&Shape));
}
