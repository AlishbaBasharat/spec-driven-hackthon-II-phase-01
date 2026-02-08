---
id: 1
title: Create Todo Constitution
stage: constitution
date: 2025-12-07
surface: agent
model: claude-opus-4-5-20251101
feature: none
branch: master
user: Claude Code
command: /sp.constitution
labels: ["constitution", "todo-app", "cli"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
 - .specify/memory/constitution.md
tests:
 - none
---

## Prompt

```text
Project Details: The Evolution of Todo
Focus and Theme: Build CLI based python Todo .
Goal: Act as Product Architects, to build progressively complex software without writing boilerplate code.

Project Overview
This project simulates the real-world evolution of software. Start with a simple and end with an fully functional todo console app with complete CRUD functioanlity.

Todo App Feature Progression
Basic Level (Core Essentials)
These form the foundation—quick to build, essential for any MVP:
Add Task – Create new todo items
Delete Task – Remove tasks from the list
Update Task – Modify existing task details
View Task List – Display all tasks
Mark as Complete – Toggle task completion status
Intermediate Level (Organization & Usability)
Add these to make the app feel polished and practical:


Priorities & Tags/Categories – Assign levels (high/medium/low) or labels (work/home)
Search & Filter – Search by keyword; filter by status, priority, or date
Sort Tasks – Reorder by due date, priority, or alphabetically
Advanced Level (Intelligent Features)
Recurring Tasks – Auto-reschedule repeating tasks (e.g., "weekly meeting")
Due Dates & Time Reminders – Set deadlines with date/time pickers; browser notifications

Phase Breakdown

Phase I: Todo In-Memory Python Console App
Basic Level Functionality
Objective: Build a command-line todo application that stores tasks in memory using Claude Code and Spec-Kit Plus.
Requirements
Implement all 5 Basic Level features (Add, Delete, Update, View, Mark Complete)
Use spec-driven development with Claude Code and Spec-Kit Plus
Follow clean code principles and proper Python project structure
Technology Stack
UV
Python 3.13+
Claude Code
Spec-Kit Plus
Deliverables
GitHub repository with:
Constitution file
specs history folder containing all specification files
/src folder with Python source code
README.md with setup instructions
CLAUDE.md with Claude Code instructions

Working console application demonstrating:
Adding tasks with title and description
Listing all tasks with status indicators
Updating task details
Deleting tasks by ID
Marking tasks as complete/incomplete
```

## Response snapshot

Created a constitution file for the CLI Todo App project that includes core principles, constraints, workflow, and governance guidelines aligned with the project requirements.

## Outcome

- ✅ Impact: Created constitution.md with 6 core principles and governance structure
- 🧪 Tests: none
- 📁 Files: Updated .specify/memory/constitution.md with project-specific principles
- 🔁 Next prompts: Continue with spec creation using /sp.specify
- 🧠 Reflection: Constitution properly captures CLI-first, in-memory storage, and Python standards requirements

## Evaluation notes (flywheel)

- Failure modes observed: none
- Graders run and results (PASS/FAIL): PASS - Constitution follows template and project requirements
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Begin spec creation for the todo app features