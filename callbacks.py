from typing import Any, Optional
from uuid import UUID

from dotenv import load_dotenv
from langchain_core.callbacks import BaseCallbackHandler
from langchain_core.outputs import LLMResult


load_dotenv()

# 디버깅용도 클래스
class AgentCallbackHandler(BaseCallbackHandler):  #BaseCallbackHandler ==> 특정 이벤트가 발생했을 때 알려주는 기본 틀
    def on_llm_start(  #언어 모델(LLM) 호출 시작 시 호출
        self,
        serialized: dict[str, Any],
        prompts: list[str],
        **kwargs: Any) -> Any:

        print(f"****prompts To LLm was : *-*** \n{prompts[0]}")
        print("****")

    def on_llm_end( #LLM 호출이 정상적으로 종료될 때 호출
        self,
        response: LLMResult,
        *,
        run_id: UUID,
        parent_run_id: Optional[UUID] = None,
        **kwargs: Any,
    ) -> Any:
        print(f"****LLm Response : *-*** \n{response.generations[0][0].text}")
        print("****")