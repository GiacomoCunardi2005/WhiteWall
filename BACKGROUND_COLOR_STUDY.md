# How Background Colour Affects the Viewing of a Photograph

## Executive summary

The background around a photograph is part of the visual stimulus. It changes how bright, contrasty, colourful, neutral, and separated from the page the photograph appears, even though the photograph's pixels do not change.

The strongest evidence supports five conclusions:

1. A darker surround generally makes image tones appear lighter, particularly dark tones, and reduces apparent contrast. A brighter surround generally increases apparent contrast. This is the Bartleson–Breneman surround effect.
2. A chromatic surround shifts colour appearance and the observer's idea of neutral. The effect grows with surround chroma and is strongest next to the image boundary.
3. There is no universally optimal background for aesthetic image quality. The result depends on image luminance, contrast, content, display brightness, ambient light, and whether the goal is faithful evaluation or attractive presentation.
4. Neutral, controlled surrounds are the defensible choice for colour-critical viewing. Imaging standards use neutral grey surrounds and explicitly model the viewing environment.
5. For an aesthetic adaptive background, evidence favours a colour related to the image's average palette over its complement. The tint should remain restrained because every chromatic surround induces a perceptual colour shift.

For WhiteWall, the best product design is to separate two intents:

- **Faithful view:** a fixed, achromatic near-white chosen as WhiteWall's clean presentation baseline. It is not a colour-grading reference surround.
- **Adaptive presentation:** a light, low-chroma tint on the same hue axis as the image's average colour, with lightness responding inversely to the perimeter. Folder mode uses the median of the per-photo recommendations so every result receives exactly the same background.

## 1. Scope: background, surround, and viewing environment

Three layers must be distinguished:

- **Embedded background:** the border WhiteWall writes into the JPEG or Reel frame.
- **Display surround:** Instagram's interface and the unused portion of the screen around the media.
- **Physical surround:** room illumination, wall colour, reflections, and the viewer's adaptation state.

WhiteWall controls only the first layer. Most laboratory research manipulates the second or third. The mechanisms still apply because the embedded border is an extended area directly adjacent to the photograph, but numerical recommendations for a room or monitor surround cannot be transferred to an embedded border without validation.

This distinction matters on Instagram: the same file can be viewed in light mode, dark mode, on different displays, at different brightness settings, and under daylight or at night. No exported RGB value can guarantee a single perceived appearance in all those conditions.

## 2. What vision science says

### 2.1 Luminance changes apparent brightness and contrast

Simultaneous brightness contrast demonstrates that identical luminance patches appear different when their surrounds differ. A grey region appears lighter against a dark surround and darker against a light surround. The effect occurs early in visual processing and persists even when the inducing context is not consciously visible ([Shimojo et al., 2012](https://pmc.ncbi.nlm.nih.gov/articles/PMC3278746/); [Shroff et al., 2020](https://pmc.ncbi.nlm.nih.gov/articles/PMC7310601/)).

For complex images, Bartleson and Breneman measured brightness functions under different surround luminances. Their data established that apparent image contrast changes with surround luminance ([Bartleson & Breneman, 1967](https://opg.optica.org/josa/abstract.cfm?uri=josa-57-7-953)). Fairchild's review states the practical consequence: a dark surround lifts the apparent brightness of all tones, with a stronger effect on dark tones, reducing perceived contrast; projected transparencies therefore need more physical contrast than prints viewed in an illuminated surround ([Fairchild, 1995](https://onlinelibrary.wiley.com/doi/abs/10.1002/col.5080200604)).

The practical direction is:

- **Darker background:** shadows appear less deep; the photograph can feel softer or flatter.
- **Brighter background:** dark tones appear darker relative to the surround; apparent contrast can increase, but a very bright field can dominate the view and make the image feel dim.

This is not a simple rule that “more contrast is always better.” An experiment using natural-scene patches on black, grey, and white surrounds found that the background changed which combinations of mean luminance and physical contrast received the highest quality ratings. The authors concluded that background-aware models are needed and warned that a general model across displays is difficult ([Kane & Bertalmío, 2016](https://library.imaging.org/admin/apis/public/api/ist/website/downloadArticle/ei/28/6/art00007)).

### 2.2 Background hue changes colour appearance

The eye adapts to surrounding colour. In a controlled display experiment, red, yellow, green, and blue surrounds systematically shifted the colour that observers adjusted to appear neutral; the shift increased as surround chroma increased. The same study found changes in perceived chroma spacing, especially for some red regions ([Rosen et al., 2008](https://library.imaging.org/admin/apis/public/api/ist/website/downloadArticle/cic/16/1/art00029)). Earlier experiments likewise found that chromatic induction tends to push a test colour away from the inducing surround in opponent-colour space ([Krauskopf, Zaidi & Mandler, 1986](https://pubmed.ncbi.nlm.nih.gov/3772638/)).

Consequences for photographs include:

- A blue-grey surround can make neutral image regions appear slightly warmer or yellower.
- Skin, wood, and warm artificial light may appear warmer against a cool surround.
- A saturated surround can alter perceived saturation and colour distance, not merely white balance.
- A neutral surround minimises systematic hue bias, although it cannot remove every contextual effect.

WhiteWall's `#818589` is visually grey but not achromatic: its channels are RGB `(129, 133, 137)`. In CIELAB under D65 it is approximately `L*=55.3, a*=-0.7, b*=-2.7`, a small cool bias. The cited chromatic-surround experiments used much higher chroma, so they establish the direction of risk but do not quantify the visible size of WhiteWall's much smaller bias.

### 2.3 The immediate edge matters most

The border touching the photograph has disproportionate influence. A recent chromatic-induction experiment found a strong effect from an immediately adjacent uniform surround and a much smaller effect when even a thin black rim separated target and surround. Rim width had a statistically significant effect ([Li et al., 2026](https://journals.sagepub.com/doi/10.1177/03010066251409616)).

This makes a photo's perimeter more relevant than its central pixels when selecting an embedded background. A global image average may be dominated by a bright sky, face, or central light while the actual boundary is dark foliage. The resulting border can then create a large and unintended edge contrast.

An edge-based rule is therefore a reasonable product hypothesis, not yet a universal law: sample an outer band of the image, use a robust luminance statistic, and validate the result on real photographs.

### 2.4 Viewing conditions must be controlled for critical judgement

Colour-appearance models exist precisely because colour appearance depends on viewing conditions. CIECAM16 transforms physical colour measurements into perceptual correlates using a specified viewing condition and is intended for photographic prints and self-luminous displays ([CIE 248:2022](https://www.cie.co.at/publications/cie-2016-colour-appearance-model-colour-management-systems-ciecam16)).

Reference standards converge on a controlled neutral surround:

- The ICC reference environment assumes a **uniform matte neutral grey with 20% reflectance** immediately around an image ([ICC.1:2022, section 6.3.3.4](https://www.color.org/specifications/ICC.1-2022-05.pdf)).
- ITU-R BT.500 specifies a D65 background and background luminance around 15% of display peak for critical video assessment ([ITU-R BT.500-14, section 2.1.1](https://www.itu.int/dms_pubrec/itu-r/rec/bt/R-REC-BT.500-14-201910-S%21%21PDF-E.pdf)).
- ISO 3664:2025 standardises viewing conditions for critical and practical appraisal of photographic and graphic images ([ISO 3664:2025](https://www.iso.org/standard/83759.html)).

These are reference-viewing recommendations, not Instagram styling rules. They nevertheless provide a strong baseline: if faithful colour judgement is the goal, use a neutral, stable surround rather than changing the surround with every image.

## 3. WhiteWall's baseline behaviour at the time of the study

At the time of this study, WhiteWall performs the following steps:

1. Decode the first image frame, auto-orient it, and convert it to sRGB.
2. Reduce a copy to at most `64×64` pixels.
3. Convert that copy to grey and calculate its arithmetic mean, `g`, from `0` to `255`.
4. Map `g` linearly in encoded sRGB from `#818589` to `#FFFFFF`:

   ```text
   output_channel(g) = base_channel + round(g × (255 − base_channel) / 255)
   base = (129, 133, 137)
   ```

5. In folder mode, calculate one mean per image, average those image means with equal weight, and apply the resulting colour to every output.

The resulting scale is:

| Input mean `g` | Output | Relative sRGB luminance Y | CIELAB L* |
|---:|---:|---:|---:|
| 0 | `#818589` | 23.25% | 55.33 |
| 32 | `#919498` | 29.47% | 61.19 |
| 64 | `#A1A4A7` | 36.92% | 67.22 |
| 96 | `#B0B3B5` | 44.81% | 72.76 |
| 128 | `#C0C2C4` | 53.78% | 78.33 |
| 160 | `#D0D2D3` | 64.21% | 84.07 |
| 192 | `#E0E1E2` | 75.19% | 89.48 |
| 224 | `#F0F0F1` | 87.20% | 94.82 |
| 255 | `#FFFFFF` | 100% | 100 |

Relative luminance in this table uses linearised sRGB and the standard coefficients `0.2126 R + 0.7152 G + 0.0722 B` ([W3C relative-luminance definition](https://www.w3.org/WAI/GL/wiki/Relative_luminance)).

### Strengths

- The rule is deterministic and inexpensive.
- It responds to image tone rather than selecting an unrelated colour.
- It avoids black surrounds, which can hide the separation between dark image edges and the canvas.
- Folder mode gives every photo equal influence regardless of megapixel count, which is usually more appropriate for a coherent series than pooling every pixel.
- The scale is smooth, and its darkest endpoint is close in luminance to the ICC's 20% reference surround.

### Weaknesses

- `#818589 → #FFFFFF` is a cool chromatic ramp, not a greyscale.
- The output occupies only the upper half of perceptual lightness (`L*=55–100`). A normal midtone input (`g≈128`) creates a very bright `L*=78` surround.
- A global arithmetic mean says little about the tones touching the border.
- Means are sensitive to large bright or dark regions and can be a poor description of a bimodal image.
- Interpolation occurs in encoded sRGB channels rather than in linear luminance or a perceptually uniform lightness dimension.
- The algorithm adapts the surround for every image, so two identical colours can appear different across a carousel even when their encoded pixels are identical.

## 4. Expected effects by image type

### Dark, low-key photograph

The current scale produces a surround no darker than `L*=55`. Against a genuinely dark photograph this creates strong boundary contrast and tends to make the image's shadows appear darker and the overall contrast stronger. Subject separation may improve, but subtle shadow detail may feel suppressed.

### Bright, high-key photograph

The scale approaches white. White clothing, clouds, and pale backgrounds may lose figure-ground separation at the edge. The large bright area also raises adaptation and can make the photograph itself feel dimmer.

### Warm portrait or interior

The low end's cool bias can make warm colours appear warmer by contextual contrast. This may be aesthetically pleasing for skin or tungsten light but is not colour-neutral.

### Image with unrelated centre and edge

A bright central subject against dark edge foliage receives a relatively bright background because the whole-image mean includes the subject. Edge contrast becomes much larger than an edge-aware method would choose.

### Folder or carousel

A single background improves series cohesion and prevents the page from flashing between different surround luminances. The arithmetic mean, however, can be pulled by an outlier such as a night shot or a snow scene. A median of per-image recommendations is more robust.

## 5. Candidate strategies

| Strategy | Colour fidelity | Series consistency | Aesthetic adaptation | Main risk |
|---|---:|---:|---:|---|
| Fixed neutral 20% surround | High | High | Low | Can feel generic |
| Current `#818589 → white` global mean | Medium-low | Medium | High | Bright and slightly cool surround biases appearance |
| Adaptive neutral global median | Medium-high | Medium | Medium | Ignores the edge |
| Adaptive neutral perimeter median | Medium | Medium | High | Can overfit an unusual frame or vignette |
| Adaptive chromatic/dominant colour | Low | Low | Potentially high | Strong hue and saturation induction |

No single strategy optimises all objectives. “Faithful” and “beautiful” are different targets and should not be silently merged into one score.

## 6. Initial recommendation for WhiteWall (superseded by section 10)

### 6.1 Provide two explicit intents

**Faithful**

- Use a fixed achromatic background around 20% relative luminance.
- A practical sRGB approximation is about `#7C7C7C` (`R=G=B`), subject to display calibration.
- This mode is for comparing edits, checking colour, and keeping a carousel perceptually stable.

**Adaptive**

- Preserve `#818589` only if its cool character is a deliberate visual identity.
- Calculate luminance in linear-light sRGB, then work in CIELAB L* or another perceptual-lightness scale.
- Use a robust perimeter statistic: begin with the median luminance of the outer 8% image band.
- Constrain the output to an experimentally tested range. A reasonable pilot range is `L*=52–75`; this is a design hypothesis, not a published optimum.
- For a strictly greyscale result, force `R=G=B`. If the blue-grey ramp is retained, label it as a styled background rather than greyscale.

### 6.2 Folder mode

For each photograph, compute the same per-image target that Adaptive mode would use. Then choose the **median** target across all photographs and apply it unchanged to the entire folder. The median is robust to one unusually dark or bright photo and preserves equal influence per photograph.

### 6.3 Do not modify the photograph to compensate automatically

Changing image gamma or contrast to offset the surround would alter the actual photograph and create a new dependency on display conditions. WhiteWall should first control the border only. Any surround compensation should be a separate, optional colour-managed feature based on a recognised appearance model such as CIECAM16.

## 7. Validation study for WhiteWall

The research literature establishes the phenomenon, but WhiteWall needs product-specific evidence because its border is embedded in social media and occupies a large fraction of the final frame.

### 7.1 Questions

1. Which strategy best preserves perceived colour neutrality?
2. Which strategy gives the best subject separation and aesthetic preference?
3. Does the optimum differ for dark, middle, and bright photographs?
4. Does one shared folder background improve perceived cohesion?
5. Does the result change between controlled desktop viewing and ordinary phone viewing?

### 7.2 Stimuli

Use at least 36 photographs, balanced across:

- dark, middle, and bright mean luminance;
- low and high contrast;
- warm, neutral, and cool colour balance;
- portraits, interiors, landscapes, and graphic/architectural scenes;
- light and dark image perimeters.

Render every photograph with five conditions:

1. fixed neutral 20%;
2. current global-mean ramp;
3. adaptive neutral global median;
4. adaptive neutral perimeter median;
5. black and white controls, split across balanced trials.

### 7.3 Participants and environment

- Start with 24–30 participants with normal or corrected vision and no known colour-vision deficiency.
- Use a calibrated sRGB display at D65 and record peak luminance.
- Keep the physical surround neutral and background luminance near 15% of display peak, following ITU-R BT.500 as the controlled reference.
- Run a second, shorter session on participants' normal phones under ordinary indoor lighting to test ecological validity.

### 7.4 Tasks

Randomise presentation order and use pairwise comparisons rather than asking participants to remember an absolute scale. Measure separately:

- perceived contrast;
- visible shadow detail;
- naturalness of colour and skin;
- subject/background separation;
- overall aesthetic preference;
- carousel cohesion for groups of 6–10 photographs.

Include a neutral-matching task on a subset of images: participants adjust a small nominally neutral patch until it appears neutral. This provides a more diagnostic measure of chromatic induction than preference alone.

### 7.5 Analysis and decision rule

Use a mixed-effects logistic or ordinal model with background strategy as a fixed effect and participant and photograph as random effects. Report confidence intervals and results separately for image-luminance and edge-luminance groups.

Choose the default only after defining the product objective:

- If fidelity is primary, prefer the strategy with the smallest neutral-match error and no meaningful loss of preference.
- If presentation is primary, prefer the strategy with the highest subject-separation and aesthetic scores, but retain Faithful mode.
- If no adaptive method wins reliably across image groups, use fixed neutral grey. Consistency is preferable to an adaptive rule with unstable benefits.

## 8. Final conclusion

Background colour materially changes the viewing of an image; it is not decoration outside the perceptual system. Luminance alters perceived contrast and tone, chroma alters neutral and hue appearance, and the border immediately touching the image has the strongest contextual leverage.

WhiteWall's current adaptive ramp is coherent as a visual style. Its darkest endpoint is close to a conventional reference-surround luminance, but the ramp quickly becomes much brighter and retains a cool tint. It therefore favours presentation over faithful evaluation.

The evidence-backed product direction is a fixed neutral **Faithful** mode plus a separately labelled **Adaptive** mode, with the latter based on robust perimeter lightness and validated on actual phones and photographs. Folder mode should use the median of per-photo targets to keep every image visually consistent.

---

## 9. First implementation decision (superseded by section 10)

Implemented on 21 August 2026:

- **Adaptive** analyses CIELAB lightness, weighting the outer 8% perimeter at 70% and the global image median at 30%.
- The adaptive perceptual scale runs from `#818589` (L* ≈ 55) to neutral `#B9B9B9` (L* ≈ 75).
- **Faithful** uses a fixed neutral `#7C7C7C` background (about 20% relative luminance).
- Folder processing takes the median of the per-photo adaptive targets and applies the exact same background to every output.

Study prepared 21 August 2026. The study itself made no application change; this section records the subsequent implementation.

## 10. Colour-theory revision

### 10.1 Colour theory is perceptual, not just a colour wheel

The traditional complementary/analogous vocabulary describes geometric hue relationships, but it does not by itself predict how a photograph will look. Three different outcomes must be separated:

- **Colour appearance:** a coloured surround changes the colour perceived inside the image through chromatic induction.
- **Figure–ground separation:** differences in lightness, hue, and saturation make the image boundary easier to distinguish.
- **Harmony or preference:** a combination can be harmonious without preserving colour faithfully, and a high-contrast combination can be noticeable without being pleasant.

A uniform coloured surround generally biases the perceived target away from the surround's hue. The effect is strongest when the surround touches the target; even a thin separating rim greatly reduces it ([Li et al., 2026](https://journals.sagepub.com/doi/10.1177/03010066251409616)). Experiments also distinguish chromatic contrast, where the target shifts away from the surround, from assimilation, where fine spatial patterns shift it toward the surround ([Kanematsu et al., 2022](https://www.frontiersin.org/journals/psychology/articles/10.3389/fpsyg.2022.818149/full)). WhiteWall creates a large, uniform, adjacent border, so contrast induction is the more relevant risk.

### 10.2 Complementary is vivid, but not the safest adaptive rule

A complementary background can intensify an existing image hue through simultaneous contrast. For example, a cool surround can make a warm photograph appear warmer. This creates separation, but it also means that the photograph is no longer perceived independently of the frame.

The aesthetic evidence does not support a universal “complements are best” rule. Experiments on figure/ground colour combinations found no general preference or harmony advantage for complementary pairs. Preference for the figure increased with lightness and hue difference, and with a more saturated figure on a less saturated ground ([Schloss & Palmer, 2011](https://link.springer.com/article/10.3758/s13414-010-0027-0)).

An especially relevant experiment presented seven paintings on simulated uniform walls to 38 observers. Backgrounds followed an achromatic path, the painting's global-average hue, or its complementary hue. Backgrounds near the average image colour produced the best harmony; complementary backgrounds were judged unpleasant more often, and white was not the optimum for harmony ([Lachheb, Colantoni & Dinet, 2010](https://library.imaging.org/admin/apis/public/api/ist/website/downloadArticle/cgiv/5/1/art00003)). The study used paintings rather than social-media photographs and only seven images, so it supports the direction of the rule, not an exact universal formula.

### 10.3 Lightness remains a separate control

Surround luminance changes perceived brightness, contrast, colourfulness, and naturalness. In a 14-observer large-display experiment, a bright surround made images appear slightly more colourful, while the dark surround received the highest overall image-quality ratings; naturalness was the strongest predictor of quality ([Choi et al., 2007](https://library.imaging.org/admin/apis/public/api/ist/website/downloadArticle/cic/15/1/art00030)). This again rules out a single universal “brighter is better” value.

For WhiteWall, the embedded frame must also remain visibly separate from the pixels that touch it. The revised rule therefore uses the image perimeter only for lightness and the whole image for hue:

```text
edge_L* = median L* of the outer 8% band
background_L* = 90 - 0.10 × edge_L*        # range 80–90
if |background_L* - edge_L*| < 15:          # crossover near edge_L* ≈ 82
    background_L* = edge_L* ± 15            # lighter below crossover, darker above

image_hue = direction of the global mean (a*, b*)
background_chroma = min(0.35 × image_chroma, 10)
background_hue = image_hue
```

The inverse lightness mapping keeps a visible boundary: a dark edge receives a lighter frame and a light edge receives a somewhat darker frame. The same-hue rule favours palette harmony rather than complementary tension. The `C*=10` ceiling keeps the background less saturated than the photograph and limits chromatic induction. These constants are conservative product hypotheses, not values published as an optimum.

### 10.4 Revised WhiteWall modes

**Faithful** now uses fixed neutral `#F2F2F2`, following the requested near-white visual identity. The name means faithful to WhiteWall's clean white presentation, not faithful colour-critical viewing. A near-white surround can make the photograph appear darker by simultaneous contrast; `#F2F2F2` therefore must not be described as a calibration surround.

**Adaptive** uses the formula above in CIELAB. It deliberately makes a mild aesthetic intervention: the frame echoes the image palette and may alter perceived colour slightly. It avoids complementary colours because they create stronger tension and a less predictable perceptual shift.

For a folder, WhiteWall calculates one CIELAB target per photograph, takes the median independently for `L*`, `a*`, and `b*`, and applies that exact shared colour to all outputs. This preserves carousel cohesion and resists a single tonal or chromatic outlier.

Revision implemented 21 August 2026.
