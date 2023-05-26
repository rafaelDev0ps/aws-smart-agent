class Controller:
    def __init__(self, demandAgent, executeAgent, documentationAgent):
        self.demandAgent = demandAgent
        self.executeAgent = executeAgent
        self.documentationAgent = documentationAgent

    def solve_problem_and_create_documentation(self, demand:str, directory:str):
        specifications = self.demandAgent.receive_demand(demand)
        commands = self.executeAgent.generate_boto3_commands(specifications)
        result, commands = self.executeAgent.execute_commands(commands, specifications)
        self.documentationAgent.create_documentation(demand, commands, directory)
        return result

