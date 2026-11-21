#!/usr/bin/env python3
"""
CISA KEV(Known Exploited Vulnerabilities) 공식 피드에서 최신 보안 취약점을 조회해
Astro 블로그 마크다운 포스트를 자동 생성하는 스크립트.
"""

from __future__ import annotations

import datetime as dt
import json
import os
import re
import urllib.request
from pathlib import Path

KEV_URL = "https://www.cisa.gov/sites/default/files/feeds/known_exploited_vulnerabilities.json"
BLOG_DIR = Path(__file__).resolve().parent.parent / "src" / "content" / "blog"
MAX_POSTS_PER_RUN = int(os.environ.get("MAX_CVE_POSTS", "2"))
LOOKBACK_DAYS = int(os.environ.get("CVE_LOOKBACK_DAYS", "7"))


def yaml_escape(text: str) -> str:
    """YAML 단일 인용 문자열 내부의 작은따옴표 및 줄바꿈을 안전하게 처리한다."""
    cleaned = " ".join(text.split())
    return cleaned.replace("'", "''")


def existing_cve_ids(blog_dir: Path) -> set[str]:
    """이미 게시된 포스트 파일명 및 내용에서 CVE ID를 수집해 중복 생성을 막는다."""
    found: set[str] = set()
    pattern = re.compile(r"CVE-\d{4}-\d+", re.IGNORECASE)
    for md_file in blog_dir.glob("*.md*"):
        for match in pattern.findall(md_file.name):
            found.add(match.upper())
        try:
            head = md_file.read_text(encoding="utf-8")[:1000]
            for match in pattern.findall(head):
                found.add(match.upper())
        except OSError:
            continue
    return found


def fetch_kev_vulnerabilities() -> list[dict]:
    req = urllib.request.Request(
        KEV_URL,
        headers={"User-Agent": "epter-blog-cve-bot/1.0"},
    )
    with urllib.request.urlopen(req, timeout=20) as resp:
        data = json.loads(resp.read().decode("utf-8"))
    return data.get("vulnerabilities", [])


def build_post_markdown(item: dict) -> str:
    cve_id = item["cveID"].upper()
    vendor = item.get("vendorProject", "Unknown")
    product = item.get("product", "Unknown")
    vuln_name = item.get("vulnerabilityName", cve_id)
    date_added = item.get("dateAdded", dt.date.today().isoformat())
    short_desc = item.get("shortDescription", "")
    required_action = item.get("requiredAction", "")
    due_date = item.get("dueDate", "N/A")
    ransomware = item.get("knownRansomwareCampaignUse", "Unknown")
    cwes = item.get("cwes") or []
    notes_raw = item.get("notes", "")

    title = f"[보안 취약점] {cve_id}: {vendor} {product}"
    description = f"{vendor} {product}에서 확인된 실제 악용 취약점({cve_id}) 요약 및 권고 조치 안내입니다."

    tags = ["CVE", "보안취약점", "CISA-KEV", vendor.replace(" ", "")]
    for cwe in cwes[:3]:
        if cwe not in tags:
            tags.append(cwe)
    tags_yaml = ", ".join(f"'{yaml_escape(t)}'" for t in tags)

    notes_links = [n.strip() for n in notes_raw.split(";") if n.strip()]
    notes_md = "\n".join(f"- {link}" for link in notes_links) if notes_links else f"- https://nvd.nist.gov/vuln/detail/{cve_id}"

    cwe_text = ", ".join(cwes) if cwes else "미지정"

    return f"""---
title: '{yaml_escape(title)}'
description: '{yaml_escape(description)}'
pubDate: '{date_added}'
category: 'Security'
tags: [{tags_yaml}]
---

미국 CISA(사이버보안 및 인프라 보안국)의 **알려진 악용 취약점 목록(KEV)**에 신규 등록된 보안 취약점 브리핑입니다. 실제 공격에 악용 사례가 보고된 항목이므로 해당 제품을 운영 중이라면 빠른 점검이 필요합니다.

## 1. 기본 정보

| 항목 | 내용 |
| :--- | :--- |
| **CVE ID** | `{cve_id}` |
| **벤더 / 제품** | {vendor} / {product} |
| **취약점 명칭** | {vuln_name} |
| **CISA 등록일** | {date_added} |
| **조치 기한(Due Date)** | {due_date} |
| **랜섬웨어 악용 여부** | {ransomware} |
| **CWE 분류** | {cwe_text} |

## 2. 취약점 개요 (원문 요약)

> {short_desc}

## 3. 권고 조치 사항

> {required_action}

## 4. 참고 링크

{notes_md}
"""


def main() -> int:
    BLOG_DIR.mkdir(parents=True, exist_ok=True)
    seen = existing_cve_ids(BLOG_DIR)
    vulns = fetch_kev_vulnerabilities()

    # 최신 등록일 기준 내림차순 정렬
    vulns.sort(key=lambda v: v.get("dateAdded", ""), reverse=True)

    cutoff_date = (dt.date.today() - dt.timedelta(days=LOOKBACK_DAYS)).isoformat()
    created_files: list[str] = []

    for item in vulns:
        if len(created_files) >= MAX_POSTS_PER_RUN:
            break
        cve_id = item.get("cveID", "").upper()
        date_added = item.get("dateAdded", "")
        if not cve_id or cve_id in seen:
            continue
        if date_added < cutoff_date:
            break

        slug = f"{date_added}-{cve_id.lower()}"
        target = BLOG_DIR / f"{slug}.md"
        if target.exists():
            continue

        target.write_text(build_post_markdown(item), encoding="utf-8")
        created_files.append(str(target.name))
        seen.add(cve_id)
        print(f"Created: {target}")

    if not created_files:
        print("No new vulnerabilities to post.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
