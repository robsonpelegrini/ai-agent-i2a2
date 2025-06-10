# NF Assistant - Agente que responde perguntas sobre Notas Fiscais 

Este projeto é um assistente fiscal interativo, desenvolvido em Python com Streamlit e CrewAI, que permite ao usuário fazer perguntas sobre notas fiscais presentes nos arquivos CSV fornecidos. O assistente utiliza inteligência artificial e agentes autônomos para analisar e responder questões relacionadas ao conteúdo das notas fiscais.


> **Importante:** Também é obrigatório possuir uma chave de API da OpenAI, que deve ser configurada no arquivo `.env` com a variável `OPENAI_API_KEY`.

## Funcionalidades
- Interface web interativa via Streamlit
- Chat para perguntas e respostas sobre notas fiscais
- Análise dos arquivos `202401_NFs_Cabecalho.csv` e `202401_NFs_Itens.csv`
- Uso de agentes CrewAI para análise automatizada dos dados
- Execução de código Python em ambiente isolado via Docker

## Pré-requisitos
- Python 3.12+
- Instalar as dependências do projeto (recomenda-se uso de ambiente virtual)

## Instalação
1. Clone este repositório:
   ```sh
   git clone https://github.com/robsonpelegrini/ai-agent-i2a2.git
   cd ai-agent-i2a2
   ```
2. Instale as dependências:
   ```sh
   pip install -r requirements.txt
   ```

## Como usar
1. Certifique-se de que os arquivos de notas fiscais estejam na pasta `data/`:
    - `data/202401_NFs_Itens.csv`
2. Execute o aplicativo Streamlit:
   ```sh
   streamlit run app.py
   ```
3. Acesse o endereço exibido no terminal (geralmente http://localhost:8501) para interagir com o assistente.

## Exemplo de Perguntas


- `Exiba os registros cujo destinatario seja INSTITUTO CHICO MENDES DE CONSERVACAO DA BIODIVERSIDADE.`
- `Quais os registros onde MUNICÍPIO EMITENTE é PORTO ALEGRE ?`
- `Agrupe os dados por MUNICÍPIO EMITENTE e some o valor total.`
- `Quantos registros foram emitidos entre 12/01/2024 e 16/01/2024?`


 O assistente irá analisar os arquivos e responder com base nos dados disponíveis.

## Estrutura do projeto
```
ai-agent-i2a2/
├── app.py                # Interface Streamlit
├── main.py               # Classe principal do assistente
├── crew.py               # Gerenciamento de agentes/tarefas CrewAI
├── config/
│   ├── agents.yaml       # Configuração de agentes
│   └── tasks.yaml        # Configuração de tarefas
├── data/
│   ├── 202401_NFs_Cabecalho.csv
│   └── 202401_NFs_Itens.csv
├── requirements.txt      # Dependências do projeto
```

## Principais dependências
- streamlit
- pandas
- crewai
- crewai-tools

## Licença
Este projeto é apenas para fins educacionais/demonstração.
