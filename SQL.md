# SQL Task Solutions

## 1. Get all statuses, not repeating, alphabetically ordered
```sql
SELECT DISTINCT status 
FROM tasks 
ORDER BY status ASC;
```

## 2. Get the count of all tasks in each project, order by tasks count descending
```sql
SELECT p.name, COUNT(t.id) as task_count
FROM projects p
LEFT JOIN tasks t ON p.id = t.project_id
GROUP BY p.id, p.name
ORDER BY task_count DESC;
```

## 3. Get the count of all tasks in each project, order by projects names
```sql
SELECT p.name, COUNT(t.id) as task_count
FROM projects p
LEFT JOIN tasks t ON p.id = t.project_id
GROUP BY p.id, p.name
ORDER BY p.name ASC;
```

## 4. Get the tasks for all projects having the name beginning with "N" letter
```sql
SELECT t.*
FROM tasks t
JOIN projects p ON t.project_id = p.id
WHERE p.name LIKE 'N%';
```

## 5. Get the list of all projects containing the 'a' letter in the middle of the name, and show the tasks count near each project
*Note: We use `LEFT JOIN` to ensure projects without tasks are included. Tasks with `project_id = NULL` are ignored.*

```sql
SELECT p.name, COUNT(t.id) as task_count
FROM projects p
LEFT JOIN tasks t ON p.id = t.project_id
WHERE p.name LIKE '_%a%_'
GROUP BY p.id, p.name;
```

## 6. Get the list of tasks with duplicate names. Order alphabetically
```sql
SELECT name
FROM tasks
GROUP BY name
HAVING COUNT(*) > 1
ORDER BY name ASC;
```

## 7. Get the list of tasks having several exact matches of both name and status, from the project 'Delivery’. Order by matches count
```sql
SELECT t.name, t.status, COUNT(*) as matches_count
FROM tasks t
JOIN projects p ON t.project_id = p.id
WHERE p.name = 'Delivery'
GROUP BY t.name, t.status
HAVING COUNT(*) > 1
ORDER BY matches_count DESC;
```

## 8. Get the list of project names having more than 10 tasks in status 'completed'. Order by project_id
```sql
SELECT p.name
FROM projects p
JOIN tasks t ON p.id = t.project_id
WHERE t.status = 'completed'
GROUP BY p.id, p.name
HAVING COUNT(t.id) > 10
ORDER BY p.id ASC;
```
