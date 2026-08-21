/**
 * AI Career Copilot — Frontend Application Logic
 * Author: Fenil Varde | github.com/vardefenil
 *
 * Features:
 *  - Multi-Session Chat Threads (thread_id management & persistence)
 *  - Full Markdown & HTML Table parsing via Marked.js
 *  - Live Resume PDF Upload & Automatic Vector Indexing
 *  - 5 Specialized AI Tools: ATS Audit, JD Matcher, Mock Interview, Cold Outreach
 *  - 1-Click Copy & Typewriter streaming
 */

// ── Configuration ───────────────────────────────────────────────────────────
const CONFIG = {
  isDemo: window.location.hostname.includes('github.io') ||
          new URLSearchParams(window.location.search).get('demo') === 'true',
  apiBase: window.location.origin,
  typingSpeed: 6,
  typingVariance: 4,
};

if (window.location.protocol === 'file:') {
  CONFIG.apiBase = 'http://localhost:8000';
}

// Configure Marked.js options
if (typeof marked !== 'undefined') {
  marked.setOptions({
    gfm: true,
    breaks: true,
  });
}

// ── Demo Response Data ───────────────────────────────────────────────────────
const DEMO_QA = [
  {
    keywords: ['ats', 'score', 'audit', 'review resume', 'format'],
    answer: `### 📊 Comprehensive ATS Resume Scan & Score

| Metric | Score / Status | Details |
| :--- | :--- | :--- |
| **Overall ATS Score** | **88 / 100** | Grade: Strong Candidate |
| **Contact & Header** | 10 / 10 | Clean links to GitHub, LinkedIn, LeetCode, Email, Phone |
| **Formatting & Structure** | 18 / 20 | Standard ATS headers, clean bullet points |
| **Technical Keywords** | 22 / 25 | Python, scikit-learn, LangChain, FAISS, Flask |
| **Quantified Impact** | 18 / 20 | 60% review reduction, 20+ commands, 10+ fields |

---

### 🔍 Recommended Keywords for AI/ML Roles:
• Add: \`FastAPI\`, \`Vector Databases\`, \`RAG (Retrieval-Augmented Generation)\`, \`Prompt Engineering\`, \`Docker\`, \`CI/CD\`.

### 🚀 Action Verb Enhancement:
• **Before:** *'Built an end-to-end fraud detection system...'*
• **After:** *'Architected & deployed a production ML fraud detection pipeline across 4 classifier models with 94%+ ROC-AUC.'*`,
  },
  {
    keywords: ['job match', 'match', 'jd', 'job description', 'fit', 'qualif'],
    answer: `### 💼 Job Description Match Analysis

| Category | Match % | Key Highlights |
| :--- | :--- | :--- |
| **Overall Alignment** | **85%** | Strong fit for AI/ML & Python Developer Roles |
| **Core Languages** | 95% | Python, C++, HTML, CSS |
| **AI & Frameworks** | 90% | RAG Pipelines, FAISS Vector Search, LangGraph, Gemini |
| **Data & Modeling** | 85% | scikit-learn, Pandas, NumPy, Feature Engineering |

---

### 🟢 Exact Matches:
• **Languages & Tools:** Python, C++, scikit-learn, Pandas, NumPy, Flask, FastAPI, Git, SQL.
• **AI Architectures:** RAG, Vector Search, ReAct Agents, Embedding Pipelines.

### 🟡 Growth Opportunities:
• Add containerization (**Docker**) and cloud deployment (**GCP/AWS**) to your projects.`,
  },
  {
    keywords: ['interview', 'mock', 'prep', 'behavioral', 'questions'],
    answer: `### 🎙️ Tailored Technical & Behavioral Mock Interview

#### 1. Technical Project Deep-Dive (Credit Card Fraud Detection):
* **Question:** *"How did you handle class imbalance in your fraud dataset, and why choose Precision-Recall over Accuracy?"*
* 👉 **Key talking points:** Mention SMOTE, class weights in Random Forest / XGBoost, and why high accuracy is misleading in 99:1 imbalanced data.

#### 2. Architecture & RAG (AI Career Copilot):
* **Question:** *"Explain how chunk size and overlap impact semantic retrieval accuracy in FAISS."*
* 👉 **Key talking points:** Discuss context boundaries (1000 chars / 200 overlap) and preventing LLM hallucinations.

#### 3. Behavioral (STAR Method):
* **Question:** *"Tell me about a challenging bug you encountered while integrating Gemini AI in your voice assistant and how you resolved it."*`,
  },
  {
    keywords: ['cold email', 'email', 'cover letter', 'outreach', 'recruiter'],
    answer: `### ✉️ Recruiter Cold Outreach & Cover Letter

#### 📬 High-Conversion Cold Email:
**Subject:** B.E. Computer Engineering Student | Applied AI & RAG Developer — Fenil Varde

Hi [Hiring Manager Name],

I've been following [Company Name]'s recent work in AI engineering. As a Computer Engineering undergraduate with hands-on experience building end-to-end RAG systems (LangGraph + FAISS + Gemini) and production ML pipelines (Fraud Detection with XGBoost), I would love to contribute to your engineering team.

**Flagship Work:**
• **AI Career Copilot:** Live RAG agent querying complex unstructured documents with sub-second retrieval.
• **Fraud Detection System:** Evaluated 4 ML algorithms on imbalanced data with real-time Flask analytics.

Are you open to a brief 10-minute chat this week?

Best regards,  
**Fenil Varde**  
🔗 LinkedIn: linkedin.com/in/fenil-varde-58145b318/ | 🐙 GitHub: github.com/vardefenil`,
  },
  {
    keywords: ['project', 'built', 'created', 'portfolio', 'app', 'application'],
    answer: `### 🚀 Key Projects on Fenil's Resume:

1. **AI Career Copilot** *(2026 — Flagship)*
   * **Tech:** Python, LangGraph, FAISS, Google Gemini 3.6 Flash, FastAPI.
   * **Highlights:** Full RAG pipeline with live PDF upload & re-indexing, ATS scoring, and interview prep.

2. **Credit Card Fraud Detection System** *(2026)*
   * **Tech:** Python, scikit-learn, Pandas, Flask.
   * **Highlights:** Trained Logistic Regression, Random Forest, SVM & XGBoost on highly imbalanced transaction datasets.

3. **AI-Based Resume Analytics Tool** *(2026)*
   * **Tech:** Python, Flask, NLP, scikit-learn.
   * **Highlights:** Parsed PDF resumes, extracted 10+ structured fields, reduced manual review effort by 60%.

4. **AI-Powered Voice Assistant** *(2024)*
   * **Tech:** Python, Google Gemini AI, NewsAPI.
   * **Highlights:** Voice-controlled desktop assistant with 20+ command types and real-time news.`,
  },
  {
    keywords: ['skill', 'tech', 'technology', 'language', 'tools', 'stack', 'know'],
    answer: `### 🛠️ Technical Skills & Tooling:

* **Programming Languages:** Python, C++, HTML, CSS
* **AI / ML Frameworks:** LangChain, LangGraph, FAISS, Google Gemini, HuggingFace, scikit-learn
* **Data Science Libraries:** NumPy, Pandas, Matplotlib, Seaborn
* **Web & Backend:** FastAPI, Flask, REST APIs, SQL
* **Developer Tools:** Git, GitHub, VS Code, Jupyter Notebook, Docker`,
  },
  {
    keywords: ['education', 'college', 'university', 'degree', 'study', 'school', 'gpa', 'cpi'],
    answer: `### 🎓 Education Background:

* **Bachelor of Engineering in Computer Engineering** (2023 – 2027)
  * **Institute:** LDRP Institute of Technology and Research, Gandhinagar, Gujarat
  * **CPI:** **7.66 / 10.00**
  * **Coursework:** Data Structures & Algorithms, OOP, Database Management Systems, Operating Systems

* **Higher Secondary (Class XII, GSEB Science - 2023):** 56.92%
* **Secondary School (Class X, GSEB - 2021):** 80.83%`,
  },
  {
    keywords: ['contact', 'email', 'phone', 'linkedin', 'github', 'reach', 'hire'],
    answer: `### 📬 Contact & Connect with Fenil:

* 📧 **Email:** [vardefenil6@gmail.com](mailto:vardefenil6@gmail.com)
* 📱 **Phone:** +91 87804 71545
* 💼 **LinkedIn:** [fenil-varde-58145b318](https://linkedin.com/in/fenil-varde-58145b318/)
* 🐙 **GitHub:** [vardefenil](https://github.com/vardefenil)
* ⚡ **LeetCode:** [vardefenil6](https://leetcode.com/u/vardefenil6/)`,
  },
];

// ── State Management (Threads & Sessions) ───────────────────────────────────
let currentThreadId = null;
let sessions = {}; // { threadId: { id, title, messages: [{role, text, time}], updatedAt } }
let isTyping = false;

// ── DOM References ───────────────────────────────────────────────────────────
const messagesEl         = document.getElementById('messages');
const welcomeEl          = document.getElementById('welcome-state');
const inputEl            = document.getElementById('chat-input');
const sendBtn            = document.getElementById('send-btn');
const clearBtn           = document.getElementById('clear-btn');
const modeBadge          = document.getElementById('mode-badge');
const modeIndicator      = document.getElementById('mode-indicator');
const sessionListEl      = document.getElementById('session-list');
const currentThreadTitle = document.getElementById('current-thread-title');
const fileInput          = document.getElementById('pdf-file-input');
const dropZone           = document.getElementById('drop-zone');
const uploadText         = document.getElementById('upload-text');
const jdModal            = document.getElementById('jd-modal');
const jdTextarea         = document.getElementById('jd-textarea');

// ── Initialization ───────────────────────────────────────────────────────────
function init() {
  loadSessionsFromStorage();
  updateModeUI();
  attachEventListeners();
  setupFileUpload();
  inputEl.focus();
}

// ── Session & Thread Management ──────────────────────────────────────────────
function generateThreadId() {
  return 'thread_' + Math.random().toString(36).substring(2, 9) + '_' + Date.now();
}

function loadSessionsFromStorage() {
  try {
    const saved = localStorage.getItem('ai_career_sessions');
    if (saved) {
      sessions = JSON.parse(saved);
    }
  } catch (e) {
    sessions = {};
  }

  const threadIds = Object.keys(sessions);
  if (threadIds.length === 0) {
    createNewSession('New Chat');
  } else {
    // Select the most recent session
    threadIds.sort((a, b) => (sessions[b].updatedAt || 0) - (sessions[a].updatedAt || 0));
    switchSession(threadIds[0]);
  }
}

function saveSessionsToStorage() {
  try {
    localStorage.setItem('ai_career_sessions', JSON.stringify(sessions));
  } catch (e) {}
}

function createNewSession(customTitle) {
  const newId = generateThreadId();
  sessions[newId] = {
    id: newId,
    title: customTitle || 'New Conversation',
    messages: [],
    updatedAt: Date.now(),
  };
  saveSessionsToStorage();
  switchSession(newId);
}

function switchSession(threadId) {
  if (!sessions[threadId]) return;
  currentThreadId = threadId;
  renderSessionList();
  renderCurrentSessionMessages();

  if (currentThreadTitle) {
    currentThreadTitle.textContent = sessions[threadId].title || 'AI Career Copilot';
  }
}

function deleteSession(e, threadId) {
  e.stopPropagation();
  delete sessions[threadId];
  saveSessionsToStorage();

  const remaining = Object.keys(sessions);
  if (remaining.length === 0) {
    createNewSession('New Chat');
  } else if (currentThreadId === threadId) {
    switchSession(remaining[0]);
  } else {
    renderSessionList();
  }
}

function renderSessionList() {
  if (!sessionListEl) return;
  sessionListEl.innerHTML = '';

  const threadIds = Object.keys(sessions);
  threadIds.sort((a, b) => (sessions[b].updatedAt || 0) - (sessions[a].updatedAt || 0));

  threadIds.forEach(id => {
    const sess = sessions[id];
    const item = document.createElement('div');
    item.className = `session-item ${id === currentThreadId ? 'active' : ''}`;
    item.onclick = () => switchSession(id);
    item.innerHTML = `
      <span class="session-title" title="${escapeHtml(sess.title)}">💬 ${escapeHtml(sess.title)}</span>
      <button class="session-del-btn" onclick="deleteSession(event, '${id}')" title="Delete thread">✕</button>
    `;
    sessionListEl.appendChild(item);
  });
}

function renderCurrentSessionMessages() {
  messagesEl.innerHTML = '';
  const current = sessions[currentThreadId];
  if (!current || current.messages.length === 0) {
    if (welcomeEl) {
      welcomeEl.style.display = 'flex';
      messagesEl.appendChild(welcomeEl);
    }
    return;
  }

  if (welcomeEl) welcomeEl.style.display = 'none';

  current.messages.forEach(msg => {
    if (msg.role === 'user') {
      renderUserMessageBubble(msg.text, msg.time);
    } else {
      renderAIMessageBubble(msg.text, msg.time);
    }
  });
  scrollBottom();
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
  clearBtn.addEventListener('click', () => {
    if (sessions[currentThreadId]) {
      sessions[currentThreadId].messages = [];
      saveSessionsToStorage();
      renderCurrentSessionMessages();
    }
  });
}

// ── PDF File Upload Handling ────────────────────────────────────────────────
function setupFileUpload() {
  if (!fileInput || !dropZone) return;

  fileInput.addEventListener('change', (e) => {
    if (e.target.files.length > 0) {
      uploadResumeFile(e.target.files[0]);
    }
  });

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

    // Automatically trigger analysis on the new resume
    createNewSession(`Resume: ${file.name}`);
    askQuestion(`I have uploaded a new resume (${file.name}). Please review it, provide an ATS compatibility score & overview, and list the key projects.`);
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
  createNewSession('Job Match Audit');
  askQuestion(`Here is a target Job Description. Please compare my resume against it, calculate the match percentage, identify any missing skills, and give custom interview talking points:\n\n${jd}`);
}

// ── Chat Logic ───────────────────────────────────────────────────────────────
async function handleSend() {
  const query = inputEl.value.trim();
  if (!query || isTyping) return;

  hideWelcome();

  // Auto-generate session title from first query
  if (sessions[currentThreadId] && sessions[currentThreadId].messages.length === 0) {
    const shortTitle = query.length > 24 ? query.substring(0, 24) + '...' : query;
    sessions[currentThreadId].title = shortTitle;
    if (currentThreadTitle) currentThreadTitle.textContent = shortTitle;
    renderSessionList();
  }

  const timeStr = getTime();
  addUserMessage(query, timeStr);
  clearInput();

  isTyping = true;
  sendBtn.disabled = true;

  const typingEl = showTypingIndicator();

  try {
    let answer;
    if (CONFIG.isDemo) {
      await delay(400 + Math.random() * 500);
      answer = getDemoAnswer(query);
    } else {
      answer = await callLiveAPI(query, currentThreadId);
    }
    removeElement(typingEl);
    await addAIMessage(answer, getTime());
  } catch (err) {
    removeElement(typingEl);
    await addAIMessage(
      `⚠️ **Connection Error**\n\nCould not reach the backend API.\n\n` +
      `Make sure the FastAPI server is running:\n\`\`\`\nuvicorn app.main:app --reload\n\`\`\`\n\n` +
      `Or use **Demo Mode**.`,
      getTime()
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
  return `### 👋 Hi! I'm Fenil's AI Career Copilot.\n\nTry our specialized career tools:\n• 📊 **ATS Audit:** *"Calculate my ATS score"* \n• 💼 **Job Match:** *"Match this job description: [paste JD]"*\n• 🎙️ **Mock Interview:** *"Simulate a technical interview"*\n• ✉️ **Outreach:** *"Write a cold email to a recruiter"*\n• 🚀 **Projects:** *"What AI projects has Fenil built?"*`;
}

async function callLiveAPI(query, threadId) {
  const res = await fetch(`${CONFIG.apiBase}/chat`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ query, thread_id: threadId, demo: false }),
  });
  if (!res.ok) throw new Error(`API error ${res.status}`);
  const data = await res.json();
  return data.answer;
}

// ── UI Message Rendering ─────────────────────────────────────────────────────
function hideWelcome() {
  if (welcomeEl) welcomeEl.style.display = 'none';
}

function addUserMessage(text, timeStr) {
  if (sessions[currentThreadId]) {
    sessions[currentThreadId].messages.push({ role: 'user', text, time: timeStr });
    sessions[currentThreadId].updatedAt = Date.now();
    saveSessionsToStorage();
  }
  renderUserMessageBubble(text, timeStr);
}

function renderUserMessageBubble(text, timeStr) {
  const div = document.createElement('div');
  div.className = 'message user-message';
  div.innerHTML = `
    <div class="msg-avatar user-avatar">F</div>
    <div class="bubble-container">
      <div class="bubble user-bubble">${escapeHtml(text)}</div>
      <div class="msg-meta">${timeStr || getTime()}</div>
    </div>`;
  messagesEl.appendChild(div);
  scrollBottom();
}

async function addAIMessage(text, timeStr) {
  if (sessions[currentThreadId]) {
    sessions[currentThreadId].messages.push({ role: 'ai', text, time: timeStr });
    sessions[currentThreadId].updatedAt = Date.now();
    saveSessionsToStorage();
  }

  const bubbleId = `ai-bubble-${Date.now()}`;
  const div = document.createElement('div');
  div.className = 'message';
  div.innerHTML = `
    <div class="msg-avatar ai-avatar">🤖</div>
    <div class="bubble-container">
      <div class="bubble ai-bubble" id="${bubbleId}"></div>
      <div style="display:flex; align-items:center; gap:8px;">
        <span class="msg-meta">${timeStr || getTime()}</span>
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

function renderAIMessageBubble(text, timeStr) {
  const div = document.createElement('div');
  div.className = 'message';
  div.innerHTML = `
    <div class="msg-avatar ai-avatar">🤖</div>
    <div class="bubble-container">
      <div class="bubble ai-bubble">${renderMarkdown(text)}</div>
      <div style="display:flex; align-items:center; gap:8px;">
        <span class="msg-meta">${timeStr || getTime()}</span>
        <button class="copy-btn" onclick="copyText(this, \`${escapeJs(text)}\`)">
          📋 Copy
        </button>
      </div>
    </div>`;
  messagesEl.appendChild(div);
}

async function typewrite(el, text) {
  const formatted = renderMarkdown(text);
  const chars = text.split('');
  let current = '';
  for (let i = 0; i < chars.length; i += 2) {
    current += chars.slice(i, i + 2).join('');
    el.innerHTML = renderMarkdown(current) + '<span class="cursor">▊</span>';
    scrollBottom();
    await delay(CONFIG.typingSpeed);
  }
  el.innerHTML = formatted;
}

function renderMarkdown(text) {
  if (typeof marked !== 'undefined') {
    try {
      return marked.parse(text);
    } catch (e) {}
  }
  // Fallback if marked fails
  return text
    .replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;')
    .replace(/^### (.*$)/gim, '<h3>$1</h3>')
    .replace(/^## (.*$)/gim, '<h2>$1</h2>')
    .replace(/^# (.*$)/gim, '<h1>$1</h1>')
    .replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>')
    .replace(/\n/g, '<br>');
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
