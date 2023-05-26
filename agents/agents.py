import openai
import boto3

class DemandAgent:
    def receive_demand(self, demand:str):
        prompt = f"Generate specifications to execute this AWS demand:\n{demand}\n Please, don't write anything else than the specifications."
        response = openai.Completion.create(engine="text-davinci-003", prompt=prompt, max_tokens=400, n=1, stop=None, temperature=0.7)
        specifications = response.choices[0].text.strip()
        print("Demand Agent: specifications generated")
        print(specifications)
        return specifications

class ExecuteAgent:
    def generate_boto3_commands(self, specifications:str):
        prompt = f"Generate ONLY the Python boto3 commands to execute the AWS demand based on the following these specifications:\n{specifications}\n. The Python boto3 commands are going to run in the next agent. Do not comment the steps descriptions, only code."
        response = openai.Completion.create(engine="text-davinci-003", prompt=prompt, max_tokens=400, n=1, stop=None, temperature=0.7)
        commands = response.choices[0].text.strip()
        print("Execute Agent: boto3 commands generated")
        print(commands)
        return commands
    
    def execute_commands(self, commands:str, specifications:str):
        success = False
        attempts = 0
        result = None

        while not success and attempts < 3:
            try:
                exec(commands)
                success = True
            except Exception as e:
                print(f"Execute Agent: boto3 commands failed: {e}.")
                attempts += 1
                if attempts < 3:
                    commands = self.generate_boto3_commands(specifications)

        if success:
            result = "Execute Agent: boto3 commands executed sucessfully!"
        else:
            result = "Execute Agent: boto3 commands failed."

        return result, commands

class DocumentationAgent:
    def create_documentation(self, problem, solution, directory):
        documentation = f"Problem: {problem}\nSolution: {solution}"
        with open(f"{directory}/script.py", "w") as f:
            f.write(documentation)
        print("Documentation Agent: documentation created!")

