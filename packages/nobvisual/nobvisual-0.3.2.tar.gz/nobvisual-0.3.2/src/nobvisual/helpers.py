
import circlify

from nobvisual.objects import PackingCircle


def from_nested_struct_to_nobvisual(nstruct):
    circlify_circles = circlify.circlify(nstruct, show_enclosure=False)
    return from_circlify_to_nobvisual(circlify_circles)


def from_circlify_to_nobvisual(circlify_circles):
    circles = [from_circlify_circle_to_packing_circle(circlify_circle)
               for circlify_circle in circlify_circles]

    circle_ids = [circle.ex['id'] for circle in circlify_circles]

    # add children
    for circle, circlify_circle in zip(circles, circlify_circles):
        children_ids = [child['id'] for child in circlify_circle.ex.get('children', [])]
        for child_id in children_ids:
            circle.add_children(circles[circle_ids.index(child_id)])

    return circles


def from_circlify_circle_to_packing_circle(circlify_circle):
    x, y, r = circlify_circle.circle
    level = circlify_circle.level

    data = circlify_circle.ex
    color = data.get('color', 'default')
    name = data.get('name', '')
    short_name = data.get('short_name', '')
    text = data.get('text', '')
    short_text = data.get('short_text', text)

    return PackingCircle(x, y, r, level, color=color, name=name, text=text,
                         short_name=short_name, short_text=short_text)
