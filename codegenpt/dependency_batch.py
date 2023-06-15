import click
from codegenpt.codegenpt_instructions import CodeGenPTInstructions
import os

def batch_instructions_by_dependencies(instructions: list[CodeGenPTInstructions]) -> list[list[CodeGenPTInstructions]]:
    # Initiate variables
    batches = []
    dependency_dict = {}
    dependency_count = {}

    # Calculate dependency count
    for instruction in instructions:
        # filter dependencies out if they're existing files on the diretory
        dependencies = [dependency for dependency in instruction.dependencies if (not os.path.exists(os.sep.join(instruction.path + [dependency]))) and (not dependency.endswith('.codegenpt.json'))]
        if len(dependencies) > 0:
            dependency_count[instruction] = len(dependencies)
        for dependency in dependencies:
            normalized_path = os.path.normpath(os.sep.join(instruction.path + [dependency]))
            if normalized_path not in dependency_dict:
                dependency_dict[normalized_path] = set()
            dependency_dict[normalized_path].add(instruction)

    # Start with the instructions that have no depedencies
    available_instructions = [instruction for instruction in instructions if instruction not in dependency_count]

    # Generate batches
    while available_instructions != []:

        current_batch = available_instructions.copy()
        available_instructions = []

        for instruction in current_batch:
            fullPath = os.path.normpath(instruction.fullPath)

            # Collect instructions that depend on this instruction
            dependants = dependency_dict.get(fullPath, set())

            for dependant in dependants:
                dependency_count[dependant] -= 1
                if dependency_count[dependant] <= 0:
                    available_instructions.append(dependant)
                    del dependency_count[dependant]

        batches.append(current_batch)

    if dependency_count != {}:
        raise Exception("Circular dependencies found", [dependency_count])

    return batches