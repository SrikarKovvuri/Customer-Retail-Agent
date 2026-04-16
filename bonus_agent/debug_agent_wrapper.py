from __future__ import annotations

from arksim.simulation_engine.agent.base import BaseAgent
from arksim.config import AgentConfig
from agent import run_agent


class DebugAgent(BaseAgent):
    """Wrapper for the Python debugging agent."""

    def __init__(self, agent_config: AgentConfig) -> None:
        super().__init__(agent_config)
        self.session_count = 0

    async def get_chat_id(self) -> str:
        self.session_count += 1
        return f"debug-session-{self.session_count}"

    async def execute(self, user_query: str, **kwargs: object) -> str:
        """Execute the debugging agent on the user query."""
        # run_agent is synchronous, call it directly (no await needed)
        try:
            response = run_agent(user_query, model="gpt-4o-mini")
            return response
        except Exception as e:
            return f"Agent encountered an error: {str(e)}"