/**
 * content.js — ExamGoal Question Scraper
 * Injected on https://*.examgoal.com/*
 *
 * ┌─────────────────────────────────────────────────────────────┐
 * │  CONFIGURABLE SELECTORS — adjust here if the site updates   │
 * └─────────────────────────────────────────────────────────────┘
 */

"use strict";

const SELECTORS = {
  // Outer wrapper for a single question card
  questionContainer: [
    ".question-container",
    ".question-card",
    ".question-box",
    ".q-container",
    "[class*='question']",    // broad fallback
    ".practice-question",
  ],

  // Question text / stem
  questionText: [
    ".question-text",
    ".question-stem",
    ".q-text",
    "[class*='question-text']",
    "p.question",
    ".question-content p",
  ],

  // Option list items
  optionsList: [
    ".options-list li",
    ".option-list li",
    ".answer-options li",
    ".choices li",
    "[class*='option'] li",
    "ul.options > li",
  ],

  // A single option label/letter
  optionLabel: [
    ".option-label",
    ".choice-label",
    "span.label",
    "strong",
  ],

  // A single option text body
  optionText: [
    ".option-text",
    ".choice-text",
    "span.text",
    "p",
  ],

  // Correct-answer indicator (highlighted / checked option)
  correctOption: [
    ".correct-answer",
    ".correct",
    "[class*='correct']",
    ".right-answer",
    "li.active",
  ],

  // Explanation / rationale block
  explanation: [
    ".explanation",
    ".rationale",
    ".solution",
    ".answer-explanation",
    "[class*='explanation']",
    "[class*='rationale']",
    ".answer-description",
  ],

  // "Next" pagination button
  nextButton: [
    "a.next",
    "button.next",
    "[aria-label='Next']",
    ".pagination .next",
    "a[rel='next']",
    ".next-question",
    "button[class*='next']",
    "a[class*='next']",
  ],

  // Container that holds all question cards on a "list" page
  questionsWrapper: [
    ".questions-list",
    ".practice-list",
    ".all-questions",
    "main",
    "#main-content",
  ],
};

// Delay between automated page-turns (ms) — be polite to the server
const PAGE_TURN_DELAY_MS = 2000;

// ─── Selector helpers ─────────────────────────────────────────────────────────

function queryFirst(parent, selectorList) {
  for (const sel of selectorList) {
    try {
      const el = parent.querySelector(sel);
      if (el) return el;
    } catch (_) { /* invalid selector — skip */ }
  }
  return null;
}

function queryAll(parent, selectorList) {
  for (const sel of selectorList) {
    try {
      const els = parent.querySelectorAll(sel);
      if (els && els.length > 0) return Array.from(els);
    } catch (_) { /* skip */ }
  }
  return [];
}

// ─── Core: extract one question block ────────────────────────────────────────

function extractQuestion(container, index) {
  // ── Question text ──
  const qtEl = queryFirst(container, SELECTORS.questionText);
  let questionText = qtEl ? qtEl.innerText.trim() : container.innerText.trim().slice(0, 500);

  // ── Options ──
  const optionEls = queryAll(container, SELECTORS.optionsList);
  const options = optionEls.map((li, i) => {
    const labelEl = queryFirst(li, SELECTORS.optionLabel);
    const textEl  = queryFirst(li, SELECTORS.optionText);

    let label = labelEl ? labelEl.innerText.trim() : String.fromCharCode(65 + i); // A, B, C…
    let text  = textEl  ? textEl.innerText.trim()  : li.innerText.trim();

    // Strip the label from the text if it accidentally got included
    if (text.startsWith(label)) text = text.slice(label.length).trim();

    const isCorrect = li.matches(SELECTORS.correctOption.join(",")) ||
                      li.querySelector(SELECTORS.correctOption.join(",")) !== null ||
                      li.classList.toString().match(/correct|right|active/) !== null;

    return { label, text, isCorrect };
  });

  // ── Correct answer ──
  let correctAnswer = null;
  const correctOpts = options.filter((o) => o.isCorrect);
  if (correctOpts.length > 0) {
    correctAnswer = correctOpts.map((o) => o.label).join(", ");
  } else {
    // Try a dedicated correct-answer element outside the list
    const caEl = queryFirst(container, SELECTORS.correctOption);
    if (caEl) correctAnswer = caEl.innerText.trim();
  }

  // ── Explanation ──
  const expEl = queryFirst(container, SELECTORS.explanation);
  const explanation = expEl ? expEl.innerText.trim() : null;

  // ── Question index / ID ──
  const id = container.dataset.questionId ||
             container.dataset.id ||
             container.id ||
             String(index + 1);

  return {
    id,
    index: index + 1,
    questionText,
    options: options.map(({ label, text }) => ({ label, text })),
    correctAnswer,
    explanation,
    sourceUrl: window.location.href,
    scrapedAt: new Date().toISOString(),
  };
}

// ─── Scrape all question containers on the current DOM ───────────────────────

function scrapeCurrentPage() {
  const containers = queryAll(document, SELECTORS.questionContainer);
  if (containers.length === 0) {
    // Heuristic fallback: find elements with option lists inside
    const allLists = Array.from(document.querySelectorAll("ul, ol")).filter(
      (ul) => ul.querySelectorAll("li").length >= 2 &&
               ul.querySelectorAll("li").length <= 8
    );
    if (allLists.length > 0) {
      return allLists.map((ul, i) => extractQuestion(ul.closest("div") || ul, i));
    }
    return [];
  }
  return containers.map((c, i) => extractQuestion(c, i));
}

// ─── Network interception — capture XHR/Fetch JSON responses ─────────────────
// We patch fetch & XHR early so API-driven pages are also covered.

const _interceptedQuestions = [];

(function patchNetwork() {
  // ── Patch fetch ──
  const origFetch = window.fetch;
  window.fetch = async function (...args) {
    const response = await origFetch.apply(this, args);
    const url = typeof args[0] === "string" ? args[0] : args[0]?.url || "";
    if (url.includes("question") || url.includes("exam") || url.includes("quiz")) {
      try {
        const clone = response.clone();
        clone.json().then((data) => {
          const parsed = tryParseAPIResponse(data, url);
          if (parsed.length) _interceptedQuestions.push(...parsed);
        }).catch(() => {});
      } catch (_) {}
    }
    return response;
  };

  // ── Patch XHR ──
  const origOpen = XMLHttpRequest.prototype.open;
  const origSend = XMLHttpRequest.prototype.send;

  XMLHttpRequest.prototype.open = function (method, url) {
    this._egUrl = url;
    return origOpen.apply(this, arguments);
  };

  XMLHttpRequest.prototype.send = function () {
    this.addEventListener("load", function () {
      const url = this._egUrl || "";
      if (url.includes("question") || url.includes("exam") || url.includes("quiz")) {
        try {
          const data = JSON.parse(this.responseText);
          const parsed = tryParseAPIResponse(data, url);
          if (parsed.length) _interceptedQuestions.push(...parsed);
        } catch (_) {}
      }
    });
    return origSend.apply(this, arguments);
  };
})();

/**
 * Attempt to normalise an arbitrary API payload into our question schema.
 * ExamGoal APIs often return { data: [ {question, options, answer, explanation} ] }
 * or flat arrays. Extend this as you reverse-engineer their endpoints.
 */
function tryParseAPIResponse(data, url) {
  const questions = [];

  const records = Array.isArray(data)
    ? data
    : data?.data || data?.questions || data?.items || data?.results || [];

  if (!Array.isArray(records)) return questions;

  records.forEach((rec, i) => {
    if (!rec || typeof rec !== "object") return;

    const questionText =
      rec.question || rec.question_text || rec.title || rec.stem || "";
    if (!questionText) return;

    const rawOptions = rec.options || rec.choices || rec.answers || [];
    const options = rawOptions.map((opt, idx) => {
      if (typeof opt === "string") {
        return { label: String.fromCharCode(65 + idx), text: opt };
      }
      return {
        label: opt.label || opt.key || String.fromCharCode(65 + idx),
        text: opt.text || opt.value || opt.option || String(opt),
      };
    });

    const correctAnswer =
      rec.correct_answer || rec.answer || rec.correctAnswer || rec.correct || null;

    const explanation =
      rec.explanation || rec.rationale || rec.solution || rec.detail || null;

    questions.push({
      id: String(rec.id || rec.question_id || i + 1),
      index: i + 1,
      questionText: String(questionText).trim(),
      options,
      correctAnswer: correctAnswer !== null ? String(correctAnswer).trim() : null,
      explanation: explanation ? String(explanation).trim() : null,
      sourceUrl: url,
      scrapedAt: new Date().toISOString(),
    });
  });

  return questions;
}

// ─── Pagination helper ────────────────────────────────────────────────────────

function getNextButton() {
  for (const sel of SELECTORS.nextButton) {
    try {
      const btn = document.querySelector(sel);
      if (btn && !btn.disabled && btn.offsetParent !== null) return btn;
    } catch (_) {}
  }
  return null;
}

function hasNextPage() {
  return getNextButton() !== null;
}

// ─── Message listener (from popup / background) ───────────────────────────────

chrome.runtime.onMessage.addListener((msg, _sender, sendResponse) => {
  if (msg.action === "ping") {
    sendResponse({ ok: true });
    return;
  }

  if (msg.action === "scrapeCurrentPage") {
    const domQuestions = scrapeCurrentPage();
    const allQuestions = deduplicateQuestions([
      ...domQuestions,
      ..._interceptedQuestions,
    ]);
    sendResponse({ questions: allQuestions, hasNext: hasNextPage() });
    return;
  }

  if (msg.action === "scrapeAllPages") {
    // Kick off async pagination — returns immediately, progress via storage
    scrapeAllPagesAsync();
    sendResponse({ started: true });
    return;
  }

  if (msg.action === "clickNext") {
    const btn = getNextButton();
    if (btn) {
      btn.click();
      sendResponse({ clicked: true });
    } else {
      sendResponse({ clicked: false });
    }
    return;
  }

  if (msg.action === "getIntercepted") {
    sendResponse({ questions: _interceptedQuestions });
    return;
  }
});

// ─── Scrape-all-pages orchestration (runs in content script context) ──────────

async function scrapeAllPagesAsync() {
  let aggregated = [];
  let pageNum = 1;

  async function doPage() {
    await sleep(pageNum === 1 ? 0 : PAGE_TURN_DELAY_MS);

    const domQuestions = scrapeCurrentPage();
    const combined = deduplicateQuestions([
      ...domQuestions,
      ..._interceptedQuestions,
    ]);
    aggregated = mergeQuestions(aggregated, combined);

    // Persist progress
    await chrome.storage.local.set({
      eg_questions: aggregated,
      eg_scraping: true,
      eg_page: pageNum,
    });

    const nextBtn = getNextButton();
    if (nextBtn) {
      pageNum++;
      nextBtn.click();
      // Wait for DOM to update then recurse
      setTimeout(doPage, PAGE_TURN_DELAY_MS);
    } else {
      await chrome.storage.local.set({ eg_scraping: false });
    }
  }

  await doPage();
}
