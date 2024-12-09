# Coding Agent Setup

This repository provides an environment for running the Coding Agent powered by OIlama and the `qwen2.5-coder:3b` model. Follow the instructions below to get started.

## Prerequisites

- [Python](https://www.python.org/) (Version 3.7 or higher)
- [OIlama](https://ollama.com/) installed on your machine.

---

## Installation Guide

### 1. Install OIlama

Download and install OIlama from their [official website](https://ollama.com/).

### 2. Install the Required Model

Run the following command to install the `qwen2.5-coder:3b` model:

```bash
ollama qwen2.5-coder:3b
```

### 3. Install dependencies
From root, run the following command:
```bash
pip requirements.txt
```

### 4. Run:
From root, run the following command:
```bash
python -m coding_agent.agent.coding_agent
```
