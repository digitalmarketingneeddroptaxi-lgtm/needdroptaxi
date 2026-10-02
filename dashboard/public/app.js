/**
 * Need Drop Taxi — Ahrefs Dashboard Application Logic
 * Pure Vanilla JavaScript: No sensitive keys stored on client-side.
 */

// State
let dashboardState = {
  hasKey: false,
  target: 'needdroptaxi.com',
  overview: null,
  keywords: [],
  backlinks: [],
  refdomains: [],
  brokenBacklinks: [],
  topPages: [],
  competitors: [],
  siteAuditProjects: [],
  currentAuditIssues: [],
  activeBacklinkTab: 'all',
  keywordFilter: 'all',
  rankingChartInstance: null
};

// DOM ready
document.addEventListener('DOMContentLoaded', () => {
  setupNavigation();
  setupApiSettingsModal();
  setupEventListeners();
  checkApiStatus();
});

// Setup Tab Navigation
function setupNavigation() {
  const tabs = document.querySelectorAll('.tab-btn');
  tabs.forEach(tab => {
    tab.addEventListener('click', () => {
      const targetTab = tab.getAttribute('data-tab');
      switchTab(targetTab);
    });
  });

  // Backlink sub-tabs
  document.querySelectorAll('.bl-subtab-btn').forEach(btn => {
    btn.addEventListener('click', () => {
      document.querySelectorAll('.bl-subtab-btn').forEach(b => {
        b.classList.remove('bg-blue-50', 'text-blue-700', 'font-semibold');
        b.classList.add('text-slate-600', 'font-medium');
      });
      btn.classList.add('bg-blue-50', 'text-blue-700', 'font-semibold');
      btn.classList.remove('text-slate-600', 'font-medium');
      dashboardState.activeBacklinkTab = btn.getAttribute('data-backlink-tab');
      renderBacklinksTable();
    });
  });

  // Keyword position filters
  document.querySelectorAll('.kw-tier-btn').forEach(btn => {
    btn.addEventListener('click', () => {
      document.querySelectorAll('.kw-tier-btn').forEach(b => {
        b.classList.remove('bg-blue-600', 'text-white', 'font-semibold');
        b.classList.add('bg-slate-100', 'text-slate-700', 'font-medium');
      });
      btn.classList.add('bg-blue-600', 'text-white', 'font-semibold');
      btn.classList.remove('bg-slate-100', 'text-slate-700', 'font-medium');
      dashboardState.keywordFilter = btn.getAttribute('data-filter');
      renderKeywordsTable();
    });
  });

  // Keyword search inputs
  const kwSearch = document.getElementById('keywordSearchInput');
  const kwUrlSearch = document.getElementById('keywordUrlSearchInput');
  if (kwSearch) kwSearch.addEventListener('input', renderKeywordsTable);
  if (kwUrlSearch) kwUrlSearch.addEventListener('input', renderKeywordsTable);
}

function switchTab(tabId) {
  // Update nav buttons
  document.querySelectorAll('.tab-btn').forEach(btn => {
    if (btn.getAttribute('data-tab') === tabId) {
      btn.classList.add('bg-blue-50', 'text-blue-700', 'font-semibold');
      btn.classList.remove('text-slate-600', 'font-medium');
    } else {
      btn.classList.remove('bg-blue-50', 'text-blue-700', 'font-semibold');
      btn.classList.add('text-slate-600', 'font-medium');
    }
  });

  // Show corresponding section
  document.querySelectorAll('.tab-content').forEach(section => {
    section.classList.add('hidden');
  });
  const targetSection = document.getElementById(`tab-${tabId}`);
  if (targetSection) {
    targetSection.classList.remove('hidden');
  }

  // Auto-fetch if data is empty when navigating to tab
  if (tabId === 'keywords' && dashboardState.keywords.length === 0 && dashboardState.hasKey) {
    fetchKeywords();
  } else if (tabId === 'backlinks' && dashboardState.backlinks.length === 0 && dashboardState.hasKey) {
    fetchBacklinkData();
  } else if (tabId === 'top-pages' && dashboardState.topPages.length === 0 && dashboardState.hasKey) {
    fetchTopPages();
  } else if (tabId === 'competitors' && dashboardState.competitors.length === 0 && dashboardState.hasKey) {
    fetchCompetitors();
  } else if (tabId === 'site-audit' && dashboardState.siteAuditProjects.length === 0 && dashboardState.hasKey) {
    loadSiteAuditProjects();
  }
}

// Modal handling
function setupApiSettingsModal() {
  const modal = document.getElementById('keyModal');
  const openBtn = document.getElementById('openKeyModalBtn');
  const closeBtn = document.getElementById('closeKeyModalBtn');
  const keyForm = document.getElementById('keyForm');
  const testKeyBtn = document.getElementById('testKeyBtn');

  if (openBtn) openBtn.onclick = () => modal.classList.remove('hidden');
  if (closeBtn) closeBtn.onclick = () => modal.classList.add('hidden');

  if (keyForm) {
    keyForm.onsubmit = async (e) => {
      e.preventDefault();
      const apiKey = document.getElementById('apiKeyInput').value;
      const feedback = document.getElementById('keyModalFeedback');
      feedback.classList.remove('hidden', 'bg-red-50', 'text-red-700', 'bg-emerald-50', 'text-emerald-700');
      feedback.textContent = 'Saving key securely to server session...';

      try {
        const res = await fetch('/api/set-key', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ apiKey })
        });
        const data = await res.json();
        if (res.ok) {
          feedback.classList.add('bg-emerald-50', 'text-emerald-700');
          feedback.textContent = `Success! Key stored in server session (${data.apiKeyMasked}). Refreshing data...`;
          dashboardState.hasKey = true;
          updateKeyBadge(true, data.apiKeyMasked);
          setTimeout(() => {
            modal.classList.add('hidden');
            fetchAllData();
          }, 1200);
        } else {
          feedback.classList.add('bg-red-50', 'text-red-700');
          feedback.textContent = data.error || 'Failed to save key';
        }
      } catch (err) {
        feedback.classList.add('bg-red-50', 'text-red-700');
        feedback.textContent = 'Network error saving API key';
      }
    };
  }

  if (testKeyBtn) {
    testKeyBtn.onclick = async () => {
      const feedback = document.getElementById('keyModalFeedback');
      feedback.classList.remove('hidden', 'bg-red-50', 'text-red-700', 'bg-emerald-50', 'text-emerald-700');
      feedback.textContent = 'Testing connection with Ahrefs API v3...';

      const tempKey = document.getElementById('apiKeyInput').value;
      if (tempKey) {
        // Temporarily set key on server first
        await fetch('/api/set-key', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ apiKey: tempKey })
        });
      }

      try {
        const res = await fetch('/api/test-connection');
        const data = await res.json();
        if (res.ok && data.connected) {
          feedback.classList.add('bg-emerald-50', 'text-emerald-700');
          feedback.textContent = `Connected! Subscription: ${data.subscription || 'Active'}`;
        } else {
          feedback.classList.add('bg-red-50', 'text-red-700');
          feedback.textContent = data.error || 'Connection failed: Unauthorized or invalid key';
        }
      } catch (err) {
        feedback.classList.add('bg-red-50', 'text-red-700');
        feedback.textContent = 'Network error contacting server test endpoint';
      }
    };
  }
}

function setupEventListeners() {
  const refreshBtn = document.getElementById('refreshDataBtn');
  if (refreshBtn) refreshBtn.onclick = () => fetchAllData(true);

  const loadKwBtn = document.getElementById('loadKeywordsBtn');
  if (loadKwBtn) loadKwBtn.onclick = () => fetchKeywords(true);

  const loadBlBtn = document.getElementById('loadBacklinksBtn');
  if (loadBlBtn) loadBlBtn.onclick = () => fetchBacklinkData(true);

  const loadTpBtn = document.getElementById('loadTopPagesBtn');
  if (loadTpBtn) loadTpBtn.onclick = () => fetchTopPages(true);

  const loadCompBtn = document.getElementById('loadCompetitorsBtn');
  if (loadCompBtn) loadCompBtn.onclick = () => fetchCompetitors(true);

  const exportCsvBtn = document.getElementById('exportCsvBtn');
  if (exportCsvBtn) exportCsvBtn.onclick = exportKeywordsCsv;

  const printBtn = document.getElementById('printReportBtn');
  if (printBtn) printBtn.onclick = () => window.print();

  // --- NEW FREE STACK: Lighthouse & AI Listeners ---
  const runLighthouseBtn = document.getElementById('runLighthouseBtn');
  if (runLighthouseBtn) runLighthouseBtn.onclick = runLighthouseAudit;

  const generateAiInsightsBtn = document.getElementById('generateAiInsightsBtn');
  if (generateAiInsightsBtn) generateAiInsightsBtn.onclick = generateAiInsights;
}

// --- NEW FREE STACK: Functions ---

async function runLighthouseAudit() {
  const btn = document.getElementById('runLighthouseBtn');
  const originalText = btn.textContent;
  btn.textContent = 'Running Scan (May take 30s)...';
  btn.disabled = true;

  try {
    const res = await fetch(`/api/lighthouse?url=https://${dashboardState.target}`);
    const data = await res.json();

    if (res.ok && data.lighthouseResult) {
      const cats = data.lighthouseResult.categories;
      const formatScore = (score) => Math.round((score || 0) * 100);
      
      const perf = formatScore(cats.performance?.score);
      const acc = formatScore(cats.accessibility?.score);
      const best = formatScore(cats['best-practices']?.score);
      const seo = formatScore(cats.seo?.score);

      document.getElementById('lhPerf').textContent = perf;
      document.getElementById('lhAccess').textContent = acc;
      document.getElementById('lhBest').textContent = best;
      document.getElementById('lhSeo').textContent = seo;

      // Color coding
      const colorize = (elId, score) => {
        const el = document.getElementById(elId);
        el.className = `text-3xl font-extrabold ${score >= 90 ? 'text-emerald-600' : score >= 50 ? 'text-amber-500' : 'text-red-600'}`;
      };
      colorize('lhPerf', perf);
      colorize('lhAccess', acc);
      colorize('lhBest', best);
      colorize('lhSeo', seo);

      dashboardState.lighthouseScores = { perf, acc, best, seo };
    } else {
      let errorMsg = 'Unknown error';
      if (data.error) {
        if (typeof data.error === 'string') errorMsg = data.error;
        else if (data.error.message) errorMsg = data.error.message;
        else errorMsg = JSON.stringify(data.error);
      }
      alert('Lighthouse scan failed: ' + errorMsg);
    }
  } catch (err) {
    alert('Network error connecting to Lighthouse API.');
  } finally {
    btn.textContent = originalText;
    btn.disabled = false;
  }
}

async function generateAiInsights() {
  const contentDiv = document.getElementById('aiInsightsContent');
  const btn = document.getElementById('generateAiInsightsBtn');
  
  if (!dashboardState.lighthouseScores) {
    alert('Please run the Lighthouse scan first to give the AI some data to analyze.');
    return;
  }

  contentDiv.innerHTML = '<span class="text-slate-500 italic">Asking local Ollama (Llama 3) for insights...</span>';
  btn.disabled = true;

  const prompt = `You are an expert Technical SEO consultant. Analyze the following Lighthouse scores for my website needdroptaxi.com:
  - Performance: ${dashboardState.lighthouseScores.perf}/100
  - Accessibility: ${dashboardState.lighthouseScores.acc}/100
  - Best Practices: ${dashboardState.lighthouseScores.best}/100
  - SEO: ${dashboardState.lighthouseScores.seo}/100
  
  Provide a short, actionable, bulleted action plan on what I should prioritize fixing.`;

  try {
    const res = await fetch('/api/ollama', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ model: 'llama3', prompt })
    });
    const data = await res.json();

    if (res.ok) {
      // Very basic markdown handling for bold/bullets
      const formatted = data.response
        .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
        .replace(/\n\*/g, '<br/>•')
        .replace(/\n/g, '<br/>');
      contentDiv.innerHTML = formatted;
    } else {
      contentDiv.innerHTML = `<span class="text-red-500">Ollama API Error: ${data.error || 'Could not connect to localhost:11434'}</span>`;
    }
  } catch (err) {
    contentDiv.innerHTML = '<span class="text-red-500">Failed to connect to local Ollama instance. Is it running on port 11434?</span>';
  } finally {
    btn.disabled = false;
  }
}

// Check Backend API Status
async function checkApiStatus() {
  try {
    const res = await fetch('/api/status');
    const data = await res.json();
    dashboardState.hasKey = data.hasApiKey;
    updateKeyBadge(data.hasApiKey, data.apiKeyMasked);

    if (data.hasApiKey) {
      fetchAllData();
    } else {
      showAlert(
        'Ahrefs API Key Required',
        'Please configure your Ahrefs API v3 key in .env (AHREFS_API_KEY) or click the "API Settings" button to input your key securely.',
        'warning'
      );
    }
  } catch (err) {
    updateKeyBadge(false);
    showAlert('Server Connection Error', 'Could not connect to the local Ahrefs proxy server.', 'error');
  }
}

function updateKeyBadge(hasKey, masked) {
  const badge = document.getElementById('keyStatusBadge');
  const text = document.getElementById('keyStatusText');
  if (hasKey) {
    badge.className = 'flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs font-medium bg-emerald-50 text-emerald-800 border border-emerald-200';
    text.textContent = `Ahrefs Key: ${masked || 'Active'}`;
  } else {
    badge.className = 'flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs font-medium bg-amber-50 text-amber-800 border border-amber-200 cursor-pointer';
    badge.onclick = () => document.getElementById('keyModal').classList.remove('hidden');
    text.textContent = 'API Key Not Set (Click to Add)';
  }
}

function showAlert(title, desc, type = 'info') {
  const alertEl = document.getElementById('statusAlert');
  const titleEl = document.getElementById('statusAlertTitle');
  const descEl = document.getElementById('statusAlertDesc');
  const iconEl = document.getElementById('statusAlertIcon');

  alertEl.classList.remove('hidden', 'bg-blue-50', 'border-blue-200', 'bg-amber-50', 'border-amber-200', 'bg-red-50', 'border-red-200');

  if (type === 'error') {
    alertEl.classList.add('bg-red-50', 'border-red-200');
    iconEl.textContent = '⚠️';
  } else if (type === 'warning') {
    alertEl.classList.add('bg-amber-50', 'border-amber-200');
    iconEl.textContent = '🔑';
  } else {
    alertEl.classList.add('bg-blue-50', 'border-blue-200');
    iconEl.textContent = 'ℹ️';
  }

  titleEl.textContent = title;
  descEl.textContent = desc;
}

// Fetch All Overview Data
async function fetchAllData(force = false) {
  if (!dashboardState.hasKey) {
    document.getElementById('keyModal').classList.remove('hidden');
    return;
  }

  showAlert('Syncing Ahrefs v3 Data', 'Retrieving live metrics from Ahrefs API...', 'info');

  try {
    const url = `/api/overview?target=${dashboardState.target}${force ? '&force=true' : ''}`;
    const res = await fetch(url);
    const data = await res.json();

    if (res.ok) {
      dashboardState.overview = data;
      renderOverview(data);
      document.getElementById('statusAlert').classList.add('hidden');
      document.getElementById('lastSyncLabel').textContent = new Date().toLocaleTimeString();
      document.getElementById('reportDateVal').textContent = new Date().toLocaleDateString();
    } else {
      showAlert('API Response Issue', data.error || 'Unable to retrieve Ahrefs overview metrics.', 'error');
    }
  } catch (err) {
    showAlert('Network Error', 'Failed to fetch overview data from server.', 'error');
  }

  // Also fetch keywords for opportunity table
  fetchKeywords(force);
}

function renderOverview(data) {
  // Domain Rating
  const drVal = data.domainRating?.domain_rating?.domain_rating;
  const ahrefsRank = data.domainRating?.domain_rating?.ahrefs_rank;
  document.getElementById('kpiDR').textContent = drVal !== undefined ? drVal : (data.domainRating?.error ? 'Plan Limit' : '--');
  document.getElementById('reportDR').textContent = drVal !== undefined ? drVal : '--';
  if (ahrefsRank) {
    document.getElementById('kpiAhrefsRank').textContent = `AR: #${ahrefsRank.toLocaleString()}`;
  }

  // Organic Traffic & Keywords from metrics
  const metrics = data.metrics?.metrics;
  if (metrics) {
    const traffic = metrics.org_traffic || 0;
    const keywords = metrics.org_keywords || 0;
    const top3 = metrics.org_keywords_1_3 || 0;

    document.getElementById('kpiTraffic').textContent = traffic.toLocaleString();
    document.getElementById('reportTraffic').textContent = traffic.toLocaleString();

    document.getElementById('kpiKeywords').textContent = keywords.toLocaleString();
    document.getElementById('reportKeywords').textContent = keywords.toLocaleString();
    document.getElementById('kpiKeywordsTop3').textContent = `Top 3: ${top3.toLocaleString()}`;
  } else if (data.metrics?.error) {
    document.getElementById('kpiTraffic').innerHTML = `<span class="text-sm text-red-500 font-medium">Upgrade Required</span>`;
    document.getElementById('kpiKeywords').innerHTML = `<span class="text-sm text-red-500 font-medium">Upgrade Required</span>`;
  }

  // Backlinks stats
  const blMetrics = data.backlinksStats?.metrics;
  if (blMetrics) {
    document.getElementById('kpiBacklinks').textContent = (blMetrics.live || 0).toLocaleString();
    document.getElementById('kpiRefdomains').textContent = (blMetrics.live_refdomains || 0).toLocaleString();
    document.getElementById('reportRefdomains').textContent = (blMetrics.live_refdomains || 0).toLocaleString();
  } else if (data.backlinksStats?.error) {
    document.getElementById('kpiBacklinks').innerHTML = `<span class="text-sm text-red-500 font-medium">Upgrade Required</span>`;
    document.getElementById('kpiRefdomains').innerHTML = `<span class="text-sm text-red-500 font-medium">Upgrade Required</span>`;
  }

  // Subscription Info
  const sub = data.subscription?.limits_and_usage;
  if (sub) {
    document.getElementById('planBadge').textContent = sub.subscription || 'Active Plan';
    const used = sub.units_usage_api_key || 0;
    const limit = sub.units_limit_api_key;
    document.getElementById('unitsUsageText').textContent = `${used.toLocaleString()} / ${limit ? limit.toLocaleString() : 'Unlimited'}`;

    if (limit) {
      const pct = Math.min(100, Math.round((used / limit) * 100));
      document.getElementById('unitsUsageBar').style.width = `${pct}%`;
    } else {
      document.getElementById('unitsUsageBar').style.width = '10%';
    }

    document.getElementById('resetDateText').textContent = sub.usage_reset_date || 'N/A';
    document.getElementById('workspaceUnitsText').textContent = sub.units_usage_workspace !== null && sub.units_usage_workspace !== undefined
      ? `${sub.units_usage_workspace.toLocaleString()} used`
      : 'Active';
  }
}

// Fetch Keywords
async function fetchKeywords(force = false) {
  const tbody = document.getElementById('keywordsTableBody');
  tbody.innerHTML = '<tr><td colspan="8" class="py-8 text-center text-slate-400">Loading keywords from Ahrefs API v3...</td></tr>';

  try {
    const url = `/api/keywords?target=${dashboardState.target}&limit=100${force ? '&force=true' : ''}`;
    const res = await fetch(url);
    const data = await res.json();

    if (res.ok && data.keywords) {
      dashboardState.keywords = data.keywords;
      renderKeywordsTable();
      renderStrikingDistanceTable();
      updateRankingTiersChart(data.keywords);
    } else {
      tbody.innerHTML = `<tr><td colspan="8" class="py-6 text-center text-amber-600">${data.error || 'No keywords returned for this domain or subscription tier.'}</td></tr>`;
    }
  } catch (err) {
    tbody.innerHTML = '<tr><td colspan="8" class="py-6 text-center text-red-500">Failed to load keywords.</td></tr>';
  }
}

function renderKeywordsTable() {
  const tbody = document.getElementById('keywordsTableBody');
  const kwSearch = (document.getElementById('keywordSearchInput')?.value || '').toLowerCase();
  const urlSearch = (document.getElementById('keywordUrlSearchInput')?.value || '').toLowerCase();
  const filter = dashboardState.keywordFilter;

  let filtered = dashboardState.keywords.filter(item => {
    // Keyword text filter
    if (kwSearch && !item.keyword.toLowerCase().includes(kwSearch)) return false;
    // URL filter
    if (urlSearch && !((item.best_position_url || '').toLowerCase().includes(urlSearch))) return false;

    // Position filter
    const pos = item.best_position;
    if (filter === '1-3') return pos >= 1 && pos <= 3;
    if (filter === '4-10') return pos >= 4 && pos <= 10;
    if (filter === '11-20') return pos >= 11 && pos <= 20;
    if (filter === '21-50') return pos >= 21 && pos <= 50;
    if (filter === '51-100') return pos >= 51 && pos <= 100;
    return true;
  });

  document.getElementById('keywordsCountLabel').textContent = filtered.length;

  if (filtered.length === 0) {
    tbody.innerHTML = '<tr><td colspan="8" class="py-6 text-center text-slate-400">No matching keywords found.</td></tr>';
    return;
  }

  tbody.innerHTML = filtered.map(kw => {
    let badgeClass = 'badge-pos-low';
    if (kw.best_position <= 3) badgeClass = 'badge-pos-top3';
    else if (kw.best_position <= 10) badgeClass = 'badge-pos-top10';
    else if (kw.best_position <= 20) badgeClass = 'badge-pos-mid';

    const intent = kw.is_transactional ? 'Transactional'
      : kw.is_commercial ? 'Commercial'
      : kw.is_navigational ? 'Navigational'
      : kw.is_informational ? 'Informational' : 'General';

    return `
      <tr class="hover:bg-slate-50 transition">
        <td class="py-2.5 px-3 font-semibold text-slate-800">${escapeHtml(kw.keyword)}</td>
        <td class="py-2.5 px-3">
          <span class="inline-flex items-center px-2 py-0.5 rounded text-xs font-bold ${badgeClass}">
            #${kw.best_position || '-'}
          </span>
        </td>
        <td class="py-2.5 px-3 text-slate-400">${kw.best_position_prev ? `#${kw.best_position_prev}` : '-'}</td>
        <td class="py-2.5 px-3 font-medium text-slate-700">${(kw.volume || 0).toLocaleString()}</td>
        <td class="py-2.5 px-3 text-slate-700">${Math.round(kw.sum_traffic || 0).toLocaleString()}</td>
        <td class="py-2.5 px-3 max-w-[220px] truncate" title="${escapeHtml(kw.best_position_url || '')}">
          <a href="${escapeHtml(kw.best_position_url || '#')}" target="_blank" class="text-blue-600 hover:underline">
            ${escapeHtml(kw.best_position_url ? kw.best_position_url.replace('https://needdroptaxi.com', '') : '-')}
          </a>
        </td>
        <td class="py-2.5 px-3 uppercase text-slate-500">${escapeHtml(kw.keyword_country || 'in')}</td>
        <td class="py-2.5 px-3 text-slate-600">
          <span class="px-2 py-0.5 rounded bg-slate-100 text-[10px] font-medium">${intent}</span>
        </td>
      </tr>
    `;
  }).join('');
}

function renderStrikingDistanceTable() {
  const tbody = document.getElementById('strikingDistanceBody');
  const striking = dashboardState.keywords
    .filter(kw => kw.best_position >= 4 && kw.best_position <= 20)
    .sort((a, b) => (b.volume || 0) - (a.volume || 0))
    .slice(0, 8);

  if (striking.length === 0) {
    tbody.innerHTML = '<tr><td colspan="6" class="py-4 text-center text-slate-400">No striking-distance keywords detected in sample.</td></tr>';
    return;
  }

  tbody.innerHTML = striking.map(kw => `
    <tr class="hover:bg-slate-50">
      <td class="py-2.5 px-3 font-semibold text-slate-900">${escapeHtml(kw.keyword)}</td>
      <td class="py-2.5 px-3">
        <span class="inline-flex px-2 py-0.5 rounded font-bold text-xs ${kw.best_position <= 10 ? 'badge-pos-top10' : 'badge-pos-mid'}">
          #${kw.best_position}
        </span>
      </td>
      <td class="py-2.5 px-3 font-medium">${(kw.volume || 0).toLocaleString()}</td>
      <td class="py-2.5 px-3">${Math.round(kw.sum_traffic || 0).toLocaleString()}</td>
      <td class="py-2.5 px-3 max-w-[200px] truncate">
        <a href="${escapeHtml(kw.best_position_url || '#')}" target="_blank" class="text-blue-600 hover:underline">
          ${escapeHtml(kw.best_position_url ? kw.best_position_url.replace('https://needdroptaxi.com', '') : '-')}
        </a>
      </td>
      <td class="py-2.5 px-3 text-emerald-700 font-medium">Add internal links & refresh content</td>
    </tr>
  `).join('');
}

function updateRankingTiersChart(keywords) {
  const ctx = document.getElementById('rankingTiersChart');
  if (!ctx) return;

  let top3 = 0, top10 = 0, top20 = 0, top50 = 0, top100 = 0;
  keywords.forEach(kw => {
    const p = kw.best_position;
    if (p <= 3) top3++;
    else if (p <= 10) top10++;
    else if (p <= 20) top20++;
    else if (p <= 50) top50++;
    else top100++;
  });

  if (dashboardState.rankingChartInstance) {
    dashboardState.rankingChartInstance.destroy();
  }

  dashboardState.rankingChartInstance = new Chart(ctx, {
    type: 'bar',
    data: {
      labels: ['Pos 1–3', 'Pos 4–10', 'Pos 11–20', 'Pos 21–50', 'Pos 51–100'],
      datasets: [{
        label: 'Keywords Count',
        data: [top3, top10, top20, top50, top100],
        backgroundColor: [
          '#22c55e', // Green for top 3
          '#3b82f6', // Blue for 4-10
          '#eab308', // Amber for 11-20
          '#f97316', // Orange for 21-50
          '#94a3b8'  // Gray for 51-100
        ],
        borderRadius: 6
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: { display: false }
      },
      scales: {
        y: {
          beginAtZero: true,
          grid: { color: '#f1f5f9' },
          ticks: { font: { size: 10 } }
        },
        x: {
          grid: { display: false },
          ticks: { font: { size: 11, weight: 'bold' } }
        }
      }
    }
  });
}

// Fetch Backlink Data
async function fetchBacklinkData(force = false) {
  const tbody = document.getElementById('backlinksTableBody');
  tbody.innerHTML = '<tr><td colspan="7" class="py-8 text-center text-slate-400">Loading backlinks from Ahrefs API v3...</td></tr>';

  try {
    const [blRes, refRes, brokenRes] = await Promise.all([
      fetch(`/api/backlinks?target=${dashboardState.target}&limit=50${force ? '&force=true' : ''}`).then(r => r.json()),
      fetch(`/api/refdomains?target=${dashboardState.target}&limit=50${force ? '&force=true' : ''}`).then(r => r.json()),
      fetch(`/api/broken-backlinks?target=${dashboardState.target}&limit=50${force ? '&force=true' : ''}`).then(r => r.json())
    ]);

    dashboardState.backlinks = blRes.backlinks || [];
    dashboardState.refdomains = refRes.refdomains || [];
    dashboardState.brokenBacklinks = brokenRes.backlinks || [];

    renderBacklinksTable();
  } catch (err) {
    tbody.innerHTML = '<tr><td colspan="7" class="py-6 text-center text-red-500">Failed to load backlink data.</td></tr>';
  }
}

function renderBacklinksTable() {
  const thead = document.getElementById('backlinksTableHead');
  const tbody = document.getElementById('backlinksTableBody');
  const tab = dashboardState.activeBacklinkTab;

  if (tab === 'all') {
    thead.innerHTML = `
      <tr>
        <th class="py-2.5 px-3">Referring Page (URL From)</th>
        <th class="py-2.5 px-3">Anchor Text</th>
        <th class="py-2.5 px-3">Target URL (URL To)</th>
        <th class="py-2.5 px-3">DR</th>
        <th class="py-2.5 px-3">Type</th>
        <th class="py-2.5 px-3">First Seen</th>
        <th class="py-2.5 px-3">Last Seen</th>
      </tr>
    `;
    if (dashboardState.backlinks.length === 0) {
      tbody.innerHTML = '<tr><td colspan="7" class="py-6 text-center text-slate-400">No backlinks found.</td></tr>';
      return;
    }
    tbody.innerHTML = dashboardState.backlinks.map(bl => `
      <tr class="hover:bg-slate-50 transition">
        <td class="py-2.5 px-3 max-w-[260px] truncate" title="${escapeHtml(bl.url_from || '')}">
          <a href="${escapeHtml(bl.url_from || '#')}" target="_blank" class="text-blue-600 hover:underline">
            ${escapeHtml(bl.url_from || '-')}
          </a>
        </td>
        <td class="py-2.5 px-3 font-medium text-slate-800">${escapeHtml(bl.anchor || '(No anchor text)')}</td>
        <td class="py-2.5 px-3 max-w-[200px] truncate" title="${escapeHtml(bl.url_to || '')}">
          ${escapeHtml(bl.url_to ? bl.url_to.replace('https://needdroptaxi.com', '') : '-')}
        </td>
        <td class="py-2.5 px-3 font-bold">${bl.domain_rating_source !== undefined ? bl.domain_rating_source : '-'}</td>
        <td class="py-2.5 px-3">
          <span class="px-2 py-0.5 rounded text-[10px] font-semibold ${bl.is_dofollow ? 'bg-emerald-50 text-emerald-700' : 'bg-slate-100 text-slate-600'}">
            ${bl.is_dofollow ? 'Dofollow' : 'Nofollow'}
          </span>
        </td>
        <td class="py-2.5 px-3 text-slate-400">${bl.first_seen ? bl.first_seen.split('T')[0] : '-'}</td>
        <td class="py-2.5 px-3 text-slate-400">${bl.last_seen ? bl.last_seen.split('T')[0] : '-'}</td>
      </tr>
    `).join('');
  } else if (tab === 'refdomains') {
    thead.innerHTML = `
      <tr>
        <th class="py-2.5 px-3">Referring Domain</th>
        <th class="py-2.5 px-3">Domain Rating (DR)</th>
        <th class="py-2.5 px-3">Links to Target</th>
        <th class="py-2.5 px-3">Dofollow Links</th>
        <th class="py-2.5 px-3">Domain Traffic</th>
        <th class="py-2.5 px-3">First Seen</th>
      </tr>
    `;
    if (dashboardState.refdomains.length === 0) {
      tbody.innerHTML = '<tr><td colspan="6" class="py-6 text-center text-slate-400">No referring domains found.</td></tr>';
      return;
    }
    tbody.innerHTML = dashboardState.refdomains.map(rd => `
      <tr class="hover:bg-slate-50 transition">
        <td class="py-2.5 px-3 font-semibold text-slate-900">${escapeHtml(rd.domain || '-')}</td>
        <td class="py-2.5 px-3 font-bold text-blue-600">${rd.domain_rating !== undefined ? rd.domain_rating : '-'}</td>
        <td class="py-2.5 px-3 font-medium">${(rd.links_to_target || 0).toLocaleString()}</td>
        <td class="py-2.5 px-3 text-emerald-600">${(rd.dofollow_links || 0).toLocaleString()}</td>
        <td class="py-2.5 px-3 text-slate-600">${Math.round(rd.traffic_domain || 0).toLocaleString()}</td>
        <td class="py-2.5 px-3 text-slate-400">${rd.first_seen ? rd.first_seen.split('T')[0] : '-'}</td>
      </tr>
    `).join('');
  } else if (tab === 'broken') {
    thead.innerHTML = `
      <tr>
        <th class="py-2.5 px-3">Referring Page</th>
        <th class="py-2.5 px-3">Anchor</th>
        <th class="py-2.5 px-3">Broken Target URL</th>
        <th class="py-2.5 px-3">Target HTTP Code</th>
        <th class="py-2.5 px-3">DR</th>
        <th class="py-2.5 px-3">Recommended Fix</th>
      </tr>
    `;
    if (dashboardState.brokenBacklinks.length === 0) {
      tbody.innerHTML = '<tr><td colspan="6" class="py-6 text-center text-emerald-600 font-medium">🎉 Excellent! No broken backlinks found for Need Drop Taxi.</td></tr>';
      return;
    }
    tbody.innerHTML = dashboardState.brokenBacklinks.map(b => `
      <tr class="hover:bg-slate-50 transition">
        <td class="py-2.5 px-3 max-w-[200px] truncate">${escapeHtml(b.url_from || '-')}</td>
        <td class="py-2.5 px-3">${escapeHtml(b.anchor || '-')}</td>
        <td class="py-2.5 px-3 max-w-[200px] truncate text-red-600">${escapeHtml(b.url_to || '-')}</td>
        <td class="py-2.5 px-3"><span class="px-2 py-0.5 rounded bg-red-100 text-red-800 font-bold">${b.http_code_target || 404}</span></td>
        <td class="py-2.5 px-3 font-bold">${b.domain_rating_source || '-'}</td>
        <td class="py-2.5 px-3 text-blue-600">Add 301 Redirect in _redirects</td>
      </tr>
    `).join('');
  }
}

// Fetch Top Pages
async function fetchTopPages(force = false) {
  const tbody = document.getElementById('topPagesTableBody');
  tbody.innerHTML = '<tr><td colspan="8" class="py-8 text-center text-slate-400">Loading top landing pages from Ahrefs API v3...</td></tr>';

  try {
    const url = `/api/top-pages?target=${dashboardState.target}&limit=50${force ? '&force=true' : ''}`;
    const res = await fetch(url);
    const data = await res.json();

    if (res.ok && data.pages) {
      dashboardState.topPages = data.pages;
      renderTopPagesTable();
    } else {
      tbody.innerHTML = `<tr><td colspan="8" class="py-6 text-center text-amber-600">${data.error || 'No pages returned or requires upgraded plan.'}</td></tr>`;
    }
  } catch (err) {
    tbody.innerHTML = '<tr><td colspan="8" class="py-6 text-center text-red-500">Failed to load top pages.</td></tr>';
  }
}

function renderTopPagesTable() {
  const tbody = document.getElementById('topPagesTableBody');
  if (dashboardState.topPages.length === 0) {
    tbody.innerHTML = '<tr><td colspan="8" class="py-6 text-center text-slate-400">No pages found.</td></tr>';
    return;
  }

  tbody.innerHTML = dashboardState.topPages.map(page => {
    const traffic = Math.round(page.sum_traffic || 0);
    const isTopPerformer = traffic > 50 || page.top_keyword_best_position <= 5;
    return `
      <tr class="hover:bg-slate-50 transition">
        <td class="py-2.5 px-3 font-medium text-slate-900 max-w-[260px] truncate" title="${escapeHtml(page.url || '')}">
          <a href="${escapeHtml(page.url || '#')}" target="_blank" class="text-blue-600 hover:underline">
            ${escapeHtml(page.url ? page.url.replace('https://needdroptaxi.com', '') || '/' : '-')}
          </a>
        </td>
        <td class="py-2.5 px-3 font-bold text-slate-800">${traffic.toLocaleString()}</td>
        <td class="py-2.5 px-3">${(page.keywords || 0).toLocaleString()}</td>
        <td class="py-2.5 px-3 font-semibold text-slate-800">${escapeHtml(page.top_keyword || '-')}</td>
        <td class="py-2.5 px-3">
          <span class="px-2 py-0.5 rounded text-xs font-bold ${page.top_keyword_best_position <= 3 ? 'badge-pos-top3' : 'badge-pos-top10'}">
            #${page.top_keyword_best_position || '-'}
          </span>
        </td>
        <td class="py-2.5 px-3">${(page.top_keyword_volume || 0).toLocaleString()}</td>
        <td class="py-2.5 px-3">${(page.referring_domains || 0).toLocaleString()}</td>
        <td class="py-2.5 px-3">
          <span class="px-2 py-0.5 rounded text-[10px] font-semibold ${isTopPerformer ? 'bg-emerald-50 text-emerald-700' : 'bg-amber-50 text-amber-700'}">
            ${isTopPerformer ? 'Strong Performer' : 'Opportunity'}
          </span>
        </td>
      </tr>
    `;
  }).join('');
}

// Fetch Competitors
async function fetchCompetitors(force = false) {
  const tbody = document.getElementById('competitorsTableBody');
  tbody.innerHTML = '<tr><td colspan="7" class="py-8 text-center text-slate-400">Analyzing organic competitors in India...</td></tr>';

  try {
    const url = `/api/competitors?target=${dashboardState.target}&country=in&limit=15${force ? '&force=true' : ''}`;
    const res = await fetch(url);
    const data = await res.json();

    if (res.ok && data.competitors) {
      dashboardState.competitors = data.competitors;
      renderCompetitorsTable();
    } else {
      tbody.innerHTML = `<tr><td colspan="7" class="py-6 text-center text-amber-600">${data.error || 'Competitor endpoint requires an eligible Ahrefs plan.'}</td></tr>`;
    }
  } catch (err) {
    tbody.innerHTML = '<tr><td colspan="7" class="py-6 text-center text-red-500">Failed to load competitors.</td></tr>';
  }
}

function renderCompetitorsTable() {
  const tbody = document.getElementById('competitorsTableBody');
  if (dashboardState.competitors.length === 0) {
    tbody.innerHTML = '<tr><td colspan="7" class="py-6 text-center text-slate-400">No competitors returned.</td></tr>';
    return;
  }

  tbody.innerHTML = dashboardState.competitors.map(comp => `
    <tr class="hover:bg-slate-50 transition">
      <td class="py-2.5 px-3 font-semibold text-slate-900">${escapeHtml(comp.competitor_domain || '-')}</td>
      <td class="py-2.5 px-3 font-bold text-blue-600">${comp.domain_rating !== undefined ? comp.domain_rating : '-'}</td>
      <td class="py-2.5 px-3 font-bold text-emerald-600">${(comp.keywords_common || 0).toLocaleString()}</td>
      <td class="py-2.5 px-3">${(comp.keywords_competitor || 0).toLocaleString()}</td>
      <td class="py-2.5 px-3">${(comp.keywords_target || 0).toLocaleString()}</td>
      <td class="py-2.5 px-3 font-medium">${Math.round(comp.traffic || 0).toLocaleString()}</td>
      <td class="py-2.5 px-3">${(comp.pages || 0).toLocaleString()}</td>
    </tr>
  `).join('');
}

// Site Audit Projects
async function loadSiteAuditProjects() {
  try {
    const res = await fetch('/api/site-audit/projects');
    const data = await res.json();

    if (res.ok && data.healthscores && data.healthscores.length > 0) {
      dashboardState.siteAuditProjects = data.healthscores;
      const select = document.getElementById('siteAuditProjectSelect');
      select.innerHTML = data.healthscores.map(p => `
        <option value="${p.project_id}">${escapeHtml(p.project_name || p.target_url)} (Score: ${p.health_score || 'N/A'})</option>
      `).join('');

      // Auto-load first project
      loadProjectIssues(data.healthscores[0].project_id, data.healthscores[0]);
    } else {
      const errorMsg = data.error || 'To enable Site Audit issue reporting, ensure you have set up a project in your Ahrefs account for <code class="bg-slate-100 px-1 py-0.5 rounded">https://needdroptaxi.com/</code>.';
      document.getElementById('siteAuditPlaceholder').innerHTML = `
        <div class="text-3xl mb-2">ℹ️</div>
        <h4 class="font-semibold text-slate-800">Site Audit Not Available</h4>
        <p class="text-xs text-slate-500 max-w-md mx-auto mt-1">${errorMsg}</p>
      `;
    }
  } catch (err) {
    console.error('Error fetching site audit projects:', err);
  }
}

async function loadProjectIssues(projectId, projectMeta) {
  try {
    const res = await fetch(`/api/site-audit/issues?project_id=${projectId}`);
    const data = await res.json();

    document.getElementById('siteAuditPlaceholder').classList.add('hidden');
    document.getElementById('siteAuditLoadedView').classList.remove('hidden');

    if (projectMeta) {
      document.getElementById('auditHealthScoreVal').textContent = projectMeta.health_score || '--';
      document.getElementById('auditErrorsVal').textContent = (projectMeta.urls_with_errors || 0).toLocaleString();
      document.getElementById('auditWarningsVal').textContent = (projectMeta.urls_with_warnings || 0).toLocaleString();
      document.getElementById('auditNoticesVal').textContent = (projectMeta.urls_with_notices || 0).toLocaleString();

      document.getElementById('kpiHealthScore').textContent = projectMeta.health_score || '--';
      document.getElementById('kpiIssuesTotal').textContent = `${(projectMeta.urls_with_errors || 0)} errors detected`;
    }

    if (res.ok && data.issues) {
      dashboardState.currentAuditIssues = data.issues;
      renderAuditIssues(data.issues);
    }
  } catch (err) {
    console.error('Error loading project issues:', err);
  }
}

function renderAuditIssues(issues) {
  const tbody = document.getElementById('siteAuditIssuesBody');
  if (issues.length === 0) {
    tbody.innerHTML = '<tr><td colspan="6" class="py-6 text-center text-slate-400">No issues reported in current crawl.</td></tr>';
    return;
  }

  tbody.innerHTML = issues.map(iss => {
    let impClass = 'bg-slate-100 text-slate-700';
    if (iss.importance === 'error') impClass = 'bg-red-100 text-red-800 font-bold';
    else if (iss.importance === 'warning') impClass = 'bg-amber-100 text-amber-800 font-semibold';
    else if (iss.importance === 'notice') impClass = 'bg-blue-100 text-blue-800';

    return `
      <tr class="hover:bg-slate-50 transition">
        <td class="py-2.5 px-3 font-semibold text-slate-900">${escapeHtml(iss.name || iss.issue_id || '-')}</td>
        <td class="py-2.5 px-3 capitalize text-slate-600">${escapeHtml(iss.category || 'General')}</td>
        <td class="py-2.5 px-3">
          <span class="px-2 py-0.5 rounded text-[10px] uppercase ${impClass}">${iss.importance || 'Notice'}</span>
        </td>
        <td class="py-2.5 px-3">${(iss.crawled || 0).toLocaleString()}</td>
        <td class="py-2.5 px-3 ${iss.added > 0 ? 'text-red-600 font-semibold' : 'text-slate-400'}">+${iss.added || 0}</td>
        <td class="py-2.5 px-3 text-slate-700">Review HTML templates & meta directives</td>
      </tr>
    `;
  }).join('');
}

// Export Keywords to CSV
function exportKeywordsCsv() {
  if (dashboardState.keywords.length === 0) {
    alert('No keywords available to export. Please fetch keywords first.');
    return;
  }

  const headers = ['Keyword', 'Position', 'Previous Position', 'Volume', 'Estimated Traffic', 'URL', 'Country'];
  const rows = dashboardState.keywords.map(kw => [
    `"${(kw.keyword || '').replace(/"/g, '""')}"`,
    kw.best_position || '',
    kw.best_position_prev || '',
    kw.volume || 0,
    Math.round(kw.sum_traffic || 0),
    `"${(kw.best_position_url || '').replace(/"/g, '""')}"`,
    kw.keyword_country || 'in'
  ]);

  const csvContent = 'data:text/csv;charset=utf-8,' + [headers.join(','), ...rows.map(r => r.join(','))].join('\n');
  const encodedUri = encodeURI(csvContent);
  const link = document.createElement('a');
  link.setAttribute('href', encodedUri);
  link.setAttribute('download', `needdroptaxi_ahrefs_keywords_${new Date().toISOString().split('T')[0]}.csv`);
  document.body.appendChild(link);
  link.click();
  document.body.removeChild(link);
}

// Utility
function escapeHtml(str) {
  if (!str) return '';
  return String(str)
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#039;');
}
