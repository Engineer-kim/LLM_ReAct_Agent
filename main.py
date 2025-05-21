from typing import Union, List

from dotenv import load_dotenv
from langchain.agents.output_parsers import ReActSingleInputOutputParser
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.schema import AgentAction, AgentFinish
from langchain.tools import Tool, tool
from langchain.tools.render import render_text_description

load_dotenv()


@tool
def get_text_length(text: str) -> int:
    print(f"get_text_length enter with {text=}")
    text = text.strip("'\n").strip(
        '"'
    )#텍스트가 아닌 불필요한 문자 제거

    return len(text)


def find_tool_by_name(tools: List[Tool], tool_name: str) -> Tool:
    for tool in tools:
        if tool.name == tool_name:
            return tool
    raise ValueError(f"Tool wtih name {tool_name} not found")


if __name__ == "__main__":
    print("Hello ReAct LangChain!(tetstset)")
    tools = [get_text_length]

    template = """
    Answer the following questions as best you can. You have access to the following tools:

    {tools}

    Use the following format:

    Question: the input question you must answer
    Thought: you should always think about what to do
    Action: the action to take, should be one of [{tool_names}]
    Action Input: the input to the action
    Observation: the result of the action
    ... (this Thought/Action/Action Input/Observation can repeat N times)
    Thought: I now know the final answer
    Final Answer: the final answer to the original input question

    Begin!

    Question: {input}
    Thought:
    """
    #Use the following format 부분은 ==> 행동 가이드
    # Question: 에 사용자 질문,
    #Thought:  스스로 추론 과정
    #Action:  Action:과 Action Input: 형식에 맞춰 그 도구와 입력값을 '글자'로 출력
    #=> 결론은: LLM이 맥락을 파악해서 그에 맞춰 필요한 정보를 생성하거나 특정 형식을 따르는 '글자'를 출력
    prompt = PromptTemplate.from_template(template=template).partial(
        tools=render_text_description(tools), #객체에 대한 설명을 문장 형태로 만들어서 보여주는 함수
        #ex)
        #item = {
        #     "name": "불의 검",
        #     "damage": 50,
        #     "type": "화염"
        # }  => 불의 검은 50의 피해를 주는 화염 속성 무기입니다.
        tool_names=", ".join([t.name for t in tools]),
    )

    llm = ChatOpenAI(temperature=0, stop=["\nObservation", "Observation"])
    agent = {"input": lambda x:x["input"]} | prompt | llm | ReActSingleInputOutputParser()
    #ReActSingleInputOutputParser ==> LLM이 생성한 행동을 파싱하는 도구인데 쉽게 말하면 더 정확하고 일관된 답변이 보장됨
    
    
    #invoke => agent 실행지점
    res = agent.invoke({"input": "what is the length of the text 'DOG'?  | in characters"})
    
    #Union [AgentAction, AgentFinish] ==> 두가지 타입을 모두 받을 수 있는 타입
    #AgentAction ==> 에이전트가 어떤 행동을 하기 위한 중간 단계 정보 (복잡한 건 도구를 순서대로 써서 해결 (AgentAction → Action → Finish))
    #AgentFinish ==> 에이전트가 작업을 완료한 최종 결과 단계(간단한 건 직접 답)
    agent_step: Union[AgentAction, AgentFinish] = agent.invoke({"input" : "what is the length of the text 'DOG'?  | in characters"})
    print(agent_step)

    if isinstance(agent_step, AgentFinish): # agent_step이 AgentFinish 타입인지 확인 == 에이전트가 "작업 끝났어!"라고 한 경우
        tool_name = agent_step.tool
        tool_to_use = find_tool_by_name(tools, tool_name)
        tool_input = agent_step.tool_input

        observation = tool_to_use.func(str(tool_input))  # .func => 객체.메서드 호출(자바로 치면 isquals, Getter ,Setter등을 호출함)
        print(f"{observation=}")  #리터럴 출력


    #print(res) # 3이 나옴