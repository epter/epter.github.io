---
title: 'Epter 블로그 리뉴얼: Astro 기반 정적 블로그 시작하기'
description: '흩어져 있던 블로그를 하나로 통합하고, 검색 최적화(SEO)와 수익화 확장을 위해 Astro 기반으로 새롭게 구축했습니다.'
pubDate: '2026-11-21'
category: 'Blog'
tags: ['Astro', 'GitHubPages', '블로그']
---

기존에 여러 테스트 저장소에 흩어져 있던 기술 노트들을 정리하고, [`epter.github.io`](https://epter.github.io)로 단일 통합 블로그를 새롭게 구축했습니다.

## 왜 Astro인가?

- **빠른 로딩 속도**: 정적 HTML을 미리 생성해 검색엔진(SEO)과 방문자 경험 모두에 유리합니다.
- **마크다운 기반 관리**: `src/content/blog/` 폴더에 `.md` 또는 `.mdx` 파일만 추가하고 `git push`하면 GitHub Actions가 자동으로 빌드·배포합니다.
- **수익화 준비**: `sitemap.xml`, `robots.txt`, `개인정보처리방침`, 그리고 `src/consts.ts`에서 Google AdSense 및 GA4 ID만 입력하면 바로 연동되도록 구조를 잡았습니다.

앞으로 라즈베리파이 홈서버 운영기, 리눅스/도커 자동화, 유용한 IT 팁들을 꾸준히 기록해 나갈 예정입니다.
