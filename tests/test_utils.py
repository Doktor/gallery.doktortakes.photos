from PIL import Image

from photos.utils import fit_image


def create_image(w, h):
    return Image.new('RGB', (w, h))


def test_simple_downsize():
    old = create_image(1000, 1000)
    new = fit_image(old, (100, 100))

    assert new.size == (100, 100)


def test_simple_upsize():
    old = create_image(100, 100)
    new = fit_image(old, (1000, 1000))

    assert new.size == (1000, 1000)


def test_crop():
    old = create_image(1000, 1000)

    px = old.load()
    px[0, 250] = (255, 0, 0)
    new = fit_image(old, (1000, 500))

    px = new.load()
    assert px[0, 0] == (255, 0, 0)
