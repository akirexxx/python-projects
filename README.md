# RANSOM! — Incident Response Project

"We hold the world in a firm grip."

This repository contains my solutions for the RANSOM! cybersecurity and Python programming project. The project is structured as a four-part investigative scenario where logs, tracking data, and access permissions are analyzed using Python to uncover the culprit behind a ransomware attack.

## Anaconda Industries

Industry: Multinational conglomerate in energy, logistics, and data infrastructure.

Scale: 140,000 employees across 60 countries.

The Core: A high-security data center beneath the headquarters housing account credentials for the entire corporation.

Security Record: Never suffered a security breach. Until now.

__Note: All companies, individuals, and events in this project are entirely fictional.__

## August 14 — The Breach

- The company website was hijacked — replaced with an **encrypted message**
- Hackers claim they stole **the computer containing all account credentials**
- The theft occurred **between 1:00 PM and 6:00 PM**
- No forced entry, no signs of a break-in — suspicion points to someone with an **access card**

Nobody knows who. Yet.

# Welcome to ANTIVENOM

You are an analyst in Anaconda Industries' **incident response group**. The hackers are the poison — **you are the antidote.**

1. **Crack the Code** — decrypt the message
2. **Follow the Access Cards** — who left the data center?
3. **Track the Computer** — which one is isolated?
4. **Expose the Extortionist** — connect the evidence

## Project Structure & Tasks

Each part of the investigation is organized into its own subfolder (task-1/ through task-4/), set up as an independent uv Python project. Each subsequent task builds upon the findings from the previous steps.

| Part | Task | What You Use |
|---|---|---|
| **1** | Decrypt the hackers' message | strings, functions |
| **2** | Read `access.log` — who left the data center 13–18? | files, `with`, filtering |
| **3** | Read `tracking.json` — which computer is isolated? | `json`, helper functions, floats, error handling |
| **4** | Connect `users.yml` + `rooms.csv` — who is the culprit? | `pyyaml`, `csv`, slicing |

## Workflow & Running the Code

Each subfolder contains its own solution.py, test suite, and local README.md detailing specific assumptions and results for that step.

# Structure of Your Project Folder

```text
my-project/
│
├── projekt-inlamningsuppgift.md
├── task-1/
│   ├── solution.py
│   └── README.md
├── task-2/
│   ├── solution.py
│   └── README.md
├── task-3/
│   ├── solution.py
│   └── README.md
└── task-4/
    ├── solution.py
    └── README.md
```