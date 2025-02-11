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
    """
    Creates or fetches the 4 base sample companies.
    We won't add more companies, just ensure these exist.
    """
    company_names = [
        "TechCorp",
        "Innovate Ltd",
        "FutureVision",
        "NextGen Solutions"
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


def create_users_for_companies(companies, users_per_company=10):
    """
    Creates 'users_per_company' new users for each company in 'companies'.
    That means total = len(companies) * users_per_company.
    """
    FIRST_NAMES = ["Evan", "Sophia", "Max", "Olivia", "Liam", "Mia",
                   "Noah", "Luna", "James", "Ava", "Grace", "Daniel",
                   "Bella", "Julia", "David", "Amy", "Ray", "Hannah",
                   "Sam", "Chloe", "Kevin", "Nina", "Zoe", "Ivan", "Leo",
                   "Ella", "Amy", "Rachel"]
    LAST_NAMES = ["Choi", "Lee", "Kim", "Park", "Kang", "Yang", "Yoon",
                  "Shin", "Song", "Cho", "Moon", "Jeon", "Hong", "Seo",
                  "Jung", "Lim", "Woo", "Ma", "Ha"]

    created_users = []

    for company in companies:
        # For each company, create the desired number of new users
        for i in range(users_per_company):
            fname = random.choice(FIRST_NAMES)
            lname = random.choice(LAST_NAMES)
            name = f"{fname} {lname}"
            username = f"{fname.lower()}{lname.lower()}{random.randint(100,9999)}"
            email = f"{username}@example.com"

            try:
                user = User.objects.create_user(
                    name=name,
                    email=email,
                    password="test1234",
                    company=company
                )
                print(f"[User] Created {user.name} in {company.name}")
                created_users.append(user)
            except IntegrityError:
                print(f"[User] {email} exists, skipping.")
                # In practice, might try again with a different name

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
    questions_by_cat = {}
    for cat in categories:
        qs = list(Question.objects.filter(category=cat))
        questions_by_cat[cat] = qs
        print(f"[Questions] Fetched {len(qs)} in category: {cat}")
    return questions_by_cat


def create_responses_and_answers(users, questions_by_cat):
    """
    For each user:
      - pick random SurveyType & CourseType
      - create 2 responses (pre & post)
      - for each response, answer all questions.
    """
    survey_types = list(SurveyType.objects.all())
    course_types = list(CourseType.objects.all())

    if not survey_types or not course_types:
        print("[Error] No SurveyTypes or CourseTypes found. Cannot create responses.")
        return

    for user in users:
        # We'll create 'pre' and 'post' for a random st/ct combo
        st = random.choice(survey_types)
        ct = random.choice(course_types)

        for phase in ["pre", "post"]:
            # Check if user already has a response for st/ct/phase
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

            # Now answer every question in each category
            for cat, qlist in questions_by_cat.items():
                for q in qlist:
                    if q.question_type == "radio":
                        if q.options:
                            chosen = random.choice(q.options)
                            Answer.objects.create(response=sr, question=q, answer_text=chosen)
                            print(f"  - [radio] {q.text[:25]} => {chosen}")
                        else:
                            # fallback
                            Answer.objects.create(response=sr, question=q, answer_text="N/A")

                    elif q.question_type == "rating":
                        val = random.randint(1,5)
                        Answer.objects.create(response=sr, question=q, answer_value=val)
                        print(f"  - [rating] {q.text[:25]} => {val}")

                    elif q.question_type == "checkbox":
                        if q.options:
                            subset_size = random.randint(0, len(q.options))
                            chosen_opts = random.sample(q.options, subset_size)
                            Answer.objects.create(
                                response=sr,
                                question=q,
                                answer_text=", ".join(chosen_opts)
                            )
                            print(f"  - [checkbox] {q.text[:25]} => {chosen_opts}")
                        else:
                            Answer.objects.create(response=sr, question=q, answer_text="")

                    elif q.question_type == "text":
                        Answer.objects.create(response=sr, question=q, answer_text="Test answer")
                        print(f"  - [text] {q.text[:25]} => 'Test answer'")

                    else:
                        # fallback
                        Answer.objects.create(response=sr, question=q, answer_text="Unhandled Q type")
                        print(f"  - [???] {q.text[:25]} => 'Unhandled Q type'")


def main():
    print("=== Populating Extended Sample Data ===")
    # 1) Create or reuse the same 4 companies
    companies = create_companies()

    # 2) For each of those 4 companies, create 10 new users => total 40
    all_users = create_users_for_companies(companies, users_per_company=10)

    # 3) Fetch questions by category
    questions_by_cat = fetch_questions_by_category()

    # 4) For each user, create 2 responses (pre/post) with random st & ct
    create_responses_and_answers(all_users, questions_by_cat)

    print("✅ Done. Created more users per company and responses/answers!")


if __name__ == "__main__":
    main()
