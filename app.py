#!/usr/bin/python3.14
"""WhiteWall desktop app for Fedora."""

from __future__ import annotations

import os
import re
import shutil
import subprocess
import tempfile
import threading
from concurrent.futures import ThreadPoolExecutor
from math import ceil, hypot
from pathlib import Path
from statistics import median

import gi

gi.require_version("Adw", "1")
gi.require_version("Gtk", "4.0")
from gi.repository import Adw, Gdk, Gio, GLib, Gtk


FORMATS = {
    "post": (4, 5, "jpg"),
    "reel": (9, 16, "mp4"),
}
FAITHFUL_BACKGROUND = (0xF2, 0xF2, 0xF2)
MIN_EDGE_CONTRAST = 15  # minimum ΔL* between photo edge and adaptive frame
# One magick process per core; the work is in ImageMagick, so threads are enough (no GIL contention).
# shortcut: no memory cap; ~14 large RAWs at once need several GB, add a lower limit if RAM runs out.
WORKERS = os.cpu_count() or 1
# Parallelism comes from running many processes; ImageMagick's own threads would only oversubscribe the CPU.
os.environ.setdefault("MAGICK_THREAD_LIMIT", "1")
EXTENSIONS = {
    ".3fr", ".arw", ".cr2", ".cr3", ".crw", ".dcr", ".dng", ".erf",
    ".fff", ".iiq", ".k25", ".kdc", ".mef", ".mos", ".mrw", ".nef",
    ".nrw", ".orf", ".pef", ".raf", ".raw", ".rw2", ".rwl", ".sr2",
    ".srf", ".srw", ".x3f", ".tif", ".tiff", ".jpg", ".jpeg", ".png",
    ".webp",
}


class RenderError(Exception):
    pass


def run(
    command: list[str], timeout: int = 120, text: bool = True
) -> subprocess.CompletedProcess[str] | subprocess.CompletedProcess[bytes]:
    try:
        return subprocess.run(
            command, check=True, capture_output=True, text=text, timeout=timeout
        )
    except FileNotFoundError as error:
        raise RenderError(f"Comando non disponibile: {command[0]}") from error
    except subprocess.TimeoutExpired as error:
        raise RenderError("La conversione ha impiegato troppo tempo") from error
    except subprocess.CalledProcessError as error:
        detail = error.stderr or error.stdout or "File non leggibile"
        if isinstance(detail, bytes):
            detail = detail.decode(errors="replace")
        detail = detail.strip().splitlines()[-1]
        raise RenderError(detail) from error


def photo_lab(source: Path) -> tuple[float, float, float]:
    result = run([
        # jpeg:size lets libjpeg decode at reduced scale; other formats ignore it.
        "magick", "-define", "jpeg:size=256x256", f"{source}[0]", "-auto-orient", "-resize", "128x128!",
        "-background", "white", "-alpha", "remove", "-colorspace", "Lab",
        "-separate", "-depth", "8", "gray:-",
    ], text=False)
    pixels = result.stdout
    count = 128 * 128
    if not isinstance(pixels, bytes) or len(pixels) != count * 3:
        raise RenderError("Impossibile calcolare il colore dello sfondo")

    lightness, a, b = pixels[:count], pixels[count:count * 2], pixels[count * 2:]
    band = ceil(128 * 0.08)
    perimeter = [
        value for index, value in enumerate(lightness)
        if index // 128 < band or index // 128 >= 128 - band
        or index % 128 < band or index % 128 >= 128 - band
    ]
    average_a, average_b = sum(a) / count - 128, sum(b) / count - 128
    if hypot(average_a, average_b) < 1.5:
        average_a = average_b = 0
    return median(perimeter) * 100 / 255, average_a, average_b


def lab_to_srgb(lightness: float, a: float, b: float) -> tuple[int, int, int]:
    fy = (lightness + 16) / 116
    fx, fz = fy + a / 500, fy - b / 200
    delta = 6 / 29

    def inverse(value: float) -> float:
        return value ** 3 if value > delta else 3 * delta ** 2 * (value - 4 / 29)

    x, y, z = 0.95047 * inverse(fx), inverse(fy), 1.08883 * inverse(fz)
    linear = (
        3.2404542 * x - 1.5371385 * y - 0.4985314 * z,
        -0.9692660 * x + 1.8760108 * y + 0.0415560 * z,
        0.0556434 * x - 0.2040259 * y + 1.0572252 * z,
    )

    def encode(value: float) -> int:
        value = 12.92 * value if value <= 0.0031308 else 1.055 * value ** (1 / 2.4) - 0.055
        return round(255 * max(0, min(1, value)))

    return tuple(encode(value) for value in linear)


def adaptive_lab(photo: tuple[float, float, float]) -> tuple[float, float, float]:
    edge_lightness, a, b = photo
    edge_lightness = max(0, min(100, edge_lightness))
    chroma = hypot(a, b)
    tint = min(0.35, 10 / chroma) if chroma else 0
    lightness = 90 - edge_lightness / 10
    # The inverse mapping crosses the edge at L*≈82: push the frame away so it stays visible.
    # Lighter frame below the crossover, darker above it (jump at the crossover is intentional).
    if abs(lightness - edge_lightness) < MIN_EDGE_CONTRAST:
        lightness = (
            edge_lightness + MIN_EDGE_CONTRAST if lightness > edge_lightness
            else edge_lightness - MIN_EDGE_CONTRAST
        )
    return lightness, a * tint, b * tint


def adaptive_color(photo: tuple[float, float, float]) -> tuple[int, int, int]:
    return lab_to_srgb(*adaptive_lab(photo))


def select_background(sources: list[Path], mode: str) -> tuple[int, int, int]:
    if mode == "faithful":
        return FAITHFUL_BACKGROUND
    if mode != "adaptive":
        raise RenderError("Modalità sfondo non valida")
    with ThreadPoolExecutor(WORKERS) as pool:
        targets = [adaptive_lab(photo) for photo in pool.map(photo_lab, sources)]
    return lab_to_srgb(*(median(channel) for channel in zip(*targets)))


def image_size(source: Path) -> tuple[int, int]:
    # -ping reads only the header; -auto-orient does not apply to it, so swap sides by hand.
    result = run([
        "magick", "identify", "-ping", "-format", "%w %h %[orientation]", f"{source}[0]"
    ])
    try:
        width, height, orientation = result.stdout.split()
        width, height = int(width), int(height)
    except ValueError as error:
        raise RenderError("Impossibile leggere le dimensioni della foto") from error
    if orientation in {"LeftTop", "RightTop", "RightBottom", "LeftBottom"}:
        return height, width
    return width, height


def render(
    source: Path,
    preset: str,
    destination: Path,
    color: tuple[int, int, int] | None = None,
    preview: Path | None = None,
    mode: str = "adaptive",
    border: int = 20,
) -> tuple[int, int, int]:
    try:
        ratio_width, ratio_height, _ = FORMATS[preset]
    except KeyError as error:
        raise RenderError("Formato di uscita non valido") from error

    color = select_background([source], mode) if color is None else color
    source_width, source_height = image_size(source)
    margin = 1 + border / 100
    unit = ceil(max(source_width * margin / ratio_width, source_height * margin / ratio_height))
    width, height = ratio_width * unit, ratio_height * unit
    framed = (
        destination if preset == "post"
        else available_path(destination.with_name(f"{destination.stem}-master.jpg"))
    )
    run([
        "magick", f"{source}[0]", "-auto-orient", "-colorspace", "sRGB",
        "-background", f"rgb({color[0]},{color[1]},{color[2]})", "-alpha", "remove",
        "-gravity", "center", "-extent", f"{width}x{height}",
        "-strip", "-sampling-factor", "4:4:4", "-quality", "96", str(framed),
    ])

    if preset == "reel":
        run([
            "ffmpeg", "-hide_banner", "-loglevel", "error", "-y",
            "-loop", "1", "-i", str(framed), "-t", "5", "-r", "30",
            "-vf", "scale=1080:1920:flags=lanczos:in_range=pc:out_range=tv,format=yuv420p",
            "-c:v", "libx264", "-pix_fmt", "yuv420p", "-color_range", "tv",
            "-crf", "15", "-tune", "stillimage", "-movflags", "+faststart",
            str(destination),
        ])
    if preview:
        run(["magick", str(framed), "-resize", "1200x1200>", "-quality", "88", str(preview)])
    return color


def available_path(path: Path, taken: set[Path] = frozenset()) -> Path:
    if not path.exists() and path not in taken:
        return path
    for number in range(2, 10_000):
        candidate = path.with_stem(f"{path.stem}-{number}")
        if not candidate.exists() and candidate not in taken:
            return candidate
    raise RenderError("Troppi file con lo stesso nome nella cartella di uscita")


def render_many(
    sources: list[Path], preset: str, output_dir: Path, preview: Path | None = None,
    mode: str = "adaptive", border: int = 20,
) -> tuple[tuple[int, int, int], list[Path]]:
    if not sources:
        raise RenderError("La cartella non contiene foto supportate")

    shared_color = select_background(sources, mode)
    output_dir.mkdir(parents=True, exist_ok=True)
    extension = FORMATS[preset][2]
    # Names are reserved up front: parallel renders would otherwise pick the same free name.
    outputs: list[Path] = []
    for source in sources:
        stem = re.sub(r"[^\w.-]+", "-", source.stem).strip("-._") or "foto"
        outputs.append(available_path(output_dir / f"{stem}-whitewall.{extension}", set(outputs)))

    def render_one(index: int) -> None:
        render(
            sources[index], preset, outputs[index], shared_color,
            preview if index == 0 else None, border=border,
        )

    with ThreadPoolExecutor(WORKERS) as pool:
        list(pool.map(render_one, range(len(sources))))
    return shared_color, outputs


class WhiteWallWindow(Adw.ApplicationWindow):
    def __init__(self, **kwargs: object) -> None:
        super().__init__(**kwargs)
        self.set_title("WhiteWall")
        self.set_default_size(980, 680)
        self.sources: list[Path] = []
        self.source_folder: Path | None = None
        self.preview_dir = tempfile.TemporaryDirectory(prefix="whitewall-preview-")
        self.preview_path = Path(self.preview_dir.name) / "preview.jpg"
        self.output_dir: Path | None = None

        toolbar = Adw.ToolbarView()
        toolbar.add_top_bar(Adw.HeaderBar())
        self.set_content(toolbar)

        content = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        toolbar.set_content(content)

        controls = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=18)
        controls.set_size_request(390, -1)
        controls.set_margin_top(42)
        controls.set_margin_bottom(42)
        controls.set_margin_start(42)
        controls.set_margin_end(42)
        content.append(controls)

        eyebrow = Gtk.Label(label="INSTAGRAM FORMATTER · DESKTOP", xalign=0)
        eyebrow.add_css_class("caption")
        eyebrow.add_css_class("dim-label")
        controls.append(eyebrow)

        title = Gtk.Label(label="Più spazio\nalla foto.", xalign=0)
        title.add_css_class("hero")
        controls.append(title)

        lead = Gtk.Label(
            label="Scegli una foto o una cartella. WhiteWall trova il grigio giusto, centra ogni immagine e non taglia nulla.",
            xalign=0,
            wrap=True,
        )
        lead.add_css_class("dim-label")
        controls.append(lead)

        format_label = Gtk.Label(label="Formato", xalign=0)
        format_label.add_css_class("heading")
        controls.append(format_label)

        formats = Gtk.Box(spacing=8, homogeneous=True)
        self.post_button = Gtk.ToggleButton(label="Post · 4:5 · qualità originale")
        self.reel_button = Gtk.ToggleButton(label="Reel · master + MP4")
        self.reel_button.set_group(self.post_button)
        self.post_button.set_active(True)
        formats.append(self.post_button)
        formats.append(self.reel_button)
        controls.append(formats)

        background_label = Gtk.Label(label="Sfondo", xalign=0)
        background_label.add_css_class("heading")
        controls.append(background_label)

        backgrounds = Gtk.Box(spacing=8, homogeneous=True)
        self.adaptive_button = Gtk.ToggleButton(label="Adattivo · dalla foto")
        self.faithful_button = Gtk.ToggleButton(label="Fedele · #F2F2F2")
        self.faithful_button.set_group(self.adaptive_button)
        self.adaptive_button.set_active(True)
        backgrounds.append(self.adaptive_button)
        backgrounds.append(self.faithful_button)
        controls.append(backgrounds)

        border_row = Gtk.Box(spacing=12)
        border_label = Gtk.Label(label="Bordo (%)", xalign=0)
        border_label.add_css_class("heading")
        self.border_scale = Gtk.Scale.new_with_range(
            Gtk.Orientation.HORIZONTAL, 5, 40, 5
        )
        self.border_scale.set_value(20)
        self.border_scale.set_digits(0)
        self.border_scale.set_value_pos(Gtk.PositionType.RIGHT)
        self.border_scale.set_hexpand(True)
        self.border_scale.set_tooltip_text("Bordo dal 5% al 40%, a incrementi di 5")
        self.border_scale.connect(
            "value-changed",
            lambda scale: scale.set_value(round(scale.get_value() / 5) * 5),
        )
        border_row.append(border_label)
        border_row.append(self.border_scale)
        controls.append(border_row)

        pickers = Gtk.Box(spacing=8, homogeneous=True)
        self.file_button = Gtk.Button(label="Scegli foto")
        self.folder_button = Gtk.Button(label="Scegli cartella")
        self.file_button.connect("clicked", self.choose_file)
        self.folder_button.connect("clicked", self.choose_folder)
        pickers.append(self.file_button)
        pickers.append(self.folder_button)
        controls.append(pickers)

        self.selection_label = Gtk.Label(label="Nessuna foto selezionata", xalign=0, wrap=True)
        self.selection_label.add_css_class("dim-label")
        controls.append(self.selection_label)

        self.render_button = Gtk.Button(label="Crea il formato")
        self.render_button.add_css_class("suggested-action")
        self.render_button.add_css_class("pill")
        self.render_button.set_sensitive(False)
        self.render_button.connect("clicked", self.start_render)
        controls.append(self.render_button)

        activity = Gtk.Box(spacing=10)
        self.spinner = Gtk.Spinner()
        self.status_label = Gtk.Label(label="", xalign=0, wrap=True)
        activity.append(self.spinner)
        activity.append(self.status_label)
        controls.append(activity)

        self.open_button = Gtk.Button(label="Apri cartella risultati")
        self.open_button.set_visible(False)
        self.open_button.connect("clicked", self.open_output)
        controls.append(self.open_button)

        stage = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        stage.add_css_class("stage")
        stage.set_hexpand(True)
        stage.set_vexpand(True)
        content.append(stage)

        self.picture = Gtk.Picture()
        self.picture.set_content_fit(Gtk.ContentFit.CONTAIN)
        self.picture.set_can_shrink(True)
        self.picture.set_hexpand(True)
        self.picture.set_vexpand(True)
        self.picture.set_margin_top(42)
        self.picture.set_margin_bottom(42)
        self.picture.set_margin_start(42)
        self.picture.set_margin_end(42)
        self.picture.set_visible(False)
        stage.append(self.picture)

        self.empty_label = Gtk.Label(label="Qui apparirà l’anteprima.")
        self.empty_label.add_css_class("dim-label")
        self.empty_label.set_vexpand(True)
        stage.append(self.empty_label)

    def choose_file(self, _button: Gtk.Button) -> None:
        chooser = Gtk.FileChooserNative.new(
            "Scegli una foto", self, Gtk.FileChooserAction.OPEN, "Apri", "Annulla"
        )
        photo_filter = Gtk.FileFilter(name="Foto RAW, TIFF e immagini")
        for extension in EXTENSIONS:
            photo_filter.add_pattern(f"*{extension}")
            photo_filter.add_pattern(f"*{extension.upper()}")
        chooser.set_filter(photo_filter)
        chooser.connect("response", self.file_chosen)
        chooser.show()

    def file_chosen(self, chooser: Gtk.FileChooserNative, response: int) -> None:
        if response == Gtk.ResponseType.ACCEPT:
            path = Path(chooser.get_file().get_path())
            self.sources = [path]
            self.source_folder = None
            self.selection_label.set_label(path.name)
            self.render_button.set_sensitive(True)
            self.status_label.set_label("")
        chooser.destroy()

    def choose_folder(self, _button: Gtk.Button) -> None:
        chooser = Gtk.FileChooserNative.new(
            "Scegli una cartella", self, Gtk.FileChooserAction.SELECT_FOLDER, "Apri", "Annulla"
        )
        chooser.connect("response", self.folder_chosen)
        chooser.show()

    def folder_chosen(self, chooser: Gtk.FileChooserNative, response: int) -> None:
        if response == Gtk.ResponseType.ACCEPT:
            folder = Path(chooser.get_file().get_path())
            self.sources = sorted(
                path for path in folder.rglob("*")
                if path.is_file()
                and path.suffix.lower() in EXTENSIONS
                and not any(part.startswith("WhiteWall-") for part in path.relative_to(folder).parts)
            )
            self.source_folder = folder
            self.selection_label.set_label(
                f"{folder.name} · {len(self.sources)} foto supportate"
                if self.sources else f"{folder.name} · nessuna foto supportata"
            )
            self.render_button.set_sensitive(bool(self.sources))
            self.status_label.set_label("")
        chooser.destroy()

    def start_render(self, _button: Gtk.Button) -> None:
        preset = "post" if self.post_button.get_active() else "reel"
        mode = "adaptive" if self.adaptive_button.get_active() else "faithful"
        border = round(self.border_scale.get_value())
        output_dir = (
            self.source_folder / f"WhiteWall-{preset}"
            if self.source_folder else self.sources[0].parent
        )
        self.set_busy(True)
        self.status_label.set_label(f"Elaborazione di {len(self.sources)} foto…")
        threading.Thread(
            target=self.render_worker,
            args=(self.sources.copy(), preset, output_dir, mode, border),
            daemon=True,
        ).start()

    def render_worker(
        self, sources: list[Path], preset: str, output_dir: Path,
        mode: str, border: int,
    ) -> None:
        try:
            color, outputs = render_many(
                sources, preset, output_dir, self.preview_path, mode, border
            )
            GLib.idle_add(self.render_done, color, outputs, output_dir)
        except Exception as error:
            GLib.idle_add(self.render_failed, str(error))

    def render_done(
        self, color: tuple[int, int, int], outputs: list[Path], output_dir: Path
    ) -> bool:
        self.output_dir = output_dir
        self.picture.set_filename(None)
        self.picture.set_filename(str(self.preview_path))
        self.picture.set_visible(True)
        self.empty_label.set_visible(False)
        self.status_label.set_label(
            f"Pronto: {len(outputs)} foto · pixel originali mantenuti · sfondo #{color[0]:02X}{color[1]:02X}{color[2]:02X}"
        )
        self.open_button.set_visible(True)
        self.set_busy(False)
        return GLib.SOURCE_REMOVE

    def render_failed(self, message: str) -> bool:
        self.status_label.set_label(f"Errore: {message}")
        self.set_busy(False)
        return GLib.SOURCE_REMOVE

    def set_busy(self, busy: bool) -> None:
        self.file_button.set_sensitive(not busy)
        self.folder_button.set_sensitive(not busy)
        self.render_button.set_sensitive(not busy and bool(self.sources))
        self.post_button.set_sensitive(not busy)
        self.reel_button.set_sensitive(not busy)
        self.adaptive_button.set_sensitive(not busy)
        self.faithful_button.set_sensitive(not busy)
        self.border_scale.set_sensitive(not busy)
        self.spinner.set_spinning(busy)

    def open_output(self, _button: Gtk.Button) -> None:
        if self.output_dir:
            Gio.AppInfo.launch_default_for_uri(self.output_dir.as_uri(), None)


class WhiteWallApp(Adw.Application):
    def __init__(self) -> None:
        super().__init__(application_id="it.whitewall.WhiteWall")
        self.connect("activate", self.activate)

    def activate(self, app: "WhiteWallApp") -> None:
        css = Gtk.CssProvider()
        css.load_from_string("""
            .hero { font-size: 46px; font-weight: 900; line-height: .9; }
            .stage { background: #dedbd3; border-radius: 18px; }
            .caption { letter-spacing: 2px; font-family: monospace; font-weight: 700; }
        """)
        Gtk.StyleContext.add_provider_for_display(
            Gdk.Display.get_default(), css, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
        )
        window = self.props.active_window or WhiteWallWindow(application=app)
        window.present()


def main() -> None:
    missing = [name for name in ("magick", "ffmpeg") if not shutil.which(name)]
    if missing:
        raise SystemExit(f"Comandi mancanti: {', '.join(missing)}")

    WhiteWallApp().run()


if __name__ == "__main__":
    main()
