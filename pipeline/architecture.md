# Pipeline n8n — Zayfy Growth Engine (Fase 2)

## Flujo de 4 fases

```
[Apify] → Scraping hashtags
    ↓
[Claude Haiku] → Calificación (score 1-10, JSON)
    ↓ (score ≥ 7)
[Claude Sonnet] → Generación de DM personalizado
    ↓
[WhatsApp Business] → Aprobación humana ("SÍ" / "NO")
    ↓ (SÍ)
[Buffer] → Publicación programada
    ↓
[Google Sheets] → Log de leads + métricas
```

## Hashtags monitoreados

```
#tiendaonline #vendoporinsta #negocioscolombia
#venderportiktok #emprendimientocol #negociodigital
#microempresa #emprendedora
```

## Criterio de calificación (Haiku)

Micronegocio colombiano/latinoamericano con señales de:
- Venta online activa (menciona productos, precios, envíos)
- Sin herramientas propias (usa solo WhatsApp o DMs)
- Perfil activo (publicaciones recientes)
- NO agencias, NO revendedores de otros servicios tech

## Costo estimado por semana

| Tarea | Modelo | Volumen | Costo |
|---|---|---|---|
| Calificación de leads | Haiku | ~40 perfiles | ~USD 0.08 |
| Generación de DMs | Sonnet | ~10 mensajes | ~USD 0.30 |
| Generación de posts | Sonnet | ~3 posts | ~USD 0.12 |
| **Total** | | | **~USD 0.50** |

## Observabilidad

- **Métricas de negocio:** leads calificados/semana, score promedio, tasa de aprobación, conversión a cliente
- **Métricas operativas:** latencia por nodo n8n, tasa de error por API externa
- **Alertas:** 0 resultados Apify → WhatsApp; JSON inválido Claude → log + reintento; fallo Buffer → email
- **Log:** Google Sheets al final de cada ciclo (un registro por lead)
