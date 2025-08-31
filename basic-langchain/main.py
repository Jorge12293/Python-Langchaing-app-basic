from dotenv import load_dotenv

load_dotenv()

from langchain import hub
from langchain.agents import AgentExecutor
from langchain.agents.react.agent import create_react_agent
from langchain_core.output_parsers.pydantic import PydanticOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnableLambda
from langchain_openai import ChatOpenAI
from langchain_tavily import TavilySearch

# from langchain_ollama import ChatOllama
from langchain_core.prompts import PromptTemplate

from prompt import REACT_PROMPT_WITH_FORMAT_INSTRUCTIONS
from schemas import AgentResponse

import re
from typing import Any, Dict

# 2) Función de parseo seguro:
def safe_parse_output(text: str) -> Dict[str, Any]:
    """
    Extrae el JSON del 'Final Answer' si existe; si no, devuelve un dict de error.
    Acepta tres casos:
    - Salida es SOLO JSON
    - 'Final Answer: { ... }'
    - Fallo (no hay JSON) -> devuelve {'error': ..., 'raw_output': ...}
    """
    if not isinstance(text, str):
        return {"error": "Non-string output", "raw_output": text}

    # a) ¿La salida completa ya es JSON puro?
    text_strip = text.strip()
    if text_strip.startswith("{") and text_strip.endswith("}"):
        return output_parser.parse(text_strip).model_dump()

    # b) ¿Hay un bloque JSON después de 'Final Answer:'?
    m = re.search(r"Final Answer:\s*(\{.*\})\s*$", text_strip, re.DOTALL)
    if m:
        json_part = m.group(1)
        return output_parser.parse(json_part).model_dump()

    # c) No hay JSON → devuelve error controlado para que tu app lo maneje
    return {
        "error": "No valid JSON in output",
        "raw_output": text_strip
    }

tools = [TavilySearch()]
llm = ChatOpenAI(model="gpt-4.1-mini",temperature=0)
react_prompt = hub.pull("hwchase17/react")

output_parser = PydanticOutputParser(pydantic_object=AgentResponse)
react_prompt_with_format_instructions = PromptTemplate(
    template=REACT_PROMPT_WITH_FORMAT_INSTRUCTIONS,
    input_variables=["input", "agent_scratchpad", "tool_names"],
).partial(format_instructions=output_parser.get_format_instructions())

agent = create_react_agent(
    llm=llm, 
    tools=tools, 
    prompt=react_prompt_with_format_instructions
    #prompt=react_prompt
)
agent_executor = AgentExecutor(
    agent=agent, 
    tools=tools, 
    verbose=True,
    # Mensaje de reintento guiado
    handle_parsing_errors=(
        "FORMAT ERROR. You must use the ReAct format. "
        "Never output JSON except in the 'Final Answer'. "
        "Continue your Thought/Action/Observation loop and try again."
    ),
    return_intermediate_steps=True,
    max_iterations=12,
    early_stopping_method="force",   # <- o quítalo y deja el default
)
extract_output = RunnableLambda(lambda x: x["output"])
parse_output = RunnableLambda(safe_parse_output)
# 3) La cadena final (igual que tenías, pero con safe_parse)
chain = agent_executor | extract_output | parse_output
#parse_output = RunnableLambda(lambda x: output_parser.parse(x))
#chain = agent_executor | extract_output | parse_output

from prompt import REACT_PROMPT_WITH_FORMAT_INSTRUCTIONS
from schemas import AgentResponse

def main():
    print("Search TavilySearch!")
    result = chain.invoke(
        input={
            "input": "Search for 3 jobs postings for an ai engineer using langchain in the bay area on linkedin and list their details"
        }
    )
    print(result)


def main_open_ai():
    print("Search Open AI!")
    information = """
    Elon Reeve Musk (Pretoria, 28 de junio de 1971) es un empresario, inversor, activista político de derecha radical[3]​[4]​ y magnate.[nota 1]​ Es el fundador, consejero delegado e «ingeniero» en jefe de la empresa SpaceX; inversor ángel, director general y arquitecto de productos de Tesla, Inc.; fundador de The Boring Company; y cofundador de Neuralink y OpenAI.[nota 2]​ Además, es el director de tecnología de X Corp.[5]​ Entre enero y mayo de 2025, ejerció como administrador de facto del Departamento de Eficiencia Gubernamental de la Casa Blanca bajo la segunda presidencia de Donald Trump.[6]​[7]​
    Con un patrimonio neto estimado en unos cuatrocientos mil millones de dólares en diciembre de 2024,[8]​ es la persona más rica del mundo según el índice de multimillonarios en tiempo real de Forbes.[9]​[10]​
    Musk nació y se crio en una rica familia de Pretoria (Sudáfrica). Su madre es canadiense y su padre un sudafricano blanco. Estudió brevemente en la Universidad de Pretoria antes de trasladarse a Canadá a los 17 años. Se matriculó en la Universidad de Queen y se trasladó a la Universidad de Pensilvania dos años después, donde se graduó en Economía y Física. En 1995 se trasladó a California para asistir a la Universidad Stanford, pero en su lugar decidió seguir una carrera empresarial, cofundando la empresa de software web Zip2 con su hermano Kimbal. Zip2 fue adquirida por Compaq por 307 millones de dólares en 1999. Ese mismo año, Musk cofundó el banco en línea X.com, que se fusionó con Confinity en 2000 para formar PayPal. La empresa fue comprada por eBay en 2002 por mil quinientos millones de dólares.
    En 2002, Musk fundó SpaceX, fabricante aeroespacial y empresa de servicios de transporte espacial, de la que es director general e ingeniero jefe. En 2003, se unió al fabricante de vehículos eléctricos Tesla Motors, Inc. (ahora Tesla, Inc.) como presidente y arquitecto de productos, convirtiéndose en su consejero delegado en 2008. En 2006, ayudó a crear SolarCity, una empresa de servicios de energía solar que posteriormente fue adquirida por Tesla y se convirtió en Tesla Energy. En 2015, cofundó OpenAI, una empresa de investigación sin ánimo de lucro que promueve la inteligencia artificial amigable. En 2016, cofundó Neuralink, una empresa de neuro tecnología centrada en el desarrollo de interfaces cerebro-ordenador, y fundó The Boring Company, una empresa de construcción de túneles. También acordó la compra de la importante red social estadounidense Twitter en 2022 por 44 000 millones de dólares. Musk también ha propuesto el hyperloop. En noviembre de 2021, el director general de Tesla fue la primera persona de la historia en acumular una fortuna de trescientos mil millones de dólares.[11]​
    Ha sido criticado por hacer declaraciones poco científicas y controvertidas. En 2018, fue demandado por la Comisión de Bolsa y Valores de Estados Unidos (SEC) por tuitear falsamente que había conseguido financiación para una adquisición privada de Tesla. Llegó a un acuerdo con la SEC, pero no admitió su culpabilidad, renunciando temporalmente a su presidencia y aceptando limitaciones en su uso de Twitter. En 2019, ganó un juicio por difamación presentado contra él por un espeleólogo británico que asesoró en el rescate de la cueva Tham Luang. Musk también ha sido criticado por difundir información errónea sobre la pandemia de COVID-19 y teorías de conspiración; y por sus controvertidas opiniones sobre asuntos como la inteligencia artificial, las criptomonedas y el transporte público.
    """

    summary_template = """
    Given the information {information} about a person I want you create:
    1. A short summary
    2. Two interesting facts about them
    """

    summary_prompt_template = PromptTemplate(
        input_variables=["information"], template=summary_template
    )


    # llm = ChatOllama(temperature=0,model="gemma3:270m")
    llm = ChatOpenAI(temperature=0, model="gpt-4.1-mini")
    chain = summary_prompt_template | llm

    response = chain.invoke(input={"information": information})
    print(response.content)


if __name__ == "__main__":
    main()
