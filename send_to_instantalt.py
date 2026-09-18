"""
send_to_instantalt.py
---------------------
Live test script for InstantAlt CMS webhook integration.
Scans all index.html files in the needdroptaxi.com site, extracts <img> src
attributes (skipping SVGs and icons), sends each to the InstantAlt CMS webhook,
and saves the AI-generated alt text suggestions to alt_suggestions.json.

Usage:  python send_to_instantalt.py
Output: alt_suggestions.json
"""

import os, re, json, urllib.request, urllib.error, time

SITE_ROOT      = os.path.dirname(os.path.abspath(__file__))
SITE_BASE_URL  = "https://needdroptaxi.com"
WEBHOOK_URL    = "https://ozvvhracfdhjeawlwfkp.supabase.co/functions/v1/cms-webhook"
WEBHOOK_SECRET = "whsec_91add28850537f36ae4f88a033e7449f249dae5a98f6bb57"
OUTPUT_FILE    = os.path.join(SITE_ROOT, "alt_suggestions.json")
DELAY_SECONDS  = 1.0
SUPPORTED_EXTS = (".webp", ".jpg", ".jpeg", ".png", ".gif")


def find_html_files(root):
    html_files = []
    for dirpath, _, filenames in os.walk(root):
        if any(part.startswith(".") for part in dirpath.split(os.sep)):
            continue
        for fname in filenames:
            if fname == "index.html":
                html_files.append(os.path.join(dirpath, fname))
    return html_files


def extract_img_srcs(html, page_url):
    pat = re.compile(r'<img\b[^>]*\bsrc=["\']([^"\']+)["\'][^>]*?(?:\balt=["\']([^"\']*)["\'])?[^>]*>',
                     re.IGNORECASE | re.DOTALL)
    results, seen = [], set()
    for m in pat.finditer(html):
        src = m.group(1).strip()
        alt = m.group(2) or ""
        # skip data URIs, tracking scripts, SVGs, and favicon-like icons
        if src.startswith("data:") or "partytown" in src or "gtm" in src:
            continue
        lower = src.lower().split("?")[0]
        if not any(lower.endswith(ext) for ext in SUPPORTED_EXTS):
            continue
        if src.startswith("http"):
            full_url = src
        elif src.startswith("//"):
            full_url = "https:" + src
        elif src.startswith("/"):
            full_url = SITE_BASE_URL + src
        else:
            full_url = SITE_BASE_URL + "/" + src
        if full_url not in seen:
            seen.add(full_url)
            results.append({"url": full_url, "existing_alt": alt, "page": page_url})
    return results


def call_webhook(image_url, existing_alt, page):
    payload = json.dumps({
        "imageUrl": image_url,
        "existingAlt": existing_alt,
        "source": "needdroptaxi",
        "page": page,
    }).encode("utf-8")
    req = urllib.request.Request(
        WEBHOOK_URL, data=payload,
        headers={"Content-Type": "application/json", "x-webhook-secret": WEBHOOK_SECRET},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            body = resp.read().decode("utf-8")
            return {"status": resp.status, "body": json.loads(body) if body else {}}
    except urllib.error.HTTPError as e:
        return {"status": e.code, "error": e.read().decode("utf-8")}
    except Exception as exc:
        return {"status": 0, "error": str(exc)}


def main():
    print("=" * 62)
    print("  InstantAlt CMS Webhook -- Live Integration Test")
    print(f"  Webhook: {WEBHOOK_URL}")
    print("=" * 62)

    html_files = find_html_files(SITE_ROOT)
    print(f"\nScanning {len(html_files)} HTML pages...")

    all_images = {}
    for fpath in html_files:
        rel = os.path.relpath(fpath, SITE_ROOT)
        page_url = SITE_BASE_URL + "/" + rel.replace("\\", "/").replace("index.html", "")
        try:
            with open(fpath, encoding="utf-8", errors="ignore") as f:
                html = f.read()
        except Exception as exc:
            print(f"  [SKIP] {rel}: {exc}")
            continue
        for img in extract_img_srcs(html, page_url):
            if img["url"] not in all_images:
                all_images[img["url"]] = img

    total = len(all_images)
    print(f"Found {total} unique raster images (webp/jpg/png/gif)\n")

    suggestions, failed = {}, []

    for i, (url, meta) in enumerate(all_images.items(), 1):
        short = url.replace(SITE_BASE_URL, "")
        print(f"[{i:>3}/{total}] {short}")
        print(f"         existing_alt: {repr(meta['existing_alt'])}")
        result = call_webhook(url, meta["existing_alt"], meta["page"])

        if result["status"] == 200:
            body = result.get("body", {})
            alt_obj = body.get("altText", {})
            accessibility = alt_obj.get("accessibility", "")
            seo = alt_obj.get("seo", "")
            print(f"         OK  accessibility: {repr(accessibility[:100])}")
            print(f"             seo          : {repr(seo[:100])}")
            suggestions[url] = {
                "existing_alt": meta["existing_alt"],
                "suggested_accessibility_alt": accessibility,
                "suggested_seo_alt": seo,
                "page": meta["page"],
            }
        else:
            err = result.get("error", "")
            print(f"         FAIL HTTP {result['status']}: {err[:120]}")
            failed.append(url)
            suggestions[url] = {
                "existing_alt": meta["existing_alt"],
                "suggested_accessibility_alt": None,
                "suggested_seo_alt": None,
                "error": err,
                "page": meta["page"],
            }

        if i < total:
            time.sleep(DELAY_SECONDS)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(suggestions, f, ensure_ascii=False, indent=2)

    print("\n" + "=" * 62)
    print(f"  SUCCESS : {total - len(failed)}/{total} images processed")
    print(f"  FAILED  : {len(failed)}/{total} images")
    print(f"  SAVED   : {OUTPUT_FILE}")
    print("=" * 62)


if __name__ == "__main__":
    main()
