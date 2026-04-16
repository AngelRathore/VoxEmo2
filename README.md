# 🎙 Voxemo — Speech Emotion Recognition System

> Production-ready full-stack system classifying 8 emotions from speech audio using deep learning.

![FastAPI](https://img.shields.io/badge/FastAPI-Backend-009688?style=flat-square)
![React](https://img.shields.io/badge/React-Frontend-61DAFB?style=flat-square)
![TensorFlow](https://img.shields.io/badge/TensorFlow-Model-FF6F00?style=flat-square)
![SQLite](https://img.shields.io/badge/SQLite-Database-003B57?style=flat-square)

---

## ✨ Features

- **Upload or Record** — Drag-and-drop WAV/MP3 or record live via browser mic with real-time waveform
- **Deep Learning** — Keras model trained on RAVDESS with 194-dim features (MFCC, Chroma, Mel, Contrast, Tonnetz)
- **8 Emotion Classes** — angry, calm, disgust, fearful, happy, neutral, sad, surprised
- **Confidence Scores** — Full probability breakdown with animated bar chart
- **SQLite History** — Every prediction persisted to DB, viewable and clearable from `/history`
- **Robust Validation** — File type, size (max 10 MB), duration (max 30s), and corruption checks
- **Config via `.env`** — All paths, limits, and API keys configurable without touching code
- **Groq-ready** — `GROQ_API_KEY` wired in for future LLM feature extensions

---

## 🏗️ Architecture

```
voxemo/
├── .vscode/
│   ├── launch.json        # Debug: Backend / Frontend / Both
│   ├── tasks.json         # Tasks: install, start, health check
│   ├── settings.json      # Python venv, Black, Prettier, file nesting
│   └── extensions.json    # Recommended extensions
│
├── backend/
│   ├── app/
│   │   ├── config.py              # Pydantic Settings — reads .env
│   │   ├── main.py                # FastAPI + CORS + DB init on startup
│   │   ├── routes/
│   │   │   ├── health.py          # GET  /health  (model + config status)
│   │   │   ├── predict.py         # POST /predict (full validation pipeline)
│   │   │   └── history.py         # GET  /history · DELETE /history
│   │   ├── services/
│   │   │   └── predictor.py       # Inference: features → scaler → PCA → model
│   │   ├── models/
│   │   │   └── loader.py          # Thread-safe lazy singleton loader
│   │   ├── db/
│   │   │   └── database.py        # SQLAlchemy + Prediction model + get_db()
│   │   └── utils/
│   │       └── feature_extractor.py   # 194-dim librosa pipeline (config-driven)
│   ├── models/            # ← place your .h5 / .pkl files here
│   ├── .env.example
│   └── requirements.txt
│
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── Navbar.js           # Home · Analyze · History · GitHub
│   │   │   ├── AudioUploader.js    # Drag-and-drop upload
│   │   │   ├── Recorder.js         # Mic recording + canvas waveform
│   │   │   ├── ResultCard.js       # Emotion result + probability bars
│   │   │   └── Loader.js           # Animated loading indicator
│   │   ├── pages/
│   │   │   ├── HomePage.js         # Landing: hero, emotion grid, features
│   │   │   ├── PredictPage.js      # Main analysis page
│   │   │   └── HistoryPage.js      # DB-backed prediction history table
│   │   ├── hooks/
│   │   │   └── useAudioRecorder.js # MediaRecorder hook
│   │   └── styles/global.css
│   ├── .env.example
│   └── package.json
│
├── api.http               # REST Client test file (VS Code)
├── Makefile               # make install / dev / health / clean
├── package.json           # Root: concurrently dev runner
└── README.md
```

---

## ⚙️ Setup

### Prerequisites
- Python 3.10+
- Node.js 18+
- Your trained model files:
  - `emotion_keras_model_22113034.h5`
  - `minmax_scaler_22113034.pkl`
  - `pca_transform_22113034.pkl`

---

### 1. Clone & install everything

```bash
# Install Python venv + npm packages in one shot
make install

# Or manually:
cd backend && python -m venv venv && source venv/bin/activate && pip install -r requirements.txt
cd frontend && npm install
npm install   # root (installs concurrently)
```

### 2. Configure environment

```bash
cd backend
cp .env.example .env
# Edit .env — set GROQ_API_KEY if needed, adjust paths/limits
```

### 3. Place model files

```bash
cp /path/to/emotion_keras_model_22113034.h5   backend/models/
cp /path/to/minmax_scaler_22113034.pkl        backend/models/
cp /path/to/pca_transform_22113034.pkl        backend/models/
```

### 4. Run

```bash
make dev
# Backend  → http://localhost:8000
# Frontend → http://localhost:3000
# API docs → http://localhost:8000/docs
```

---

## 🔌 API Reference

### `GET /health`
```json
{
  "status": "ok",
  "service": "Voxemo API",
  "model_ready": true,
  "model_dir": "./models",
  "max_audio_size_mb": 10,
  "max_audio_duration_sec": 30
}
```

### `POST /predict`
Upload audio file (`multipart/form-data`, field name `file`).

**Validated:** extension, MIME type, size ≤ 10 MB, duration 0.5–30s, not corrupted.

```json
{
  "emotion": "happy",
  "confidence": 0.8714,
  "emoji": "😄",
  "color": "#22c55e",
  "id": 42,
  "saved_at": "2024-06-01 14:32:10",
  "all_emotions": [
    { "label": "happy", "probability": 0.8714, "emoji": "😄", "color": "#22c55e" },
    ...
  ]
}
```

**Error responses:**
| Code | Reason |
|------|--------|
| 400  | Empty file |
| 413  | File exceeds size limit |
| 415  | Unsupported file type |
| 422  | Audio too short/long or corrupted |
| 500  | Model inference failure |

### `GET /history?limit=20&offset=0`
```json
{
  "total": 87,
  "offset": 0,
  "limit": 20,
  "results": [{ "id": 42, "emotion": "happy", "confidence": 0.87, ... }]
}
```

### `DELETE /history`
Clears all records from SQLite.

---

## 🔑 Environment Variables

| Variable | Default | Description |
|---|---|---|
| `PORT` | `8000` | API server port |
| `MODEL_DIR` | `./models` | Directory containing model files |
| `MODEL_FILE` | `emotion_keras_model_22113034.h5` | Keras model filename |
| `SCALER_FILE` | `minmax_scaler_22113034.pkl` | MinMaxScaler filename |
| `PCA_FILE` | `pca_transform_22113034.pkl` | PCA transform filename |
| `MAX_AUDIO_SIZE_MB` | `10` | Maximum upload size in MB |
| `MAX_AUDIO_DURATION_SEC` | `30` | Maximum audio duration in seconds |
| `DATABASE_URL` | `sqlite:///./voxemo.db` | SQLAlchemy DB URL |
| `GROQ_API_KEY` | _(empty)_ | Your Groq API key |
| `GROQ_MODEL` | `llama3-8b-8192` | Groq model to use |

---

## 🧠 Model Details

| Item | Value |
|---|---|
| Dataset | RAVDESS |
| Architecture | Dense NN: 512 → 256 → 128 → 64 → 8 |
| Features | 194-dim (MFCC×40, Chroma×12, Mel×128, Contrast×7, Tonnetz×6, Flatness×1) |
| Preprocessing | MinMaxScaler → PCA (97 components) |
| Training | AdamW, EarlyStopping, ReduceLROnPlateau, class weights |
| Output | 8 emotions: angry · calm · disgust · fearful · happy · neutral · sad · surprised |

---

## 🛠 VS Code Workflow

Open the `voxemo/` folder in VS Code.

| Action | How |
|---|---|
| Run both servers | Run & Debug panel → **🎙 Voxemo (Both Servers)** |
| Run tasks | `Ctrl+Shift+B` → **▶ Start Full Stack** |
| Test API | Open `api.http`, click **Send Request** (REST Client extension) |
| Install all | Terminal: `make install` |
