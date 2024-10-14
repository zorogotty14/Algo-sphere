from flask import Flask, request, jsonify, render_template
import os
from openai import AzureOpenAI
import json
import re
import subprocess

# Load environment variables from .env file

# Initialize Flask app
app = Flask(__name__)

# Set up Azure OpenAI client using environment variables
endpoint = os.getenv("ENDPOINT_URL", "your-endpioint")
deployment = os.getenv("DEPLOYMENT_NAME", "gpt-35-turbo")
subscription_key = os.getenv("AZURE_OPENAI_API_KEY", "your api key")

client = AzureOpenAI(
    azure_endpoint=endpoint,
    api_key=subscription_key,
    api_version="2024-05-01-preview",
)


# Path to the test.py file
TEST_FILE_PATH = os.path.join(os.getcwd(), 'test.py')


@app.route('/search', methods=['POST'])
def search():
    # Access the form data from the POST request
    search_query = request.form.get('search-query', '').strip().lower()

    if not search_query:
        return render_template('search.html', explanation="No input provided.", code="")

    chat_history = []

    chat_prompt = chat_history + [
    {
        "role": "system",
        "content": "You are a code tutoring assistant that explains algorithms step by step. Your response must be a valid JSON object with exactly two fields: 'explanation' (a plain step-by-step algorithm explanation) and 'code' (the corresponding code, properly escaped for JSON) with no extra text or commentary."
    },
    {
        "role": "user",
        "content": search_query
    }
    ]


    try:
        # Generate the completion using OpenAI
        completion = client.chat.completions.create(
            model=deployment,
            messages=chat_prompt,
            max_tokens=800,
            temperature=0.7,
            top_p=0.95,
            frequency_penalty=0,
            presence_penalty=0
        )

        # Get the raw GPT response
        response_content = completion.choices[0].message.content
        print("raw gpt", response_content)
        # Try parsing the response as JSON
        try:
            response_json = json.loads(response_content)
        except json.JSONDecodeError:
            return render_template('search.html', explanation=response_content, code="")
        explanation, code = parse_gpt_output(response_json)
        # Parse the GPT output


        # Display the results
        print("Explanation:")
        print(explanation)
        print("\nCode:")
        print(code)

        # Render the search.html template with explanation and code
        return render_template('search.html', explanation=explanation, code=code)

    except Exception as e:
        # Handle any errors that occur
        return render_template('search.html', explanation="An error occurred.", code="", error=str(e))

# Function to parse explanation and code
def parse_gpt_output(output):
    # Split the output by the markers 'Explanation:' and 'Code:'
    explanation_start = output.find("Explanation:") + len("Explanation:")
    code_start = output.find("Code:")
    
    # Extract explanation and code
    explanation = output[explanation_start:code_start].strip()
    code = output[code_start + len("Code:"):].strip()
    
    return explanation, code


@app.route('/get_bubble_sort_info', methods=['GET'])
def get_bubble_sort_info():
    explanation = """Here's a step-by-step explanation of how the BFS (Breadth-First Search) algorithm works in the given code:

### 1. **Function Definition:**
   The function `bfs(graph, start_vertex)` takes two arguments:
   - `graph`: A dictionary representing the graph, where each key is a vertex, and its value is a list of adjacent (neighboring) vertices.
   - `start_vertex`: The vertex from which the BFS search begins.

### 2. **Initialization:**
   Inside the function, the following steps are taken:
   
   - `visited = set()` creates an empty set called `visited` to store the vertices that have already been visited. This ensures that each vertex is processed only once.
   
   - `queue = deque([start_vertex])` initializes a double-ended queue (`deque`) with the starting vertex. The queue will be used to process each vertex in the order they are discovered, ensuring a level-by-level exploration.
   
   - `visited.add(start_vertex)` adds the `start_vertex` to the `visited` set to mark it as explored right at the beginning.

### 3. **BFS Algorithm Execution:**
   The algorithm runs inside a `while queue:` loop, which continues as long as there are vertices in the queue.

   - **Step 1**: `current_vertex = queue.popleft()` takes the first vertex from the queue (the vertex at the front). This vertex is now considered to be the current vertex being processed.
   
   - **Step 2**: `print(current_vertex)` prints the current vertex. This simulates "visiting" the vertex.
   
   - **Step 3**: The algorithm loops over all the neighbors of the current vertex using `for neighbor in graph[current_vertex]:`. These are the vertices directly connected to the current vertex by an edge.
   
     - For each neighbor, the algorithm checks if the neighbor has already been visited by using `if neighbor not in visited:`.
     
     - If the neighbor has not been visited:
       - The neighbor is added to the `queue` using `queue.append(neighbor)`, which means it will be processed later in BFS order (after all previously added vertices have been processed).
       - The neighbor is marked as visited by adding it to the `visited` set using `visited.add(neighbor)`.

### 4. **Repeating the Process:**
   The BFS algorithm continues this process, repeatedly visiting the next vertex in the queue, processing its neighbors, and adding any unvisited neighbors to the queue, until the queue is empty.

   Once the queue is empty, the algorithm has visited all reachable vertices from the start vertex, and the BFS terminates.

### 5. **Example Walkthrough:**

Consider the graph:
```plaintext
    A
   / \
  B   D
  | \   \
  C  E   E
   \    /
    F--G
```

And the adjacency list representation:
```python
graph = {
    'A': ['B', 'D'],
    'B': ['A', 'C', 'E'],
    'C': ['B', 'F'],
    'D': ['A', 'E'],
    'E': ['B', 'D', 'G'],
    'F': ['C', 'G'],
    'G': ['E', 'F']
}
```

**Execution of `bfs(graph, 'A')`:**

- **Step 1**: Start at vertex 'A':
  - `visited = {'A'}`.
  - `queue = deque(['A'])`.
  - `current_vertex = 'A'`. Print 'A'.
  - Add 'B' and 'D' to the queue, mark them as visited: `visited = {'A', 'B', 'D'}`, `queue = deque(['B', 'D'])`.

- **Step 2**: Visit 'B':
  - `current_vertex = 'B'`. Print 'B'.
  - Add 'C' and 'E' to the queue (since 'A' is already visited): `visited = {'A', 'B', 'C', 'D', 'E'}`, `queue = deque(['D', 'C', 'E'])`.

- **Step 3**: Visit 'D':
  - `current_vertex = 'D'`. Print 'D'.
  - 'A' is already visited, add 'E' to the queue (already visited): No new additions.

- **Step 4**: Visit 'C':
  - `current_vertex = 'C'`. Print 'C'.
  - Add 'F' to the queue: `visited = {'A', 'B', 'C', 'D', 'E', 'F'}`, `queue = deque(['E', 'F'])`.

- **Step 5**: Visit 'E':
  - `current_vertex = 'E'`. Print 'E'.
  - 'B', 'D', and 'G' are adjacent, add 'G' to the queue: `visited = {'A', 'B', 'C', 'D', 'E', 'F', 'G'}`, `queue = deque(['F', 'G'])`.

- **Step 6**: Visit 'F':
  - `current_vertex = 'F'`. Print 'F'.
  - 'C' and 'G' are adjacent, no new additions (already visited).

- **Step 7**: Visit 'G':
  - `current_vertex = 'G'`. Print 'G'.
  - 'E' and 'F' are adjacent, no new additions (already visited).

- **End of BFS**: The queue is now empty, and all reachable vertices from 'A' have been visited. The BFS terminates.

### Output:
```
A
B
D
C
E
F
G
```

This order reflects the breadth-first traversal of the graph, where vertices are explored level by level.
"""
    code = """
    from collections import deque

    def bfs(graph, start_vertex):
        visited = set()   # To keep track of visited nodes
        queue = deque([start_vertex])  # Queue for BFS
        visited.add(start_vertex)

        while queue:
            current_vertex = queue.popleft()  # Get the vertex from the front of the queue
            print(current_vertex)  # Process the current vertex (in this case, we print it)

            # Visit all the adjacent vertices
            for neighbor in graph[current_vertex]:
                if neighbor not in visited:
                    queue.append(neighbor)  # Add unvisited neighbors to the queue
                    visited.add(neighbor)  # Mark the neighbor as visited

    # Example graph represented as an adjacency list (dictionary)
    graph = {
        'A': ['B', 'D'],
        'B': ['A', 'C', 'E'],
        'C': ['B', 'F'],
        'D': ['A', 'E'],
        'E': ['B', 'D', 'G'],
        'F': ['C', 'G'],
        'G': ['E', 'F']
    }

    # Run BFS starting from vertex 'A'
    bfs(graph, 'A')

    """
    return jsonify({
        'explanation': explanation,
        'code': code
    })

dsa_content = {
    "arrays": {
        "description": "Arrays are data structures that contain a group of elements. These elements are stored in contiguous memory locations.",
        "image": "../static/images/arrays.jpg",  # Path to the image
        "video": "https://www.youtube.com/watch?v=55l-aZ7_F24",  # YouTube video URL
        "topics": {
            "introduction": "An introduction to arrays, explaining their structure and basic operations.",
            "sorting_algorithms": {
                "bubble_sort": "An easy-to-understand sorting algorithm that repeatedly steps through the list and swaps adjacent elements if they are in the wrong order.",
                "insertion_sort": "A simple sorting algorithm where elements are inserted into their correct position within a sorted portion of the array.",
                "merge_sort": "A divide and conquer algorithm that splits the array into smaller subarrays, sorts them, and merges them back together.",
                "quicksort": "An efficient, recursive divide-and-conquer algorithm that picks a pivot and partitions the array into two halves.",
                "selection_sort": "A comparison-based algorithm that repeatedly selects the smallest element and swaps it with the first unsorted element."
            },
            "searching_algorithms": {
                "linear_search": "A straightforward algorithm that checks each element of the array sequentially until the target element is found.",
                "binary_search": "A more efficient search for sorted arrays by dividing the search interval in half repeatedly.",
                "jump_search": "A searching algorithm that checks elements by jumping ahead by a fixed step, then performing a linear search in the reduced interval.",
                "interpolation_search": "An improved binary search for uniformly distributed data, using interpolation to find likely position.",
                "exponential_search": "A search algorithm that works for unbounded or infinite-length arrays by expanding search exponentially."
            },
            "two_pointer_technique": "A popular technique for solving array-based problems, where two pointers are used to iterate from both ends of the array.",
            "dynamic_arrays": "An array that resizes itself automatically as elements are added, providing flexibility with size management."
        }
    },
    "strings": {
        "description": "Strings are sequences of characters. In most programming languages, they are used to handle textual data.",
        "image": "../static/images/Strings.jpg",  # Path to the image
        "video": "https://www.youtube.com/watch?v=0qcQ3ciVezQ",  # YouTube video URL
        "topics": {
            "introduction": "An introduction to strings, explaining basic operations like concatenation, substring, etc.",
            "pattern_matching": {
                "naive_pattern_matching": "A simple pattern matching algorithm that checks for the presence of a pattern by sliding it one by one over the text.",
                "rabin_karp": "An efficient hashing-based algorithm for searching multiple patterns at once in a string.",
                "kmp_algorithm": "An efficient string matching algorithm that preprocesses the pattern to avoid redundant comparisons.",
                "boyer_moore": "An algorithm that scans the pattern from right to left and uses mismatches to skip sections of the text.",
                "aho_corasick": "A pattern matching algorithm that builds a state machine to match multiple patterns in parallel."
            },
            "string_manipulations": {
                "concatenation": "Combining two or more strings together to form one string.",
                "substring_search": "Locating a smaller string within a larger string.",
                "reverse_a_string": "Reversing the order of characters in a string.",
                "anagram_detection": "Checking if two strings are permutations of each other.",
                "palindrome_check": "Checking whether a string reads the same forwards and backwards."
            },
            "string_compression": {
                "run_length_encoding": "A basic form of data compression that replaces consecutive repeated characters with a single character and a count.",
                "huffman_encoding": "A variable-length compression algorithm used for reducing the size of text.",
                "lz77_compression": "A lossless data compression algorithm that finds repeating patterns in data.",
                "burrows_wheeler_transform": "A transformation used in compression algorithms to make similar characters group together.",
                "arithmetic_coding": "A coding technique used to encode data into a single number based on probability."
            },
            "trie_data_structure": "A tree-like data structure used to efficiently store and search prefixes of strings."
        }
    },
    "linked_lists": {
        "description": "Linked lists are linear data structures where elements are not stored in contiguous locations, but rather contain pointers to the next node in the sequence.",
        "image": "../static/images/LinkedList.jpg",  # Path to the image
        "video": "https://www.youtube.com/watch?v=R9PTBwOzceo",  # YouTube video URL
        "topics": {
            "introduction": "An introduction to linked lists, explaining basic operations like traversal and insertion.",
            "types_of_linked_lists": {
                "singly_linked_list": "A type of linked list where each node points to the next node in the sequence.",
                "doubly_linked_list": "A type of linked list where each node contains pointers to both the previous and the next nodes.",
                "circular_linked_list": "A linked list where the last node points back to the first node, forming a circular structure."
            },
            "operations_on_linked_lists": {
                "insertion": "Adding an element to a linked list at a specific position.",
                "deletion": "Removing an element from a linked list.",
                "traversal": "Navigating through the elements of a linked list, node by node."
            }
        }
    }
}

@app.route('/')
def home1():
    return render_template('home.html', dsa_content=dsa_content)

@app.route('/api/topic/<topic>')
def get_topic_details(topic):
    if topic in dsa_content:
        return jsonify(dsa_content[topic])
    else:
        return jsonify({"error": "Topic not found"}), 404

@app.route('/topic/<topic>')
def topic_page(topic):
    if topic in dsa_content:
        return render_template('topic.html', topic=topic, details=dsa_content[topic])
    else:
        return render_template('404.html'), 404
    

if __name__ == '__main__':
    app.run(debug=True)