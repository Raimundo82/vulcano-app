# Vulcano – PVC and MySQL Database Maintenance Guide

This document describes how to manage persistent directories and how to fully replace the MySQL database running in a separate pod within an OpenShift/Kubernetes cluster.

---

## Storage Structure (PVC)

The application uses two persistent directories mounted via PVC:

- `/app/pdfs` → PVC subPath: `pdfs`
- `/app/processed` → PVC subPath: `processed`

These directories are **not part of the Docker image**.
They reside in a PersistentVolumeClaim (PVC) and are mounted at runtime.

Updating the image **does not modify** their contents.

---

## Replace `/app/processed` Directory Content

### 1. Get application pod name

```bash
kubectl get pods -n dsi-paas
```

Example:
```bash
vulcano-app-747cf86d8c-25mn5
```

---

### 2. Enter the pod

```bash
kubectl exec -it vulcano-app-747cf86d8c-25mn5 -n dsi-paas -- sh
```

---

### 3. Verify mounted directory

```bash
cd /app/processed
```

---

### 4. Clean existing files (optional)

```bash
rm -rf /app/processed/*
```

---

### 5. Copy new files (correct approach)

To avoid creating `/app/processed/processed`, copy the **contents** of the folder:

```bash
oc cp /c/Users/m22600/Downloads/processed/processed/. dsi-paas/vulcano-app-747cf86d8c-25mn5:/app/processed/
```

The trailing `.` means “copy everything inside the directory”.

---

### 6. Remove duplicated folder (if exists)

```bash
oc exec -n dsi-paas vulcano-app-747cf86d8c-25mn5 -- rm -rf /app/processed/processed
```

---

### 7. Verify

```bash
oc exec -it vulcano-app-747cf86d8c-25mn5 -n dsi-paas -- ls -l /app/processed
```

---

## Replace MySQL Database (separate pod)

Database pod:

```bash
vulcano-db-64455bcb8f-p2vln
```

Credentials (from Secret):

- root password: vulcano_password
- user: vulcano
- password: vulcano_password
- database: vulcano

---

### 1. Copy dump to database pod

```bash
oc cp /c/Users/m22600/Downloads/dump.sql dsi-paas/vulcano-db-64455bcb8f-p2vln:/tmp/dump.sql
```

---

### 2. Enter database pod

```bash
oc exec -it vulcano-db-64455bcb8f-p2vln -n dsi-paas -- sh
```

---

### 3. Drop and recreate database (full replacement)

```bash
mysql -u root -pvulcano_password -e "DROP DATABASE vulcano; CREATE DATABASE vulcano;"
```

---

### 4. Import dump

```bash
mysql -u root -pvulcano_password vulcano < /tmp/dump.sql
```

---

### 5. Verify

```bash
mysql -u root -pvulcano_password -e "SHOW TABLES IN vulcano;"
```

---

## Restart Application Pod (optional)

If the application caches data:

```bash
oc delete pod vulcano-app-747cf86d8c-25mn5 -n dsi-paas
```

The Deployment will recreate it automatically.

---

## Notes

- PVC data persists even if pods are deleted
- Image updates do not affect PVC data
- Use an initContainer for automated cleanup if needed
- Use root user for full database replacement

---
