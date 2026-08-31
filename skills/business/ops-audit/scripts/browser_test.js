#!/usr/bin/env node
/* Exercise rendered feedback behavior with a minimal browser DOM. */
const fs = require('fs'), vm = require('vm');
const page = fs.readFileSync(process.argv[2], 'utf8');
const source = page.match(/<script>([\s\S]*)<\/script>/)[1];

function element() { return {hidden: false, value: '', textContent: '', className: '', listeners: {}, focus() {}, addEventListener(type, fn) { this.listeners[type] = fn; }}; }
function article(id, version) {
  const textarea = element(), radios = ['accept', 'change', 'reject'].map(value => ({value, checked: false}));
  return {dataset: {cardId: id, version: String(version)}, querySelector(query) {
    if (query === 'textarea') return textarea;
    if (query === 'input:checked') return radios.find(radio => radio.checked) || null;
    const match = query.match(/^input\[value="(.+)"\]$/);
    return match ? radios.find(radio => radio.value === match[1]) : null;
  }, textarea, radios};
}
async function load(storage, clipboard) {
  const articles = [article('meeting-actions', 1), article('report-format', 1)];
  const copy = element(), status = element(), fallback = element(), fallbackLabel = element(), clear = element();
  const ids = {copy, status, fallback, 'fallback-label': fallbackLabel, 'clear-fallback': clear};
  const document = {querySelectorAll(query) { return query === 'article' ? articles : []; }, querySelector() { return null; }, getElementById(id) { return ids[id] || null; }, addEventListener() {}};
  const localStorage = {getItem(key) { return storage[key] || null; }, setItem(key, value) { storage[key] = value; }, removeItem(key) { delete storage[key]; }};
  vm.runInNewContext(source, {document, localStorage, navigator: {clipboard}, Number, JSON, Promise});
  return {articles, copy, status, fallback, fallbackLabel, clear};
}
(async () => {
  const key = 'ops-audit-feedback-example-works-20260830';
  let storage = {[key]: JSON.stringify({roadmapRevision: 0, cards: {'meeting-actions': {version: 1, choice: 'accept', note: 'stale'}}})};
  let ui = await load(storage, undefined);
  if (ui.articles[0].radios.some(radio => radio.checked) || ui.articles[0].textarea.value) throw Error('stale revision restored');
  storage = {[key]: JSON.stringify({roadmapRevision: 1, cards: {'meeting-actions': {version: 0, choice: 'accept', note: 'stale'}}})};
  ui = await load(storage, undefined);
  if (ui.articles[0].radios.some(radio => radio.checked) || ui.articles[0].textarea.value) throw Error('stale card version restored');

  storage = {[key]: JSON.stringify({roadmapRevision: 1, cards: {'meeting-actions': {version: 1, choice: 'accept', note: ''}}})}; ui = await load(storage, undefined); ui.copy.listeners.click();
  if (ui.fallback.hidden || ui.clear.hidden || !storage[key]) throw Error('clipboard-unavailable fallback cleared storage');
  ui.clear.listeners.click(); if (storage[key] || !ui.fallback.hidden || !ui.fallbackLabel.hidden || ui.status.className !== 'success') throw Error('fallback acknowledgement did not clear storage');

  storage = {[key]: JSON.stringify({roadmapRevision: 1, cards: {'meeting-actions': {version: 1, choice: 'accept', note: ''}}})}; ui = await load(storage, {writeText() { return Promise.reject(Error('denied')); }}); ui.copy.listeners.click(); await Promise.resolve(); await Promise.resolve();
  if (ui.fallback.hidden || !storage[key] || ui.status.className !== 'error') throw Error('clipboard failure state is not visible');

  storage = {}; ui = await load(storage, undefined); ui.articles[0].radios[1].checked = true; ui.copy.listeners.click();
  if (ui.status.className !== 'error' || ui.articles[0].textarea.className !== 'error') throw Error('change-without-note error state is not visible');

  storage = {[key]: 'saved'}; ui = await load(storage, {writeText() { return Promise.resolve(); }}); ui.articles[0].radios[0].checked = true; ui.copy.listeners.click(); await Promise.resolve();
  if (storage[key] || ui.status.className !== 'success' || !ui.status.textContent.startsWith('✓')) throw Error('copy-success state is not visible');
  console.log('browser feedback tests passed');
})().catch(error => { console.error(error.message); process.exit(1); });
