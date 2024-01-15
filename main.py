import asyncio

import semantic_kernel as sk
from semantic_kernel.connectors.ai.open_ai import OpenAIChatCompletion
from semantic_kernel.connectors.search_engine import BingConnector
from semantic_kernel.planning import ActionPlanner, StepwisePlanner
from semantic_kernel.planning.stepwise_planner.stepwise_planner_config import StepwisePlannerConfig

from Skills.Search.WebSearch import WebSearchEngineSkill

# import semantic_kernel.connectors.ai.hugging_face as sk_hf

kernel = sk.Kernel()
# Integrating OpenAI model
api_key, org_id = sk.openai_settings_from_dot_env()
kernel.add_chat_service("OpenAI_chat_gpt", OpenAIChatCompletion("gpt-3.5-turbo", api_key, org_id))

# Integrating transforms HuggingFace
# -- Need the model running on local first
# kernel.add_text_completion_service(
#     "gpt2", sk_hf.HuggingFaceTextCompletion("gpt2", task="text-generation")
# )


skills_directory = "./"
funFunctions = kernel.import_semantic_skill_from_directory(skills_directory, "Skills")
jokeFunction = funFunctions["Jokes"]
joke_prompt = "Traveling to the dinosaur era"
result = jokeFunction(joke_prompt)
# print(result)

# Doing some websearching
BING_API_KEY = sk.bing_search_settings_from_dot_env()
connector = BingConnector(BING_API_KEY)
skill = kernel.import_skill(WebSearchEngineSkill(connector))
search = skill["searchAsync"]
search_prompt = "Which country won the most gold medals in the 2023 Asian Games?"
result = search(search_prompt)


# print(f"search prompt : {search_prompt}\n")
# print(f"result: {result}")


# Using the Planner to execute the more appropriate function as it sees fit
async def action_planner(ask: str):
    # kernel has the previously demonstrated Semantic and Native Functions added
    planner = ActionPlanner(kernel)
    plan = await planner.create_plan_async(goal=ask)
    result = await plan.invoke_async()
    print(result)


# Interesting to note without the contextual prefix added below to the previous prompts the planners throws an error
# asyncio.run(action_planner("Tell a Joke about " + joke_prompt))
# asyncio.run(action_planner("Web Search: " + search_prompt))


# StepwisePlanner gives more fine grained control
# you can set the maximum number of iterations and minimum iteration time.
# The maximum number of iterations indicates how many rounds of thinking are allowed


async def stepwise_planner(ask: str):
    # kernel has the previously demonstrated Semantic and Native Functions added
    planner = StepwisePlanner(
        kernel, StepwisePlannerConfig(max_iterations=10, min_iteration_time_ms=1000)
    )
    plan = planner.create_plan(goal=ask)
    result = await plan.invoke_async()
    print(result)
    for index, step in enumerate(plan._steps):
        print("Step:", index)
        print("Description:", step.description)
        print("Function:", step.skill_name + "." + step._function.name)
        if len(step._outputs) > 0:
            print("  Output:\n", str.replace(result[step._outputs[0]], "\n", "\n  "))


# Notice how this is a combination of both the previous prompts
asyncio.run(stepwise_planner(
    "Based on the 2023 Asian Games gold medal count, tell a joke about time traveling from that country to the dinosaur era"))
