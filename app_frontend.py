import streamlit as st
import requests

st.set_page_config(page_title="Detector de Diabetes IA", page_icon="🩺", layout="centered")

st.title("🩺 Sistema Inteligente de Detecção de Diabetes")
st.markdown("Insira os dados clínicos do paciente abaixo para obter a análise do modelo preditivo.")
st.divider()

with st.form("formulario_paciente"):
    st.subheader("Dados do Paciente")
    col1, col2 = st.columns(2)
    
    with col1:
        age = st.number_input("Idade", min_value=0, max_value=120, value=40)
        bmi = st.number_input("IMC (Índice de Massa Corporal)", min_value=10.0, max_value=60.0, value=25.0)
        gender = st.selectbox("Gênero", ["Feminino", "Masculino"])
        
    with col2:
        HbA1c = st.number_input("Nível de HbA1c", min_value=3.0, max_value=15.0, value=5.5)
        glicose = st.number_input("Nível de Glicose no Sangue", min_value=50, max_value=300, value=100)
        
    st.subheader("Histórico Médico e Hábitos")
    col3, col4 = st.columns(2)
    
    with col3:
        hypertension = st.checkbox("Paciente tem Hipertensão?")
        heart_disease = st.checkbox("Paciente tem Histórico de Doença Cardíaca?")
    
    with col4:
        # Opções mapeadas exatamente com as strings em inglês da base de dados original
        tabagismo = st.selectbox("Histórico de Tabagismo", [
            "Nunca fumou", 
            "Fumante atual", 
            "Ex-fumante", 
            "Parou recentemente", 
            "Não informado"
        ])
    
    submetido = st.form_submit_button("Analisar Paciente")

if submetido:
    # Correção do mapeamento: Traduzindo a escolha do usuário para o padrão de coluna gerado pelo get_dummies
    payload = {
        "age": float(age),
        "hypertension": int(hypertension),
        "heart_disease": int(heart_disease),
        "bmi": float(bmi),
        "HbA1c_level": float(HbA1c),
        "blood_glucose_level": float(glicose),
        "gender_Male": 1 if gender == "Masculino" else 0,
        "smoking_history_current": 1 if tabagismo == "Fumante atual" else 0,
        "smoking_history_ever": 0, # Mantido por padrão estrutural
        "smoking_history_former": 1 if tabagismo == "Ex-fumante" else 0,
        "smoking_history_never": 1 if tabagismo == "Nunca fumou" else 0,
        "smoking_history_not_current": 1 if tabagismo == "Parou recentemente" else 0
    }
    
    with st.spinner("A IA está analisando os dados..."):
        try:
            url_api = "http://127.0.0.1:8000/predicao"
            resposta = requests.post(url_api, json=payload)
            
            if resposta.status_code == 200:
                resultado = resposta.json()
                st.divider()
                if resultado["status_diabetes"] == "Diabético":
                    st.error(f"⚠️ Alerta: O modelo indica que o paciente é **{resultado['status_diabetes']}**.")
                else:
                    st.success(f"✅ Resultado: O modelo indica que o paciente é **{resultado['status_diabetes']}**.")
                st.info(f"Confiança do modelo nesta previsão: {resultado['confianca']}")
            else:
                st.error(f"Erro na API: Código {resposta.status_code}. Detalhes no terminal do FastAPI.")
                
        except Exception as e:
            st.error("Erro ao conectar com o servidor da API. Certifique-se de que o FastAPI está rodando no terminal.")