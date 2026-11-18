# Zayfy Growth Engine

Proyecto integrador del programa **AI-Driven DevOps Accelerator** (SoftServe, sept–nov 2026).

**Participante:** Yasmín Giraldo — Co-fundadora Zayfy · DevOps & Cloud (AWS)  
**Ruta:** B — Problema propio



---

## Problema

Zayfy necesita encontrar clientes potenciales y producir contenido para redes sociales sin que eso consuma el tiempo de las dos fundadoras que también hacen el trabajo técnico.

## Solución: 3 fases

### Fase 1 — Content Studio  (nov 2026)
Herramienta web que genera posts listos para publicar en Instagram, TikTok y LinkedIn, adaptados a los 4 servicios de Zayfy y al Paquete Emprendedor.

- **Archivo:** [`content-studio.html`](content-studio.html)
- **Resultado:** De 30 min a 2 min por post. Sin costo de API (templates locales).

### Fase 2 — Pipeline Python + CI/CD  (nov 2026)
Pipeline ejecutable en Python que califica leads con Claude Haiku (patrón ReAct) y genera mensajes de outreach personalizados con Claude Sonnet. CI/CD con GitHub Actions: 2 jobs (demo + real), 6 tests unitarios con pytest.

- **Pipeline:** [`pipeline/lead_pipeline.py`](pipeline/lead_pipeline.py)
- **Tests:** [`pipeline/tests/test_pipeline.py`](pipeline/tests/test_pipeline.py)
- **CI:** `.github/workflows/pipeline-demo.yml` —  verde

### Fase 3 — Pipeline n8n completo (dic 2026)
Pipeline automatizado que monitorea hashtags en IG/TikTok, califica leads con Claude API y genera mensajes de outreach personalizados, con aprobación humana antes de enviar.

- **Arquitectura diseñada:** [`pipeline/architecture.md`](pipeline/architecture.md)
- **Prompts:** [`pipeline/prompts/`](pipeline/prompts/)

---

## Stack

| Herramienta | Uso |
|---|---|
| Claude Code (Sonnet) | Harness de desarrollo |
| Python + pytest | Pipeline de leads + tests unitarios |
| GitHub Actions | CI/CD (demo + real) |
| Claude API (Haiku) | Calificación de leads |
| Claude API (Sonnet) | Generación de outreach y contenido |
| n8n | Orquestación del pipeline (Fase 3) |
| Apify | Scraping de hashtags IG/TikTok (Fase 3) |
| Buffer / Later | Publicación programada (Fase 3) |
| AWS (ECS, RDS, CloudFront) | Infraestructura |

---

## Niveles agénticos aplicados

- **Fase 1:** L2 Active Partnership (IA genera, humano aprueba y publica)
- **Fase 2:** L3 Human Oversight (IA ejecuta el ciclo, humano aprueba resultados clave)
- **Fase 3:** L3 → L4 (publicación autónoma con calendario editorial aprobado previamente)
