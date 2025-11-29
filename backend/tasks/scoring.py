from __future__ import annotations
from dataclasses import dataclass
from datetime import date
from typing import List, Dict, Optional


@dataclass
class TaskInput:
    id: str
    title: str
    due_date: Optional[date]
    estimated_hours: Optional[float]
    importance: Optional[int]
    dependencies: List[str]


@dataclass
class ScoredTask:
    task: TaskInput
    score: float
    explanation: str
    has_circular_dependency: bool = False


# -------------------- SCORING HELPERS --------------------

def urgency_score(due: Optional[date]) -> float:
    if due is None:
        return 0.5
    today = date.today()
    days = (due - today).days

    if days < 0:
        return 1.0
    if days == 0:
        return 0.9
    if days <= 3:
        return 0.8
    if days <= 7:
        return 0.6
    return 0.4


def importance_score(value: Optional[int]) -> float:
    if value is None:
        return 0.5
    return max(1, min(value, 10)) / 10


def quickness_score(hours: Optional[float]) -> float:
    if hours is None or hours <= 0:
        return 0.6
    return min(1, 1 / (hours + 1) * 3)


def reverse_dependency_map(tasks: Dict[str, TaskInput]) -> Dict[str, int]:
    count = {tid: 0 for tid in tasks}
    for t in tasks.values():
        for d in t.dependencies:
            if d in count:
                count[d] += 1
    return count


def detect_cycles(tasks: Dict[str, TaskInput]) -> Dict[str, bool]:
    visited = {}
    cycle_map = {tid: False for tid in tasks}

    def dfs(node, stack):
        state = visited.get(node, 0)

        if state == 1:
            for s in stack:
                cycle_map[s] = True
            return

        if state == 2:
            return

        visited[node] = 1
        stack.append(node)
        for dep in tasks[node].dependencies:
            if dep in tasks:
                dfs(dep, stack)
        stack.pop()
        visited[node] = 2

    for tid in tasks:
        if visited.get(tid, 0) == 0:
            dfs(tid, [])

    return cycle_map


# -------------------- MAIN ANALYSIS --------------------

def analyze_tasks(raw_tasks: List[dict], strategy: str = "smart_balance") -> List[ScoredTask]:
    # Convert input to TaskInput objects
    tasks = {}
    for i, rt in enumerate(raw_tasks):
        tid = str(rt.get("id", i))
        tasks[tid] = TaskInput(
            id=tid,
            title=rt["title"],
            due_date=rt.get("due_date"),
            estimated_hours=rt.get("estimated_hours"),
            importance=rt.get("importance"),
            dependencies=[str(x) for x in rt.get("dependencies", [])],
        )

    dep_map = reverse_dependency_map(tasks)
    cycle_map = detect_cycles(tasks)

    scored_list = []

    for tid, t in tasks.items():
        u = urgency_score(t.due_date)
        imp = importance_score(t.importance)
        q = quickness_score(t.estimated_hours)
        # Avoid division by zero even when max dependency weight is 0
        dep_values = list(dep_map.values())
        denominator = max(dep_values) if dep_values else 1
        if denominator == 0:
           denominator = 1

        d = dep_map.get(tid, 0) / denominator




        # Apply strategy
        if strategy == "fastest_wins":
            score = 0.6*q + 0.2*u + 0.2*imp
        elif strategy == "high_impact":
            score = 0.7*imp + 0.2*d + 0.1*u
        elif strategy == "deadline_driven":
            score = 0.7*u + 0.2*imp + 0.1*q
        else:
            score = 0.35*imp + 0.30*u + 0.20*q + 0.15*d

        if cycle_map[tid]:
            score *= 0.7

        explanation = f"Strategy: {strategy}. Importance={imp}, Urgency={u}, Quickness={q}, Dependencies={d}."

        scored_list.append(
            ScoredTask(task=t, score=round(score*100, 2), explanation=explanation, has_circular_dependency=cycle_map[tid])
        )

    scored_list.sort(key=lambda x: x.score, reverse=True)
    return scored_list
