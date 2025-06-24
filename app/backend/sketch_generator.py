from graphviz import Digraph
import re
from typing import Optional, List, Tuple
 
def parse_flowchart_description(description: str) -> List[Tuple[str, str, str]]:
    lines = [line.rstrip() for line in description.strip().split('\n') if line.strip()]
    edges = []
    i = 0
    prev_node = None
    condition_stack = []
    current_indent = 0

    while i < len(lines):
        line = lines[i]
        indent = len(line) - len(line.lstrip())
        line = line.strip()

        # Close deeper condition blocks if indent decreases
        while condition_stack and indent <= current_indent:
            condition_stack.pop()
            if condition_stack:
                current_indent = condition_stack[-1][1]
            else:
                current_indent = 0

        # --- Handle consecutive [condition] -> action as branches from the same parent ---
        cond_arrow_lines = []
        cond_arrow_start = i
        while i < len(lines):
            cond_arrow_match = re.match(r'^\[(.+?)\]\s*->\s*(.+)', lines[i])
            if cond_arrow_match:
                cond_arrow_lines.append(lines[i])
                i += 1
            else:
                break

        if cond_arrow_lines:
            # The parent is the last non-empty node before this block
            parent_node = prev_node
            for cond_line in cond_arrow_lines:
                cond, actions = re.match(r'^\[(.+?)\]\s*->\s*(.+)', cond_line).groups()
                if parent_node:
                    edges.append((parent_node, cond, ""))
                chain = [cond] + [a.strip() for a in actions.split('->')]
                for j in range(len(chain) - 1):
                    edges.append((chain[j], chain[j+1], ""))
            # Do NOT update prev_node here, so further blocks can branch from the same parent
            prev_node = parent_node  # keep the parent for further siblings
            continue

        # Match `[condition]`
        cond_match = re.match(r'^\[(.+?)\]$', line)
        if cond_match:
            cond_text = cond_match.group(1)
            if prev_node:
                edges.append((prev_node, cond_text, ""))
            condition_stack.append((cond_text, indent))
            current_indent = indent
            prev_node = cond_text
            i += 1
            continue

        # Handle Yes:/No: branches
        branch_match = re.match(r'^/?\s*(Yes|No):\s*(.+)', line, re.IGNORECASE)
        if branch_match and condition_stack:
            branch_label = branch_match.group(1).capitalize()
            branch_content = branch_match.group(2).strip()
            current_condition = condition_stack[-1][0]

            if branch_content.startswith('[') and branch_content.endswith(']'):
                nested_condition = branch_content[1:-1].strip()
                edges.append((current_condition, nested_condition, branch_label))
                condition_stack.append((nested_condition, indent))
                current_indent = indent
                prev_node = nested_condition
            else:
                edges.append((current_condition, branch_content, branch_label))
                prev_node = branch_content
            i += 1
            continue

        # Handle A -> B -> C
        if '->' in line:
            chain = [part.strip() for part in line.split('->')]
            if prev_node:
                edges.append((prev_node, chain[0], ""))
            for j in range(len(chain) - 1):
                edges.append((chain[j], chain[j+1], ""))
            prev_node = chain[-1]
            i += 1
            continue

        # Handle simple single node line
        if prev_node:
            edges.append((prev_node, line, ""))
        prev_node = line
        i += 1

    return edges

def generate_flowchart(description: str, output_path: Optional[str] = "flowchart.png") -> str:
    edges = parse_flowchart_description(description)
    dot = Digraph(format='png')
    node_ids = {}
    node_count = 0

    def get_node_id(label):
        nonlocal node_count
        if label not in node_ids:
            node_ids[label] = f"n{node_count}"
            dot.node(node_ids[label], label)
            node_count += 1
        return node_ids[label]

    for src, dst, label in edges:
        src_id = get_node_id(src)
        dst_id = get_node_id(dst)
        dot.edge(src_id, dst_id, label=label)

    dot.render(filename=output_path, cleanup=True)
    return output_path if output_path.endswith('.png') else output_path + '.png'

if __name__ == "__main__":
    desc = """
Flowchart description:
Start ->
      Define function 'getDayName' ->
         Accept a single argument, 'dayNumber' ->
            If 'dayNumber' equals 0 ->
               Return "Sunday"
            Else if 'dayNumber' equals 1 ->
               Return "Monday"
            Otherwise (default) ->
               Return "Unknown"
      Define function 'main' ->
         Attempt to execute the following steps repeatedly for 'i' from 0 to less than 3 ->     
            Call 'getDayName(i)' and assign result to temporary variable ->
            Print the value of the temporary variable using console.log()
         If an error occurs during execution ->
            Print "An error occurred" using console.log()
   End
    """

    out = generate_flowchart(desc, "combined_flowchart")
    print(f"Flowchart saved to {out}")