/**
 * AI Career Copilot — Frontend Application Logic
 * Author: Fenil Varde | github.com/vardefenil
 *
 * Features:
 *  - Custom Resume PDF Upload & Live Re-Indexing
 *  - ATS Scorer, Job Matcher, Mock Interviewer, Cold Email Tools
 *  - Live Gemini 3.6 Flash mode + Demo mode for GitHub Pages
 *  - Typewriter animation & Markdown formatting
 *  - Copy to clipboard
 */

// ── Configuration ───────────────────────────────────────────────────────────
const CONFIG = {
  isDemo: window.location.hostname.includes('github.io') ||
          new URLSearchParams(window.location.search).get('demo') === 'true',
  apiBase: window.location.origin,
  typingSpeed: 10,
  typingVariance: 6,
};

// If running directly as static file without a server, point API to localhost
if (window.location.protocol === 'file:') {
  CONFIG.apiBase = 'http://localhost:8000';
}

// ── Demo Response Data ───────────────────────────────────────────────────────
const DEMO_QA = [
  {
    keywords: ['ats', 'score', 'audit', 'review resume', 'format'],
    answer: `📊 **Comprehensive ATS Resume Scan & Score**

### 🎯 Estimated ATS Score: **88 / 100** (Grade: Strong Candidate)

---

### ✅ Key Strengths:
• **Quantifiable Metrics:** Clear impact points (*"reducing manual review by 60%"*, *"20+ voice command types"*, *"10+ structured fields"*).
• **Clean Tech Stacks:** Distinct technologies listed per project (Python, scikit-learn, LangChain, FAISS, Flask).
• **Standard Headings:** Follows universal ATS section conventions (*Summary, Education, Projects, Technical Skills, Certifications*).

### 🔍 Recommended Keywords for AI/ML Roles:
• Add: \`FastAPI\`, \`Vector Databases\`, \`RAG (Retrieval-Augmented Generation)\`, \`Prompt Engineering\`, \`Docker\`, \`CI/CD\`.

### 🚀 Action Verb Enhancement:
• *Before:* 'Built an end-to-end fraud detection system...'
• *After:* 'Architected & deployed a production ML fraud detection pipeline across 4 classifier models with 94%+ ROC-AUC.'`,
  },
  {
    keywords: ['job match', 'match', 'jd', 'job description', 'fit', 'qualif'],
    answer: `💼 **Job Description Match Analysis**

### 🎯 Match Score: **85% Alignment for AI/ML & Python Developer Roles**

---

### 🟢 Exact Matches Found:
• **Languages & Frameworks:** Python, C++, scikit-learn, Pandas, NumPy, Flask, FastAPI.
• **AI / Architecture:** RAG Pipelines, Vector Search (FAISS), ReAct Agents (LangGraph), LLM APIs (Gemini).
• **Core CS:** Data Structures & Algorithms, OOP, Database Management (SQL).

### 🟡 Recommendations / Next Steps:
• Emphasize containerization (Docker) and Cloud deployment (AWS/GCP).
• Highlight the end-to-end RAG workflow built in the AI Career Copilot project during technical rounds.`,
  },
  {
    keywords: ['interview', 'mock', 'prep', 'behavioral', 'questions'],
    answer: `🎙️ **Tailored Technical & Behavioral Mock Interview**

### 1. Technical Project Deep-Dive (Credit Card Fraud Detection):
**Q:** *"How did you handle the class imbalance in your fraud detection dataset, and why choose Precision-Recall / ROC-AUC over Accuracy?"*
👉 **Key talking points:** Mention techniques like SMOTE, class weighting in Random Forest / XGBoost, and how accuracy is deceptive in 99:1 imbalanced transaction data.

### 2. Architecture & RAG (AI Career Copilot):
**Q:** *"Explain how chunk size and overlap in RecursiveCharacterTextSplitter impact retrieval accuracy in FAISS."*
👉 **Key talking points:** Discuss context preservation across chunk boundaries (1000 chars with 200 overlap) and avoiding hallucination in LLM prompts.

### 3. Behavioral (STAR Method):
**Q:** *"Tell me about a challenging bug you encountered while integrating Gemini AI in your voice assistant and how you resolved it."*`,
  },
  {
    keywords: ['cold email', 'email', 'cover letter', 'outreach', 'recruiter'],
    answer: `✉️ **Tailored Recruiter Outreach & Cover Letter**

### 📬 High-Conversion Cold Email:

**Subject:** B.E. Computer Engineering Student | Applied AI & RAG Developer — Fenil Varde

Hi [Hiring Manager / Recruiter Name],

I've been following [Company Name]'s recent work in AI engineering. As a Computer Engineering undergraduate with hands-on experience building end-to-end RAG systems (LangGraph + FAISS + Gemini) and production ML pipelines (Fraud Detection with XGBoost), I would love to contribute to your engineering team.

A quick look at my work:
• **AI Career Copilot:** Live RAG agent querying complex unstructured documents with sub-second retrieval.
• **Fraud Detection System:** Evaluated 4 ML algorithms on imbalanced data with real-time Flask analytics.

Are you open to a brief 10-minute chat this week?

Best regards,
**Fenil Varde**
🔗 LinkedIn: linkedin.com/in/fenil-varde-58145b318/ | 🐙 GitHub: github.com/vardefenil`,
  },
  {
    keywords: ['project', 'built', 'created', 'portfolio', 'app', 'application'],
    answer: `🚀 Here are Fenil's key projects:

**1. AI Career Copilot** (2026 — This Project!)
→ RAG-based AI agent that answers questions about a resume locally using FAISS + LangGraph + Google Gemini 3.6 Flash. Includes live PDF upload, ATS scoring, and interview prep.

**2. Credit Card Fraud Detection System** (2026)
→ End-to-end fraud detection using Logistic Regression, Random Forest, SVM & XGBoost on highly imbalanced datasets. Built a Flask dashboard for real-time transaction analysis.

**3. AI-Based Resume Analytics Tool** (2026)
→ Parses PDF resumes, extracts 10+ structured fields (skills, education, experience) using Python, Flask & NLP. Reduced manual review effort by ~60%.

**4. AI-Powered Voice Assistant** (2024)
→ Voice-controlled desktop assistant with 20+ command types. Integrates Google Gemini AI, NewsAPI, music playback & website navigation.`,
  },
  {
    keywords: ['skill', 'tech', 'technology', 'language', 'tools', 'stack', 'know', 'expertise'],
    answer: `🛠️ Fenil's Technical Skills:

**Languages:** Python · C++ · HTML · CSS

**AI / ML / RAG:**
LangChain · LangGraph · FAISS · Google Gemini · HuggingFace Transformers · RAG Pipelines · ReAct Agents

**ML Libraries:**
scikit-learn · NumPy · Pandas · Matplotlib · Seaborn

**Web & Backend:**
FastAPI · Flask · REST APIs

**Tools & Platforms:**
Git · GitHub · VS Code · Jupyter Notebook

**Concepts:**
Feature Engineering · Model Evaluation · Cross Validation · Imbalanced Data Handling · Vector Embeddings · Semantic Search`,
  },
  {
    keywords: ['education', 'college', 'university', 'degree', 'study', 'school', 'gpa', 'cpi'],
    answer: `🎓 Education:

**B.E. in Computer Engineering** (2023 – 2027)
LDRP Institute of Technology and Research, Gandhinagar, Gujarat
CPI: 7.66 / 10.00

**Relevant Coursework:**
Data Structures · Object-Oriented Programming · Database Management Systems · Operating Systems

**Higher Secondary (Class XII):** GSEB Science — 56.92%
**Secondary School (Class X):** GSEB — 80.83%`,
  },
  {
    keywords: ['contact', 'email', 'phone', 'linkedin', 'github', 'reach', 'hire', 'connect'],
    answer: `📬 Get in touch with Fenil:

📧 **Email:** vardefenil6@gmail.com
📱 **Phone:** +91 87804 71545
💼 **LinkedIn:** linkedin.com/in/fenil-varde-58145b318/
🐙 **GitHub:** github.com/vardefenil
⚡ **LeetCode:** leetcode.com/u/vardefenil6/

Feel free to reach out for collaborations, internship opportunities, or just to connect! 🤝`,
  },
];

// ── State ────────────────────────────────────────────────────────────────────
let isTyping = false;
let messageCount = 0;

// ── DOM References ───────────────────────────────────────────────────────────
const messagesEl    = document.getElementById('messages');
const welcomeEl     = document.getElementById('welcome-state');
const inputEl       = document.getElementById('chat-input');
const sendBtn       = document.getElementById('send-btn');
const clearBtn      = document.getElementById('clear-btn');
const modeBadge     = document.getElementById('mode-badge');
const modeIndicator = document.getElementById('mode-indicator');
const fileInput     = document.getElementById('pdf-file-input');
const dropZone      = document.getElementById('drop-zone');
const uploadText    = document.getElementById('upload-text');
const jdModal       = document.getElementById('jd-modal');
const jdTextarea    = document.getElementById('jd-textarea');

// ── Initialization ───────────────────────────────────────────────────────────
function init() {
  updateModeUI();
  attachEventListeners();
  setupFileUpload();
  inputEl.focus();
}

async function updateModeUI() {
  if (CONFIG.isDemo) {
    modeBadge.textContent = '🟢 Demo Mode';
    modeIndicator.querySelector('.mode-text').textContent = 'Demo mode — pre-built answers (GitHub Pages)';
    return;
  }

  try {
    const res = await fetch(`${CONFIG.apiBase}/health`);
    if (res.ok) {
      const data = await res.json();
      if (data.mode === 'live') {
        modeBadge.textContent = '⚡ Gemini 3.6 Flash (Live)';
        modeIndicator.querySelector('.mode-text').textContent = 'Live mode — Gemini 3.6 Flash & FAISS';
      } else {
        modeBadge.textContent = '🟢 Demo Fallback';
        modeIndicator.querySelector('.mode-text').textContent = 'Demo fallback — add GEMINI_API_KEY to .env';
      }
    }
  } catch (e) {
    modeBadge.textContent = '🟢 Demo Mode';
    modeIndicator.querySelector('.mode-text').textContent = 'Running locally';
  }
}

function attachEventListeners() {
  sendBtn.addEventListener('click', handleSend);
  inputEl.addEventListener('keydown', (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  });
  inputEl.addEventListener('input', () => {
    inputEl.style.height = 'auto';
    inputEl.style.height = Math.min(inputEl.scrollHeight, 100) + 'px';
    sendBtn.disabled = inputEl.value.trim() === '';
  });
  clearBtn.addEventListener('click', clearChat);
}

// ── PDF File Upload Handling ────────────────────────────────────────────────
function setupFileUpload() {
  if (!fileInput || !dropZone) return;

  fileInput.addEventListener('change', (e) => {
    if (e.target.files.length > 0) {
      uploadResumeFile(e.target.files[0]);
    }
  });

  // Drag & drop
  ['dragenter', 'dragover'].forEach(name => {
    dropZone.addEventListener(name, (e) => {
      e.preventDefault();
      dropZone.classList.add('dragover');
    });
  });

  ['dragleave', 'drop'].forEach(name => {
    dropZone.addEventListener(name, (e) => {
      e.preventDefault();
      dropZone.classList.remove('dragover');
    });
  });

  dropZone.addEventListener('drop', (e) => {
    if (e.dataTransfer.files.length > 0) {
      uploadResumeFile(e.dataTransfer.files[0]);
    }
  });
}

async function uploadResumeFile(file) {
  if (!file) return;
  if (!file.name.endsWith('.pdf') && !file.name.endsWith('.txt') && !file.name.endsWith('.md')) {
    showToast('Please upload a .pdf, .txt, or .md file', 'error');
    return;
  }

  if (CONFIG.isDemo) {
    showToast(`Uploaded ${file.name} (Simulated in Demo Mode)`, 'success');
    uploadText.textContent = `Indexed: ${file.name}`;
    askQuestion(`I just uploaded ${file.name}. Can you summarize my background and key strengths?`);
    return;
  }

  const formData = new FormData();
  formData.append('file', file);

  uploadText.textContent = `Uploading & Vectorizing...`;
  showToast(`Uploading ${file.name}...`, 'info');

  try {
    const res = await fetch(`${CONFIG.apiBase}/upload-resume`, {
      method: 'POST',
      body: formData,
    });

    if (!res.ok) {
      const err = await res.json();
      throw new Error(err.detail || 'Upload failed');
    }

    const data = await res.json();
    uploadText.textContent = `Active: ${file.name}`;
    showToast(`Successfully indexed ${file.name} (${data.chunks_indexed} chunks)!`, 'success');

    // Automatically ask AI about the new resume
    askQuestion(`I have uploaded a new resume (${file.name}). Please review it, provide an ATS compatibility overview, and list the key projects.`);
  } catch (err) {
    uploadText.textContent = 'Upload your PDF / Resume';
    showToast(`Upload failed: ${err.message}`, 'error');
  }
}

// ── Job Match Modal Handlers ────────────────────────────────────────────────
function triggerJobMatchModal() {
  if (jdModal) {
    jdModal.style.display = 'flex';
    if (jdTextarea) jdTextarea.focus();
  }
}

function closeJobMatchModal() {
  if (jdModal) jdModal.style.display = 'none';
}

function submitJobMatch() {
  const jd = jdTextarea.value.trim();
  if (!jd) {
    showToast('Please paste a Job Description', 'error');
    return;
  }
  closeJobMatchModal();
  jdTextarea.value = '';
  askQuestion(`Here is a target Job Description. Please compare my resume against it, calculate the match percentage, identify any missing skills, and give custom interview talking points:\n\n${jd}`);
}

// ── Chat Logic ───────────────────────────────────────────────────────────────
async function handleSend() {
  const query = inputEl.value.trim();
  if (!query || isTyping) return;

  hideWelcome();
  addUserMessage(query);
  clearInput();

  isTyping = true;
  sendBtn.disabled = true;

  const typingEl = showTypingIndicator();

  try {
    let answer;
    if (CONFIG.isDemo) {
      await delay(500 + Math.random() * 600);
      answer = getDemoAnswer(query);
    } else {
      answer = await callLiveAPI(query);
    }
    removeElement(typingEl);
    await addAIMessage(answer);
  } catch (err) {
    removeElement(typingEl);
    await addAIMessage(
      `⚠️ **Connection Error**\n\nCould not reach the backend API.\n\n` +
      `Make sure the FastAPI server is running:\n\`\`\`\nuvicorn app.main:app --reload\n\`\`\`\n\n` +
      `Or use **Demo Mode**.`
    );
  }

  isTyping = false;
  sendBtn.disabled = false;
  inputEl.focus();
}

function getDemoAnswer(query) {
  const q = query.toLowerCase();
  for (const item of DEMO_QA) {
    if (item.keywords.some(k => q.includes(k))) return item.answer;
  }
  return `👋 Hi! I'm Fenil's AI Career Copilot.\n\nTry our specialized career tools:\n• 📊 **ATS Audit:** *"Calculate my ATS score"* \n• 💼 **Job Match:** *"Match this job description: [paste JD]"*\n• 🎙️ **Mock Interview:** *"Simulate a technical interview"*\n• ✉️ **Outreach:** *"Write a cold email to a recruiter"*\n• 🚀 **Projects:** *"What AI projects has Fenil built?"*`;
}

async function callLiveAPI(query) {
  const res = await fetch(`${CONFIG.apiBase}/chat`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ query, demo: false }),
  });
  if (!res.ok) throw new Error(`API error ${res.status}`);
  const data = await res.json();
  return data.answer;
}

// ── UI Helpers ───────────────────────────────────────────────────────────────
function hideWelcome() {
  if (welcomeEl) welcomeEl.style.display = 'none';
}

function addUserMessage(text) {
  messageCount++;
  const div = document.createElement('div');
  div.className = 'message user-message';
  div.innerHTML = `
    <div class="msg-avatar user-avatar">F</div>
    <div class="bubble-container">
      <div class="bubble user-bubble">${escapeHtml(text)}</div>
      <div class="msg-meta">${getTime()}</div>
    </div>`;
  messagesEl.appendChild(div);
  scrollBottom();
}

async function addAIMessage(text) {
  messageCount++;
  const bubbleId = `ai-bubble-${messageCount}`;
  const div = document.createElement('div');
  div.className = 'message';
  div.innerHTML = `
    <div class="msg-avatar ai-avatar">🤖</div>
    <div class="bubble-container">
      <div class="bubble ai-bubble" id="${bubbleId}"></div>
      <div style="display:flex; align-items:center; gap:8px;">
        <span class="msg-meta">${getTime()}</span>
        <button class="copy-btn" onclick="copyText(this, \`${escapeJs(text)}\`)">
          📋 Copy
        </button>
      </div>
    </div>`;
  messagesEl.appendChild(div);
  scrollBottom();

  const bubble = document.getElementById(bubbleId);
  await typewrite(bubble, text);
}

async function typewrite(el, text) {
  const formatted = formatMarkdown(text);
  const chars = text.split('');
  let current = '';
  for (const ch of chars) {
    current += ch;
    el.innerHTML = formatMarkdown(current) + '<span class="cursor">▊</span>';
    scrollBottom();
    await delay(CONFIG.typingSpeed + Math.random() * CONFIG.typingVariance);
  }
  el.innerHTML = formatted;
}

function showTypingIndicator() {
  const wrapper = document.createElement('div');
  wrapper.className = 'message';
  wrapper.innerHTML = `
    <div class="msg-avatar ai-avatar">🤖</div>
    <div class="typing-indicator">
      <div class="typing-dot"></div>
      <div class="typing-dot"></div>
      <div class="typing-dot"></div>
    </div>`;
  messagesEl.appendChild(wrapper);
  scrollBottom();
  return wrapper;
}

function formatMarkdown(text) {
  return text
    .replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;')
    .replace(/^### (.*$)/gim, '<h3>$1</h3>')
    .replace(/^## (.*$)/gim, '<h2>$1</h2>')
    .replace(/^# (.*$)/gim, '<h1>$1</h1>')
    .replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>')
    .replace(/\*(.+?)\*/g, '<em>$1</em>')
    .replace(/`([^`]+)`/g, '<code>$1</code>')
    .replace(/^---$/gim, '<hr style="border:0; border-top:1px solid rgba(255,255,255,0.1); margin:10px 0;">')
    .replace(/\n/g, '<br>');
}

function escapeHtml(text) {
  return text.replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;');
}

function escapeJs(text) {
  return text.replace(/\\/g, '\\\\').replace(/`/g, '\\`').replace(/\$/g, '\\$');
}

function copyText(btn, text) {
  navigator.clipboard.writeText(text).then(() => {
    const original = btn.innerHTML;
    btn.innerHTML = '✅ Copied!';
    setTimeout(() => btn.innerHTML = original, 2000);
  });
}

function clearChat() {
  messagesEl.innerHTML = '';
  if (welcomeEl) welcomeEl.style.display = 'flex';
  messageCount = 0;
}

function clearInput() {
  inputEl.value = '';
  inputEl.style.height = 'auto';
  sendBtn.disabled = true;
}

function scrollBottom() {
  messagesEl.scrollTop = messagesEl.scrollHeight;
}

function removeElement(el) {
  el?.parentNode?.removeChild(el);
}

function getTime() {
  return new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
}

function delay(ms) {
  return new Promise(r => setTimeout(r, ms));
}

function askQuestion(text) {
  inputEl.value = text;
  inputEl.dispatchEvent(new Event('input'));
  handleSend();
}

function showToast(msg, type = 'info') {
  const t = document.createElement('div');
  t.className = `toast toast-${type}`;
  t.textContent = msg;
  document.body.appendChild(t);
  setTimeout(() => t.remove(), 3500);
}

// Injected styles
const cursorStyle = document.createElement('style');
cursorStyle.textContent = `.cursor { animation: blink 0.7s steps(1) infinite; } @keyframes blink { 50% { opacity: 0; } }`;
document.head.appendChild(cursorStyle);

// ── Boot ─────────────────────────────────────────────────────────────────────
init();
