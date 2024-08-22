# Localmetric Task Automation Tool

This repository contains the tool developed for Localmetric, designed to automate the creation and management of tasks in ClickUp. The tool covers two main functionalities:

1. **Management of Tasks for Negative Reviews.**
2. **Phase 1: Creation of Tasks for New Clients with Subtasks.**

## Features

### 1. Management of Tasks for Negative Reviews

- **Description:** Creates tasks for unanswered negative reviews with a deadline of seven days. If the task is delayed by a week, it is marked as an urgent priority. Additionally, if the review has more than 200 characters, it is marked as a high priority; otherwise, it is marked as normal.
- **Integration:** Uses the ClickUp API to manage tasks.
- **Priority Rules:**
  - **Normal:** Tasks without special characteristics.
  - **High:** Reviews with more than 200 characters.
  - **Urgent:** Tasks delayed by a week.

### 2. Phase 1: Creation of Tasks for New Clients

- **Description:** Creates various tasks with subtasks in the client's folder, with a deadline of five days.
- **Integration:** Uses the ClickUp API for task creation and organization.
- **Process:**
  - Creates a folder for the new client.
  - Adds main tasks with their respective subtasks.

## Installation

### Prerequisites

- **ClickUp account and access to ClickUp API.**
- **ClickUp API token.**
- **Python 3.12.**