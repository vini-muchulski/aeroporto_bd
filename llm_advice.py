from openai import OpenAI
from dotenv import load_dotenv
import os
import json

def gemini_interpretacao(consulta_resultado, model_name="gemini-1.5-flash-002"):
    
    load_dotenv()

    api_key=os.getenv("GEMINI_API_KEY")
    client = OpenAI(
    api_key=api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/"
    )

    schema_description = """
    O banco de dados 'aeroporto' contém informações sobre voos, passageiros, aeronaves, empresas aéreas, etc.
    As tabelas incluem: passageiro, bilhete_voo, voo, aeronave, empresa_aerea, portao_embarque, area_bagagem, tripulantes, destinos e manutencao.  
    Elas se relacionam por meio de chaves estrangeiras. Por exemplo, 'bilhete_voo' se relaciona com 'passageiro' e 'voo'.
    """
    # Converter o resultado da consulta para JSON para facilitar o processamento pelo modelo
    json_result = json.dumps(consulta_resultado, indent=4, default=str)  # default=str para lidar com tipos de dados do SQLAlchemy

    response = client.chat.completions.create(
        model="gemini-1.5-flash-002",
        #model="gemini-1.5-pro-002",
        n=1,
        messages=[
            {
                "role": "system",
                "content": f"""Você é um assistente útil para interpretar consultas de banco de dados.
                {schema_description}
                Seu trabalho é fornecer uma breve explicação em português do significado de uma consulta SQL, com foco em insights acionáveis que ajudem na tomada de decisões.  
                Seja conciso e direto ao ponto. Concentre-se no que os dados revelam e nas possíveis implicações.
                """
            },
            {
                "role": "user",
                "content": f"Aqui está o resultado de uma consulta no banco de dados 'aeroporto':\n```json\n{json_result}\n```\nExplique o significado desta consulta e forneça insights acionáveis."
            }
        ]
    )

    print(response.choices[0].message.content)
    
    

def local_llm_interpretacao(user_message):
    client = OpenAI(base_url="http://localhost:1234/v1", api_key="lm-studio")
    messages = [
        {"role": "system", "content": (
                "Você é um assistente especializado em interpretar consultas de banco de dados. "
                "O banco de dados 'aeroporto' contém informações sobre voos, passageiros, aeronaves, empresas aéreas, etc. "
                "As tabelas incluem: passageiro, bilhete_voo, voo, aeronave, empresa_aerea, portao_embarque, area_bagagem, tripulantes, destinos e manutencao. "
                "Essas tabelas se relacionam por meio de chaves estrangeiras, como 'bilhete_voo' que se conecta com 'passageiro' e 'voo'. "
                "Seu trabalho é fornecer explicações claras e úteis em português sobre consultas SQL e seus resultados, destacando insights acionáveis "
                "que ajudem na tomada de decisões. Responda de forma concisa, clara e sem formatação especial."
            )},
        
        {"role": "user", "content": user_message}
    ]
    
    print("\n")
    print(client.chat.completions.create(
        model="model-identifier",
        messages=messages,
        temperature=0.7
    ).choices[0].message.content)

