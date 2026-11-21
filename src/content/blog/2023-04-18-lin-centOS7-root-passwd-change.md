---
title: 'CentOS 7 root 비밀번호 변경 및 SSH 키 기반 원격 접속 설정'
description: 'CentOS 7에서 root 패스워드를 변경하고 ssh-keygen 및 ssh-copy-id로 비밀번호 없는 SSH 접속을 구성하는 방법입니다.'
pubDate: '2023-04-18'
category: 'Linux'
tags: ['CentOS7', 'Linux', 'SSH', 'Ansible']
---

CentOS 7에서 `root` 비밀번호 변경과 SSH 키 기반 원격 접속 설정 방법입니다.

## 1. root 패스워드 변경

```bash
passwd
```

명령 실행 후 새로운 패스워드를 두 번 입력합니다.

## 2. SSH 원격 접속

```bash
ssh <id>@<ip>
# 예시: ssh root@192.168.0.10
```

## 3. SSH 키 생성 및 자동 로그인 설정 (Ansible 등)

매번 비밀번호를 입력하지 않고 안전하게 원격 접속하려면 SSH 키를 생성해 배포합니다.

```bash
# SSH 키 생성
ssh-keygen

# 원격 서버에 공개키 배포 (최초 1회 비밀번호 입력)
ssh-copy-id <id>@<ip>
```

이후에는 비밀번호 입력 없이 바로 원격 접속이 가능합니다.
참고로 SSH 세션이 응답 없을 때 강제 종료하려면 엔터 후 `~.`를 입력하면 세션을 빠져나올 수 있습니다.
