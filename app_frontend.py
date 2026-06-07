import streamlit as st
import requests






# Controle de página
if "pagina" not in st.session_state:
    st.session_state.pagina = "home"




# ==================================================
# PÁGINA INICIAL
# ==================================================
if st.session_state.pagina == "home":


    st.markdown("<h1 style='text-align: center;'>🩺 GlycoAI</h1>", unsafe_allow_html=True)


    st.markdown(
        "<h3 style='text-align: center;'>"
        "Inteligência Artificial aplicada ao monitoramento glicêmico"
        "</h3>",
        unsafe_allow_html=True
    )


    st.write("")
    st.write("")


    st.markdown("""
    O **GlycoAI** é uma aplicação desenvolvida para auxiliar na análise
    de indicadores relacionados ao diabetes, utilizando Inteligência Artificial
    para apoiar interpretações clínicas de glicose e HbA1c.


    ### Funcionalidades:
    - Inserção de dados clínicos
    - Análise automatizada
    - Classificação de risco
    - Apoio visual para interpretação de resultados


    ⚠️ Este sistema não substitui avaliação médica profissional.
    """)


    st.write("")


    col1, col2, col3 = st.columns([1,1,1])


    with col2:
        if st.button("🚀 Iniciar aplicação", use_container_width=True):
            st.session_state.pagina = "app"
            st.rerun()




# ==================================================
# APLICAÇÃO PRINCIPAL
# ==================================================
elif st.session_state.pagina == "app":


    #






# =====================================================
# CONFIGURAÇÃO DA PÁGINA
# =====================================================


    st.set_page_config(
        page_title="Triagem Inteligente - Detecção de Diabetes",
        page_icon="🩺",
        layout="centered",
        initial_sidebar_state="collapsed"
    )


    # =====================================================
    # MENU IDIOMA
    # =====================================================


    st.sidebar.title("🌎 Language / Idioma")


    idioma = st.sidebar.selectbox(
        "",
        ["🇧🇷 Português", "🇺🇸 English"]
    )


    # =====================================================
    # TEXTOS DINÂMICOS
    # =====================================================


    if idioma == "🇧🇷 Português":


        titulo = "🩺 Sistema de Triagem Clínica - Predição de Diabetes"


        descricao = """
        Esta aplicação utiliza Inteligência Artificial e aprendizado de máquina
        para analisar indicadores clínicos associados ao diabetes.


        Com base nas informações fornecidas, o modelo preditivo realiza uma
        avaliação probabilística para auxiliar na identificação de possíveis casos.


        ⚠️ Este sistema não substitui diagnóstico médico profissional.
        """


        sub1 = "Parâmetros Fisiológicos e Clínicos"
        sub2 = "Histórico Médico e Estilo de Vida"


        idade_txt = "Idade (Anos)"
        bmi_txt = "IMC (Índice de Massa Corporal)"
        genero_txt = "Gênero Biológico"


        hba1c_txt = "Hemoglobina Glicada - HbA1c (%)"
        glicose_txt = "Glicose Plasmática em Jejum (mg/dL)"


        hipertensao_txt = "Diagnóstico Prévio de Hipertensão"
        cardiaco_txt = "Histórico de Cardiopatia (Doença Cardíaca)"
        tabagismo_txt = "Histórico de Tabagismo"


        botao_txt = "Executar Análise de Risco"


        erro_preenchimento = (
            "⚠️ Certifique-se de preencher todos os campos antes de continuar."
        )


        spinner_txt = (
            "Conectando ao modelo preditivo e processando métricas..."
        )


        genero_opts = [
            "Selecione...",
            "Feminino",
            "Masculino"
        ]


        tabaco_opts = [
            "Selecione...",
            "Nunca fumou",
            "Fumante atual",
            "Ex-fumante",
            "Parou recentemente",
            "Não informado"
        ]


    else:


        titulo = "🩺 Clinical Screening System - Diabetes Prediction"


        descricao = """
        This application uses Artificial Intelligence and Machine Learning
        to analyze clinical indicators associated with diabetes.


        Based on the provided information, the predictive model performs a
        probabilistic assessment to assist in identifying possible cases.


        ⚠️ This system does not replace professional medical diagnosis.
        """


        sub1 = "Physiological and Clinical Parameters"
        sub2 = "Medical History and Lifestyle"


        idade_txt = "Age (Years)"
        bmi_txt = "BMI (Body Mass Index)"
        genero_txt = "Biological Gender"


        hba1c_txt = "HbA1c (%)"
        glicose_txt = "Fasting Blood Glucose (mg/dL)"


        hipertensao_txt = "Previous Hypertension Diagnosis"
        cardiaco_txt = "History of Heart Disease"
        tabagismo_txt = "Smoking History"


        botao_txt = "Run Risk Analysis"


        erro_preenchimento = (
            "⚠️ Please complete all fields before continuing."
        )


        spinner_txt = (
            "Connecting to predictive model and processing metrics..."
        )


        genero_opts = [
            "Select...",
            "Female",
            "Male"
        ]


        tabaco_opts = [
            "Select...",
            "Never smoked",
            "Current smoker",
            "Former smoker",
            "Recently quit",
            "Not informed"
        ]


    # =====================================================
    # CABEÇALHO
    # =====================================================


    st.title(titulo)


    st.markdown(descricao)


    st.divider()


    # =====================================================
    # FORMULÁRIO
    # =====================================================


    with st.form("formulario_paciente"):


        st.subheader(sub1)


        col1, col2 = st.columns(2)


        with col1:


            age = st.number_input(
                idade_txt,
                min_value=0,
                max_value=120,
                value=None,
                placeholder="Ex: 45" if idioma == "🇧🇷 Português" else "Ex: 45"
            )


            bmi = st.number_input(
                bmi_txt,
                min_value=10.0,
                max_value=60.0,
                value=None,
                format="%.2f",
                placeholder="Ex: 27.50"
            )


            gender = st.selectbox(
                genero_txt,
                genero_opts
            )


        with col2:


            HbA1c = st.number_input(
                hba1c_txt,
                min_value=0.0,
                max_value=15.0,
                value=None,
                format="%.2f",
                placeholder="Ex: 5.70"
            )


            glicose = st.number_input(
                glicose_txt,
                min_value=0,
                max_value=700,
                value=None,
                placeholder="Ex: 95"
            )


        st.subheader(sub2)


        col3, col4 = st.columns(2)


        with col3:


            hypertension = st.checkbox(
                hipertensao_txt
            )


            heart_disease = st.checkbox(
                cardiaco_txt
            )


        with col4:


            tabagismo = st.selectbox(
                tabagismo_txt,
                tabaco_opts
            )


        st.markdown("<br>", unsafe_allow_html=True)


        submetido = st.form_submit_button(
            botao_txt
        )


    # =====================================================
    # PROCESSAMENTO
    # =====================================================


    if submetido:


        if (
            age is None or
            bmi is None or
            HbA1c is None or
            glicose is None or
            gender in ["Selecione...", "Select..."] or
            tabagismo in ["Selecione...", "Select..."]
        ):


            st.warning(erro_preenchimento)


        else:


            payload = {


                "age": float(age),


                "hypertension": int(hypertension),


                "heart_disease": int(heart_disease),


                "bmi": float(bmi),


                "HbA1c_level": float(HbA1c),


                "blood_glucose_level": float(glicose),


                "gender_Male": (
                    1 if gender in ["Masculino", "Male"]
                    else 0
                ),


                "smoking_history_current": (
                    1 if tabagismo in [
                        "Fumante atual",
                        "Current smoker"
                    ]
                    else 0
                ),


                "smoking_history_ever": 0,


                "smoking_history_former": (
                    1 if tabagismo in [
                        "Ex-fumante",
                        "Former smoker"
                    ]
                    else 0
                ),


                "smoking_history_never": (
                    1 if tabagismo in [
                        "Nunca fumou",
                        "Never smoked"
                    ]
                    else 0
                ),


                "smoking_history_not_current": (
                    1 if tabagismo in [
                        "Parou recentemente",
                        "Recently quit"
                    ]
                    else 0
                )
            }


            with st.spinner(spinner_txt):


                try:


                    resposta = requests.post(
                        "http://127.0.0.1:8000/predicao",
                        json=payload
                    )


                    if resposta.status_code == 200:


                        dados = resposta.json()


                        status_ia = dados["status_diabetes"]


                        confianca = dados["confianca"]


                        # =================================================
                        # FATORES DE RISCO
                        # =================================================


                        fatores_risco = []


                        if bmi >= 25:


                            if idioma == "🇧🇷 Português":


                                fatores_risco.append(
                                    "⚠️ Sobrepeso/obesidade é um fator de risco importante para desenvolvimento de Diabetes Tipo 2."
                                )


                            else:


                                fatores_risco.append(
                                    "⚠️ Excess weight/obesity is an important risk factor for Type 2 Diabetes."
                                )


                        if hypertension:


                            if idioma == "🇧🇷 Português":


                                fatores_risco.append(
                                    "⚠️ Hipertensão arterial está associada à resistência insulínica e síndrome metabólica."
                                )


                            else:


                                fatores_risco.append(
                                    "⚠️ Hypertension is associated with insulin resistance and metabolic syndrome."
                                )


                        if heart_disease:


                            if idioma == "🇧🇷 Português":


                                fatores_risco.append(
                                    "⚠️ Histórico cardiovascular aumenta riscos metabólicos futuros."
                                )


                            else:


                                fatores_risco.append(
                                    "⚠️ Cardiovascular history increases future metabolic risks."
                                )


                        # Somente fumante atual e parou recentemente


                        if tabagismo in [
                            "Fumante atual",
                            "Parou recentemente",
                            "Current smoker",
                            "Recently quit"
                        ]:


                            if idioma == "🇧🇷 Português":


                                fatores_risco.append(
                                    "⚠️ O tabagismo está associado ao aumento do risco cardiovascular e metabólico."
                                )


                            else:


                                fatores_risco.append(
                                    "⚠️ Smoking is associated with increased cardiovascular and metabolic risk."
                                )


                        # =================================================
                        # RELATÓRIO
                        # =================================================


                        st.divider()


                        if idioma == "🇧🇷 Português":
                            st.subheader("🩺 Relatório Técnico de Avaliação")
                        else:
                            st.subheader("🩺 Technical Assessment Report")


                        # =================================================
                        # CRÍTICO
                        # =================================================


                        if (
                            status_ia == "Diabético" or
                            glicose >= 126 or
                            HbA1c >= 6.5
                        ):


                            if idioma == "🇧🇷 Português":


                                st.error(
                                    "🚨 ALERTA CRÍTICO: ALTO RISCO DE DIABETES DETECTADO"
                                )


                                st.write(
                                    f"- Glicose informada: {glicose} mg/dL"
                                )


                                st.write(
                                    f"- HbA1c informado: {HbA1c}%"
                                )


                                st.markdown("""
                                > **Conduta Recomendada:** Encaminhamento médico especializado e exames confirmatórios.
                                """)


                            else:


                                st.error(
                                    "🚨 CRITICAL ALERT: HIGH DIABETES RISK DETECTED"
                                )


                                st.write(
                                    f"- Reported glucose: {glicose} mg/dL"
                                )


                                st.write(
                                    f"- Reported HbA1c: {HbA1c}%"
                                )


                                st.markdown("""
                                > **Recommended Action:** Specialized medical evaluation and confirmatory testing are recommended.
                                """)


                        # =================================================
                        # MODERADO
                        # =================================================


                        elif (
                            (100 <= glicose < 126) or
                            (5.7 <= HbA1c < 6.5)
                        ):


                            if idioma == "🇧🇷 Português":


                                st.warning(
                                    "⚠️ PACIENTE EM ZONA DE RISCO MODERADO (PRÉ-DIABETES)"
                                )


                                st.write(
                                    f"- Glicose informada: {glicose} mg/dL"
                                )


                                st.write(
                                    f"- HbA1c informado: {HbA1c}%"
                                )


                                st.markdown("""
                                > **Conduta Recomendada:** Monitoramento periódico e intervenção preventiva no estilo de vida.
                                """)


                            else:


                                st.warning(
                                    "⚠️ PATIENT IN MODERATE RISK ZONE (PRE-DIABETES)"
                                )


                                st.write(
                                    f"- Reported glucose: {glicose} mg/dL"
                                )


                                st.write(
                                    f"- Reported HbA1c: {HbA1c}%"
                                )


                                st.markdown("""
                                > **Recommended Action:** Periodic monitoring and preventive lifestyle intervention.
                                """)


                        # =================================================
                        # NORMAL
                        # =================================================


                        else:


                            if idioma == "🇧🇷 Português":


                                st.success(
                                    "✅ STATUS: PACIENTE DENTRO DOS PADRÕES DA NORMALIDADE"
                                )


                                st.write(
                                    f"- Todas as taxas avaliadas (Glicose: {glicose} mg/dL | HbA1c: {HbA1c}%) encontram-se dentro dos valores fisiológicos de referência."
                                )


                                st.markdown("""
                                > **Conduta Recomendada:** Manter hábitos saudáveis e acompanhamento preventivo periódico.
                                """)


                            else:


                                st.success(
                                    "✅ STATUS: PATIENT WITHIN NORMAL PARAMETERS"
                                )


                                st.write(
                                    f"- All evaluated markers (Glucose: {glicose} mg/dL | HbA1c: {HbA1c}%) are within reference values."
                                )


                                st.markdown("""
                                > **Recommended Action:** Maintain healthy lifestyle habits and periodic preventive monitoring.
                                """)


                        # =================================================
                        # ALERTAS COMPLEMENTARES
                        # =================================================


                        if fatores_risco:


                            if idioma == "🇧🇷 Português":


                                st.info(
                                    "🧬 Fatores de risco complementares identificados:"
                                )


                            else:


                                st.info(
                                    "🧬 Additional risk factors identified:"
                                )


                            for risco in fatores_risco:


                                st.write(f"- {risco}")


                        # =================================================
                        # CONFIANÇA
                        # =================================================


                        if idioma == "🇧🇷 Português":


                            st.caption(
                                f"Análise estatística baseada em Random Forest Classifier. Confiança do algoritmo: {confianca}"
                            )


                        else:


                            st.caption(
                                f"Statistical analysis generated using Random Forest Classifier. Model confidence: {confianca}"
                            )


                    else:


                        st.error(
                            f"Erro interno da API ({resposta.status_code})"
                        )


                except Exception:


                    if idioma == "🇧🇷 Português":


                        st.error(
                            "Erro crítico: backend FastAPI indisponível."
                        )


                    else:


                        st.error(
                            "Critical error: FastAPI backend unavailable."
                        )

