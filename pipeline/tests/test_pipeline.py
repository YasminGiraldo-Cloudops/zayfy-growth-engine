"""
Tests unitarios del pipeline de leads.
Generados con ayuda de Claude Code — AI-Driven DevOps Accelerator, Semana 2.
Correr con: python -m pytest pipeline/tests/ -v
"""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from lead_pipeline import qualify_lead, generate_outreach, SAMPLE_LEADS


class TestQualifyLeadDemo:
    def test_salon_belleza_es_potencial(self):
        lead = SAMPLE_LEADS[0]  # @belleza_cali_oficial
        result = qualify_lead(None, lead, demo=True)
        assert result["es_potencial"] is True
        assert result["score"] >= 7

    def test_agencia_digital_es_descartada(self):
        lead = SAMPLE_LEADS[2]  # @agencia_digital_xyz
        result = qualify_lead(None, lead, demo=True)
        assert result["es_potencial"] is False
        assert result["score"] < 7

    def test_respuesta_tiene_campos_requeridos(self):
        lead = SAMPLE_LEADS[0]
        result = qualify_lead(None, lead, demo=True)
        required = ["score", "es_potencial", "razon", "nicho",
                    "señales_positivas", "señales_negativas"]
        for field in required:
            assert field in result, f"Falta campo requerido: {field}"

    def test_score_en_rango_valido(self):
        for lead in SAMPLE_LEADS:
            result = qualify_lead(None, lead, demo=True)
            assert 1 <= result["score"] <= 10, \
                f"Score fuera de rango para {lead['handle']}: {result['score']}"


class TestGenerateOutreachDemo:
    def test_dm_generado_para_lead_calificado(self):
        lead = SAMPLE_LEADS[0]  # @belleza_cali_oficial, nicho belleza
        qualification = {
            "score": 9, "es_potencial": True, "nicho": "belleza",
            "razon": "Agenda por WhatsApp sin tienda propia",
            "señales_positivas": ["citas por WhatsApp"],
            "señales_negativas": []
        }
        result = generate_outreach(None, lead, qualification, demo=True)
        assert "dm" in result
        assert len(result["dm"]) > 20

    def test_dm_no_usa_palabras_prohibidas(self):
        lead = SAMPLE_LEADS[0]
        qualification = {
            "score": 9, "es_potencial": True, "nicho": "belleza",
            "razon": "test", "señales_positivas": [], "señales_negativas": []
        }
        result = generate_outreach(None, lead, qualification, demo=True)
        dm_lower = result["dm"].lower()
        for palabra in ["precio de lanzamiento", "primeros clientes", "garantizamos"]:
            assert palabra not in dm_lower, f"DM usa palabra prohibida: '{palabra}'"
