from app.agent.llm import LLMClient
from app.agent.prompts import SYSTEM_PROMPT
from app.agent.memory import MemoryStore
from app.tools.registry import ToolRegistry
from app.utils.timeouts import with_timeout
from app.config import settings

class AgentRunner:
    def __init__(self, tools: ToolRegistry):
        self.llm = LLMClient()
        self.mem = MemoryStore()
        self.tools = tools

    async def run(self, user_id: str, goal: str) -> tuple[list[dict], str]:
        steps: list[dict] = []
        memory = self.mem.get_all(user_id)

        messages = []
        if memory:
            messages.append({
                "role": "user",
                "content": f"Prior memory context (json list): {memory}"
            })
        messages.append({"role": "user", "content": f"Goal: {goal}"})

        for step_idx in range(1, settings.agent_max_steps + 1):
            plan = await self.llm.chat_json(SYSTEM_PROMPT, messages)

            thought = str(plan.get("thought", ""))[:400]
            action = plan.get("action", "")
            tool_name = plan.get("tool_name")
            args = plan.get("args") or {}
            final = plan.get("final")

            step_obj = {"step": step_idx, "thought": thought, "action": action}

            if action == "tool":
                if not tool_name:
                    obs = "Error: tool_name missing."
                else:
                    try:
                        tool_fn = self.tools.get(tool_name)
                        obs = await with_timeout(
                            self.tools.execute(tool_name, args),
                            settings.tool_timeout_seconds
                        )
                    except Exception as e:
                        obs = f"Tool error: {e}"

                step_obj["tool_call"] = {"tool_name": tool_name, "args": args}
                step_obj["observation"] = obs

                messages.append({"role": "assistant", "content": str(plan)})
                messages.append({"role": "user", "content": f"Tool observation: {obs}"})
                steps.append(step_obj)
                continue

            if action == "final":
                answer = str(final or "No final answer provided.")
                step_obj["final"] = answer
                steps.append(step_obj)

                self.mem.append(user_id, {"goal": goal, "answer": answer})
                return steps, answer

            # malformed response handling
            obs = "Error: invalid action. Use 'tool' or 'final'."
            step_obj["observation"] = obs
            steps.append(step_obj)
            messages.append({"role": "user", "content": obs})

        answer = "Stopped: max steps exceeded. Try a simpler goal."
        self.mem.append(user_id, {"goal": goal, "answer": answer})
        return steps, answer
