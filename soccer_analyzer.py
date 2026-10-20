"""Interactive soccer team performance analyzer."""

from pathlib import Path


def prompt_text(message):
    """Ask until the user enters non-empty text."""
    while True:
        value = input(message).strip()
        if value:
            return value
        print("Please enter a value.")


def prompt_positive_int(message):
    """Ask until the user enters a whole number greater than zero."""
    while True:
        try:
            value = int(input(message))
            if value > 0:
                return value
            print("Please enter a number greater than zero.")
        except ValueError:
            print("Please enter a whole number.")


def prompt_non_negative_int(message):
    """Ask until the user enters a whole number that is zero or greater."""
    while True:
        try:
            value = int(input(message))
            if value >= 0:
                return value
            print("Goals cannot be negative.")
        except ValueError:
            print("Please enter a whole number.")


def collect_matches(match_count):
    """Collect the opponent and score for every match."""
    matches = []
    for number in range(1, match_count + 1):
        print(f"\nMatch {number}")
        opponent = prompt_text("Opponent: ")
        goals_for = prompt_non_negative_int("Goals scored by your team: ")
        goals_against = prompt_non_negative_int("Goals scored by the opponent: ")
        matches.append(
            {
                "opponent": opponent,
                "goals_for": goals_for,
                "goals_against": goals_against,
            }
        )
    return matches


def analyze_matches(team_name, matches):
    """Calculate the team record and summary statistics."""
    if not matches:
        raise ValueError("At least one match is required.")

    wins = draws = losses = 0
    goals_for = goals_against = clean_sheets = 0
    form = []

    for match in matches:
        scored = match["goals_for"]
        conceded = match["goals_against"]
        goals_for += scored
        goals_against += conceded

        if conceded == 0:
            clean_sheets += 1

        if scored > conceded:
            wins += 1
            form.append("W")
        elif scored == conceded:
            draws += 1
            form.append("D")
        else:
            losses += 1
            form.append("L")

    best_match = max(
        matches,
        key=lambda match: (
            match["goals_for"] - match["goals_against"],
            match["goals_for"],
        ),
    )
    played = len(matches)

    return {
        "team": team_name,
        "played": played,
        "wins": wins,
        "draws": draws,
        "losses": losses,
        "points": wins * 3 + draws,
        "goals_for": goals_for,
        "goals_against": goals_against,
        "goal_difference": goals_for - goals_against,
        "average_goals": goals_for / played,
        "clean_sheets": clean_sheets,
        "form": "-".join(form),
        "best_match": best_match,
    }


def format_report(report):
    """Create a readable report from the calculated statistics."""
    best = report["best_match"]
    return (
        "Soccer Team Performance Report\n"
        f"Team: {report['team']}\n"
        f"Record: {report['wins']} wins, {report['draws']} draws, "
        f"{report['losses']} losses\n"
        f"Points: {report['points']}\n"
        f"Goals: {report['goals_for']} for, {report['goals_against']} against, "
        f"difference {report['goal_difference']:+d}\n"
        f"Average goals scored: {report['average_goals']:.2f}\n"
        f"Clean sheets: {report['clean_sheets']}\n"
        f"Form: {report['form']}\n"
        f"Best result: {best['goals_for']}-{best['goals_against']} "
        f"vs {best['opponent']}"
    )


def save_report(report_text, filename="soccer_report.txt"):
    """Save the report so it can be shared with the team."""
    path = Path(filename)
    path.write_text(report_text + "\n", encoding="utf-8")
    return path


def main():
    """Run the interactive soccer analysis program."""
    print("Soccer Team Performance Analyzer")
    team_name = prompt_text("Team name: ")
    match_count = prompt_positive_int("How many matches will you enter? ")
    matches = collect_matches(match_count)
    report = analyze_matches(team_name, matches)
    report_text = format_report(report)
    print("\n" + report_text)
    saved_path = save_report(report_text)
    print(f"\nReport saved to {saved_path.resolve()}")


if __name__ == "__main__":
    main()
