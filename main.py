from agents.agents import DemandAgent, ExecuteAgent, DocumentationAgent
from agents.controller import Controller
import openai
import boto3
import os
import yaml

openai.api_key = os.environ['OPENAI_API_KEY']

def read_yaml(file):
    with open(file, 'r') as stream:
        data_loaded = yaml.safe_load(stream)
    return data_loaded

def main():
    demandAgent = DemandAgent()
    executeAgent = ExecuteAgent()
    documentationAgent = DocumentationAgent()
    controller = Controller(demandAgent, executeAgent, documentationAgent)

    env_list = read_yaml('environments.yaml')['environments']
    services_list = read_yaml('services.yaml')['services']

    print(env_list, services_list)


    demand = f"""
        Given the following environment:
        {env_list[services_list[0]['env']]} 
        Create following services using ONLY Python boto3 commands. Ommit optional parameters.
        {services_list}
    """

    output_directory = "output"

    result = controller.solve_problem_and_create_documentation(demand, output_directory)
    print(f"Result: {result}")
    print(f"Documentation created successfully. Saved in {output_directory}/script.py")

if __name__ == "__main__":
    main()
