"""
Zayfy Growth Engine — Pipeline de leads con Claude API
AI-Driven DevOps Accelerator (SoftServe, nov 2026)

Demuestra:
- Uso de Claude Haiku para calificación (tarea simple, costo bajo)
- Uso de Claude Sonnet para generación de outreach (tarea creativa)
- Separación de modelos por tarea (patrón del curso: Rápido vs. Razonamiento)

Requisito: pip install anthropic
Uso: python lead_pipeline.py
     python lead_pipeline.py --demo  (corre sin API key, con respuesta simulada)
"""

import json
import argparse
import os
import sys

# Fix Unicode en Windows
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")

# ── Datos de prueba (leads simulados de Instagram) ──────────────────────────
SAMPLE_LEADS = [
    {
        "handle": "@belleza_cali_oficial",
        "bio": "✂️ Salón de belleza en Cali | Cortes, tintes, uñas 💅 | Pide tu cita por WhatsApp",
        "recent_posts": "Resultados de tinte balayage | Promoción noviembre: manicure + pedicure $45k | Escríbenos al DM para agendar",
        "followers": 1240,
        "location": "Cali, Colombia"
    },
    {
        "handle": "@modas_valentina_mde",
        "bio": "👗 Ropa femenina al por mayor y detal | Envíos a toda Colombia 🇨🇴 | DM para catálogo",
        "recent_posts": "Nueva colección invierno 🧥 | Leggins desde $28k | ¿Quieres ser revendedora? escríbeme",
        "followers": 3800,
        "location": "Medellín, Colombia"
    },
    {
        "handle": "@agencia_digital_xyz",
        "bio": "🚀 Agencia de marketing digital | Community management | Pauta en Meta y Google",
        "recent_posts": "Casos de éxito: aumentamos ventas 200% | Contáctanos para tu estrategia digital",
        "followers": 12000,
        "location": "Bogotá, Colombia"
    }
]

# ── Prompts ──────────────────────────────────────────────────────────────────
QUALIFICATION_PROMPT = """Eres un asistente de ventas para Zayfy, empresa tech de Medellín que ayuda a micronegocios a vender online.

Evalúa si esta cuenta es un cliente potencial ideal. Devuelve SOLO JSON válido, sin texto adicional.

Cuenta:
- Handle: {handle}
- Bio: {bio}
- Posts recientes: {recent_posts}
- Seguidores: {followers}
- Ubicación: {location}

Criterios:
- ¿Vende productos/servicios online (menciona precios, envíos, pedidos)?
- ¿Usa solo WhatsApp o DMs para vender (sin tienda propia)?
- ¿Es un micronegocio real (NO agencia, NO revendedor tech)?
- ¿Está en Colombia o Latinoamérica?
- ¿Tiene actividad reciente?

Formato exacto de respuesta:
{{"score": 8, "es_potencial": true, "razon": "...", "nicho": "...", "señales_positivas": ["..."], "señales_negativas": ["..."]}}

Escala: 9-10 caliente, 7-8 tibio, 5-6 posible, 1-4 no aplica. Solo score >= 7 es potencial."""

OUTREACH_PROMPT = """Eres el asistente de ventas de Zayfy (empresa tech de Medellín). Escribes DMs para Instagram que abren conversación con micronegocios.

Restricciones absolutas:
- Nunca prometas ventas, alcance ni resultados específicos
- Máximo 3 líneas, tono cálido y directo
- Siempre termina con una pregunta

Lead:
- Handle: {handle}
- Nicho: {nicho}
- Señales: {senales}
- Por qué es potencial: {razon}

Devuelve SOLO JSON:
{{"dm": "mensaje aquí", "variacion": "alternativa aquí"}}"""


def qualify_lead(client, lead: dict, demo: bool = False) -> dict:
    """Califica un lead con Claude Haiku (modelo rápido, tarea simple)."""
    if demo:
        # Respuesta simulada para demo sin API key
        demos = {
            "@belleza_cali_oficial": {"score": 9, "es_potencial": True, "razon": "Salón activo en Cali, agenda por WhatsApp sin tienda propia", "nicho": "belleza", "señales_positivas": ["citas por WhatsApp", "precios en posts", "ubicación Colombia"], "señales_negativas": []},
            "@modas_valentina_mde": {"score": 8, "es_potencial": True, "razon": "Venta de ropa con envíos, catálogo por DM, sin tienda propia", "nicho": "moda", "señales_positivas": ["envíos Colombia", "catálogo por DM", "precios visibles"], "señales_negativas": []},
            "@agencia_digital_xyz": {"score": 2, "es_potencial": False, "razon": "Es una agencia de marketing, no un micronegocio con necesidad de tienda", "nicho": "agencia", "señales_positivas": [], "señales_negativas": ["es agencia", "ya tiene herramientas digitales", "muchos seguidores"]},
        }
        return demos.get(lead["handle"], {"score": 5, "es_potencial": False, "razon": "No hay suficiente información", "nicho": "desconocido", "señales_positivas": [], "señales_negativas": []})

    prompt = QUALIFICATION_PROMPT.format(**lead)
    response = client.messages.create(
        model="claude-haiku-4-5",        # Modelo rápido y económico para clasificación
        max_tokens=256,
        messages=[{"role": "user", "content": prompt}]
    )
    return json.loads(response.content[0].text)


def generate_outreach(client, lead: dict, qualification: dict, demo: bool = False) -> dict:
    """Genera el DM de outreach con Claude Sonnet (modelo de razonamiento, tarea creativa)."""
    if demo:
        dms = {
            "belleza": {"dm": f"Hola {lead['handle']} 👋 Vi que agendas citas por WhatsApp — ¿has pensado en tener tu propio link con catálogo de servicios para que tus clientes vean precios y pidan solos? En Zayfy lo armamos en 3 días. ¿Te gustaría ver cómo quedaría para tu salón?", "variacion": f"Hola {lead['handle']}! Sigo tu trabajo y me encanta 💅 Noto que gestionas todo por WhatsApp — ¿cuánto tiempo te toma responder mensajes de citas al día?"},
            "moda": {"dm": f"Hola {lead['handle']} 👋 Tu colección se ve increíble — ¿sabías que puedes tener un catálogo con carrito de compras donde tus clientas pidan solas sin que tengas que responder cada DM? En Zayfy lo configuramos con tus productos. ¿Quieres ver un ejemplo?", "variacion": f"Hola {lead['handle']}! Vi que envías a toda Colombia 🇨🇴 ¿Cuántos pedidos manejas a la semana por DM? Pregunto porque tenemos algo que podría ahorrarte horas."},
        }
        return dms.get(qualification.get("nicho", ""), {"dm": f"Hola {lead['handle']} 👋 Vi tu negocio y creo que podríamos ayudarte a vender más fácil online. ¿Tienes 5 min para contarme cómo gestionas tus pedidos ahora?", "variacion": "alternativa"})

    prompt = OUTREACH_PROMPT.format(
        handle=lead["handle"],
        nicho=qualification["nicho"],
        senales=", ".join(qualification.get("señales_positivas", [])),
        razon=qualification["razon"]
    )
    response = client.messages.create(
        model="claude-sonnet-4-5",       # Modelo de razonamiento para generación creativa
        max_tokens=512,
        messages=[{"role": "user", "content": prompt}]
    )
    return json.loads(response.content[0].text)


def run_pipeline(demo: bool = False):
    """Corre el pipeline completo: calificación → outreach para leads con score >= 7."""
    client = None
    if not demo:
        try:
            import anthropic
            api_key = os.environ.get("ANTHROPIC_API_KEY")
            if not api_key:
                print("⚠️  ANTHROPIC_API_KEY no encontrada. Usando --demo.")
                demo = True
            else:
                client = anthropic.Anthropic(api_key=api_key)
        except ImportError:
            print("⚠️  anthropic no instalado. Ejecuta: pip install anthropic")
            print("     Usando modo demo.\n")
            demo = True

    print("=" * 60)
    print("🚀 ZAYFY GROWTH ENGINE — Pipeline de Leads")
    print(f"   Modo: {'DEMO (simulado)' if demo else 'REAL (Claude API)'}")
    print("=" * 60)

    aprobados = []

    for lead in SAMPLE_LEADS:
        print(f"\n📋 Analizando: {lead['handle']}")
        print(f"   Bio: {lead['bio'][:60]}...")

        # Fase 1: Calificación con Haiku
        print(f"   → Calificando con {'Haiku (simulado)' if demo else 'Claude Haiku'}...")
        qualification = qualify_lead(client, lead, demo)

        score = qualification["score"]
        icono = "🔥" if score >= 9 else "👍" if score >= 7 else "❌"
        print(f"   {icono} Score: {score}/10 — {qualification['razon']}")

        if not qualification["es_potencial"]:
            print(f"   ⏭️  Descartado (score < 7)")
            continue

        # Fase 2: Generación de outreach con Sonnet
        print(f"   → Generando DM con {'Sonnet (simulado)' if demo else 'Claude Sonnet'}...")
        outreach = generate_outreach(client, lead, qualification, demo)

        aprobados.append({
            "lead": lead,
            "qualification": qualification,
            "outreach": outreach
        })

        print(f"\n   ✉️  DM propuesto:")
        print(f"   \"{outreach['dm']}\"")
        print(f"\n   📌 Variación:")
        print(f"   \"{outreach['variacion']}\"")
        print(f"\n   ⚠️  REQUIERE APROBACIÓN humana antes de enviar.")

    print("\n" + "=" * 60)
    print(f"✅ Resumen: {len(aprobados)}/{len(SAMPLE_LEADS)} leads calificados")
    if aprobados:
        nichos = [a["qualification"]["nicho"] for a in aprobados]
        print(f"   Nichos: {', '.join(nichos)}")
    print("=" * 60)

    # Guardar resultados en JSON
    output_path = os.path.join(os.path.dirname(__file__), "pipeline_results.json")
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(aprobados, f, ensure_ascii=False, indent=2)
    print(f"\n💾 Resultados guardados en: pipeline_results.json")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Zayfy Growth Engine — Pipeline de leads")
    parser.add_argument("--demo", action="store_true", help="Corre sin API key con respuestas simuladas")
    args = parser.parse_args()
    run_pipeline(demo=args.demo)
