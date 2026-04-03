const {
  Document, Packer, Paragraph, TextRun, Table, TableRow, TableCell,
  ImageRun, AlignmentType, HeadingLevel, BorderStyle, WidthType,
  ShadingType, LevelFormat, PageNumber, PageBreak, Header, Footer,
  VerticalAlign
} = require("docx");
const fs = require("fs");
const path = require("path");

const BASE = path.join(__dirname, "..");
const RESULTS = path.join(BASE, "results");

function loadImg(filename) {
  const p = path.join(RESULTS, filename);
  if (!fs.existsSync(p)) return null;
  return fs.readFileSync(p);
}

const border = { style: BorderStyle.SINGLE, size: 1, color: "CCCCCC" };
const borders = { top: border, bottom: border, left: border, right: border };
const CM = (cm) => Math.round(cm * 567); // 1 cm ≈ 567 DXA

function heading1(text) {
  return new Paragraph({
    heading: HeadingLevel.HEADING_1,
    spacing: { before: 300, after: 120 },
    children: [new TextRun({ text, bold: true, size: 32, color: "1F4E79" })]
  });
}

function heading2(text) {
  return new Paragraph({
    heading: HeadingLevel.HEADING_2,
    spacing: { before: 200, after: 80 },
    children: [new TextRun({ text, bold: true, size: 26, color: "2E75B6" })]
  });
}

function para(text, opts = {}) {
  return new Paragraph({
    spacing: { before: 60, after: 60 },
    alignment: opts.center ? AlignmentType.CENTER : AlignmentType.JUSTIFIED,
    children: [new TextRun({ text, size: 22, font: "Arial", ...opts })]
  });
}

function bullet(text) {
  return new Paragraph({
    numbering: { reference: "bullets", level: 0 },
    spacing: { before: 40, after: 40 },
    children: [new TextRun({ text, size: 22, font: "Arial" })]
  });
}

function codeBlock(lines) {
  return lines.map(line =>
    new Paragraph({
      spacing: { before: 20, after: 20 },
      shading: { type: ShadingType.CLEAR, fill: "F0F4F8" },
      indent: { left: 360 },
      children: [new TextRun({ text: line, font: "Courier New", size: 18, color: "1A1A2E" })]
    })
  );
}

function imgRow(buf, width = 8600, height = 3600, caption = "") {
  const rows = [];
  if (buf) {
    rows.push(new Paragraph({
      alignment: AlignmentType.CENTER,
      spacing: { before: 120, after: 60 },
      children: [new ImageRun({ data: buf, transformation: { width, height }, type: "png" })]
    }));
  }
  if (caption) {
    rows.push(new Paragraph({
      alignment: AlignmentType.CENTER,
      spacing: { before: 0, after: 160 },
      children: [new TextRun({ text: caption, italics: true, size: 18, color: "555555" })]
    }));
  }
  return rows;
}

function pageBreak() {
  return new Paragraph({ children: [new PageBreak()] });
}

function sectionLine() {
  return new Paragraph({
    spacing: { before: 120, after: 120 },
    border: { bottom: { style: BorderStyle.SINGLE, size: 6, color: "2E75B6", space: 1 } },
    children: [new TextRun("")]
  });
}

// ── Q&A table ───────────────────────────────────────────────────────────────
function qaTable() {
  const rows = [
    ["Q1", "Why does histogram equalization improve contrast?",
     "It redistributes pixel intensities to span the full 0–255 range more uniformly by applying a transformation based on the cumulative distribution function (CDF). Compressed tonal regions are stretched, revealing detail hidden in dark or bright areas."],
    ["Q2", "How does gamma affect brightness?",
     "Gamma uses a power-law: output = input^γ. When γ < 1, dark pixels are raised more than bright ones (brightening). When γ > 1, bright pixels are compressed (darkening). γ = 1 leaves the image unchanged."],
    ["Q3", "What is the effect of quantization on image quality?",
     "Reducing bit depth causes posterization — visible banding in smooth gradients. At 2-bit (4 levels) the image loses nearly all tonal nuance; at 8-bit (256 levels) the image appears continuous. PSNR decreases rapidly below 4-bit."],
    ["Q4", "Which transformation is reversible and why?",
     "Geometric transformations (rotation, translation, shearing) are fully reversible via their inverse affine matrices, because they are bijective mappings — every output pixel corresponds to exactly one input pixel, with no information destroyed (assuming no cropping)."],
    ["Q5", "How do transformations affect spatial structure?",
     "Geometric transforms reposition pixels without changing their intensity values — they alter the spatial layout. Intensity transforms change pixel values without moving them — they alter the tonal distribution. Combining both modifies spatial structure and appearance simultaneously."],
  ];

  return new Table({
    width: { size: 9360, type: WidthType.DXA },
    columnWidths: [560, 2800, 6000],
    rows: rows.map((r, i) =>
      new TableRow({
        children: [
          new TableCell({
            borders, width: { size: 560, type: WidthType.DXA },
            margins: { top: 80, bottom: 80, left: 120, right: 120 },
            shading: { type: ShadingType.CLEAR, fill: i % 2 === 0 ? "DDEEFF" : "F0F6FF" },
            verticalAlign: VerticalAlign.CENTER,
            children: [new Paragraph({ children: [new TextRun({ text: r[0], bold: true, size: 20 })] })]
          }),
          new TableCell({
            borders, width: { size: 2800, type: WidthType.DXA },
            margins: { top: 80, bottom: 80, left: 120, right: 120 },
            shading: { type: ShadingType.CLEAR, fill: i % 2 === 0 ? "DDEEFF" : "F0F6FF" },
            children: [new Paragraph({ children: [new TextRun({ text: r[1], bold: true, size: 20 })] })]
          }),
          new TableCell({
            borders, width: { size: 6000, type: WidthType.DXA },
            margins: { top: 80, bottom: 80, left: 120, right: 120 },
            shading: { type: ShadingType.CLEAR, fill: i % 2 === 0 ? "FFFFFF" : "F8FBFF" },
            children: [new Paragraph({ children: [new TextRun({ text: r[2], size: 20 })] })]
          }),
        ]
      })
    )
  });
}

// ── comparison table ─────────────────────────────────────────────────────────
function samplingTable() {
  const header = ["Scale", "Resolution", "PSNR", "Quality", "Observation"];
  const data = [
    ["0.25×", "64×64",  "33.4 dB", "Degraded",  "Severe blocky artifacts, loss of fine detail"],
    ["0.5×",  "128×128","38.2 dB", "Acceptable","Mild blur, major features preserved"],
    ["1.0×",  "256×256","∞ (ref)", "Excellent", "Original — reference image"],
    ["1.5×",  "384×384","40.5 dB", "Good",      "Slight interpolation smoothing"],
    ["2.0×",  "512×512","43.6 dB", "Good",      "Upscaled; pixelation visible on zoom"],
  ];

  const headerRow = new TableRow({
    tableHeader: true,
    children: header.map((h, i) =>
      new TableCell({
        borders, width: { size: [1200,1500,1200,1500,3960][i], type: WidthType.DXA },
        margins: { top: 80, bottom: 80, left: 120, right: 120 },
        shading: { type: ShadingType.CLEAR, fill: "1F4E79" },
        children: [new Paragraph({ children: [new TextRun({ text: h, bold: true, size: 20, color: "FFFFFF" })] })]
      })
    )
  });

  const dataRows = data.map((row, ri) =>
    new TableRow({
      children: row.map((cell, ci) =>
        new TableCell({
          borders, width: { size: [1200,1500,1200,1500,3960][ci], type: WidthType.DXA },
          margins: { top: 80, bottom: 80, left: 120, right: 120 },
          shading: { type: ShadingType.CLEAR, fill: ri % 2 === 0 ? "F0F6FF" : "FFFFFF" },
          children: [new Paragraph({ children: [new TextRun({ text: cell, size: 20 })] })]
        })
      )
    })
  );

  return new Table({ width: { size: 9360, type: WidthType.DXA }, columnWidths: [1200,1500,1200,1500,3960], rows: [headerRow, ...dataRows] });
}

// ── document ─────────────────────────────────────────────────────────────────
const doc = new Document({
  numbering: {
    config: [
      { reference: "bullets", levels: [{ level: 0, format: LevelFormat.BULLET, text: "•", alignment: AlignmentType.LEFT, style: { paragraph: { indent: { left: 720, hanging: 360 } } } }] },
    ]
  },
  styles: {
    default: { document: { run: { font: "Arial", size: 22 } } },
    paragraphStyles: [
      { id: "Heading1", name: "Heading 1", basedOn: "Normal", next: "Normal", quickFormat: true, run: { size: 32, bold: true, font: "Arial", color: "1F4E79" }, paragraph: { spacing: { before: 300, after: 120 }, outlineLevel: 0 } },
      { id: "Heading2", name: "Heading 2", basedOn: "Normal", next: "Normal", quickFormat: true, run: { size: 26, bold: true, font: "Arial", color: "2E75B6" }, paragraph: { spacing: { before: 200, after: 80 }, outlineLevel: 1 } },
    ]
  },
  sections: [{
    properties: {
      page: {
        size: { width: 12240, height: 15840 },
        margin: { top: 1440, right: 1080, bottom: 1440, left: 1080 }
      }
    },
    headers: {
      default: new Header({
        children: [new Paragraph({
          border: { bottom: { style: BorderStyle.SINGLE, size: 4, color: "2E75B6", space: 1 } },
          children: [new TextRun({ text: "Lab 06 – Smart Image Enhancement & Analysis System  |  Digital Image Processing", size: 18, color: "555555" })]
        })]
      })
    },
    footers: {
      default: new Footer({
        children: [new Paragraph({
          border: { top: { style: BorderStyle.SINGLE, size: 4, color: "2E75B6", space: 1 } },
          alignment: AlignmentType.RIGHT,
          children: [
            new TextRun({ text: "Department of Computer Science  |  Page ", size: 18, color: "555555" }),
            new TextRun({ children: [{ type: "pageNumber" }], size: 18, color: "555555" })
          ]
        })]
      })
    },
    children: [
      // ── TITLE PAGE ──────────────────────────────────────────────────────
      new Paragraph({ alignment: AlignmentType.CENTER, spacing: { before: 1440, after: 240 }, children: [new TextRun({ text: "DEPARTMENT OF COMPUTER SCIENCE", size: 22, bold: true, color: "555555", font: "Arial" })] }),
      new Paragraph({ alignment: AlignmentType.CENTER, spacing: { before: 0, after: 80 }, children: [new TextRun({ text: "Digital Image Processing Lab", size: 26, bold: true, color: "1F4E79", font: "Arial" })] }),
      sectionLine(),
      new Paragraph({ alignment: AlignmentType.CENTER, spacing: { before: 480, after: 120 }, children: [new TextRun({ text: "Lab 06 – Guided Project", size: 36, bold: true, color: "1F4E79", font: "Arial" })] }),
      new Paragraph({ alignment: AlignmentType.CENTER, spacing: { before: 0, after: 600 }, children: [new TextRun({ text: "Smart Image Enhancement & Analysis System", size: 48, bold: true, color: "2E75B6", font: "Arial" })] }),
      sectionLine(),
      new Paragraph({ alignment: AlignmentType.CENTER, spacing: { before: 480, after: 80 }, children: [new TextRun({ text: "Instructor:  Mr. Ghulam Ali", size: 26, font: "Arial", color: "333333" })] }),
      new Paragraph({ alignment: AlignmentType.CENTER, spacing: { before: 80, after: 80 }, children: [new TextRun({ text: "Submitted by:  [Your Name]", size: 26, bold: true, font: "Arial", color: "1F4E79" })] }),
      new Paragraph({ alignment: AlignmentType.CENTER, spacing: { before: 80, after: 80 }, children: [new TextRun({ text: "Registration ID:  [Your Reg ID]", size: 24, font: "Arial", color: "333333" })] }),
      new Paragraph({ alignment: AlignmentType.CENTER, spacing: { before: 80, after: 80 }, children: [new TextRun({ text: "Semester:  [Your Semester]", size: 24, font: "Arial", color: "333333" })] }),
      new Paragraph({ alignment: AlignmentType.CENTER, spacing: { before: 360, after: 80 }, children: [new TextRun({ text: "GitHub: https://github.com/[your-username]/DIP-Image-Enhancement-System", size: 20, color: "2E75B6", font: "Arial" })] }),
      pageBreak(),

      // ── 1. OBJECTIVE ────────────────────────────────────────────────────
      heading1("1. Objective"),
      sectionLine(),
      para("The objective of this project is to design and implement a complete Smart Image Enhancement and Analysis System that integrates the core concepts covered in Labs 01 through 05. The system accepts a low-quality image as input and produces an enhanced, visually improved output along with analytical insights generated at each phase of the pipeline."),
      para("By the end of this project, the following skills are demonstrated:"),
      bullet("Building a modular, end-to-end image processing pipeline in Python"),
      bullet("Applying image acquisition, sampling, geometric, and intensity transformations systematically"),
      bullet("Performing histogram analysis and equalization for contrast improvement"),
      bullet("Designing a professional-grade final pipeline function: process_image()"),
      bullet("Documenting and presenting technical work in a structured report"),
      pageBreak(),

      // ── 2. METHODOLOGY ──────────────────────────────────────────────────
      heading1("2. Methodology"),
      sectionLine(),
      para("The system follows a structured processing pipeline with six distinct phases:"),
      para("Input Image  →  Phase 1 (Acquisition)  →  Phase 2 (Sampling)  →  Phase 3 (Geometric)  →  Phase 4 (Intensity)  →  Phase 5 (Histogram)  →  Phase 6 (Final Pipeline)  →  Enhanced Output + Report", { bold: true, color: "1F4E79" }),

      heading2("Phase 6.1 – Image Acquisition & Understanding"),
      para("The image is loaded using OpenCV's cv2.imread() in BGR format and then converted to grayscale using cv2.cvtColor(). The initial image report documents the resolution, number of channels, data type, and a partial print of the pixel matrix to confirm successful loading."),
      ...codeBlock([
        "import cv2",
        "img_bgr  = cv2.imread('images/input/sample.png')",
        "img_rgb  = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)",
        "img_gray = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2GRAY)",
        "print(img_gray.shape, img_gray.dtype)",
        "print(img_gray[:5, :5])  # partial matrix print",
      ]),
      ...imgRow(loadImg("phase1_acquisition.png"), 8600, 3800, "Figure 1: Phase 1 – Image acquisition report showing RGB, grayscale, and pixel matrix"),

      heading2("Phase 6.2 – Sampling & Quantization Analysis"),
      para("The image is resampled at five scales: 0.25×, 0.5×, 1.0× (original), 1.5×, and 2.0×. Each resampled image is restored to the original canvas size using nearest-neighbour interpolation for a fair visual comparison. Bit depth reduction is applied at 8-bit, 4-bit, and 2-bit by dividing pixel values into discrete levels."),
      ...codeBlock([
        "# Resampling",
        "resized = cv2.resize(img, (new_w, new_h), interpolation=cv2.INTER_LINEAR)",
        "# Quantization (4-bit example: 16 levels)",
        "quantized = (img // 16) * 16",
      ]),
      ...imgRow(loadImg("phase2_sampling.png"), 8600, 2800, "Figure 2: Sampling comparison at five scales (0.25× to 2.0×)"),
      ...imgRow(loadImg("phase2_quantization.png"), 7000, 2600, "Figure 3: Bit depth reduction — 8-bit, 4-bit, 2-bit"),

      para("Comparison Table: Resolution vs Visual Quality"),
      samplingTable(),
      para(""),

      heading2("Phase 6.3 – Geometric Transformations"),
      para("Seven rotation angles (30°, 45°, 60°, 90°, 120°, 150°, 180°) are applied using OpenCV's rotation matrix. Translation and shearing transformations are implemented using affine warp matrices. Inverse transformations (e.g., -45° rotation, inverse translation offsets) are applied to demonstrate image restoration."),
      ...codeBlock([
        "# Rotation",
        "M = cv2.getRotationMatrix2D((w/2, h/2), angle, 1.0)",
        "rotated = cv2.warpAffine(img, M, (w, h))",
        "# Translation",
        "M_t = np.float32([[1, 0, tx], [0, 1, ty]])",
        "translated = cv2.warpAffine(img, M_t, (w, h))",
        "# Shear",
        "M_s = np.float32([[1, shx, 0], [0, 1, 0]])",
        "sheared = cv2.warpAffine(img, M_s, (new_w, h))",
      ]),
      ...imgRow(loadImg("phase3_rotations.png"), 8600, 4000, "Figure 4: Rotation grid — 30° through 180°"),
      ...imgRow(loadImg("phase3_transforms.png"), 8600, 4000, "Figure 5: Translation, shear, and inverse transformation comparison"),

      heading2("Phase 6.4 – Intensity Transformations"),
      para("Four intensity transformations are applied and compared: (1) Negative — each pixel value s = 255 − r; (2) Log transform — s = c · log(1 + r), which compresses highlights and expands dark regions; (3) Gamma γ=0.5 — power-law brightening; (4) Gamma γ=1.5 — power-law darkening. Mean and standard deviation are computed for each output."),
      ...codeBlock([
        "# Negative",
        "negative = 255 - img",
        "# Log transform",
        "c = 255 / np.log(1 + img.max())",
        "log_img = (c * np.log(1 + img.astype(float))).astype(np.uint8)",
        "# Gamma correction",
        "gamma_05 = np.power(img / 255.0, 0.5) * 255",
        "gamma_15 = np.power(img / 255.0, 1.5) * 255",
      ]),
      ...imgRow(loadImg("phase4_intensity.png"), 8600, 4000, "Figure 6: Intensity transformations with histograms — negative, log, γ=0.5, γ=1.5"),
      para("Analysis: Gamma γ=0.5 is the best method for overall brightening as it non-linearly elevates dark pixels. The Log Transform is most effective for highlighting fine detail in shadow regions by compressing the highlight range."),

      heading2("Phase 6.5 – Histogram Processing"),
      para("The grayscale histogram is plotted to analyze the contrast distribution of the original image. Standard histogram equalization (cv2.equalizeHist) and CLAHE (Contrast Limited Adaptive Histogram Equalization) are applied. CDF curves are plotted for each to show the redistribution of intensities."),
      ...codeBlock([
        "# Histogram equalization",
        "equalized = cv2.equalizeHist(img_gray)",
        "# CLAHE",
        "clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))",
        "clahe_img = clahe.apply(img_gray)",
      ]),
      ...imgRow(loadImg("phase5_histogram.png"), 8600, 5200, "Figure 7: Before/after histogram and CDF comparison — original, equalized, CLAHE"),
      para("Observation: The original image has a compressed histogram (std = 22.65). After equalization, the std rises to 74.10 and the full 0–255 range is utilized. CLAHE provides local enhancement without over-brightening uniform regions."),

      heading2("Phase 6.6 – Final Integrated Pipeline"),
      para("The process_image() function combines the most effective methods from all phases into a clean, modular pipeline. The function automatically detects whether the input is grayscale or color and applies the appropriate pathway."),
      ...codeBlock([
        "def process_image(input_image):",
        "    # Color path: process luminance channel only",
        "    ycrcb = cv2.cvtColor(input_image, cv2.COLOR_BGR2YCrCb)",
        "    y, cr, cb = cv2.split(ycrcb)",
        "    y = apply_clahe(y, clip=2.0)          # Step 1: local contrast",
        "    y = gamma_correction(y, gamma=0.85)    # Step 2: brightening",
        "    y = log_blend(y, alpha=0.25)            # Step 3: shadow detail",
        "    y = unsharp_mask(y, sigma=1.0)          # Step 4: sharpening",
        "    merged = cv2.merge([y, cr, cb])",
        "    return cv2.cvtColor(merged, cv2.COLOR_YCrCb2BGR)",
      ]),
      ...imgRow(loadImg("final_comparison.png"), 8600, 3200, "Figure 8: Final pipeline — original input vs enhanced output"),
      pageBreak(),

      // ── 3. OBSERVATIONS ─────────────────────────────────────────────────
      heading1("3. Observations & Analysis"),
      sectionLine(),
      bullet("Down-sampling to 0.25× caused severe quality loss (PSNR 33.4 dB) with visible blocking; up-sampling to 2× introduced slight interpolation blur but retained structural content."),
      bullet("Bit depth reduction below 4-bit produced strong posterization; 8-bit was perceptually lossless."),
      bullet("Geometric transformations are fully reversible — applying the exact inverse affine matrix recovered the original image, with only minor interpolation error near edges."),
      bullet("Gamma γ=0.5 was the most effective brightening method, raising the image mean from 91 to 151; the Log Transform was best for detail enhancement in shadow regions."),
      bullet("Global histogram equalization boosted std from 22.65 to 74.10 but introduced over-saturation in some areas. CLAHE provided a more balanced enhancement locally."),
      bullet("The final pipeline (CLAHE + Gamma + Log Blend + Unsharp Mask) produced a perceptually superior output: improved contrast, brighter shadows, and sharper edges."),
      pageBreak(),

      // ── 4. Q&A ──────────────────────────────────────────────────────────
      heading1("4. Question & Answer"),
      sectionLine(),
      qaTable(),
      pageBreak(),

      // ── 5. CONCLUSION ───────────────────────────────────────────────────
      heading1("5. Conclusion"),
      sectionLine(),
      para("This project successfully demonstrated the design and implementation of a complete Smart Image Enhancement and Analysis System. By systematically applying concepts from all six labs — image acquisition, sampling, geometric transformations, intensity mappings, and histogram processing — a fully functional and modular pipeline was developed."),
      para("The final process_image() function integrates CLAHE for local contrast enhancement, gamma correction for non-linear brightening, a log transform blend for shadow recovery, and unsharp masking for edge sharpening. The pipeline operates on both grayscale and color images by processing the luminance channel in YCrCb space, preserving natural color balance while improving tonal quality."),
      para("Key takeaways from this project include the importance of selecting transformation methods based on the specific deficiency of the image (low contrast vs low brightness vs detail loss), and the value of modular code structure for maintainability and reusability. The project also reinforced that inverse transformations for geometric operations are mathematically exact, while intensity transformations are generally irreversible without prior knowledge of the original values."),
      sectionLine(),
      new Paragraph({ alignment: AlignmentType.CENTER, spacing: { before: 240, after: 0 }, children: [new TextRun({ text: "— End of Report —", size: 20, italics: true, color: "888888" })] }),
    ]
  }]
});

Packer.toBuffer(doc).then(buf => {
  const outPath = path.join(BASE, "report.docx");
  fs.writeFileSync(outPath, buf);
  console.log("report.docx written:", outPath);
});
