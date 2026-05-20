/**
 * popup.js — ExamGoal Scraper Popup Controller
 */

"use strict";

// ─── DOM refs ─────────────────────────────────────────────────────────────────

const statusDot    = document.getElementById("statusDot");
const statusMsg    = document.getElementById("statusMsg");
const statTotal    = document.getElementById("statTotal");
const statPage     = document.getElementById("statPage");
const statSession  = document.getElementById("statSession");
const btnScrapePage = document.getElementById("btnScrapePage");
const btnScrapeAll  = document.getElementById("btnScrapeAll");
const btnExport     = document.getElementById("btnExport");
const btnClear      = document.getElementById("btnClear");
const progressWrap  = document.getElementById("progressWrap");
const pgNum         = document.getElementById("pgNum");
const previewList   = document.getElementById("previewList");
const previewHint   = document.getElementById("previewHint");

// ─── State ────────────────────────────────────────────────────────────────────

let sessionCount = 0;

// ─── Helpers ──────────────────────────────────────────────────────────────────

function setStatus(msg, state = "idle") {
  statusMsg.textContent = msg;
  statusDot.className = `status-dot ${state}`;
}

function updateStats(questions, page = null) {
  statTotal.textContent  = questions.length;
  statSession.textContent = sessionCount;
  statPage.textContent   = page !== null ? page : "—";
  btnExport.disabled     = questions.length === 0;
}

function renderPreview(questions) {
  previewList.innerHTML = "";
  const recent = questions.slice(-8).reverse();
  if (recent.length === 0) {
    previewHint.textContent = "No questions yet";
    return;
  }
  previewHint.textContent = `Latest ${recent.length}`;
  recent.forEach((q) => {
    const li = document.createElement("li");
    li.className = "preview-item";
    li.innerHTML = `
      <span class="preview-idx">#${q.index}</span>
      <span class="preview-text">${escapeHtml(q.questionText)}</span>
    `;
    previewList.appendChild(li);
  });
}

function escapeHtml(str) {
  return String(str || "")
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;");
}

function showToast(msg, duration = 2200) {
  let toast = document.querySelector(".toast");
  if (!toast) {
    toast = document.createElement("div");
    toast.className = "toast";
    document.body.appendChild(toast);
  }
  toast.textContent = msg;
  toast.classList.add("show");
  setTimeout(() => toast.classList.remove("show"), duration);
}

function setLoading(on) {
  btnScrapePage.disabled = on;
  btnScrapeAll.disabled  = on;
  progressWrap.hidden    = !on;
}

// ─── Send message to content script via background relay ─────────────────────

async function sendToContent(payload) {
  return new Promise((resolve) => {
    chrome.runtime.sendMessage(
      { action: "relayToContent", payload },
      (response) => {
        if (chrome.runtime.lastError) {
          resolve({ error: chrome.runtime.lastError.message });
        } else {
          resolve(response || {});
        }
      }
    );
  });
}

// ─── Check if active tab is on examgoal.com ───────────────────────────────────

async function getActiveTab() {
  return new Promise((res) => {
    chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
      res(tabs[0] || null);
    });
  });
}

async function assertExamGoalTab() {
  const tab = await getActiveTab();
  if (!tab || !tab.url || !tab.url.includes("examgoal.com")) {
    setStatus("⚠️ Navigate to an ExamGoal page first.", "error");
    showToast("Not on ExamGoal — please navigate there first.");
    return false;
  }
  return true;
}

// ─── Scrape current page ──────────────────────────────────────────────────────

btnScrapePage.addEventListener("click", async () => {
  if (!(await assertExamGoalTab())) return;

  setLoading(true);
  setStatus("Scraping current page…", "running");

  const result = await sendToContent({ action: "scrapeCurrentPage" });

  if (result.error) {
    setStatus(`Error: ${result.error}`, "error");
    showToast("Content script not ready — reload the page.");
    setLoading(false);
    return;
  }

  const incoming = result.questions || [];
  if (incoming.length === 0) {
    setStatus("No questions found on this page.", "idle");
    showToast("No questions detected — try adjusting selectors.");
    setLoading(false);
    return;
  }

  // Merge with stored
  const stored = await getStoredQuestions();
  const merged = mergeQuestions(stored, incoming);
  await chrome.storage.local.set({ eg_questions: merged });

  sessionCount += incoming.length;
  setStatus(`Found ${incoming.length} questions on this page.`, "done");
  showToast(`✓ ${incoming.length} questions scraped`);
  updateStats(merged);
  renderPreview(merged);
  setLoading(false);
});

// ─── Scrape all pages ─────────────────────────────────────────────────────────

btnScrapeAll.addEventListener("click", async () => {
  if (!(await assertExamGoalTab())) return;

  setLoading(true);
  setStatus("Starting multi-page scrape…", "running");
  pgNum.textContent = "1";

  const result = await sendToContent({ action: "scrapeAllPages" });
  if (result.error) {
    setStatus(`Error: ${result.error}`, "error");
    showToast("Content script not ready — reload the page.");
    setLoading(false);
    return;
  }

  // Poll storage for updates
  pollScraping();
});

function pollScraping() {
  const interval = setInterval(async () => {
    const data = await chrome.storage.local.get(["eg_questions", "eg_scraping", "eg_page"]);
    const questions = data.eg_questions || [];
    const scraping  = data.eg_scraping;
    const page      = data.eg_page || 1;

    pgNum.textContent = page;
    updateStats(questions, page);
    renderPreview(questions);

    if (!scraping) {
      clearInterval(interval);
      setLoading(false);
      setStatus(`✓ Done — ${questions.length} total questions collected.`, "done");
      showToast(`Finished! ${questions.length} questions total.`);
      sessionCount = questions.length;
      statSession.textContent = sessionCount;
    } else {
      setStatus(`Scraping page ${page}… (${questions.length} so far)`, "running");
    }
  }, 800);
}

// ─── Export ───────────────────────────────────────────────────────────────────

btnExport.addEventListener("click", async () => {
  const questions = await getStoredQuestions();
  if (questions.length === 0) {
    showToast("Nothing to export yet.");
    return;
  }
  // Derive a filename from the page URL
  const tab = await getActiveTab();
  const slug = (tab?.url || "")
    .replace(/https?:\/\/[^/]+/, "")
    .replace(/[^a-z0-9]+/gi, "_")
    .replace(/^_|_$/g, "")
    .slice(0, 60);
  const filename = `examgoal_${slug || "questions"}_${Date.now()}.json`;

  exportToJSON(questions, filename);
  showToast(`Exported ${questions.length} questions as JSON`);
});

// ─── Clear ────────────────────────────────────────────────────────────────────

btnClear.addEventListener("click", async () => {
  await chrome.storage.local.set({ eg_questions: [], eg_scraping: false, eg_page: 0 });
  sessionCount = 0;
  updateStats([]);
  renderPreview([]);
  setStatus("Cleared — ready for a fresh scrape.", "idle");
  showToast("Cleared.");
});

// ─── Storage helper ───────────────────────────────────────────────────────────

async function getStoredQuestions() {
  return new Promise((resolve) => {
    chrome.storage.local.get("eg_questions", (data) => {
      resolve(data.eg_questions || []);
    });
  });
}

// ─── Init: load state on popup open ──────────────────────────────────────────

(async function init() {
  const data = await chrome.storage.local.get(["eg_questions", "eg_scraping", "eg_page"]);
  const questions = data.eg_questions || [];
  const scraping  = data.eg_scraping || false;
  const page      = data.eg_page || 0;

  updateStats(questions, page > 0 ? page : null);
  renderPreview(questions);

  if (scraping) {
    setStatus("Scraping in progress…", "running");
    setLoading(true);
    pollScraping();
  } else {
    const tab = await getActiveTab();
    if (!tab?.url?.includes("examgoal.com")) {
      setStatus("Navigate to ExamGoal to begin.", "idle");
    } else if (questions.length > 0) {
      setStatus(`${questions.length} questions in storage — ready to export.`, "done");
    } else {
      setStatus("Ready — click Scrape Current Page.", "idle");
    }
  }
})();
