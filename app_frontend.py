import streamlit as st
import requests

# Configurações visuais de nível profissional
st.set_page_config(page_title="Triagem Inteligente - Detecção de Diabetes", page_icon="🩺", layout="centered")

st.title("🩺 Sistema de Triagem Clínica - Predição de Diabetes")
st.markdown("Insira os dados clínicos do paciente para processamento via Inteligência Artificial e análise de marcadores de risco.")
st.divider()

with st.form("formulario_paciente"):
    st.subheader(" Parâmetros Fisiológicos e Clínicos")
    col1, col2 = st.columns(2)
    
    with col1:
        # Alterado: value=None e adicionado placeholder para iniciar limpo
        age = st.number_input("Idade (Anos)", min_value=0, max_value=120, value=None, placeholder="Digite a idade...")
        bmi = st.number_input("IMC (Índice de Massa Corporal)", min_value=0.0, max_value=60.0, value=None, format="%.2f", placeholder="Ex: 24.50", help="Peso / (Altura * Altura)")
        gender = st.selectbox("Gênero Biológico", ["Selecione...", "Feminino", "Masculino"])
        
    with col2:
        # Alterado: value=None e adicionado placeholder para evitar o '0' fixo
        HbA1c = st.number_input("Hemoglobina Glicada - HbA1c (%)", min_value=0.0, max_value=15.0, value=None, format="%.2f", placeholder="Ex: 5.50", help="Valores normais geralmente ficam abaixo de 5.7%")
        glicose = st.number_input("Glicose Plasmática em Jejum (mg/dL)", min_value=0, max_value=300, value=None, placeholder="Ex: 95", help="Valores normais em jejum ficam abaixo de 100 mg/dL")
        
    st.subheader(" Histórico Médico e Estilo de Vida")
    col3, col4 = st.columns(2)
    
    with col3:
        hypertension = st.checkbox("Diagnóstico Prévio de Hipertensão")
        heart_disease = st.checkbox("Histórico de Cardiopatia (Doença Cardíaca)")
    
    with col4:
        tabagismo = st.selectbox("Histórico de Tabagismo", [
            "Selecione...", "Nunca fumou", "Fumante atual", "Ex-fumante", "Parou recentemente", "Não informado"
        ])
    
    st.markdown("<br>", unsafe_allow_html=True)
    submetido = st.form_submit_button(" Executar Análise de Risco")

if submetido:
    # Alterado: A validação agora confere se os campos estão vazios usando 'is None'
    if age is None or bmi is None or HbA1c is None or glicose is None or gender == "Selecione..." or tabagismo == "Selecione...":
        st.warning("⚠️ Erro de Preenchimento: Certifique-se de preencher todos os campos fisiológicos e categóricos antes de submeter.")
    else:
        payload = {
            "age": float(age),
            "hypertension": int(hypertension),
            "heart_disease": int(heart_disease),
            "bmi": float(bmi),
            "HbA1c_level": float(HbA1c),
            "blood_glucose_level": float(glicose),
            "gender_Male": 1 if gender == "Masculino" else 0,
            "smoking_history_current": 1 if tabagismo == "Fumante atual" else 0,
            "smoking_history_ever": 0,
            "smoking_history_former": 1 if tabagismo == "Ex-fumante" else 0,
            "smoking_history_never": 1 if tabagismo == "Nunca fumou" else 0,
            "smoking_history_not_current": 1 if tabagismo == "Parou recentemente" else 0
        }
        
        with st.spinner("Conectando ao modelo preditivo e processando métricas..."):
            try:
                url_api = "http://127.0.0.1:8000/predicao"
                resposta = requests.post(url_api, json=payload)
                
                if resposta.status_code == 200:
                    dados_retorno = resposta.json()
                    status_ia = dados_retorno["status_diabetes"]
                    confianca = dados_retorno["confianca"]
                    
                    st.divider()
                    st.subheader("🩺 Relatório Técnico de Avaliação")
                                        
                    # CASO 1: Alto Risco Crítico (IA positiva OU marcadores de laboratório alterados)
                    if status_ia == "Diabético" or glicose >= 200 or HbA1c >= 6.5:
                        st.error("🚨 **ALERTA CRÍTICO: ALTO RISCO DE DIABETES DETECTADO**")
                        
                        # Justificativa clínica personalizada baseada nos dados inseridos
                        motivos = []
                        if status_ia == "Diabético": motivos.append("Padrão preditivo identificado pelo modelo de Machine Learning")
                        if glicose >= 200: motivos.append(f"Glicose Plasmática severamente elevada ({glicose} mg/dL)")
                        if HbA1c >= 6.5: motivos.append(f"Hemoglobina Glicada em nível de diagnóstico clínico ({HbA1c}%)")
                        
                        st.markdown(f"**Indicadores observados:**")
                        for m in motivos:
                            st.write(f"- {m}")
                            
                        st.markdown("""
                        > **Conduta Recomendada:** Recomenda-se o encaminhamento imediato do paciente para avaliação médica especializada (Endocrinologista/Clínico Geral) para realização de exames confirmatórios (Curva Glicêmica) e início de protocolo terapêutico adequado.
                        """)
                    
                    # CASO 2: Risco Moderado / Zona de Atenção (Pré-Diabetes por marcadores laboratoriais)
                    elif (100 <= glicose < 200) or (5.7 <= HbA1c < 6.5):
                        st.warning("⚠️ **ATENÇÃO: PACIENTE EM ZONA DE RISCO MODERADO (PRÉ-DIABETES)**")
                        st.markdown(f"**Análise dos Marcadores:**")
                        st.write(f"- O modelo preditivo estimou o paciente como clinicamente não-diabético, porém os valores de laboratório fornecidos ({glicose} mg/dL de Glicose e/ou {HbA1c}% de HbA1c) situam-se na zona de tolerância diminuída à glicose.")
                        st.markdown("""
                        > **Conduta Recomendada:** Monitoramento periódico das taxas glicêmicas, intervenção preventiva no estilo de vida (ajuste dietético e atividade física dirigida) e acompanhamento clínico preventivo.
                        """)
                    
                    # CASO 3: Baixo Risco / Padrão Saudável
                    else:
                        st.success("✅ **STATUS: PACIENTE DENTRO DOS PADRÕES DA NORMALIDADE**")
                        st.write(f"- Todas as taxas avaliadas (Glicose: {glicose} mg/dL | HbA1c: {HbA1c}%) encontram-se rigorosamente dentro dos intervalos de referência fisiológica de segurança.")
                        st.markdown("""
                        > **Conduta Recomendada:** Manter hábitos de vida saudáveis e repetir exames de triagem preventivos anualmente ou conforme recomendação por faixa etária.
                        """)
                    
                    # Métricas extras de robustez do modelo no rodapé
                    st.caption(f"Análise estatística gerada com base em Random Forest Classifier. Confiança do algoritmo: {confianca}")
                else:
                    st.error(f"Falha de barramento interno: Resposta inválida da API (Código {resposta.status_code}).")
                    
            except Exception as e:
                st.error("Erro crítico de infraestrutura: O servidor do backend (FastAPI) não respondeu à solicitação de dados.")