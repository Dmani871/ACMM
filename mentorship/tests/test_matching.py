import io
import sys

from django.test import TestCase

from mentorship.matching import (
    apply_matches_weights,
    generate_matches,
    print_matching_statistics,
    validate_stable_matching,
)
from mentorship.models import MenteeProfile, MentorProfile


class MatchingAlgorithmTestCase(TestCase):
    def setUp(self):
        # Create test mentors and mentees with various scenarios
        self.mentor1 = MentorProfile.objects.create(
            personal_email="mentor1@example.com",
            work_email="mentor1@example.com",
            first_name="Mentor",
            last_name="One",
            number="1234567890",
            year_applied="GRAD",
            area_of_support=["PS", "I"],
            interview_experience=["P"],
            entrance_exam_experience=["BMAT"],
            wp_scheme=False,
            applied_before=False,
            contact_consent=True,
            tcs_consent=True,
        )
        self.mentor2 = MentorProfile.objects.create(
            personal_email="mentor2@example.com",
            work_email="mentor2@example.com",
            first_name="Mentor",
            last_name="Two",
            number="1234567891",
            year_applied="GRAD",
            area_of_support=["EE"],
            interview_experience=[],
            entrance_exam_experience=["UCAT"],
            wp_scheme=False,
            applied_before=False,
            contact_consent=True,
            tcs_consent=True,
        )
        self.mentor3 = MentorProfile.objects.create(
            personal_email="mentor3@example.com",
            work_email="mentor3@example.com",
            first_name="Mentor",
            last_name="Three",
            number="1234567892",
            year_applied="A2",
            area_of_support=["PS", "WE"],
            interview_experience=["M", "G"],
            entrance_exam_experience=["BMAT", "UCAT"],
            wp_scheme=True,
            applied_before=True,
            contact_consent=True,
            tcs_consent=True,
        )
        self.mentee1 = MenteeProfile.objects.create(
            personal_email="mentee1@example.com",
            work_email="mentee1@example.com",
            first_name="Mentee",
            last_name="One",
            number="1234567893",
            year_applied="A2",
            area_of_support=["PS", "I"],
            interview_experience=["P"],
            entrance_exam_experience=["BMAT"],
            wp_scheme=False,
            applied_before=False,
            contact_consent=True,
            tcs_consent=True,
            mentor_need="Need help",
            mentor_help="Will help",
            mentor_relationship="Good relationship",
            course="M",
            current_application=True,
            commitment=True,
            state_educated=True,
            family_support=False,
        )
        self.mentee2 = MenteeProfile.objects.create(
            personal_email="mentee2@example.com",
            work_email="mentee2@example.com",
            first_name="Mentee",
            last_name="Two",
            number="1234567894",
            year_applied="A2",
            area_of_support=["EE"],
            interview_experience=[],
            entrance_exam_experience=["UCAT"],
            wp_scheme=False,
            applied_before=False,
            contact_consent=True,
            tcs_consent=True,
            mentor_need="Need exam help",
            mentor_help="Will help with exams",
            mentor_relationship="Good relationship",
            course="M",
            current_application=True,
            commitment=True,
            state_educated=True,
            family_support=False,
        )
        self.mentee3 = MenteeProfile.objects.create(
            personal_email="mentee3@example.com",
            work_email="mentee3@example.com",
            first_name="Mentee",
            last_name="Three",
            number="1234567895",
            year_applied="GRAD",
            area_of_support=["PS", "WE"],
            interview_experience=["M"],
            entrance_exam_experience=["BMAT"],
            wp_scheme=True,
            applied_before=True,
            contact_consent=True,
            tcs_consent=True,
            mentor_need="Need career help",
            mentor_help="Will help with career",
            mentor_relationship="Professional relationship",
            course="D",
            current_application=True,
            commitment=True,
            state_educated=False,
            family_support=True,
        )
        # Mentee with no compatible mentors (needs EE but mentors have no EE experience)
        self.mentee_no_match = MenteeProfile.objects.create(
            personal_email="mentee_nomatch@example.com",
            work_email="mentee_nomatch@example.com",
            first_name="Mentee",
            last_name="NoMatch",
            number="1234567896",
            year_applied="A2",
            area_of_support=["EE"],
            interview_experience=[],
            entrance_exam_experience=["GAMSAT"],  # Different exam
            wp_scheme=False,
            applied_before=False,
            contact_consent=True,
            tcs_consent=True,
            mentor_need="Need exam help",
            mentor_help="Will help with exams",
            mentor_relationship="Good relationship",
            course="M",
            current_application=True,
            commitment=True,
            state_educated=True,
            family_support=False,
        )

    def test_generate_matches_returns_dict(self):
        mentors = [self.mentor1, self.mentor2]
        mentees = [self.mentee1, self.mentee2]
        matches, preferences = generate_matches(mentors, mentees)
        self.assertIsInstance(matches, dict)
        self.assertIsInstance(preferences, dict)

    def test_matching_is_stable(self):
        mentors = [self.mentor1, self.mentor2]
        mentees = [self.mentee1, self.mentee2]
        matches, preferences = generate_matches(mentors, mentees)
        is_stable, violations = validate_stable_matching(matches, preferences)
        self.assertTrue(is_stable, f"Matching not stable: {violations}")

    def test_no_unmatched_if_possible(self):
        # With compatible pairs, should match all
        mentors = [self.mentor1, self.mentor2]
        mentees = [self.mentee1, self.mentee2]
        matches, _ = generate_matches(mentors, mentees)
        unmatched = [m for m in matches.values() if m is None]
        self.assertEqual(
            len(unmatched), 0, "Some mentees unmatched when matches possible"
        )

    def test_partial_matching_with_incompatible_mentee(self):
        # Test with mentee that has no compatible mentors
        mentors = [self.mentor1, self.mentor2]
        mentees = [self.mentee1, self.mentee2, self.mentee_no_match]
        matches, preferences = generate_matches(mentors, mentees)

        # Should have 2 matches and 1 unmatched
        matched_count = sum(1 for m in matches.values() if m is not None)
        self.assertEqual(matched_count, 2)

        # The no-match mentee should be unmatched
        self.assertIsNone(matches[self.mentee_no_match.id])

        # Check stability
        is_stable, violations = validate_stable_matching(matches, preferences)
        self.assertTrue(is_stable, f"Matching not stable: {violations}")

    def test_shared_experience_bonus(self):
        # Test WP scheme and applied_before bonuses
        mentors = [self.mentor3]  # Has wp_scheme=True, applied_before=True
        mentees = [self.mentee3]  # Has wp_scheme=True, applied_before=True
        matches, preferences = generate_matches(mentors, mentees)

        # Should match due to shared experience bonus
        self.assertEqual(matches[self.mentee3.id], self.mentor3.id)

    def test_stage_alignment_bonus(self):
        # Test same year_applied bonus
        mentor_grad = MentorProfile.objects.create(
            personal_email="grad_mentor@example.com",
            work_email="grad_mentor@example.com",
            first_name="Grad",
            last_name="Mentor",
            number="1234567897",
            year_applied="GRAD",
            area_of_support=["PS"],
            interview_experience=["P"],
            entrance_exam_experience=[],
            wp_scheme=False,
            applied_before=False,
            contact_consent=True,
            tcs_consent=True,
        )
        mentee_grad = MenteeProfile.objects.create(
            personal_email="grad_mentee@example.com",
            work_email="grad_mentee@example.com",
            first_name="Grad",
            last_name="Mentee",
            number="1234567898",
            year_applied="GRAD",
            area_of_support=["PS"],
            interview_experience=["P"],
            entrance_exam_experience=[],
            wp_scheme=False,
            applied_before=False,
            contact_consent=True,
            tcs_consent=True,
            mentor_need="Need grad help",
            mentor_help="Will help grad",
            mentor_relationship="Good relationship",
            course="M",
            current_application=True,
            commitment=True,
            state_educated=True,
            family_support=False,
        )

        mentors = [mentor_grad]
        mentees = [mentee_grad]
        matches, preferences = generate_matches(mentors, mentees)

        # Should match with stage alignment bonus
        self.assertEqual(matches[mentee_grad.id], mentor_grad.id)

    def test_penalty_for_family_support(self):
        # Test penalty for mentees with family support
        mentor_ps = MentorProfile.objects.create(
            personal_email="ps_mentor@example.com",
            work_email="ps_mentor@example.com",
            first_name="PS",
            last_name="Mentor",
            number="1234567899",
            year_applied="GRAD",
            area_of_support=["PS"],
            interview_experience=["P"],
            entrance_exam_experience=[],
            wp_scheme=False,
            applied_before=False,
            contact_consent=True,
            tcs_consent=True,
        )
        mentee_family = MenteeProfile.objects.create(
            personal_email="family_mentee@example.com",
            work_email="family_mentee@example.com",
            first_name="Family",
            last_name="Mentee",
            number="1234567800",
            year_applied="A2",
            area_of_support=["PS"],
            interview_experience=["P"],
            entrance_exam_experience=[],
            wp_scheme=False,
            applied_before=False,
            contact_consent=True,
            tcs_consent=True,
            mentor_need="Need help",
            mentor_help="Will help",
            mentor_relationship="Good relationship",
            course="M",
            current_application=True,
            commitment=True,
            state_educated=True,
            family_support=True,  # Should get penalty
        )

        mentors = [mentor_ps]
        mentees = [mentee_family]
        matches, preferences = generate_matches(mentors, mentees)

        # Should still match but with lower score due to penalty
        self.assertEqual(matches[mentee_family.id], mentor_ps.id)

    def test_empty_inputs(self):
        # Test with empty lists
        matches, preferences = generate_matches([], [])
        self.assertEqual(len(matches), 0)
        self.assertEqual(len(preferences), 0)

    def test_single_mentor_single_mentee(self):
        # Test minimal case
        mentors = [self.mentor1]
        mentees = [self.mentee1]
        matches, preferences = generate_matches(mentors, mentees)

        self.assertEqual(len(matches), 1)
        self.assertEqual(matches[self.mentee1.id], self.mentor1.id)

    def test_multiple_mentees_one_mentor(self):
        # Test oversubscription
        mentors = [self.mentor1]
        mentees = [self.mentee1, self.mentee3]  # Both need PS support
        matches, preferences = generate_matches(mentors, mentees)

        # Only one should be matched
        matched_count = sum(1 for m in matches.values() if m is not None)
        self.assertEqual(matched_count, 1)

        # Check stability
        is_stable, violations = validate_stable_matching(matches, preferences)
        self.assertTrue(is_stable, f"Matching not stable: {violations}")

    def test_apply_matches_weights_calculation(self):
        # Test the scoring function directly
        mentors = [self.mentor1, self.mentor2]
        mentees = [self.mentee1, self.mentee2]
        preferences = apply_matches_weights(mentors, mentees)

        # Check structure
        self.assertEqual(len(preferences), 2)  # 2 mentees
        self.assertIn(self.mentee1.id, preferences)
        self.assertIn(self.mentee2.id, preferences)

        # Check scores are positive for compatible pairs
        mentee1_scores = preferences[self.mentee1.id]
        mentee2_scores = preferences[self.mentee2.id]

        self.assertGreater(mentee1_scores[self.mentor1.id], 0)  # Compatible
        self.assertGreater(mentee2_scores[self.mentor2.id], 0)  # Compatible

    def test_large_dataset_performance(self):
        # Test with larger dataset (create more objects)
        # This tests that the algorithm scales reasonably
        mentors = [self.mentor1, self.mentor2, self.mentor3]
        mentees = [self.mentee1, self.mentee2, self.mentee3]
        matches, preferences = generate_matches(mentors, mentees)

        # Should complete without timeout
        self.assertIsInstance(matches, dict)
        self.assertEqual(len(matches), 3)

        # Check stability
        is_stable, violations = validate_stable_matching(matches, preferences)
        self.assertTrue(is_stable, f"Matching not stable: {violations}")

    def test_different_course_types(self):
        # Test medicine vs dentistry matching
        mentor_med = MentorProfile.objects.create(
            personal_email="med_mentor@example.com",
            work_email="med_mentor@example.com",
            first_name="Med",
            last_name="Mentor",
            number="1234567801",
            year_applied="GRAD",
            area_of_support=["PS"],
            interview_experience=["P"],
            entrance_exam_experience=[],
            wp_scheme=False,
            applied_before=False,
            contact_consent=True,
            tcs_consent=True,
        )
        mentee_dent = MenteeProfile.objects.create(
            personal_email="dent_mentee@example.com",
            work_email="dent_mentee@example.com",
            first_name="Dent",
            last_name="Mentee",
            number="1234567802",
            year_applied="A2",
            area_of_support=["PS"],
            interview_experience=["P"],
            entrance_exam_experience=[],
            wp_scheme=False,
            applied_before=False,
            contact_consent=True,
            tcs_consent=True,
            mentor_need="Need dent help",
            mentor_help="Will help dent",
            mentor_relationship="Good relationship",
            course="D",  # Dentistry
            current_application=True,
            commitment=True,
            state_educated=True,
            family_support=False,
        )

        mentors = [mentor_med]
        mentees = [mentee_dent]
        matches, preferences = generate_matches(mentors, mentees)

        # Should still match despite different courses (algorithm doesn't consider course)
        self.assertEqual(matches[mentee_dent.id], mentor_med.id)
