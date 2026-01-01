# Research: Phase I - In-Memory Console App

**Feature**: 001-phase1-console-app
**Created**: 2026-01-01
**Purpose**: Technical research and decision documentation for Phase I implementation

## Research Summary

This document consolidates all technical research findings that informed the Phase I architecture and design decisions documented in [plan.md](./plan.md).

## Research Topics

### 1. Python CLI Patterns for Interactive Applications

**Question**: What's the best approach for building an interactive CLI todo app in Python?

**Options Evaluated**:

| Approach | Pros | Cons | Verdict |
|:---------|:-----|:-----|:--------|
| Standard `input()` loop | No dependencies, simple, testable | Manual parsing required | ✅ **SELECTED** |
| `argparse` | Built-in, structured | Better for one-shot commands | ❌ Not ideal for interactive |
| `click` / `typer` | Rich features, decorators | External dependency | ❌ Overkill for Phase I |
| `cmd` module | Built-in command framework | More complex, more LOC | ❌ Unnecessary structure |
| `prompt_toolkit` | Advanced features (autocomplete) | Heavy dependency | ❌ Too complex |

**Decision**: Use standard library `input()` with command loop pattern

**Rationale**:
- Aligns with constitution principle "Simplest viable change"
- No external dependencies (Phase I constraint)
- Easy to test with mocked input/output
- Sufficient for basic command interface
- Can upgrade to richer CLI in later phases if needed

**Code Pattern**:
```python
def run(self):
    while True:
        command = input("todo> ").strip().lower()
        if command == "add":
            self.handle_add()
        elif command == "list":
            self.handle_list()
        # ...
```

**References**:
- Python documentation: `input()` built-in function
- PEP 20: "Simple is better than complex"

---

### 2. In-Memory Storage Data Structures

**Question**: What data structure should we use for storing tasks in memory?

**Options Evaluated**:

| Structure | Lookup | Insert | Delete | Memory | Verdict |
|:----------|:-------|:-------|:-------|:-------|:--------|
| `list[Task]` | O(n) | O(1) | O(n) | Low | ✅ **SELECTED** |
| `dict[int, Task]` | O(1) | O(1) | O(1) | Medium | ❌ Premature optimization |
| `deque` | O(n) | O(1) | O(n) | Low | ❌ No clear benefit |
| Custom BST | O(log n) | O(log n) | O(log n) | High | ❌ Massive overkill |

**Decision**: Use `list[Task]` with linear search by ID

**Rationale**:
- Spec requires support for 1000 tasks maximum
- O(n) operations acceptable for this scale (~1ms per lookup)
- Preserves insertion order (natural chronological display)
- Simplest to implement and understand
- Minimal memory overhead
- Easy to test
- Can optimize to dict in Phase II if needed (unlikely)

**Performance Analysis**:
```
Task count: 1000
Lookup time (O(n)): ~1ms on modern hardware
Memory per task: ~1KB → 1MB total for 1000 tasks
Success criteria: <1 second for view operations → easily met
```

**Future Consideration**: Phase II will use database with indexed lookups; in-memory structure becomes irrelevant.

**References**:
- Python list performance: https://wiki.python.org/moin/TimeComplexity
- Success criteria SC-001: View tasks <1 second (easily achievable)

---

### 3. Task Data Model Implementation

**Question**: Should we use dataclass, namedtuple, Pydantic, or plain class for Task?

**Options Evaluated**:

| Approach | Pros | Cons | Verdict |
|:---------|:-----|:-----|:--------|
| `@dataclass` | Clean syntax, type hints, auto methods | Requires Python 3.7+ | ✅ **SELECTED** |
| Plain class | Full control | Boilerplate (`__init__`, `__repr__`) | ❌ Verbose |
| `namedtuple` | Lightweight, immutable | Immutability makes updates harder | ❌ Updates required |
| `Pydantic` | Rich validation | External dependency | ❌ Overkill |
| `attrs` | Similar to dataclass | External dependency | ❌ No advantage |

**Decision**: Use Python `dataclass` with validation in `__post_init__`

**Rationale**:
- Built into Python 3.13 (no external dependency)
- Automatic generation of `__init__`, `__repr__`, `__eq__`
- Type hints integrated naturally
- Validation via `__post_init__` hook
- Mutable (allows updates per spec requirements)
- Readable and Pythonic

**Implementation Pattern**:
```python
from dataclasses import dataclass, field
from datetime import datetime

@dataclass
class Task:
    title: str
    description: str = ""
    is_completed: bool = False
    created_at: datetime = field(default_factory=datetime.now)
    id: int = 0

    def __post_init__(self):
        if not self.title or not self.title.strip():
            raise ValidationError("Title cannot be empty")
        if len(self.title) > 200:
            raise ValidationError("Title cannot exceed 200 characters")
```

**References**:
- PEP 557: Data Classes
- Python 3.13 dataclasses documentation
- Spec requirement FR-001: Title validation

---

### 4. Validation Strategy

**Question**: How should we validate user input and enforce business rules?

**Options Evaluated**:

| Strategy | Pros | Cons | Verdict |
|:---------|:-----|:-----|:--------|
| Exceptions | Pythonic, clear flow | Can be verbose | ✅ **SELECTED** |
| Return None | Simple | Ambiguous (None = not found or error?) | ❌ Unclear |
| Return tuples | Explicit | Verbose, non-idiomatic | ❌ Not Pythonic |
| Assertions | Built-in | Should not be used for validation | ❌ Wrong use case |

**Decision**: Custom exception classes for different error types

**Exception Hierarchy**:
```python
TodoAppError (base)
├── ValidationError (invalid input)
└── TaskNotFoundError (ID not found)
```

**Rationale**:
- Pythonic approach (EAFP: "Easier to Ask for Forgiveness than Permission")
- Clear separation of error types
- Easy to test with `pytest.raises()`
- CLI layer catches and displays user-friendly messages
- Business logic layer remains clean (just raises exceptions)

**Error Handling Flow**:
1. User provides input → CLI layer
2. CLI calls TodoManager method → Business logic layer
3. Business logic validates and raises exception if invalid
4. CLI catches exception and displays formatted error message
5. User sees: "Title cannot be empty (1-200 characters required)"

**References**:
- PEP 8: Exception handling best practices
- Spec requirements: AC-3 error messages

---

### 5. Display Formatting

**Question**: How should we format the task table for CLI display?

**Options Evaluated**:

| Approach | Pros | Cons | Verdict |
|:---------|:-----|:-----|:--------|
| Manual f-strings | No dependency, full control | Manual column alignment | ✅ **SELECTED** |
| `tabulate` library | Beautiful tables | External dependency | ❌ Unnecessary |
| `rich` library | Gorgeous terminal UI | Heavy dependency, overkill | ❌ Too complex |
| CSV format | Parseable | Not readable | ❌ Poor UX |

**Decision**: Manual formatting with f-strings and string methods

**Rationale**:
- No external dependencies (Phase I principle)
- Full control over format
- Testable (predictable string output)
- Sufficient for simple tabular display
- Can upgrade to `rich` in later phases if needed

**Display Format**:
```
ID  | Status | Title                    | Description
----|--------|--------------------------|-------------
1   | [ ]    | Buy groceries            | Milk, eggs, bread
2   | [X]    | Complete Phase I         | Build console app
```

**Implementation Approach**:
```python
def format_task_table(self, tasks: list[Task]) -> str:
    if not tasks:
        return "No tasks found."

    lines = []
    lines.append("ID  | Status | Title                    | Description")
    lines.append("-" * 70)

    for task in tasks:
        display = task.to_display_dict()
        line = f"{display['id']:3} | {display['status']:6} | " \
               f"{display['title']:24} | {display['description']}"
        lines.append(line)

    return "\n".join(lines)
```

**References**:
- Spec requirement FR-005: Visual status indicators
- Success criteria SC-007: Readable format

---

### 6. Testing Framework and Strategy

**Question**: What testing framework should we use, and what's the coverage strategy?

**Options Evaluated**:

| Framework | Pros | Cons | Verdict |
|:----------|:-----|:-----|:--------|
| `pytest` | Rich features, fixtures, plugins | External dep (acceptable) | ✅ **SELECTED** |
| `unittest` | Built-in | Verbose, class-based | ❌ Less ergonomic |
| `nose2` | Similar to pytest | Less popular | ❌ Smaller ecosystem |

**Decision**: pytest with unit + integration test separation

**Rationale**:
- Industry standard for Python testing
- Fixture support for setup/teardown
- Parametrized testing (test multiple scenarios efficiently)
- Coverage plugin integration (`pytest-cov`)
- Clear, readable test output
- Mocking support for CLI tests

**Test Organization**:
```
tests/
├── unit/
│   ├── test_models.py      # Task dataclass tests
│   ├── test_manager.py     # TodoManager business logic tests
│   └── test_cli.py         # CLI parsing tests (mocked I/O)
└── integration/
    └── test_workflows.py   # End-to-end user journey tests
```

**Coverage Strategy**:
- **Target**: 90% (constitutional requirement TC-008)
- **Unit tests**: Each method tested in isolation
- **Integration tests**: Complete user workflows (add → view → toggle → update → delete)
- **Edge cases**: Empty list, 1000 tasks, invalid input, boundary conditions
- **Mocking**: Mock `input()` and `print()` for CLI tests

**Test Development Approach**:
- Write tests first for TDD (where applicable)
- At minimum, write tests immediately after implementation
- Run coverage reports incrementally: `pytest --cov=src/todo_app --cov-report=html`
- Review `htmlcov/index.html` to identify uncovered lines

**References**:
- pytest documentation
- Constitution requirement: 90% test coverage
- Spec: All acceptance criteria must be verifiable via tests

---

### 7. Error Messages and User Experience

**Question**: What error messages should we display, and how should they be formatted?

**Research Findings**:

**CLI UX Best Practices**:
1. Clear, actionable error messages
2. Consistent formatting
3. No technical jargon or stack traces
4. Suggest corrective action when possible
5. Confirm successful operations

**Error Message Catalog** (from spec AC-3):

| Error Scenario | Message | Spec Reference |
|:---------------|:--------|:---------------|
| Empty title | "Title cannot be empty (1-200 characters required)" | AC-1 |
| Title too long | "Title cannot exceed 200 characters" | AC-1 |
| Task not found | "Task ID not found" | AC-3 |
| Invalid input | "Invalid command. Type 'help' for available commands." | Implied |
| Unexpected error | "Unexpected error: {message}" | Error handling |

**Success Message Catalog** (from spec FR-013):

| Operation | Message Format | Spec Reference |
|:----------|:---------------|:---------------|
| Add task | "Task '[title]' added with ID [N]" | AC-1 |
| Update task | "Task [N] updated" | AC-3 |
| Toggle task | "Task [N] marked as Complete/Incomplete" | AC-3 |
| Delete task | "Task [N] deleted" | AC-3 |
| View empty | "No tasks found." | AC-2 |

**Implementation**:
```python
def display_error(self, message: str) -> None:
    """Display error message to user."""
    print(f"❌ Error: {message}")

def display_success(self, message: str) -> None:
    """Display success message to user."""
    print(f"✅ {message}")
```

**References**:
- Spec requirement FR-013: Confirmation messages
- UX principle: Clear feedback for every action

---

### 8. ID Generation Strategy

**Question**: How should we assign unique IDs to tasks?

**Options Evaluated**:

| Strategy | Pros | Cons | Verdict |
|:---------|:-----|:-----|:--------|
| Auto-increment counter | Simple, predictable | IDs not reused after delete | ✅ **SELECTED** |
| UUID | Globally unique | Overkill, not user-friendly | ❌ Too complex |
| Timestamp | Unique (usually) | Not user-friendly | ❌ Poor UX |
| Re-use deleted IDs | Saves space | Complex, confusing | ❌ Bad UX |

**Decision**: Auto-incrementing integer starting from 1

**Rationale**:
- Spec requirement FR-002: "Unique, auto-incrementing integer ID"
- User-friendly: Easy to reference ("toggle task 5")
- Predictable for testing
- Simple to implement: `self._next_id += 1`
- IDs never reused (even after delete) - clearer semantics

**Implementation**:
```python
class TodoManager:
    def __init__(self):
        self._tasks: list[Task] = []
        self._next_id: int = 1

    def add_task(self, title: str, description: str = "") -> Task:
        task = Task(title=title, description=description)
        task.id = self._next_id
        self._next_id += 1
        self._tasks.append(task)
        return task
```

**ID Behavior After Delete**:
- Task 1 created → ID=1
- Task 2 created → ID=2
- Task 1 deleted → Next task gets ID=3 (not reusing 1)
- Rationale: Simpler logic, no ID confusion

**Future Evolution**:
- Phase II (multi-user): Composite keys (user_id, task_id) or UUIDs
- Phase III+ (distributed): UUIDs for global uniqueness

**References**:
- Spec requirement FR-002
- Spec requirement AC-1: "System assigns unique ID"

---

### 9. Module Organization and Package Structure

**Question**: How should we organize the Python package for maintainability?

**Research Findings**:

**Python Package Best Practices**:
1. Use `src/` layout (not flat structure)
2. Separate concerns into modules
3. Keep modules focused and cohesive
4. Tests mirror source structure

**Selected Structure**:
```
todo-console/
├── src/
│   └── todo_app/          # Main package
│       ├── __init__.py    # Package initialization
│       ├── models.py      # Data model (Task, exceptions)
│       ├── manager.py     # Business logic (TodoManager)
│       ├── cli.py         # CLI interface (TodoCLI)
│       └── main.py        # Entry point
└── tests/
    ├── unit/              # Unit tests (one module = one test file)
    └── integration/       # Integration tests (workflows)
```

**Rationale**:
- `src/` layout prevents accidental imports of uninstalled package
- Each module has single responsibility (SRP)
- Clear separation: data → logic → interface → entry point
- Easy to test: Each module independently testable
- Future-proof: Easy to add modules in Phase II (api.py, database.py)

**Module Responsibilities**:

| Module | Responsibility | Dependencies |
|:-------|:---------------|:-------------|
| `models.py` | Data structures, validation | stdlib only |
| `manager.py` | Business logic, storage | models.py |
| `cli.py` | User interface, I/O | models.py, manager.py |
| `main.py` | Initialization, wiring | manager.py, cli.py |

**Import Hierarchy** (no circular dependencies):
```
main.py
  ↓
cli.py ← manager.py
  ↓         ↓
  └→ models.py ←┘
```

**References**:
- Packaging Python Projects (Python.org)
- PEP 420: Implicit Namespace Packages
- Constitution principle: Clean code, separation of concerns

---

### 10. Performance Profiling (1000 Tasks Scenario)

**Question**: Can we meet performance requirements with chosen architecture?

**Performance Target** (from spec):
- SC-001: View 1000 tasks in <1 second
- SC-004: Handle 1000+ tasks without degradation
- Individual operations: <100ms

**Theoretical Analysis**:

| Operation | Complexity | 1000 Tasks | Meets Requirement? |
|:----------|:-----------|:-----------|:-------------------|
| Add task | O(1) | ~0.001ms | ✅ Yes (<100ms) |
| Get all | O(n) | ~1ms | ✅ Yes (<1 second) |
| Get by ID | O(n) | ~0.5ms | ✅ Yes (<100ms) |
| Update | O(n) | ~0.5ms | ✅ Yes (<100ms) |
| Toggle | O(n) | ~0.5ms | ✅ Yes (<100ms) |
| Delete | O(n) | ~0.5ms | ✅ Yes (<100ms) |

**Assumptions**:
- Modern hardware (2+ GHz CPU)
- Python 3.13 performance improvements
- In-memory operations (no I/O)
- Simple dataclass objects (~1KB each)

**Memory Profile**:
- 1000 tasks × 1KB/task = ~1MB memory
- Well within constraint (<100MB)

**Conclusion**: ✅ **All performance requirements easily met**

**Verification Plan**:
- Integration test with 1000 tasks (test_edge_case_1000_tasks)
- Measure actual timings during testing
- If issues found (unlikely), optimize with dict lookup

**References**:
- Success criteria SC-001, SC-004
- Python list performance characteristics

---

## Research Conclusions

### Summary of Key Decisions

1. **CLI Pattern**: Standard `input()` loop (no external framework)
2. **Storage**: Python `list[Task]` with O(n) operations
3. **Data Model**: `@dataclass` with `__post_init__` validation
4. **Validation**: Custom exception hierarchy (ValidationError, TaskNotFoundError)
5. **Display**: Manual f-string formatting (no external library)
6. **Testing**: pytest with 90% coverage target
7. **Error Messages**: Clear, actionable, user-friendly
8. **ID Generation**: Auto-increment integer (no reuse)
9. **Module Structure**: `src/` layout with separation of concerns
10. **Performance**: O(n) acceptable for 1000 tasks

### Alignment with Constitution

✅ **Principle V**: No Manual Coding - All code generated from specs/plan/tasks
✅ **Simplicity**: Smallest viable change, no premature optimization
✅ **Clean Code**: PEP 8, type hints, docstrings, 90% test coverage
✅ **Iterative Evolution**: Phase I architecture supports Phase II+ extensions

### Risk Mitigation

All identified risks have mitigation strategies:
- Performance: Validated through analysis and testing
- Input validation: Comprehensive test coverage
- Test coverage: Incremental measurement
- Platform compatibility: Standard library only

### Ready for Implementation

All technical unknowns resolved. Ready to proceed with:
1. `/sp.tasks` - Generate atomic task breakdown
2. Implementation following quickstart.md guide
3. Verification against spec.md acceptance criteria

---

**Research Status**: ✅ Complete

**Next Steps**: Generate tasks.md with `/sp.tasks` command
