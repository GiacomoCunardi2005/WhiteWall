# WhiteWall

WhiteWall è un’app desktop nativa per Fedora che prepara fotografie intere per Post e Reel Instagram, aggiungendo un bordo senza ritagliare o ridimensionare la foto originale.

L’elaborazione avviene completamente in locale: nessuna foto viene caricata online.

## Funzionalità

- **Post 4:5:** JPEG alla risoluzione necessaria per contenere tutti i pixel originali.
- **Reel 9:16:** master JPEG a piena risoluzione e MP4 H.264 `1080×1920` di 5 secondi.
- **Nessun ritaglio:** la foto viene centrata mantenendo proporzioni e megapixel.
- **Bordo regolabile:** dal 5% al 40%, a incrementi di 5; valore iniziale 20%.
- **Sfondo Adattivo:** analisi CIELAB del bordo e della palette della fotografia.
- **Sfondo Fedele:** grigio neutro quasi bianco fisso `#F2F2F2`.
- **Elaborazione cartelle:** ricerca ricorsiva delle foto e applicazione dello stesso sfondo a tutto il gruppo.
- **RAW supportati:** tramite ImageMagick e LibRaw.

La scelta percettiva dello sfondo è documentata in [How Background Colour Affects the Viewing of a Photograph](BACKGROUND_COLOR_STUDY.md).

## Requisiti

- Fedora 44
- Python 3.14 con PyGObject
- GTK 4 e libadwaita
- ImageMagick 7 con supporto LibRaw
- FFmpeg con encoder H.264 `libx264`

Installa le dipendenze dai repository Fedora/RPM Fusion già configurati:

```bash
sudo dnf install python3-gobject gtk4 libadwaita ImageMagick ffmpeg desktop-file-utils
```

## Installazione

Dalla cartella del progetto:

```bash
install -Dm755 app.py ~/.local/bin/whitewall
install -Dm644 whitewall.desktop ~/.local/share/applications/whitewall.desktop
update-desktop-database ~/.local/share/applications
```

Avvia **WhiteWall** dal menu applicazioni oppure dal terminale:

```bash
whitewall
```

## Utilizzo

1. Scegli **Post** oppure **Reel**.
2. Seleziona lo sfondo **Adattivo** o **Fedele**.
3. Regola il bordo tra 5% e 40%.
4. Scegli una singola foto oppure una cartella.
5. Premi **Crea il formato**.
6. Usa **Apri cartella risultati** per vedere i file esportati.

Con una singola foto, il risultato viene salvato accanto all’originale. Per una cartella, WhiteWall crea `WhiteWall-post` o `WhiteWall-reel` al suo interno. I file esistenti non vengono sovrascritti: al nome viene aggiunto un numero progressivo.

## Modalità dello sfondo

### Adattivo

Analizza una copia ridotta della foto in CIELAB. La luminosità considera il perimetro esterno, mentre una tinta poco satura riprende il colore medio dell’immagine. In modalità cartella viene usata la mediana dei target delle singole foto, così ogni risultato riceve esattamente lo stesso colore.

### Fedele

Usa sempre `#F2F2F2`. È la modalità più uniforme per serie e caroselli che richiedono un bordo quasi bianco.

## Formati

Formati comuni:

- JPEG, PNG, TIFF e WebP

RAW fotografici:

- DNG, ARW, CR2, CR3, NEF, NRW, RAF, RW2, ORF, PEF e altri formati riconosciuti da LibRaw

## Qualità dell’output

- JPEG qualità 96 con campionamento `4:4:4`
- foto originale inserita senza ridimensionamento
- proporzioni finali esatte `4:5` o `9:16`
- Reel H.264 `yuv420p`, CRF 15 e ridimensionamento Lanczos dal master

## Sviluppo e verifica

Avvio senza installazione:

```bash
python3.14 app.py
```

Test:

```bash
python3.14 -m unittest -v
```

Il test verifica analisi dello sfondo, bordo configurabile, dimensioni, qualità JPEG e proprietà del Reel.

## Supporto e contributi

Per segnalare un problema o proporre un miglioramento, apri una GitHub Issue descrivendo versione di Fedora, formato della foto e passaggi per riprodurre il comportamento. Prima di una pull request, esegui i test indicati sopra.

## Licenza

Il repository non include ancora una licenza. Finché non ne viene aggiunta una, il codice non è concesso automaticamente per riuso, modifica o distribuzione.
