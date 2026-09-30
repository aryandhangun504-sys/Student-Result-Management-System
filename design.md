# Design

All diagrams are written in [Mermaid](https://mermaid.js.org/) and render directly on GitHub.

## 1. System Architecture

Layered design: the UI never touches files directly, and the business logic never prints or reads input.

```mermaid
flowchart TB
    User([User])
    subgraph Presentation
        CLI["cli.py<br/>menus, prompts, tables"]
    end
    subgraph Business["Business Logic"]
        MGR["manager.py<br/>StudentManager (CRUD)"]
        REP["reports.py<br/>ranking and analytics"]
        VAL["validators.py<br/>input rules"]
        GRD["grading.py<br/>grade / result rules"]
        MOD["models.py<br/>Student"]
    end
    subgraph Data["Data Layer"]
        STO["storage.py<br/>CSVStorage"]
        CSV[("data/students.csv")]
    end
    CFG["config.py"]
    LOG["logger.py"]
    LOGF[("logs/srms.log")]

    User <--> CLI
    CLI --> MGR
    CLI --> REP
    CLI --> VAL
    MGR --> VAL
    MGR --> MOD
    MGR --> STO
    REP --> MOD
    MOD --> GRD
    STO --> CSV
    STO --> VAL
    LOG --> LOGF
    CFG -.-> GRD
    CFG -.-> VAL
    CFG -.-> STO
```

## 2. Use Case Diagram

```mermaid
flowchart LR
    T(["Teacher / Coordinator"])
    subgraph SRMS["Student Result Management System"]
        UC1(Add student)
        UC2(View all students)
        UC3(Search by roll no / name)
        UC4(Update marks)
        UC5(Delete student)
        UC6(View rank list)
        UC7(View class report)
        UC8(Save records)
        UC9(Validate input)
        UC10(Calculate grade and result)
    end
    T --- UC1 & UC2 & UC3 & UC4 & UC5 & UC6 & UC7 & UC8
    UC1 -. include .-> UC9
    UC4 -. include .-> UC9
    UC1 -. include .-> UC10
    UC4 -. include .-> UC10
```

## 3. Workflow Diagram

```mermaid
flowchart TD
    A([Start]) --> B[Setup logging]
    B --> C[Load CSV]
    C --> D{Read error?}
    D -- yes --> X[/Show error/] --> Z([Exit 1])
    D -- no --> E[/Show menu/]
    E --> F[/Read choice/]
    F --> G{Choice}
    G -- 1 --> H[Add student]
    G -- 2 --> I[View all]
    G -- 3/4 --> J[Search]
    G -- 5 --> K[Update marks]
    G -- 6 --> L[Delete]
    G -- 7/8 --> M[Rank list / Class report]
    G -- 9 --> N[Save]
    G -- 0 --> O[Save]
    G -- other --> P[/Invalid choice/]
    H & I & J & K & L & M & N & P --> E
    O --> Q{Saved OK?}
    Q -- no --> E
    Q -- yes --> R([Exit])
```

## 4. Sequence Diagram - Add a Student

```mermaid
sequenceDiagram
    actor U as User
    participant C as cli.py
    participant V as validators.py
    participant M as StudentManager
    participant S as CSVStorage

    U->>C: choose "1. Add student"
    loop until valid
        C->>U: ask name
        U->>C: text
        C->>V: validate_name()
        V-->>C: cleaned name / ValidationError
    end
    loop until valid and unique
        C->>U: ask roll number
        U->>C: text
        C->>V: validate_roll_no()
        C->>M: exists(roll_no)?
    end
    loop for each of 5 subjects
        C->>U: ask marks
        U->>C: text
        C->>V: validate_marks()
    end
    C->>M: add(roll_no, name, marks)
    M->>M: build Student (dirty = True)
    M-->>C: Student
    C->>U: show result card
    Note over U,S: Data reaches disk only on Save / Save and exit
    U->>C: choose "0. Save and exit"
    C->>M: save()
    M->>S: save(students)
    S->>S: write temp file, os.replace()
    S-->>C: OK
```

## 5. Class / Component Diagram

```mermaid
classDiagram
    class Student {
        +str roll_no
        +str name
        +List~int~ marks
        +total() int
        +percentage() float
        +grade() str
        +result() str
        +subject_marks() dict
    }
    class StudentManager {
        -dict _students
        +bool dirty
        +load() int
        +save() int
        +add(roll_no, name, marks) Student
        +get(roll_no) Student
        +exists(roll_no) bool
        +search_by_name(query) list
        +update_marks(roll_no, marks) Student
        +delete(roll_no) Student
        +all() list
    }
    class CSVStorage {
        +Path path
        +int skipped_rows
        +load() list
        +save(students)
    }
    class SRMSError
    class ValidationError
    class DuplicateStudentError
    class StudentNotFoundError
    class StorageError

    StudentManager "1" --> "*" Student : manages
    StudentManager --> CSVStorage : persists via
    CSVStorage ..> Student : creates
    SRMSError <|-- ValidationError
    SRMSError <|-- DuplicateStudentError
    SRMSError <|-- StudentNotFoundError
    SRMSError <|-- StorageError
```

Module-level function groups (no state, so not classes): `grading` (total, percentage, grade, result), `validators` (name, roll number, marks), `reports` (rank list, averages, distribution, summary), `cli` (menu actions).

## 6. Storage Design (ER Diagram)

Storage is a single CSV file, so there is one entity. Marks are stored one column per subject.

```mermaid
erDiagram
    STUDENT {
        string roll_no PK "unique, upper-case, max 20 chars"
        string name "letters, spaces . ' -, max 50"
        int Physics "0-100"
        int Maths "0-100"
        int Python "0-100"
        int Electronics "0-100"
        int English "0-100"
    }
```

`total`, `percentage`, `grade` and `result` are **derived** at run time and deliberately not stored, so they can never become inconsistent with the marks.

**Schema (`data/students.csv`)**
```
roll_no,name,Physics,Maths,Python,Electronics,English
21BCE001,Asha Rao,92,88,95,90,85
```

## 7. Design Decisions and Rationale

| Decision | Alternatives considered | Why this choice |
|----------|-------------------------|-----------------|
| Layered modules (UI / logic / storage) | Single script (the original version) | Logic can be unit-tested without keyboard input; storage can be swapped (e.g. SQLite) without touching the UI |
| `Student` stores only roll no, name, marks; other values are properties | Store total/percentage/grade in the object and the file | No stale or inconsistent values after an update |
| Dictionary keyed by roll number | List + linear search | O(1) look-up, and duplicates are impossible by construction |
| `csv` module | Manual `",".join()` / `split(",")` | Correctly handles quoting; the original approach breaks if a name contains a comma |
| Atomic save (temp file + `os.replace`) | Write directly to the file | A crash mid-write cannot leave a half-written data file |
| Skip and log corrupt rows | Crash / silently ignore | The app stays usable and the user is warned |
| Custom exception hierarchy | Return codes / bare `print` | Callers handle each failure precisely; one `except SRMSError` covers all expected errors |
| Percentage computed as `total * 100 / max_total` | `total / max * 100` | Integer arithmetic first avoids floating-point errors at grade boundaries (e.g. 57% computing as 56.999...) |
| Grade depends on percentage; PASS/FAIL on per-subject minimum | Force grade F when failing | Matches the original program's rules; a student can therefore be "B" and "FAIL" if one subject is below 40 |
| Roll numbers normalised to upper case | Case-sensitive | `21bce001` and `21BCE001` cannot become two different students |
| Standard library only | `pandas`, `rich`, SQLite | Zero installation effort; enough for the problem size |
