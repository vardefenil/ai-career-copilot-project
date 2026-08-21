/**
 * AI Career Copilot — Frontend Application Logic
 * Author: Fenil Varde | github.com/vardefenil
 *
 * Features:
 *  - Demo mode (no backend needed) for GitHub Pages
 *  - Live mode (calls FastAPI backend) when running locally
 *  - Typewriter animation for AI responses
 *  - Responsive chat UI
 */

// ── Configuration ───────────────────────────────────────────────────────────
const CONFIG = {
  // Detect demo mode: GitHub Pages URL or ?demo=true param
  isDemo: window.location.hostname.includes('github.io') ||
          new URLSearchParams(window.location.search).get('demo') === 'true',
  apiBase: 'http://localhost:8000',
  typingSpeed: 12,       // ms per character for typewriter
  typingVariance: 8,     // random variance in ms
};

// ── Demo Response Data ───────────────────────────────────────────────────────
const DEMO_QA = [
  {
    keywords: ['project', 'built', 'created', 'portfolio', 'app', 'application'],
    answer: `🚀 Here are Fenil's key projects:

**1. AI Career Copilot** (2026 — This Project!)
→ RAG-based AI agent that answers questions about a resume locally using FAISS + LangGraph + Ollama (Llama 3.1 8B). No API key needed. Zero data leaves your machine.

**2. Credit Card Fraud Detection System** (2026)
→ End-to-end fraud detection using Logistic Regression, Random Forest, SVM & XGBoost on highly imbalanced datasets. Built a Flask dashboard for real-time transaction analysis.

**3. AI-Based Resume Analytics Tool** (2026)
→ Parses PDF resumes, extracts 10+ structured fields (skills, education, experience) using Python, Flask & NLP. Reduced manual review effort by ~60%.

**4. AI-Powered Voice Assistant** (2024)
→ Voice-controlled desktop assistant with 20+ command types. Integrates Google Gemini AI, NewsAPI, music playback & website navigation.`,
  },
  {
    keywords: ['skill', 'tech', 'technology', 'language', 'tools', 'stack', 'know', 'expertise', 'use'],
    answer: `🛠️ Fenil's Technical Skills:

**Languages:** Python · C++ · HTML · CSS

**AI / ML / RAG:**
LangChain · LangGraph · FAISS · HuggingFace Transformers · RAG Pipelines · ReAct Agents · Ollama

**ML Libraries:**
scikit-learn · NumPy · Pandas · Matplotlib · Seaborn

**Web & Backend:**
FastAPI · Flask · REST APIs

**Tools & Platforms:**
Git · GitHub · VS Code · Jupyter Notebook · Ollama

**Concepts:**
Feature Engineering · Model Evaluation · Cross Validation · Imbalanced Data Handling · Vector Embeddings · Semantic Search`,
  },
  {
    keywords: ['education', 'college', 'university', 'degree', 'study', 'school', 'gpa', 'cpi', 'grade', 'academic', 'student'],
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
    keywords: ['experience', 'work', 'job', 'internship', 'company', 'role', 'position'],
    answer: `💼 Experience & Background:

Currently a **3rd-year Computer Engineering student** at LDRP Institute of Technology and Research (2023–2027).

While formal industry experience is still ahead, Fenil has built multiple end-to-end AI/ML projects independently, demonstrating strong practical skills in:
• RAG systems & LLM orchestration (this project!)
• Fraud detection with imbalanced ML datasets
• AI-powered voice assistants using Google Gemini
• Resume parsing NLP pipelines

**Actively seeking internship opportunities** in AI/ML, Python development, and full-stack roles.`,
  },
  {
    keywords: ['certif', 'achievement', 'award', 'medal', 'judo', 'jee', 'nptel', 'leetcode'],
    answer: `🏅 Certifications & Achievements:

**Certifications:**
• NPTEL — Programming in Python (IIT Madras) — Elite Badge (2024)

**Competitive Exams:**
• JEE Main 2023 — 87.38 Percentile overall
• 85.42 Percentile in Mathematics among 1M+ candidates

**Sports:**
• 🥈 Silver Medalist — District Level Judo Competition

**DSA Practice:**
• Actively solving Data Structures & Algorithms on LeetCode & Codeforces`,
  },
  {
    keywords: ['contact', 'email', 'phone', 'linkedin', 'github', 'reach', 'hire', 'connect', 'social'],
    answer: `📬 Get in touch with Fenil:

📧 **Email:** vardefenil6@gmail.com
📱 **Phone:** +91 87804 71545
💼 **LinkedIn:** linkedin.com/in/fenil-varde-58145b318/
🐙 **GitHub:** github.com/vardefenil
⚡ **LeetCode:** leetcode.com/u/vardefenil6/

Feel free to reach out for collaborations, internship opportunities, or just to connect! 🤝`,
  },
  {
    keywords: ['rag', 'how', 'work', 'architecture', 'faiss', 'ollama', 'langchain', 'langgraph'],
    answer: `🧠 How the AI Career Copilot Works:

This project uses **RAG (Retrieval-Augmented Generation)** — a cutting-edge AI technique:

**Step 1 — Ingestion:**
Resume (PDF/Markdown) → split into chunks → converted to vector embeddings using HuggingFace (all-MiniLM-L6-v2) → stored in a FAISS vector database

**Step 2 — Retrieval:**
Your query → converted to a vector → FAISS finds the 5 most semantically similar resume chunks

**Step 3 — Generation:**
Retrieved chunks + your query → fed to Llama 3.1 8B (running locally via Ollama) → natural language answer

**100% Private:** No data ever leaves your machine. No API keys. No cloud calls.

**Tech:** Python · LangChain · LangGraph · FAISS · HuggingFace · Ollama · FastAPI`,
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

// ── Initialization ───────────────────────────────────────────────────────────
function init() {
  updateModeUI();
  attachEventListeners();
  inputEl.focus();
}

function updateModeUI() {
  if (CONFIG.isDemo) {
    modeBadge.textContent = '🟢 Demo Mode';
    modeBadge.classList.add('demo-active');
    modeIndicator.querySelector('.mode-text').textContent =
      'Demo mode — pre-built answers, no server needed';
  } else {
    modeBadge.textContent = '⚡ Live Mode';
    modeIndicator.querySelector('.mode-text').textContent =
      'Live mode — powered by Ollama Llama 3.1';
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
    inputEl.style.height = Math.min(inputEl.scrollHeight, 120) + 'px';
    sendBtn.disabled = inputEl.value.trim() === '';
  });
  clearBtn.addEventListener('click', clearChat);
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
      await delay(600 + Math.random() * 800); // realistic delay
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
      `Or use **Demo Mode** (add ?demo=true to the URL).`
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
  return `👋 Hi! I'm Fenil's AI Career Copilot.\n\nI can answer questions about:\n🚀 **Projects** — What I've built\n🛠️ **Skills** — Technologies I know\n🎓 **Education** — My academic background\n🏅 **Achievements** — Certifications & awards\n🧠 **How it works** — RAG, FAISS, Ollama architecture\n📬 **Contact** — How to reach Fenil\n\nTry: *"What projects have you built?"* or *"What are your skills?"*`;
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
    <div>
      <div class="bubble user-bubble">${escapeHtml(text)}</div>
      <div class="msg-meta">${getTime()}</div>
    </div>`;
  messagesEl.appendChild(div);
  scrollBottom();
}

async function addAIMessage(text) {
  const div = document.createElement('div');
  div.className = 'message';
  div.innerHTML = `
    <div class="msg-avatar ai-avatar">🤖</div>
    <div>
      <div class="bubble ai-bubble" id="ai-bubble-${messageCount}"></div>
      <div class="msg-meta">${getTime()}</div>
    </div>`;
  messagesEl.appendChild(div);
  scrollBottom();

  const bubble = div.querySelector('.bubble');
  await typewrite(bubble, text);
}

async function typewrite(el, text) {
  const formatted = formatMarkdown(text);
  // For typewriter, work character-by-character on plain text, then render markdown at end
  const chars = text.split('');
  let current = '';
  for (const ch of chars) {
    current += ch;
    el.innerHTML = formatMarkdown(current) + '<span class="cursor">▊</span>';
    scrollBottom();
    await delay(CONFIG.typingSpeed + Math.random() * CONFIG.typingVariance);
  }
  el.innerHTML = formatted; // Final render without cursor
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
    .replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;')  // escape first
    .replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>')    // **bold**
    .replace(/\*(.+?)\*/g, '<em>$1</em>')                 // *italic*
    .replace(/`([^`]+)`/g, '<code>$1</code>')             // `code`
    .replace(/•\s/g, '• ')                                // bullet points
    .replace(/\n/g, '<br>');                              // newlines
}

function escapeHtml(text) {
  return text.replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;');
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

// ── Quick Question Handler (called from HTML) ────────────────────────────────
function askQuestion(text) {
  inputEl.value = text;
  inputEl.dispatchEvent(new Event('input'));
  handleSend();
}

// ── Toast Notification ───────────────────────────────────────────────────────
function showToast(msg, type = 'info') {
  const t = document.createElement('div');
  t.className = `toast toast-${type}`;
  t.textContent = msg;
  document.body.appendChild(t);
  setTimeout(() => t.remove(), 3000);
}

// ── Cursor blink style (injected) ────────────────────────────────────────────
const cursorStyle = document.createElement('style');
cursorStyle.textContent = `.cursor { animation: blink 0.7s steps(1) infinite; } @keyframes blink { 50% { opacity: 0; } }`;
document.head.appendChild(cursorStyle);

// ── Boot ─────────────────────────────────────────────────────────────────────
init();
