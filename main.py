import os
from crew import ComplianceCrew
import pandas as pd
from dotenv import load_dotenv
import unicodedata

load_dotenv()

def run_nf_assistant(question: str, csv_env_path: str):
       
    # Garante exibição total
    pd.set_option('display.max_rows', None)
    pd.set_option('display.max_columns', None)
    pd.set_option('display.width', None)
    pd.set_option('display.colheader_justify', 'center')
    
    df = pd.read_csv(csv_env_path)
    csv_name = os.path.basename(csv_env_path)
    columns_str = ", ".join(col for col in df.columns)
    
    crew_instance = ComplianceCrew()

    if not question.strip():
        return "⚠️ Favor entrar com uma pergunta valida."

    result = crew_instance.crew().kickoff(inputs={"pergunta": question, "colunas": columns_str,"csv_name": csv_name})

    return result

if __name__ == "__main__": 
    selected_file = "202401_NFs_Cabecalho"
    
    while True:
        pergunta = input("Digite sua pergunta sobre as notas fiscais: ")      
        resposta = run_nf_assistant(pergunta, ".data/" + selected_file)
        print(150* "-")
        print(150* "-")
        print("Resposta do agente:", resposta)
        print(150* "-")
        print(150* "-")