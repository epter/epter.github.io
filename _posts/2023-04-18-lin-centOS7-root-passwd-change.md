---
layout: post
title:  "centOS7 root passwd chanage"
date:   2023-04-18
author: lee
categories: linux
  
---
centos 7

root 패스워드 변경

passwd

새로운 패스워드 입력

다른 리눅스 원격접속
ssh id@ip

예시) ssh root@192.111.11.11
비밀번호 필요

ansible설치 후
ssh-keygen

키생성후

원격접속 컴퓨터 키 배포
ssh-copy-id id@ip
비밀번호필요
