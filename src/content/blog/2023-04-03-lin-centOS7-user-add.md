---
title: 'CentOS 7 사용자 추가 및 sudo(root) 권한 부여 방법'
description: 'CentOS 7 환경에서 useradd로 계정을 생성하고 /etc/sudoers 설정으로 관리자 권한을 부여하는 정리입니다.'
pubDate: '2023-04-03'
category: 'Linux'
tags: ['CentOS7', 'Linux', 'sudo', '사용자관리']
---

CentOS 7 환경에서 새로운 사용자를 생성하고 `sudo` 권한을 부여하는 기본 명령어 정리입니다.

## 1. 사용자 추가 / 비밀번호 설정 / 삭제

```bash
# 사용자 추가
sudo useradd <id>

# 비밀번호 설정
sudo passwd <id>

# 사용자 삭제 (홈 디렉터리 포함)
sudo userdel -r <id>
```

## 2. sudo(root) 권한 부여하기

`/etc/sudoers` 파일은 기본적으로 쓰기 권한이 없으므로, `visudo`를 사용하거나 권한을 잠시 부여해 편집합니다.

```bash
# 쓰기 권한 부여
chmod +w /etc/sudoers

# 파일 편집
vi /etc/sudoers
```

`root ALL=(ALL) ALL` 아래에 추가할 사용자를 기입합니다.

```text
root    ALL=(ALL)       ALL
<id>    ALL=(ALL)       ALL
```

저장(`:wq`) 후 보안을 위해 쓰기 권한을 다시 회수합니다.

```bash
chmod -w /etc/sudoers
```

## 3. 권한 적용 테스트

```bash
su - <id>
sudo whoami
```

출력 결과로 `root`가 나오면 정상 적용된 것입니다.
