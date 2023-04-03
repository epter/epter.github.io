---
layout: post
title:  "centOS7 user add"
date:   2023-04-03
author: lee
categories: linux
  
---
centos 7



추가

sudo useradd id

비번설정

sudo passwd id

삭제

userdel -r id





root권한 주기

sudoears의 편집권한 주기
chmod +w /etc/sudoears



sudoears 편집
vi /etc/sudoears

i 로 수정모드

root ALL=(ALL) ALL 아래로 추가할 사용자 추가

id ALL=(ALL) ALL

esc로 명령모드 전환 :wq 로 저장후 나가기

chmod -w /etc/sudoears

편집권한 회수



테스트

su - id

sudo whoami



root가 출력되면 ok
