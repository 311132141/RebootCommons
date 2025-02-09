import os
import random
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from django.db.utils import IntegrityError
from account.models import User, Company
from survey.models import (
    SurveyType, CourseType, Question,
    UserSurveyResponse, Answer
)

def create_companies():
    """Creates or fetches multiple sample companies."""
    company_names = [
        "TechCorp", "Innovate Ltd", "FutureVision",
        "NextGen Solutions", "AlphaEnterprises",
        "BetaLogics", "CyberEdge", "SkyHigh Innovations"
    ]
    created_companies = []
    for name in company_names:
        company, created = Company.objects.get_or_create(name=name)
        if created:
            print(f"[Company] Created {company.name}")
        else:
            print(f"[Company] Already existed: {company.name}")
        created_companies.append(company)
    return created_companies

def create_random_users(companies, num_users=20):
    """
    Create 'num_users' random users assigned to random companies.
    If a user with the generated email/username already exists, skip.
    """
    FIRST_NAMES = ["Evan", "Sophia", "Max", "Olivia", "Liam", "Mia",
                   "Noah", "Luna", "James", "Ava", "Grace", "Daniel",
                   "Bella", "Julia", "David", "Amy", "Ray", "Hannah"]
    LAST_NAMES = ["Choi", "Lee", "Kim", "Park", "Kang", "Yang", "Yoon",
                  "Shin", "Song", "Cho", "Moon", "Jeon", "Hong"]

    created_users = []

    for i in range(num_users):
        fname = random.choice(FIRST_NAMES)
        lname = random.choice(LAST_NAMES)
        name = f"{fname} {lname}"
        username = f"{fname.lower()}{lname.lower()}{random.randint(1,9999)}"
        email = f"{username}@example.com"

        # pick a random company
        company = random.choice(companies)

        # create user if not exists
        try:
            user = User.objects.create_user(
                name=name,
                email=email,
                password="test1234",  # default pass
                company=company
            )
            print(f"[User] Created {user.name} in {company.name}")
            created_users.append(user)
        except IntegrityError:
            print(f"[User] {email} exists, skipping.")
            # In practice, might skip or re-try with new random data

    return created_users

def fetch_questions_by_category():
    """
    Return a dict with categories as keys, question lists as values.
    E.g. {
        "demographic_corp": [Q1, Q2, ...],
        "demographic_personal": [...],
        ...
    }
    """
    categories = [
        "demographic_corp", "demographic_personal",
        "lifestyle", "ppc_efficacy", "ppc_optimism", "ppc_hope",
        "ppc_resilience", "selflead_behavior", "selflead_natural",
        "selflead_constructive", "org_affective", "org_continuance",
        "org_normative", "entrepreneur_innov", "entrepreneur_proact",
        "entrepreneur_risk"
    ]
    questions = {}
    for cat in categories:
        qs = list(Question.objects.filter(category=cat))
        questions[cat] = qs
        print(f"[Questions] Fetched {len(qs)} in category: {cat}")
    return questions

def create_responses_and_answers(users, questions_by_cat):
    """
    For each user:
      - pick a random SurveyType, CourseType
      - create 1..2 responses (e.g. pre & post)
      - for each response, answer all questions (all categories).
    """
    survey_types = list(SurveyType.objects.all())
    course_types = list(CourseType.objects.all())
    if not survey_types or not course_types:
        print("No SurveyTypes or CourseTypes found. Skipping responses.")
        return

    for user in users:
        # pick random st & ct
        st = random.choice(survey_types)
        ct = random.choice(course_types)

        # optionally, create multiple responses per user
        # for instance, "pre" and "post"
        phases = ["pre", "post"]
        for phase in phases:
            # check if user already has a response to avoid duplicates
            existing = UserSurveyResponse.objects.filter(
                user=user, survey_type=st, course_type=ct, phase=phase
            ).first()
            if existing:
                print(f"[SurveyResponse] {user.name} already has {phase} for {st.name}/{ct.name}. Skipping.")
                continue

            sr = UserSurveyResponse.objects.create(
                user=user,
                survey_type=st,
                course_type=ct,
                phase=phase
            )
            print(f"[SurveyResponse] Created for {user.name} => {st.name}/{ct.name} ({phase})")

            # now answer all questions from each category
            for cat, qlist in questions_by_cat.items():
                for q in qlist:
                    # random logic
                    if q.question_type == "radio":
                        # pick exactly 1 from q.options
                        if q.options:
                            chosen_option = random.choice(q.options)
                            Answer.objects.create(
                                response=sr,
                                question=q,
                                answer_text=chosen_option
                            )
                            print(f"  - [radio] {q.text[:25]} => {chosen_option}")
                        else:
                            # fallback
                            Answer.objects.create(
                                response=sr,
                                question=q,
                                answer_text="N/A"
                            )

                    elif q.question_type == "rating":
                        val = random.randint(1,5)
                        Answer.objects.create(
                            response=sr,
                            question=q,
                            answer_value=val
                        )
                        print(f"  - [rating] {q.text[:25]} => {val}")

                    elif q.question_type == "checkbox":
                        if q.options:
                            subset_size = random.randint(0, len(q.options))
                            chosen = random.sample(q.options, subset_size)
                            Answer.objects.create(
                                response=sr,
                                question=q,
                                answer_text=", ".join(chosen)
                            )
                            print(f"  - [checkbox] {q.text[:25]} => {chosen}")
                        else:
                            Answer.objects.create(
                                response=sr,
                                question=q,
                                answer_text=""
                            )
                    elif q.question_type == "text":
                        Answer.objects.create(
                            response=sr,
                            question=q,
                            answer_text="Test answer"
                        )
                        print(f"  - [text] {q.text[:25]} => 'Test answer'")
                    else:
                        # fallback for unknown types
                        Answer.objects.create(
                            response=sr,
                            question=q,
                            answer_text="Unhandled question type"
                        )

def main():
    print("=== Populating More Sample Data ===")
    # 1) Create more companies
    companies = create_companies()
    # 2) Create random users
    # e.g. 20 total users
    users = create_random_users(companies, num_users=20)
    # 3) fetch all questions by category
    questions_by_cat = fetch_questions_by_category()
    # 4) create responses & answers
    create_responses_and_answers(users, questions_by_cat)
    print("✅ Done populating additional data!")

if __name__ == "__main__":
    main()
