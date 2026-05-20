/**
 * background.js — Service Worker
 * Orchestrates tab management and relays messages between popup ↔ content script.
 */

"use strict";

// ─── Listen for messages from the popup ──────────────────────────────────────

chrome.runtime.onMessage.addListener((msg, sender, sendResponse) => {
  if (msg.action === "getActiveTabId") {
    chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
      if (tabs.length === 0) return sendResponse({ tabId: null });
      sendResponse({ tabId: tabs[0].id, url: tabs[0].url });
    });
    return true; // async
  }

  if (msg.action === "relayToContent") {
    // popup → background → content script
    chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
      if (!tabs.length) return sendResponse({ error: "No active tab" });
      chrome.tabs.sendMessage(tabs[0].id, msg.payload, (response) => {
        if (chrome.runtime.lastError) {
          sendResponse({ error: chrome.runtime.lastError.message });
        } else {
          sendResponse(response);
        }
      });
    });
    return true; // async
  }
});

// ─── Track scraping progress via storage changes ─────────────────────────────

chrome.storage.onChanged.addListener((changes, area) => {
  if (area !== "local") return;
  if (changes.eg_scraping) {
    const scraping = changes.eg_scraping.newValue;
    // Could notify badge, etc.
    if (!scraping) {
      chrome.action.setBadgeText({ text: "" });
    } else {
      chrome.action.setBadgeBackgroundColor({ color: "#4f46e5" });
      chrome.action.setBadgeText({ text: "…" });
    }
  }
  if (changes.eg_questions) {
    const count = (changes.eg_questions.newValue || []).length;
    if (count > 0) {
      chrome.action.setBadgeBackgroundColor({ color: "#059669" });
      chrome.action.setBadgeText({ text: String(count) });
    }
  }
});

// ─── On install: set default storage ─────────────────────────────────────────

chrome.runtime.onInstalled.addListener(() => {
  chrome.storage.local.set({
    eg_questions: [],
    eg_scraping: false,
    eg_page: 0,
  });
  console.log("[ExamGoal Scraper] Extension installed.");
});
