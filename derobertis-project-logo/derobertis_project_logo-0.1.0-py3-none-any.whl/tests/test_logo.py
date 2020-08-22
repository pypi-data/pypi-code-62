from derobertis_project_logo.triangle import Triangle


def test_generate_logo():
    t = Triangle()
    t.set_random_colors()
    t.render()
