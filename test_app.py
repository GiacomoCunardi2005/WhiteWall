import re
import subprocess
import tempfile
import unittest
from pathlib import Path

from app import adaptive_color, photo_lab, render, render_many, select_background


class WhiteWallTest(unittest.TestCase):
    def assert_corner(self, image: Path, expected: tuple[int, int, int]):
        value = subprocess.check_output([
            "magick", str(image), "-format", "%[pixel:p{0,0}]", "info:"
        ], text=True)
        actual = tuple(map(int, re.findall(r"\d+", value)))
        self.assertTrue(all(abs(left - right) <= 1 for left, right in zip(actual, expected)))

    def test_tiff_to_instagram_outputs(self):
        with tempfile.TemporaryDirectory() as directory:
            work = Path(directory)
            source = work / "sample.tiff"
            post = work / "post.jpg"
            wide = work / "wide.jpg"
            reel = work / "reel.mp4"
            subprocess.run([
                "magick", "-size", "160x90", "xc:rgb(80,120,160)", str(source)
            ], check=True)

            color = render(source, "post", post)
            render(source, "post", wide, border=40)
            render(source, "reel", reel)

            self.assertEqual(color, select_background([source], "adaptive"))
            self.assertGreater(color[2], color[0])
            self.assertEqual(adaptive_color((0, 0, 0)), (226, 226, 226))
            self.assertEqual(adaptive_color((100, 0, 0)), (198, 198, 198))
            self.assertEqual(select_background([source], "faithful"), (242, 242, 242))
            self.assertEqual(
                subprocess.check_output([
                    "magick", "identify", "-format", "%wx%h Q=%Q", str(post)
                ], text=True),
                "192x240 Q=96",
            )
            self.assert_corner(post, color)
            self.assertEqual(
                subprocess.check_output([
                    "magick", "identify", "-format", "%wx%h", str(wide)
                ], text=True),
                "224x280",
            )
            self.assertEqual(
                subprocess.check_output([
                    "ffprobe", "-v", "error", "-select_streams", "v:0",
                    "-show_entries", "stream=width,height,pix_fmt", "-of", "csv=p=0", str(reel)
                ], text=True).strip(),
                "1080,1920,yuv420p",
            )
            self.assertEqual(
                subprocess.check_output([
                    "magick", "identify", "-format", "%wx%h Q=%Q", str(work / "reel-master.jpg")
                ], text=True),
                "198x352 Q=96",
            )

            dark = work / "dark.tiff"
            light = work / "light.tiff"
            edged = work / "edged.tiff"
            subprocess.run(["magick", "-size", "40x40", "xc:black", str(dark)], check=True)
            subprocess.run(["magick", "-size", "40x40", "xc:white", str(light)], check=True)
            subprocess.run([
                "magick", "-size", "128x128", "xc:black", "-fill", "white",
                "-draw", "rectangle 12,12 115,115", str(edged),
            ], check=True)
            self.assertEqual(photo_lab(dark), (0, 0, 0))
            self.assertEqual(photo_lab(light), (100, 0, 0))
            self.assertEqual(photo_lab(edged)[0], 0)
            shared_color, outputs = render_many([dark, light], "post", work / "batch")
            self.assertEqual(shared_color, adaptive_color((50, 0, 0)))
            self.assertEqual(len(outputs), 2)
            for output in outputs:
                self.assert_corner(output, shared_color)


if __name__ == "__main__":
    unittest.main()
