---
layout: post
title: Analysis of Algorithms Study Notes (Part 1)
author: Yuchen Zhang
categories: computer
date: Fri, 02 Jul 2021 20:16:49 -0000
tags: ['study-notes', 'analysis-of-algorithms', 'stable-matching']
banner: "https://images.unsplash.com/photo-1592659762303-90081d34b277"
---

## Stable Matching

### Problem

We are interested in matching $n$ men with $n$ women so that they could stay happily married ever after.

#### Step 1: Come up with a concise problem statement

- We have a set of $n$ men, $M={m_1, ..., m_n}$
- We have a set of $n$ women, $W={w_1, ..., w_n}$