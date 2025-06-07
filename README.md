# 🧠 CodeFlow Visualizer

**CodeFlow Visualizer** is a full-stack, AI-driven pipeline that automatically converts raw source code into professional, stylized diagrams that visually explain the code’s logic. Designed for engineers, educators, and non-technical stakeholders, it streamlines code comprehension by combining state-of-the-art language models, graph rendering, and generative AI art.

---

## 🚀 Features

- **Multi-language Support:** Converts Python and other popular programming languages into flowchart logic.
- **AI-Powered Parsing:** Uses large language models to extract logical flow from code.
- **Fast Sketch Rendering:** Generates clean, intermediate flowchart sketches using Graphviz.
- **Professional Diagram Generation:** Stylizes diagrams with Stable Diffusion, ControlNet, and LoRA for a technical/blueprint look.
- **User-Friendly UI:** Minimal, elegant Gradio interface for code input and diagram output.
- **Containerized & Scalable:** Runs in Docker for easy deployment and reproducibility.

---

## 🏗️ Project Structure

```
codeflow-visualizer/
├── backend/
│   ├── code_parser.py         # Sends code to LLM and parses flowchart description
│   ├── sketch_generator.py    # Converts flowchart description to a Graphviz sketch
│   ├── comfy_client.py        # Sends sketch to ComfyUI for diagram generation
│   └── orchestrator.py        # Orchestrates the full pipeline
├── frontend/
│   └── gradio_ui.py           # Gradio-based web UI
├── workflows/
│   └── flowchart_api.json     # ComfyUI workflow definition
├── models/
│   ├── controlnet/            # ControlNet weights (e.g., control_sd15_scribble.pth)
│   └── lora/                  # LoRA weights (e.g., Blueprint / Technical Drawing.safetensors)
├── requirements.txt           # Python dependencies
├── Dockerfile                 # Docker build file
├── docker-compose.yml         # Multi-container orchestration
└── README.md                  # This file
```

---

## 🧩 Pipeline Overview

1. **Code Parsing**
    - `code_parser.py` sends code to [CodeLlama-7B-Instruct](https://huggingface.co/codellama/CodeLlama-7b-Instruct-hf) via Hugging Face API.
    - The model returns a structured, natural language flowchart description (e.g., `Start → Step1 → [Condition] → Step2`).

2. **Sketch Generation**
    - `sketch_generator.py` parses the flowchart description and uses [PyGraphviz](https://pygraphviz.github.io/) to render a fast, clean sketch (`.png`).

3. **Diagram Generation**
    - `comfy_client.py` sends the sketch to a [ComfyUI](https://github.com/comfyanonymous/ComfyUI) workflow.
    - Uses [Stable Diffusion v1.5](https://huggingface.co/runwayml/stable-diffusion-v1-5), [ControlNet (Scribble)](https://huggingface.co/lllyasviel/ControlNet), and [Blueprint / Technical Drawing LoRA](https://civitai.com/models/36659) for stylization.

4. **Orchestration**
    - `orchestrator.py` ties all steps together with a single function: `visualize_code(code: str)`.

5. **Frontend**
    - `gradio_ui.py` provides a simple web interface for code input and diagram output.

---

## 🧠 Models Used

| Stage                | Model/Tool                                      | Role/Why Chosen                                                                 |
|----------------------|-------------------------------------------------|---------------------------------------------------------------------------------|
| Code Parsing         | CodeLlama-7B-Instruct (API)                     | Accurate, multi-language code-to-flowchart parsing                              |
| Sketch Generation    | PyGraphviz (Graphviz)                           | Fast, reliable, and CPU-friendly flowchart rendering                            |
| Diagram Generation   | Stable Diffusion v1.5 + ControlNet (Scribble)   | Lightweight, preserves sketch structure, stylizes diagrams                      |
| Diagram Styling      | Blueprint / Technical Drawing LoRA              | Adds blueprint/technical style overlay                                          |

---

## ⚡ Performance & Reliability

- **Optimized for CPU:** All models/tools are chosen for CPU compatibility (though SD/ControlNet are slow on CPU).
- **Caching:** API responses and sketches can be cached for speed.
- **Error Handling:** Robust input validation and fallback logic for reliability.

---

## 🛠️ Setup & Installation

### 1. **Clone the Repository**
```sh
git clone https://github.com/HasnaKhantouche/codeflow-visualizer.git
cd codeflow-visualizer
```

### 2. **Download Models**
- Place the following in `models/`:
    - ControlNet: `control_sd15_scribble.pth` ([Hugging Face](https://huggingface.co/lllyasviel/ControlNet))
    - LoRA: `Blueprint / Technical Drawing.safetensors` ([CivitAI](https://civitai.com/models/36659))

### 3. **Build and Run with Docker**
```sh
docker-compose up --build
```
- This spins up both the main app and ComfyUI service.

### 4. **Access the UI**
- Open your browser at: [http://localhost:7860](http://localhost:7860)

---

## 📝 Usage

1. Paste your code (Python, JavaScript, C, etc.) into the input box.
2. Click **Generate**.
3. View and download the generated diagram.

---

## ❓ FAQ

**Q: Does it work for all programming languages?**  
A: It works best for Python and popular languages (JavaScript, C, Java, etc.). For less common languages, parsing accuracy may vary.

**Q: Can I run everything on CPU?**  
A: Yes, but diagram generation (Stable Diffusion/ControlNet) will be slow. For faster results, use a GPU.

**Q: Is my code sent to external APIs?**  
A: Yes, code is sent to Hugging Face’s Inference API for parsing. All image generation is local.

---

## 📦 Dependencies

- Python 3.11+
- PyGraphviz
- Gradio
- Requests
- Docker & Docker Compose

(See `requirements.txt` for full list.)

---

## 📜 License

MIT License

---

## 🙏 Credits

- [CodeLlama-7B-Instruct](https://huggingface.co/codellama/CodeLlama-7b-Instruct-hf)
- [Stable Diffusion v1.5](https://huggingface.co/runwayml/stable-diffusion-v1-5/resolve/main/v1-5-pruned.safetensors)
- [ControlNet (Scribble)](https://huggingface.co/lllyasviel/ControlNet/blob/main/models/control_sd15_scribble.pth)
- [Blueprint / Technical Drawing LoRA](https://civitai.com/models/637539/blueprint-technical-drawing)
- [ComfyUI](https://github.com/comfyanonymous/ComfyUI)
- [PyGraphviz](https://pygraphviz.github.io/)
