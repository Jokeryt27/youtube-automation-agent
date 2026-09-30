"""
Step 9 - Final User Approval Gate

Publishing is allowed only after explicit human approval.
"""

from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Optional


@dataclass
class ApprovalDecision:
    approved: bool
    reviewer: str
    timestamp: str
    note: Optional[str] = None


def request_approval(
    reviewer: str = "user",
    note: Optional[str] = None,
) -> ApprovalDecision:
    """
    Request explicit human approval from the user.

    Only APPROVE allows the workflow to continue.
    """

    print("\n" + "=" * 50)
    print("FINAL HUMAN APPROVAL REQUIRED")
    print("=" * 50)
    print("The content is ready for the final publishing step.")
    print("Nothing will be published without explicit approval.")
    print()
    print("Type APPROVE to continue.")
    print("Type REJECT to stop.")
    print()

    while True:
        decision = input("Your decision: ").strip().upper()

        if decision == "APPROVE":
            return ApprovalDecision(
                approved=True,
                reviewer=reviewer,
                timestamp=datetime.now(timezone.utc).isoformat(),
                note=note,
            )

        if decision == "REJECT":
            return ApprovalDecision(
                approved=False,
                reviewer=reviewer,
                timestamp=datetime.now(timezone.utc).isoformat(),
                note=note,
            )

        print("Invalid input. Please type APPROVE or REJECT.")


def can_publish(decision: ApprovalDecision) -> bool:
    """
    Return True only when explicit human approval was given.
    """
    return decision.approved is True


def require_approval(
    reviewer: str = "user",
    note: Optional[str] = None,
) -> ApprovalDecision:
    """
    Stop the publishing workflow unless the user explicitly approves.
    """

    decision = request_approval(
        reviewer=reviewer,
        note=note,
    )

    if not can_publish(decision):
        raise PermissionError(
            "Publishing blocked: explicit human approval was not given."
        )

    return decision


if __name__ == "__main__":
    decision = require_approval()

    print("\nApproval recorded.")
    print(f"Reviewer: {decision.reviewer}")
    print(f"Timestamp: {decision.timestamp}")
    print("Publishing is allowed.")
