"""make.fun bounty entry: "Have You Tried Turning It Off?".

The entry is one funny line, 1-199 characters, that a hopeless tech
support agent says to a desperate customer:

    I know, I know — have you tried turning it off and on again?
    That's my entire training, so we're in this together.

Three candidates were compared against the judge's brief before this
one was chosen:

1. CHOSEN -- "I know, I know — have you tried turning it off and
   on again? That's my entire training, so we're in this together."
   (114 characters). It wins because it hits every criterion in
   order. It is unmistakably a real support agent's line, opening
   with the classic "turn it off and on again". The twist lands on
   the second sentence: the classic is not one trick among many, it
   is the agent's *entire training*. The humour comes from the
   agent's cheerful uselessness -- he admits he knows nothing else
   and then, instead of panicking, offers solidarity -- and the
   customer is never the butt of it; the agent is. The customer's
   desperation is felt, not explained: "I know, I know" is the
   sound of an agent who has heard the frustration before he has
   even finished the sentence. It is tight -- every clause earns
   its place -- and clear on a first read.

2. REJECTED -- "Let's turn it off and on again together, slowly,
   like we're defusing something." (79 characters). It is vivid,
   but it loses on criterion 2: the humour comes from a bomb
   metaphor, not from the agent's cheerful uselessness, and the
   agent sounds oddly competent -- like someone defusing a bomb --
   rather than hopeless. The customer's desperation is only
   implied by the image, and the classic line is dressed up
   instead of twisted.

3. REJECTED -- "Don't worry, I've turned it off and on again
   three times today and I'm still here, so technically we're
   winning." (112 characters). It has the right cheerful
   uselessness, but it loses on criteria 3 and 4: "technically
   we're winning" is vague and needs a second read to parse,
   "three times today" spends words without adding a laugh, and
   the customer's desperation is nowhere to be felt -- the agent
   is talking about himself, not answering someone in distress.

The chosen line is built from named parts below, so the setup, the
twist and the landing each stay readable on their own, and the entry
is checked against the 1-199 character gate before anything is
written.
"""

import os

# --- Named parts of the line -------------------------------------------
# The setup: the agent hears the customer's frustration before the
# customer has finished -- "I know, I know" makes the desperation
# felt rather than explained.
SETUP = "I know, I know"

# The classic line itself, exactly as a real support agent says it.
# It is the bait: every reader recognises it instantly.
CLASSIC = "have you tried turning it off and on again?"

# The twist: the classic is not one trick among many. It is all the
# agent was ever taught -- cheerful, total uselessness, confessed.
# (TWIST itself is assembled from TWIST_SUBJECT and TWIST_SCOPE
# below, beside the landing, so the two halves of the punchline
# sit next to each other.)

# The landing: solidarity instead of a solution. The agent cannot
# fix anything, so he offers the only thing he has -- company.
# Split into the connector and the promise so each half of the
# punchline stays visible on its own.
LANDING_CONNECTOR = "so"
LANDING_PROMISE = "we're in this together."
LANDING = LANDING_CONNECTOR + " " + LANDING_PROMISE

# The twist, split the same way: what the training was, and how
# much of it there was. "Entire" is the word that does the work --
# without it, the line is just a shrug.
TWIST_SUBJECT = "That's my"
TWIST_SCOPE = "entire training"
TWIST = TWIST_SUBJECT + " " + TWIST_SCOPE

# Where the judged text goes. The grader reads this file.
OUTPUT_PATH = "/output/entry.txt"

# The gate from the kit rules: a valid entry is 1-199 characters.
MIN_LENGTH = 1
MAX_LENGTH = 199

# The chosen line, counted by hand and by machine: 114 characters.
# This is a tripwire, not a target -- if a later edit changes the
# wording, this check fails loudly instead of silently shipping a
# different joke from the one the comparison above chose.
EXPECTED_LENGTH = 114
# 23 space-separated tokens: 22 words plus the em dash standing
# alone between the setup and the classic question.
EXPECTED_WORDS = 23


def build_line(setup, classic, twist, landing):
    """Join the line's parts into one line, a sentence and nothing else.

    The setup and the classic are joined with an em dash, exactly as
    the chosen line reads: "I know, I know -- have you tried ...".
    (The docstring above spells it with two hyphens only so the
    comparison text stays plain ASCII; the built line uses the real
    em dash character.)
    """
    first = setup + " \u2014 " + classic
    second = twist + ", " + landing
    return first + " " + second


def check_line(line):
    """Assert the line is a single valid entry: 1-199 chars, not blank."""
    if not isinstance(line, str):
        raise TypeError("line must be a string")
    if line != line.strip():
        raise ValueError("line must not have leading or trailing space")
    if not MIN_LENGTH <= len(line) <= MAX_LENGTH:
        raise ValueError(
            "line must be %d-%d characters, got %d"
            % (MIN_LENGTH, MAX_LENGTH, len(line))
        )
    if not line.strip():
        raise ValueError("line must not be only whitespace")
    return line


def check_single_line(line):
    """Second validation: the entry is one line, not a paragraph.

    A support agent says one line. Any newline, tab or carriage
    return would split it, and the judge compares single lines, so
    the entry must contain none of them.
    """
    if "\n" in line or "\r" in line or "\t" in line:
        raise ValueError("line must be a single line, no newlines or tabs")
    return line


def check_no_wasted_space(line):
    """Third validation: every word earns its place, so no double spaces.

    Double spaces are dead weight in a line that must stay tight
    enough to land on a first read.
    """
    if "  " in line:
        raise ValueError("line must use single spaces between words")
    if line != " ".join(line.split(" ")):
        raise ValueError("line must not contain irregular spacing")
    return line


def check_reads_like_agent_line(line):
    """Fourth validation: it must sound like one thing a real agent says.

    Two short sentences, spoken in one breath: the classic question
    first, then the confession. It must end with a full stop, not
    trail off, and it must be short enough to say aloud -- a
    handful of words, not a speech.
    """
    words = line.split(" ")
    if not 10 <= len(words) <= 40:
        raise ValueError("line should be a spoken line, got %d words" % len(words))
    if not line.endswith("."):
        raise ValueError("line must end with a full stop")
    if line.count("?") != 1:
        raise ValueError("line must ask exactly one question, the classic one")
    if line.count(".") != 1:
        raise ValueError("line must end with a single full stop")
    return line


def check_twist_present(line):
    """Fifth validation: the classic line is there, and so is its twist.

    Without "turning it off and on again" there is no classic to
    twist; without "entire training" there is no twist, only the
    stock line the brief warns against. Both halves must survive
    any later edit, or the joke is gone.
    """
    if "turning it off and on again" not in line:
        raise ValueError("line must contain the classic restart line")
    if "entire training" not in line:
        raise ValueError("line must contain the twist: entire training")
    if "we're in this together" not in line:
        raise ValueError("line must land on solidarity, not a solution")
    return line


def check_exact_shape(line):
    """Sixth validation: the built line is exactly the chosen line.

    Length and word count are pinned to the line the candidate
    comparison chose. Any edit that adds, drops or swaps a word
    changes the joke, so it must fail here rather than ship.
    """
    if len(line) != EXPECTED_LENGTH:
        raise ValueError(
            "line must be %d characters, got %d"
            % (EXPECTED_LENGTH, len(line))
        )
    if len(line.split(" ")) != EXPECTED_WORDS:
        raise ValueError(
            "line must be %d space-separated tokens, got %d"
            % (EXPECTED_WORDS, len(line.split(" ")))
        )
    return line


def write_entry(line, path=OUTPUT_PATH):
    """Write exactly the line to the output file, creating its folder."""
    directory = os.path.dirname(path)
    if directory:
        os.makedirs(directory, exist_ok=True)
    with open(path, "w", encoding="utf-8") as handle:
        handle.write(line)
    return path


# Build the line, then run every check in order: the gate first,
# then the shape of a single spoken line, then the joke itself.
LINE = check_exact_shape(
    check_twist_present(
        check_reads_like_agent_line(
            check_no_wasted_space(
                check_single_line(
                    check_line(build_line(SETUP, CLASSIC, TWIST, LANDING))
                )
            )
        )
    )
)


def main():
    """Write the entry and print it, so both outputs always match."""
    write_entry(LINE)
    print(LINE)
    return LINE


if __name__ == "__main__":
    main()
