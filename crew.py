import os
from crewai import Agent, Crew, Process, Task, LLM
from crewai.project import CrewBase, agent, crew, task
from crewai.tools import tool, BaseTool
import pandas as pd
from dotenv import load_dotenv
from tabulate import tabulate

load_dotenv()

@tool("Executa comandos pandas sobre o CSV")
def execute_csv_query(code: str, csv_name: str = None) -> str:
    """
    Executa um código Python usando pandas no arquivo csv especificado.
    
    Args:
        code: O código deve ser uma operação válida sobre um DataFrame chamado df.
        csv_path: Caminho para o arquivo CSV. Se não fornecido, usa a variável de ambiente CSV_FILE_PATH.
    """
    MAX_LINHAS = 20

    try:
        print("Executando código:", code)
        
        # Determina o caminho do CSV
        if csv_name is None:
            raise ValueError("Caminho do CSV não fornecido e CSV_FILE_PATH não está definido nas variáveis de ambiente")
        
        # Verifica se o arquivo existe
        if not os.path.exists(f"data/{csv_name}"):
            raise FileNotFoundError(f"Arquivo CSV não encontrado: {csv_name}")
        
        print(f"Carregando CSV: {csv_name}")
        df = pd.read_csv(f"data/{csv_name}")
        df.columns = [col.strip() for col in df.columns]

        result = eval(code)
        if not isinstance(result, pd.DataFrame):
            result = pd.DataFrame([[result]], columns=["Resultado"])
            
        result = result.reset_index()

        if len(result) > MAX_LINHAS:
            result = result.head(MAX_LINHAS)
            aviso = f"\n(Mostrando apenas as primeiras {MAX_LINHAS} linhas de {len(result)} total)"
        else:
            aviso = ""

        matriz = result.values.tolist()
        tabela = tabulate(matriz, headers=result.columns.tolist(), tablefmt="outline", showindex=False)

        return str(tabela) + aviso
        
    except Exception as e:
        raise ValueError(f"Erro ao executar o código: {e}")


llm = LLM(
    model="openai/gpt-3.5-turbo",
    temperature=0
)


@CrewBase
class ComplianceCrew:
    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"
    csv_name = ""

    @agent
    def analista_dados(self) -> Agent:
        return Agent(
            config=self.agents_config["analista_dados"],
            tools=[execute_csv_query],
            verbose=True,
            allow_delegation=False,
            llm=llm
        )

    @task
    def reponder_perguntas_de_notas_fiscais(self) -> Task:
        return Task(
            config=self.tasks_config["reponder_perguntas_de_notas_fiscais"],
            tools=[execute_csv_query]
        )


    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=[self.analista_dados()],
            tasks=[self.reponder_perguntas_de_notas_fiscais()],
            process=Process.sequential,
            verbose=True
        )

