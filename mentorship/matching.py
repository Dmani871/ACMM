"""
Gale-Shapley Stable Matching Algorithm for Mentor-Mentee Matching

This module implements the Gale-Shapley algorithm to create stable matches
between mentors and mentees based on preference rankings.

Algorithm Guarantees:
- Stable: No mentee-mentor pair would both prefer each other over their current match
- Deterministic: Always produces the same result for the same input
- Efficient: O(n²) time complexity where n is number of mentees/mentors
- Mentee-optimal: Each mentee gets their best possible stable match

Reference: https://en.wikipedia.org/wiki/Gale%E2%80%93Shapley_algorithm
"""

import logging
from collections import defaultdict
from typing import Dict, List, Optional, Tuple

import numpy as np

logger = logging.getLogger("mentorship.matching")


def apply_matches_weights(mentors, mentees) -> Dict[int, Dict[int, float]]:
    """
    Calculate compatibility scores between each mentee-mentor pair.

    Args:
        mentors: List of mentor objects with attributes:
            - id: unique identifier
            - year_applied: graduation/postgrad stage
            - area_of_support: list of support areas
            - interview_experience: list of past interviews
            - entrance_exam_experience: list of exams
            - wp_scheme: bool, whether used widening participation scheme
            - applied_before: bool, whether applied in previous cycle

        mentees: List of mentee objects with same structure

    Returns:
        Dict mapping mentee_id → {mentor_id → compatibility_score}

    Scoring Logic:
        1. Base rank: 10
        2. Stage match: ×2 if same year_applied
        3. Support overlap: number of matching support areas
        4. Interview factor: mentor's interview experience count
        5. Exam factor: overlapping exam experiences
        6. Penalties: Low scores if mentee needs support mentor can't provide
        7. Amplification: ×10 for critical support areas (Interview, Exam)
        8. Scheme bonus: ×1.3 if both used WP scheme or both applied before
        9. Disadvantage penalty: ×0.01 if mentee has family support or not state-educated
    """
    logger.info(
        "Starting compatibility score calculation for %d mentees and %d mentors",
        len(mentees),
        len(mentors),
    )
    mentee_preferences = defaultdict(dict)

    for mentee in mentees:
        logger.debug("Calculating scores for mentee %d", mentee.id)
        rankings = {}

        for mentor in mentors:
            # Start with base ranking
            ranking = 10

            # FACTOR 1: Stage alignment (same stage = more relatable mentor)
            if mentor.year_applied == mentee.year_applied:
                ranking *= 2

            # FACTOR 2: Area of support overlap
            # How many support areas do they have in common?
            support_factor = len(
                np.intersect1d(mentor.area_of_support, mentee.area_of_support)
            )

            # FACTOR 3: Mentor's interview experience (quantified)
            interview_factor = len(mentor.interview_experience)

            # FACTOR 4: Exam experience overlap
            exam_factor = len(
                np.intersect1d(
                    mentor.entrance_exam_experience, mentee.entrance_exam_experience
                )
            )

            # VALIDATION: Ensure mentor can support required areas
            # If mentee needs exam help but mentor has no exam experience → incompatible
            # If mentee needs interview help but mentor has no interview experience → incompatible
            needs_exam_support = "EE" in mentee.area_of_support
            needs_interview_support = "I" in mentee.area_of_support

            if (needs_exam_support and exam_factor == 0) or (
                needs_interview_support and interview_factor == 0
            ):
                # Severely penalize incompatible pairings
                support_factor = 0.01

            # AMPLIFICATION: Critical support areas are worth more
            if needs_exam_support:
                exam_factor *= 10

            if needs_interview_support:
                interview_factor *= 10

            # FACTOR 5: Mentor compatibility factor
            # Based on their experience in mentee's needed areas
            mentor_factor = 1 + ((exam_factor + interview_factor) * 5)

            # FACTOR 6: Shared experience bonus
            # If both have been through same pathways, they understand each other better
            both_used_wp_scheme = mentee.wp_scheme and mentor.wp_scheme
            both_applied_before = mentee.applied_before and mentor.applied_before

            if both_used_wp_scheme or both_applied_before:
                mentor_factor *= 1.3

            # Calculate final ranking for this mentor-mentee pair
            ranking = ranking * support_factor * mentor_factor

            # PENALTY: Mentees with family support/private education need less help
            # (algorithm should prioritize mentees with more need)
            if mentee.family_support or not mentee.state_educated:
                ranking *= 0.01

            # Only add mentor to mentee's preference list if viable match
            if ranking > 0:
                rankings[mentor.id] = ranking
                logger.debug(
                    "Mentee %d - Mentor %d: ranking = %.2f (support_factor=%.2f, mentor_factor=%.2f)",
                    mentee.id,
                    mentor.id,
                    ranking,
                    support_factor,
                    mentor_factor,
                )

        # Store all rankings for this mentee
        mentee_preferences[mentee.id] = rankings

    logger.info("Completed compatibility score calculation")
    return dict(mentee_preferences)


def stable_matching(
    mentee_preferences: Dict[int, Dict[int, float]],
) -> Dict[int, Optional[int]]:
    """
    Execute Gale-Shapley algorithm to create stable mentor-mentee matches.

    Algorithm Steps:
    1. Precompute preference orderings (mentees rank mentors by score)
    2. While unmatched mentees exist with remaining proposals:
       a) Mentee proposes to their next-ranked mentor
       b) Mentor compares all proposals and accepts their preferred mentee
       c) Other proposing mentees are rejected and move to next choice
    3. Return final stable matching

    Args:
        mentee_preferences: Dict[mentee_id] → Dict[mentor_id] → score
                          Higher score = higher preference

    Returns:
        Dict mapping mentee_id → mentor_id (final stable matching)
        Unmatched mentees map to None

    Time Complexity: O(n²) where n = number of mentees/mentors
    Space Complexity: O(n²) for preference rankings

    Guarantees:
    - Terminates: Every mentee either gets matched or exhausts all options
    - Stable: No mentee-mentor pair would both prefer each other over current match
    - Mentee-optimal: Each mentee receives their best possible stable match
    """

    logger.info("Starting stable matching with %d mentees", len(mentee_preferences))
    # STEP 1: Precompute ranked preference lists for each mentee
    # Instead of re-sorting each iteration, precompute once
    # Format: {mentee_id: [(mentor_id, score), (mentor_id, score), ...]}
    # Sorted from highest to lowest score
    mentee_rankings = {}

    for mentee_id, mentor_scores in mentee_preferences.items():
        if mentor_scores:  # Only if mentee has at least one compatible mentor
            # Sort mentors by score (descending)
            ranked_mentors = sorted(
                mentor_scores.items(), key=lambda x: x[1], reverse=True
            )
            mentee_rankings[mentee_id] = ranked_mentors
        else:
            # Mentee has no compatible mentors
            mentee_rankings[mentee_id] = []

    logger.info("Precomputed rankings for %d mentees", len(mentee_rankings))
    # STEP 2: Initialize tracking dictionaries
    # Tracks where each mentee is in their proposal sequence
    mentee_proposal_index = {mentee_id: 0 for mentee_id in mentee_rankings.keys()}

    # Current engagements: mentor_id → mentee_id
    mentor_engagements = {}

    # Current engagements (reverse lookup): mentee_id → mentor_id
    mentee_engagements = {}

    # STEP 3: Main matching loop - continue until no proposals can be made
    max_iterations = len(mentee_rankings) * len(mentee_rankings) + 100  # Safety limit
    iteration_count = 0

    while iteration_count < max_iterations:
        iteration_count += 1
        proposal_made = False

        # STEP 3a: Each unmatched mentee proposes to next-ranked mentor
        for mentee_id, ranked_mentors in mentee_rankings.items():
            # Skip if already matched
            if mentee_id in mentee_engagements:
                continue

            # Get mentee's current proposal index
            proposal_idx = mentee_proposal_index[mentee_id]

            # Skip if mentee has exhausted all proposals
            if proposal_idx >= len(ranked_mentors):
                continue

            # Get next mentor to propose to
            mentor_id, mentee_score = ranked_mentors[proposal_idx]

            # Increment proposal counter for next iteration
            mentee_proposal_index[mentee_id] += 1
            proposal_made = True

            logger.info(
                "Mentee %d proposes to Mentor %d (score: %.2f)",
                mentee_id,
                mentor_id,
                mentee_score,
            )
            # STEP 3b: Mentor evaluates proposal
            # If mentor is not engaged, accept immediately
            if mentor_id not in mentor_engagements:
                mentor_engagements[mentor_id] = mentee_id
                mentee_engagements[mentee_id] = mentor_id
                logger.info(
                    "Mentor %d accepts Mentee %d (first proposal)", mentor_id, mentee_id
                )
            else:
                # Mentor is already engaged - compare proposals
                current_mentee_id = mentor_engagements[mentor_id]

                # Get the score mentor gave to each mentee
                current_score = mentee_preferences[current_mentee_id].get(mentor_id, 0)
                new_score = mentee_score

                # If new proposal is better, switch
                if new_score > current_score:
                    # Reject current mentee
                    del mentee_engagements[current_mentee_id]
                    # Accept new mentee
                    mentor_engagements[mentor_id] = mentee_id
                    mentee_engagements[mentee_id] = mentor_id
                    logger.debug(
                        "Mentor %d switches from Mentee %d to Mentee %d (score %.2f > %.2f)",
                        mentor_id,
                        current_mentee_id,
                        mentee_id,
                        new_score,
                        current_score,
                    )
                else:
                    logger.debug(
                        "Mentor %d rejects Mentee %d, keeps Mentee %d (score %.2f <= %.2f)",
                        mentor_id,
                        mentee_id,
                        current_mentee_id,
                        new_score,
                        current_score,
                    )
                # Otherwise, reject this proposal (implicit - continue loop)

        logger.debug(
            "Iteration %d completed: %d proposals made",
            iteration_count,
            1 if proposal_made else 0,
        )
        # STEP 3c: Check termination condition
        if not proposal_made:
            # No proposals made this iteration = all possible matches resolved
            break

    # STEP 4: Build final result with unmatched mentees set to None
    final_matches = {}
    for mentee_id in mentee_rankings.keys():
        final_matches[mentee_id] = mentee_engagements.get(mentee_id, None)

    # STEP 5: Log warning if algorithm didn't converge
    if iteration_count >= max_iterations:
        logger.warning(
            "Algorithm reached max iterations (%d) - possible infinite loop",
            max_iterations,
        )
    else:
        logger.debug("Matching complete after %d iterations", iteration_count)

    return final_matches


def generate_matches(mentors, mentees) -> Dict[int, Optional[int]]:
    """
    Generate stable mentor-mentee matches using Gale-Shapley algorithm.

    Args:
        mentors: List of mentor objects
        mentees: List of mentee objects

    Returns:
        Dict mapping mentee_id → mentor_id (or None if unmatched)

    Example:
        >>> matches = generate_matches(mentors, mentees)
        >>> logger.info(matches)
        {1: 101, 2: 103, 3: None, 4: 102, ...}
        # Mentee 1 matched with Mentor 101
        # Mentee 3 has no compatible mentor
    """
    logger.info(
        "Generating matches for %d mentors and %d mentees", len(mentors), len(mentees)
    )
    # Calculate compatibility scores
    mentee_preferences = apply_matches_weights(mentors, mentees)

    logger.info("Calculated preferences for %d mentees", len(mentee_preferences))
    # Run stable matching algorithm
    final_matches = stable_matching(mentee_preferences)

    matched_count = sum(1 for m in final_matches.values() if m is not None)
    logger.info(
        "Generated %d matches (%d matched, %d unmatched)",
        len(final_matches),
        matched_count,
        len(final_matches) - matched_count,
    )

    return final_matches, mentee_preferences


# ============================================================================
# UTILITY FUNCTIONS FOR ANALYSIS & DEBUGGING
# ============================================================================


def validate_stable_matching(
    matches: Dict[int, Optional[int]], mentee_preferences: Dict[int, Dict[int, float]]
) -> Tuple[bool, List[str]]:
    """
    Validate that the matching is actually stable.

    A matching is stable if: For every unmatched mentee-mentor pair,
    at least one of them prefers their current match over the other.

    Args:
        matches: Result from stable_matching()
        mentee_preferences: Original preferences from apply_matches_weights()

    Returns:
        Tuple of (is_stable: bool, violations: List[str])
        If stable, violations list is empty
    """
    logger.info("Validating stability of matching with %d pairs", len(matches))
    violations = []

    # Build reverse lookup: mentor → mentee
    mentor_matches = {}
    for mentee_id, mentor_id in matches.items():
        if mentor_id is not None:
            mentor_matches[mentor_id] = mentee_id

    # Check for blocking pairs (instability)
    for mentee_id, mentor_id in matches.items():
        if mentor_id is None:
            continue  # Skip unmatched mentees

        # For each mentor the mentee didn't choose
        for other_mentor_id, score in mentee_preferences[mentee_id].items():
            if other_mentor_id == mentor_id:
                continue  # Skip current match

            # Would mentee prefer this other mentor?
            current_score = mentee_preferences[mentee_id].get(mentor_id, 0)
            if score > current_score:
                # Mentee prefers other_mentor - check if other_mentor prefers mentee
                if other_mentor_id in mentor_matches:
                    other_mentee = mentor_matches[other_mentor_id]
                    other_score = mentee_preferences[other_mentee].get(
                        other_mentor_id, 0
                    )
                    this_score = mentee_preferences[mentee_id].get(other_mentor_id, 0)

                    if this_score > other_score:
                        # Both would prefer each other - BLOCKING PAIR!
                        violations.append(
                            f"Blocking pair: Mentee {mentee_id} and Mentor {other_mentor_id} "
                            f"would both prefer each other"
                        )

    is_stable = len(violations) == 0
    logger.info(
        "Stability validation complete: %s (%d violations)",
        "STABLE" if is_stable else "UNSTABLE",
        len(violations),
    )
    return is_stable, violations


def print_matching_statistics(
    matches: Dict[int, Optional[int]],
    mentee_preferences: Dict[int, Dict[int, float]],
    title: str,
) -> None:
    """
    Print statistics about the matching quality.

    Args:
        matches: Result from generate_matches()
        mentee_preferences: Original preferences
    """
    if not matches:
        logger.warning("Skipping computing matching statistics: no matches")
        return
    logger.info("Computing matching statistics for %d matches", len(matches))
    matched_count = sum(1 for m in matches.values() if m is not None)
    total_mentees = len(matches)
    unmatched_count = total_mentees - matched_count

    logger.info("\n" + "=" * 60)
    logger.info(f"MATCHING STATISTICS {title}")
    logger.info("=" * 60)
    logger.info(f"Total mentees: {total_mentees}")
    logger.info(f"Matched: {matched_count} ({100*matched_count/total_mentees:.1f}%)")
    logger.info(
        f"Unmatched: {unmatched_count} ({100*unmatched_count/total_mentees:.1f}%)"
    )

    # Calculate average match quality (score percentile)
    scores = []
    for mentee_id, mentor_id in matches.items():
        if mentor_id is not None and mentee_id in mentee_preferences:
            score = mentee_preferences[mentee_id].get(mentor_id, 0)
            max_score = (
                max(mentee_preferences[mentee_id].values())
                if mentee_preferences[mentee_id]
                else 1
            )
            percentile = (score / max_score * 100) if max_score > 0 else 0
            scores.append(percentile)

    if scores:
        avg_quality = np.mean(scores)
        median_quality = np.median(scores)
        min_quality = np.min(scores)
        max_quality = np.max(scores)
        logger.info(
            f"\nAverage match quality: {avg_quality:.1f}% of mentee's best option"
        )
        logger.info(
            f"Median match quality: {median_quality:.1f}% of mentee's best option"
        )
        logger.info(f"Min match quality: {min_quality:.1f}%")
        logger.info(f"Max match quality: {max_quality:.1f}%")
        logger.debug(
            "Match quality stats: avg=%.1f%%, median=%.1f%%, min=%.1f%%, max=%.1f%%",
            avg_quality,
            median_quality,
            min_quality,
            max_quality,
        )

    # Stability check
    is_stable, violations = validate_stable_matching(matches, mentee_preferences)
    logger.info(
        "Matching is STABLE"
        if is_stable
        else f"✗ Matching has {len(violations)} violations"
    )
    for violation in violations[:5]:  # Show first 5
        logger.info(f"  - {violation}")

    logger.info("=" * 60 + "\n")
