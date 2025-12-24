# Entity Relations Diagram

This document describes the database entity relationships for the Django Task Management Application.

## Overview

The application follows a hierarchical structure: **User** � **Projects** � **Tasks**, where users can create multiple projects, and each project can contain multiple tasks.

## Entity Relationship Diagram

```mermaid
erDiagram
    %% 2'O7:8
    auth_user ||--o{ tasks_project : "1:N (Owner)"
    tasks_project ||--o{ tasks_task : "1:N (Parent)"

    %% "01;8FO: auth_user
    auth_user {
        bigint id PK
        varchar(150) username
        varchar(254) email
        varchar(128) password
        boolean is_active
        boolean is_staff
        boolean is_superuser
        timestamp date_joined
    }

    %% "01;8FO: tasks_project
    tasks_project {
        bigint id PK
        bigint user_id FK
        varchar(255) name
        timestamp created_at
        timestamp updated_at
    }

    %% "01;8FO: tasks_task
    tasks_task {
        bigint id PK
        bigint project_id FK
        varchar(255) name
        varchar(20) status "Enum: new, in_progress, done, archived"
        integer priority "Enum: 1..5 (Low to High)"
        timestamp deadline "NULL"
        timestamp created_at
        timestamp updated_at
    }
```
