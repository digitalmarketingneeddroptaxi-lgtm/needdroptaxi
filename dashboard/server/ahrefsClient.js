/**
 * Ahrefs API v3 Client
 * Base URL: https://api.ahrefs.com/v3
 * Follows official documentation: https://docs.ahrefs.com/docs/api/reference/introduction
 */

class AhrefsClient {
  constructor(apiKey) {
    this.apiKey = apiKey || process.env.AHREFS_API_KEY || '';
    this.baseUrl = 'https://api.ahrefs.com/v3';
    this.timeoutMs = 15000;
  }

  setApiKey(key) {
    this.apiKey = key;
  }

  hasApiKey() {
    return Boolean(this.apiKey && this.apiKey.trim().length > 0);
  }

  async fetchEndpoint(endpoint, params = {}) {
    if (!this.hasApiKey()) {
      return {
        ok: false,
        status: 401,
        error: 'AHREFS_API_KEY is not configured on the server. Please configure your API key in .env or via the API settings modal.'
      };
    }

    const cleanParams = new URLSearchParams();
    for (const [key, value] of Object.entries(params)) {
      if (value !== undefined && value !== null && value !== '') {
        cleanParams.append(key, String(value));
      }
    }

    const queryString = cleanParams.toString();
    const url = `${this.baseUrl}${endpoint}${queryString ? `?${queryString}` : ''}`;

    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), this.timeoutMs);

    try {
      const response = await fetch(url, {
        method: 'GET',
        headers: {
          'Authorization': `Bearer ${this.apiKey.trim()}`,
          'Accept': 'application/json'
        },
        signal: controller.signal
      });

      clearTimeout(timeoutId);

      const contentType = response.headers.get('content-type') || '';
      let data = null;
      if (contentType.includes('application/json')) {
        data = await response.json();
      } else {
        const text = await response.text();
        try {
          data = JSON.parse(text);
        } catch {
          data = { raw: text };
        }
      }

      if (!response.ok) {
        return {
          ok: false,
          status: response.status,
          error: data?.error || data?.message || `Ahrefs API error: HTTP ${response.status} (${response.statusText})`,
          details: data
        };
      }

      return {
        ok: true,
        status: response.status,
        data
      };
    } catch (err) {
      clearTimeout(timeoutId);
      if (err.name === 'AbortError') {
        return {
          ok: false,
          status: 408,
          error: `Request timed out after ${this.timeoutMs / 1000}s while contacting Ahrefs API v3.`
        };
      }
      return {
        ok: false,
        status: 500,
        error: `Network error connecting to Ahrefs API: ${err.message}`
      };
    }
  }

  // 1. Subscription Info: Limits and usage (FREE endpoint, does not consume units)
  async getLimitsAndUsage() {
    return this.fetchEndpoint('/subscription-info/limits-and-usage');
  }

  // 2. Public Free Domain Rating (FREE endpoint, requires APIv3 key)
  async getPublicDomainRating(target = 'needdroptaxi.com') {
    return this.fetchEndpoint('/public/domain-rating-free', { target });
  }

  // 3. Site Explorer: Domain Rating
  async getDomainRating(target = 'needdroptaxi.com', date) {
    const today = date || new Date().toISOString().split('T')[0];
    return this.fetchEndpoint('/site-explorer/domain-rating', {
      target,
      date: today
    });
  }

  // 4. Site Explorer: Metrics (Organic traffic, keywords, costs)
  async getMetrics(target = 'needdroptaxi.com', options = {}) {
    const today = options.date || new Date().toISOString().split('T')[0];
    const params = {
      target,
      date: today,
      mode: options.mode || 'subdomains'
    };
    if (options.country) params.country = options.country;
    if (options.volume_mode) params.volume_mode = options.volume_mode;
    return this.fetchEndpoint('/site-explorer/metrics', params);
  }

  // 5. Site Explorer: Backlinks Stats
  async getBacklinksStats(target = 'needdroptaxi.com', options = {}) {
    const today = options.date || new Date().toISOString().split('T')[0];
    return this.fetchEndpoint('/site-explorer/backlinks-stats', {
      target,
      date: today,
      mode: options.mode || 'subdomains'
    });
  }

  // 6. Site Explorer: Organic Keywords
  async getOrganicKeywords(target = 'needdroptaxi.com', options = {}) {
    const today = options.date || new Date().toISOString().split('T')[0];
    const defaultSelect = 'keyword,volume,best_position,best_position_prev,best_position_url,sum_traffic,keyword_country,is_commercial,is_informational,is_transactional,is_navigational';
    const params = {
      target,
      date: today,
      mode: options.mode || 'subdomains',
      select: options.select || defaultSelect,
      limit: options.limit || 50
    };
    if (options.country) params.country = options.country;
    if (options.where) params.where = options.where;
    if (options.order_by) params.order_by = options.order_by;
    return this.fetchEndpoint('/site-explorer/organic-keywords', params);
  }

  // 7. Site Explorer: All Backlinks
  async getBacklinks(target = 'needdroptaxi.com', options = {}) {
    const defaultSelect = 'url_from,url_to,anchor,domain_rating_source,url_rating_source,traffic,first_seen,last_seen,is_lost,is_dofollow,is_nofollow';
    const params = {
      target,
      mode: options.mode || 'subdomains',
      select: options.select || defaultSelect,
      limit: options.limit || 50
    };
    if (options.where) params.where = options.where;
    if (options.order_by) params.order_by = options.order_by;
    if (options.history) params.history = options.history;
    return this.fetchEndpoint('/site-explorer/all-backlinks', params);
  }

  // 8. Site Explorer: Referring Domains
  async getRefdomains(target = 'needdroptaxi.com', options = {}) {
    const defaultSelect = 'domain,domain_rating,dofollow_refdomains,dofollow_links,links_to_target,traffic_domain,first_seen,last_seen';
    const params = {
      target,
      mode: options.mode || 'subdomains',
      select: options.select || defaultSelect,
      limit: options.limit || 50
    };
    if (options.where) params.where = options.where;
    if (options.order_by) params.order_by = options.order_by;
    return this.fetchEndpoint('/site-explorer/refdomains', params);
  }

  // 9. Site Explorer: Broken Backlinks
  async getBrokenBacklinks(target = 'needdroptaxi.com', options = {}) {
    const defaultSelect = 'url_from,url_to,anchor,domain_rating_source,http_code_target,first_seen,last_seen';
    const params = {
      target,
      mode: options.mode || 'subdomains',
      select: options.select || defaultSelect,
      limit: options.limit || 50
    };
    if (options.where) params.where = options.where;
    if (options.order_by) params.order_by = options.order_by;
    return this.fetchEndpoint('/site-explorer/broken-backlinks', params);
  }

  // 10. Site Explorer: Top Pages
  async getTopPages(target = 'needdroptaxi.com', options = {}) {
    const today = options.date || new Date().toISOString().split('T')[0];
    const defaultSelect = 'url,sum_traffic,keywords,top_keyword,top_keyword_best_position,top_keyword_volume,value,referring_domains';
    const params = {
      target,
      date: today,
      mode: options.mode || 'subdomains',
      select: options.select || defaultSelect,
      limit: options.limit || 50
    };
    if (options.country) params.country = options.country;
    if (options.where) params.where = options.where;
    if (options.order_by) params.order_by = options.order_by;
    return this.fetchEndpoint('/site-explorer/top-pages', params);
  }

  // 11. Site Explorer: Organic Competitors
  async getOrganicCompetitors(target = 'needdroptaxi.com', options = {}) {
    const today = options.date || new Date().toISOString().split('T')[0];
    const defaultSelect = 'competitor_domain,domain_rating,keywords_common,keywords_competitor,keywords_target,traffic,pages';
    const params = {
      target,
      date: today,
      country: options.country || 'in',
      mode: options.mode || 'subdomains',
      select: options.select || defaultSelect,
      limit: options.limit || 20
    };
    if (options.order_by) params.order_by = options.order_by;
    return this.fetchEndpoint('/site-explorer/organic-competitors', params);
  }

  // 12. Site Audit: Projects (FREE endpoint, does not consume units)
  async getSiteAuditProjects(params = {}) {
    return this.fetchEndpoint('/site-audit/projects', params);
  }

  // 13. Site Audit: Issues
  async getSiteAuditIssues(projectId, options = {}) {
    if (!projectId) {
      return { ok: false, status: 400, error: 'project_id is required for /site-audit/issues' };
    }
    const params = { project_id: projectId };
    if (options.date) params.date = options.date;
    return this.fetchEndpoint('/site-audit/issues', params);
  }

  // 14. Site Audit: Page Explorer
  async getSiteAuditPageExplorer(projectId, options = {}) {
    if (!projectId) {
      return { ok: false, status: 400, error: 'project_id is required for /site-audit/page-explorer' };
    }
    const params = {
      project_id: projectId,
      select: options.select || 'url,http_code,title,canonical,h1_1,content_length,depth,is_indexable',
      limit: options.limit || 50
    };
    if (options.date) params.date = options.date;
    if (options.where) params.where = options.where;
    return this.fetchEndpoint('/site-audit/page-explorer', params);
  }
}

module.exports = AhrefsClient;
