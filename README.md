# WhiteWall

App desktop GTK per Fedora che converte foto RAW, TIFF e formati comuni in contenuti pronti per Instagram:

- Post verticale: JPEG 4:5 alla risoluzione originale
- Reel: master JPEG 9:16 alla risoluzione originale + MP4 H.264 1080 × 1920, 5 secondi
- foto intera e centrata, con bordo selezionabile dal 5% al 40% a incrementi di 5 (predefinito 20%)
- nessun ridimensionamento della foto: proporzioni e megapixel originali restano invariati
- sfondo **Adattivo** in CIELAB: luminosità guidata dal bordo e tinta attenuata ricavata dal colore medio della foto
- Adattivo mantiene lo sfondo chiaro (`L*=80–90`) e limita la tinta a `C*=10`, così accompagna la palette senza dominarla
- sfondo **Fedele** neutro e quasi bianco `#F2F2F2`
- scelta di una cartella intera: usa la mediana dei target delle singole foto e applica lo stesso colore a ogni risultato

## Avvio

Su Fedora richiede GTK 4, Python 3.14 con PyGObject, ImageMagick 7 con LibRaw e FFmpeg.

```bash
install -Dm755 app.py ~/.local/bin/whitewall
install -Dm644 whitewall.desktop ~/.local/share/applications/whitewall.desktop
update-desktop-database ~/.local/share/applications
```

Avvia **WhiteWall** dal menu applicazioni.

## Verifica

```bash
python3.14 -m unittest -v
```
