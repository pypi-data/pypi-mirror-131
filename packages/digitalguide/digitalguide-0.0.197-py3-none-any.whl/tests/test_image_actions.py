from PIL import Image
from digitalguide.imageActions import overlay_images
import pytest

@pytest.mark.parametrize("ratio", [
    "4096_3072",
    "3072_4096"
])
def test_overlay_images(ratio):
    im = overlay_images(Image.open("./tests/assets/background_{}.png".format(ratio)), Image.open("./tests/assets/foreground.png"), resize="y")
    assert_image_equal_tofile(im, "./tests/assets/result_{}.png".format(ratio))
    # Write the stuff
    #im.save("test.png")

def assert_image_equal(a, b, msg=None):
    assert a.mode == b.mode, msg or f"got mode {repr(a.mode)}, expected {repr(b.mode)}"
    assert a.size == b.size, msg or f"got size {repr(a.size)}, expected {repr(b.size)}"
    assert a.tobytes() == b.tobytes(), msg or "got different content"

def assert_image_equal_tofile(a, filename, msg=None, mode=None):
    with Image.open(filename) as img:
        if mode:
            img = img.convert(mode)
        assert_image_equal(a, img, msg)