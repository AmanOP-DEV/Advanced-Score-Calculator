/**
 * utils.js — ExamGoal Scraper Utilities
 * Shared between content.js (injected) and popup.js (extension context).
 */

"use strict";

// ─── Simple djb2-style string hash ───────────────────────────────────────────
function hashString(str) {
  let hash = 5381;
  for (let i = 0; i < str.length; i++) {
    hash = (hash * 33) ^ str.charCodeAt(i);
  }
  return (hash >>> 0).toString(36); // unsigned 32-bit, base-36
}

/**
 * Deduplicate an array of question objects by their questionText hash.
 * @param {object[]} questions
 * @returns {object[]}
 */
function deduplicateQuestions(questions) {
  const seen = new Set();
  return questions.filter((q) => {
    const key = hashString((q.questionText || "").trim().toLowerCase());
    if (seen.has(key)) return false;
    seen.add(key);
    return true;
  });
}

/**
 * Merge two arrays of questions, keeping uniques from both.
 * @param {object[]} existing
 * @param {object[]} incoming
 * @returns {object[]}
 */
function mergeQuestions(existing, incoming) {
  return deduplicateQuestions([...existing, ...incoming]);
}

/**
 * Trigger a JSON file download in the browser.
 * Works only in extension popup / page context (not content script).
 * @param {object[]} questions
 * @param {string} filename
 */
function exportToJSON(questions, filename = "examgoal_questions.json") {
  const payload = {
    exportedAt: new Date().toISOString(),
    totalQuestions: questions.length,
    questions,
  };
  const blob = new Blob([JSON.stringify(payload, null, 2)], {
    type: "application/json",
  });
  const url = URL.createObjectURL(blob);
  const a = document.createElement("a");
  a.href = url;
  a.download = filename;
  a.click();
  setTimeout(() => URL.revokeObjectURL(url), 5000);
}

/**
 * Sleep helper.
 * @param {number} ms
 */
function sleep(ms) {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

// Export for ES-module-like usage when bundling is not used.
// In content scripts loaded via manifest, these become globals.
if (typeof module !== "undefined") {
  module.exports = { hashString, deduplicateQuestions, mergeQuestions, exportToJSON, sleep };
}
