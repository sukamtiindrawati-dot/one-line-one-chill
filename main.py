#!/usr/bin/env python3
"""One Line, One Chill — score six horror lines against the judge's brief
and write the winner to /output/entry.txt.

Judge criteria, most important first (weights 5/4/3/2/1):
  1. frightens: dread that outlasts the line, earned not announced (5)
  2. vivid: concrete images and specific detail (4)
  3. original: a turn or image not met a hundred times (3)
  4. crafted: tight sentence, rhythm builds, last word lands the blow (2)
The on-subject gate (a horror line, one sentence) is checked separately:
every candidate below passes it, or it scores 0.

Gate for the output: UTF-8, 1-200 characters, a single line.
"""

import os
import sys

# (line, fright, vivid, original, crafted) — scores 1-5 each.
CANDIDATES = [
    (
        "The baby monitor whispered my name in my mother's voice, "
        "and my mother has been dead for eleven years.",
        4, 4, 3, 4,
    ),
    (
        "I found my own obituary folded inside my coat pocket, dated "
        "tomorrow, in handwriting I recognized as mine.",
        5, 4, 5, 4,
    ),
    (
        "The house has been empty for a year, but every morning the "
        "kettle is still warm and one cup is always missing.",
        4, 4, 3, 3,
    ),
    (
        "My daughter drew our family again tonight, and this time she "
        "drew the thing standing behind me, smiling with my teeth.",
        5, 5, 4, 5,
    ),
    (
        "The voicemail was from my own number, recorded at 3 a.m., and "
        "it was me begging myself not to answer the door.",
        4, 4, 4, 4,
    ),
    # Seventh candidate, added on revision: strong dread, but the image
    # is thinner than the winner's (no face, no teeth), so it loses on
    # vivid despite matching the winner on fright.
    (
        "Every night the attic whispers the names of my children, and "
        "I have never had children.",
        5, 3, 4, 4,
    ),
    # REJECTED DRAFT — mirror cliché: the brief names the mirror as one
    # of the obvious images ("not the obvious mirror, doll or basement"),
    # so it loses on originality whatever its other scores say.
    (
        "The mirror showed me sleeping, but I was standing right in "
        "front of it, wide awake, watching myself sleep.",
        3, 3, 1, 3,
    ),
]

WEIGHTS = (5, 4, 3, 2)  # fright, vivid, original, crafted


def score(candidate):
    line, fright, vivid, original, crafted = candidate
    return sum(w * s for w, s in zip(WEIGHTS, (fright, vivid, original, crafted)))


def main():
    ranked = sorted(CANDIDATES, key=score, reverse=True)
    winner, winner_score = ranked[0][0], score(ranked[0])
    runner_up = ranked[1][0]
    assert winner != runner_up, "winner and runner-up must differ"
    # Gate: UTF-8, 1-200 characters, a single line, one sentence.
    assert 1 <= len(winner) <= 200, f"winner is {len(winner)} chars"
    assert "\n" not in winner, "winner must be one line"
    assert winner.endswith("."), "winner must be one sentence"
    out_dir = "/output"
    os.makedirs(out_dir, exist_ok=True)
    with open(os.path.join(out_dir, "entry.txt"), "w", encoding="utf-8") as f:
        f.write(winner)
    print(f"winner ({len(winner)} chars, score {winner_score}): {winner}")
    print(f"runner-up (score {score(ranked[1])}): {runner_up}")


if __name__ == "__main__":
    main()
