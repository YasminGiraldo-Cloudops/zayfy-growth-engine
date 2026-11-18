# Zayfy Growth Engine

Proyecto integrador del programa **AI-Driven DevOps Accelerator** (SoftServe, sept–nov 2026).

**Participante:** Yasmín Giraldo — Co-fundadora Zayfy · DevOps & Cloud (AWS)  
**Ruta:** B — Problema propio  
**Curso:** Modern DevOps, Built With AI

---

## Problema

Zayfy necesita encontrar clientes potenciales y producir contenido para redes sociales sin que eso consuma el tiempo de las dos fundadoras que también hacen el trabajo técnico.

## Solución: 3 fases

### Fase 1 — Content Studio ✅ (nov 2026)
Herramienta web que genera posts listos para publicar en Instagram, TikTok y LinkedIn, adaptados a los 4 servicios de Zayfy y al Paquete Emprendedor.

- **Archivo:** [`content-studio.html`](content-studio.html)
- **Resultado:** De 30 min a 2 min por post. Sin costo de API (templates locales).

### Fase 2 — Pipeline n8n de leads (dic 2026)
Pipeline automatizado que monitorea hashtags en IG/TikTok, califica leads con Claude API y genera mensajes de outreach personalizados, con aprobación humana antes de enviar.

- **Arquitectura:** [`pipeline/architecture.md`](pipeline/architecture.md)
- **Prompts:** [`pipeline/prompts/`](pipeline/prompts/)

### Fase 3 — Publicación semi-automática (ene 2027)
n8n genera según calendario editorial → humano aprueba → Buffer publica.

---

## Stack

| Herramienta | Uso |
|---|---|
| Claude Code (Sonnet) | Harness de desarrollo |
| Claude API (Haiku) | Calificación de leads |
| Claude API (Sonnet) | Generación de outreach y contenido |
| n8n | Orquestación del pipeline |
| Apify | Scraping de hashtags IG/TikTok |
| Buffer / Later | Publicación programada |
| AWS (ECS, RDS, CloudFront) | Infraestructura |
| GitHub Actions | CI/CD |

---

## Bitácora del curso

[`bitacora-devops-zayfy.html`](bitacora-devops-zayfy.html) — Semanas 1–8 + Consolidado con evidencia del proceso.

---

## Niveles agénticos aplicados

- **Fase 1:** L2 Active Partnership (IA genera, humano aprueba y publica)
- **Fase 2:** L3 Human Oversight (IA ejecuta el ciclo, humano aprueba resultados clave)
- **Fase 3:** L3 → L4 (publicación autónoma con calendario editorial aprobado previamente)
