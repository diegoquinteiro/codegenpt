from codegenpt.codegenpt_instructions import CodeGenPTInstructions


def batch_instructions_by_dependencies(instructions: list[CodeGenPTInstructions]) -> list[list[CodeGenPTInstructions]]:
    dependencies = {}
    for instruction in instructions:
        dependencies[instruction.fullPath] = instruction.dependencies
    
    # Checking for circular dependencies
    visited = set()
    temp_stack = set()
    def has_cycle(node):
        if node not in visited:
            visited.add(node)
            temp_stack.add(node)

            for neighbour in dependencies.get(node, []):
                if neighbour not in visited:
                    if has_cycle(neighbour):
                        return True
                elif neighbour in temp_stack:
                    return True

            temp_stack.remove(node)
            return False

        return False

    for instruction in instructions:
        if has_cycle(instruction.fullPath):
            raise Exception(f'Circular dependencies found in file {instruction.basename}{instruction.suffix}!')

    # Topological sorting with Depth First Search
    visited = set()
    output = []

    def DFS(node):
        visited.add(node)
        for neighbour in dependencies.get(node, []):
            if neighbour not in visited:
                DFS(neighbour)
        output.insert(0, node)

    for node in dependencies.keys():
        if node not in visited:
            DFS(node)

    sorted_instructions = []
    for node in output:
        sorted_instructions.append(list(filter(lambda instr: instr.fullPath == node, instructions)))

    return sorted_instructions
