from fastapi import FastAPI
from pydantic import BaseModel
import pickle
import pandas as pd

app = FastAPI(title="API de Detecção de Diabetes")

with open('modelo_detecao_diabetes.pkl', 'rb') as arquivo:
    modelo = pickle.load(arquivo)

class DadosPaciente(BaseModel):
    age: float
    hypertension: int
    heart_disease: int
    bmi: float
    HbA1c_level: float
    blood_glucose_level: float
    gender_Male: int
    smoking_history_current: int = 0
    smoking_history_ever: int = 0
    smoking_history_former: int = 0
    smoking_history_never: int = 0
    smoking_history_not_current: int = 0

@app.post("/predicao")
def prever_diabetes(paciente: DadosPaciente):
    dados_dict = paciente.dict()
    df_entrada = pd.DataFrame([dados_dict])
    
    # Esta linha força a API a organizar as colunas na ordem binária idêntica à do treino
    # evitando qualquer erro 500 estrutural
    colunas_treino = list(modelo.feature_names_in_)
    df_entrada = df_entrada.reindex(columns=colunas_treino, fill_value=0)
    
    predicao = modelo.predict(df_entrada)[0]
    probabilidade = modelo.predict_proba(df_entrada)[0][predicao] * 100
    
    resultado = "Diabético" if predicao == 1 else "Não Diabético"
    
    return {
        "status_diabetes": resultado,
        "confianca": f"{probabilidade:.2f}%"
    }