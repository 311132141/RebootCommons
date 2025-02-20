# populate_sample_data.py
from django.db.utils import IntegrityError
from account.models import User, Company
from survey.models import (
    SurveyType, CourseType, Question,
    UserSurveyResponse, Answer,
    SurveyTypeQuestion, CourseTypeQuestion
)
import random
import os
import django

# Set DJANGO_SETTINGS_MODULE and initialise Django before importing any Django modules
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()


def create_companies():
    """
    Create or fetch some companies, each with an intended course_name substring.
    We'll attempt to find a matching CourseType via .filter() and pick one
    if multiple match or None if none exist.
    """
    company_data = [
        ("Ark", "리더십과 혁신"),
        ("Innovate Ltd", "기업가정신과 혁신"),
        ("FutureVision", "비전하우스"),
        ("AlphaEnterprises", "리더십과 혁신"),
        ("BetaLogics", "기업가정신과 혁신"),
        ("CyberEdge", "비전하우스"),
        ("SkyHigh Innovations", "기업가정신과 혁신"),
    ]
    created_companies = []

    for (c_name, course_substring) in company_data:
        # fetch all matches
        ctype_candidates = CourseType.objects.filter(
            name__icontains=course_substring)
        if not ctype_candidates.exists():
            # No match
            print(
                f"[Warning] No CourseType matched '{course_substring}'. Setting None.")
            ctype = None
        else:
            # if multiple, pick randomly or the first
            ctype = random.choice(list(ctype_candidates))
            # or ctype = ctype_candidates.first() if you prefer consistent rather than random

        # create or get the company
        company, c_created = Company.objects.get_or_create(name=c_name)
        # assign course type
        if company.course_type != ctype:
            company.course_type = ctype
            company.save()

        if c_created:
            print(f"[Company] Created {c_name} => course_type=({ctype})")
        else:
            print(
                f"[Company] Found existing: {c_name} => course_type=({ctype})")

        created_companies.append(company)

    return created_companies


def gather_bridging_questions(survey_type, course_type, include_lifestyle=True):
    """
    Fetch bridging questions for (survey_type, course_type).
    ...
    """
    st_qs = SurveyTypeQuestion.objects.filter(
        survey_type=survey_type).select_related('question')
    ct_qs = []
    if course_type:
        ct_qs = CourseTypeQuestion.objects.filter(
            course_type=course_type).select_related('question')

    question_objs = set()
    for row in st_qs:
        if row.question.category == "lifestyle" and not include_lifestyle:
            continue
        question_objs.add(row.question)

    for row in ct_qs:
        if row.question.category == "lifestyle" and not include_lifestyle:
            continue
        question_objs.add(row.question)

    return list(question_objs)


def create_users(companies, num_in_company=20, num_no_company=5):
    """
    Create some users. 
    - `num_in_company` users for EACH company → must use 기업용
    - `num_no_company` users with no company → must use 개인용
    """
    FIRST_NAMES = ["Evan", "Sophia", "Max", "Olivia", "Liam", "Mia",
                   "Noah", "Luna", "James", "Ava", "Grace", "Daniel",
                   "Bella", "Julia", "David", "Amy", "Ray", "Hannah",
                   "Sam", "Chloe", "Kevin", "Nina", "Zoe", "Ivan", "Leo",
                   "Ella", "Amy", "Rachel"]
    LAST_NAMES = ["Choi", "Lee", "Kim", "Park", "Kang", "Yang", "Yoon",
                  "Shin", "Song", "Cho", "Moon", "Jeon", "Hong", "Seo",
                  "Jung", "Lim", "Woo", "Ma", "Ha"]

    users_in_companies = []
    users_no_company = []

    # Create users in each company
    for c in companies:
        for i in range(num_in_company):
            fname = random.choice(FIRST_NAMES)
            lname = random.choice(LAST_NAMES)
            name = f"{fname} {lname}"
            username = f"{fname.lower()}{lname.lower()}{random.randint(100, 9999)}"
            email = f"{username}@example.com"

            try:
                user = User.objects.create_user(
                    name=name,
                    email=email,
                    password="test1234",
                    company=c  # belongs to a company
                )
                print(f"[User] Created {user.name} in {c.name}")
                users_in_companies.append(user)
            except IntegrityError:
                print(f"[User] {email} already exists, skipping.")

    # Create users with no company
    for i in range(num_no_company):
        fname = random.choice(FIRST_NAMES)
        lname = random.choice(LAST_NAMES)
        name = f"{fname} {lname}"
        username = f"{fname.lower()}{lname.lower()}{random.randint(100, 9999)}"
        email = f"{username}@example.com"

        try:
            user = User.objects.create_user(
                name=name,
                email=email,
                password="test1234",
                company=None
            )
            print(f"[User] Created {user.name} (no company)")
            users_no_company.append(user)
        except IntegrityError:
            print(f"[User] {email} already exists, skipping.")

    return users_in_companies, users_no_company


def gather_bridging_questions(survey_type, course_type, include_lifestyle=True):
    """
    Fetch bridging questions for (survey_type, course_type).
    - from SurveyTypeQuestion => all relevant Q for that survey_type
    - from CourseTypeQuestion => all relevant Q for that course_type
    Then combine them, optionally filtering out 'lifestyle' if needed.
    Return a unique set of Questions.
    """
    st_qs = SurveyTypeQuestion.objects.filter(
        survey_type=survey_type).select_related('question')
    ct_qs = []
    if course_type:
        ct_qs = CourseTypeQuestion.objects.filter(
            course_type=course_type).select_related('question')

    # combine
    question_objs = set()
    for row in st_qs:
        if not (row.question.category == "lifestyle" and not include_lifestyle):
            question_objs.add(row.question)
    for row in ct_qs:
        if not (row.question.category == "lifestyle" and not include_lifestyle):
            question_objs.add(row.question)

    return list(question_objs)


def create_responses_and_answers(users_in_company, users_no_company):
    """
    For users in a company => survey_type=기업용, course_type=company.course_type
    For users with no company => survey_type=개인용, course_type=ANY from DB
    We'll create a 'pre' and 'post' response for each user.
    Lifestyle questions => only in 'pre'.
    """
    # Find the actual SurveyType objects for "개인용" & "기업용" by name
    try:
        personal_survey_type = SurveyType.objects.get(name="개인용")
    except SurveyType.DoesNotExist:
        personal_survey_type = None
        print("[Error] SurveyType '개인용' not found in DB.")

    try:
        corporate_survey_type = SurveyType.objects.get(name="기업용")
    except SurveyType.DoesNotExist:
        corporate_survey_type = None
        print("[Error] SurveyType '기업용' not found in DB.")

    all_course_types = list(CourseType.objects.all())

    # [1] For users in a company => (survey_type=기업용, course_type=that_company.course_type)
    for user in users_in_company:
        if not corporate_survey_type:
            continue
        c_type = user.company.course_type if user.company else None
        # pre & post
        for phase in ["pre", "post"]:
            existing = UserSurveyResponse.objects.filter(
                user=user,
                survey_type=corporate_survey_type,
                course_type=c_type,
                phase=phase
            ).first()
            if existing:
                print(
                    f"[Response] {user.name} already has {phase} for {corporate_survey_type.name}/{c_type}. Skipping.")
                continue

            response = UserSurveyResponse.objects.create(
                user=user,
                survey_type=corporate_survey_type,
                course_type=c_type,
                phase=phase
            )
            print(
                f"[Response] Created for {user.name} => {corporate_survey_type.name}/{c_type} ({phase})")

            # gather bridging
            include_lifestyle = (phase == "pre")  # only in pre
            qset = gather_bridging_questions(
                corporate_survey_type, c_type, include_lifestyle=include_lifestyle)

            # generate random answers
            generate_random_answers(response, qset)

    # [2] For users with no company => (survey_type=개인용, course_type=ANY random)
    for user in users_no_company:
        if not personal_survey_type or not all_course_types:
            continue
        # pick random course for them
        c_type = random.choice(all_course_types)

        for phase in ["pre", "post"]:
            existing = UserSurveyResponse.objects.filter(
                user=user,
                survey_type=personal_survey_type,
                course_type=c_type,
                phase=phase
            ).first()
            if existing:
                print(
                    f"[Response] {user.name} already has {phase} for {personal_survey_type.name}/{c_type}. Skipping.")
                continue

            response = UserSurveyResponse.objects.create(
                user=user,
                survey_type=personal_survey_type,
                course_type=c_type,
                phase=phase
            )
            print(
                f"[Response] Created for {user.name} => {personal_survey_type.name}/{c_type} ({phase})")

            include_lifestyle = (phase == "pre")
            qset = gather_bridging_questions(
                personal_survey_type, c_type, include_lifestyle)
            generate_random_answers(response, qset)


def generate_random_answers(response, question_list):
    """
    For each question, create an Answer with random logic.
    radio => pick 1 from question.options
    rating => 1..5
    checkbox => random subset
    text => "Test answer"
    """
    for q in question_list:
        if q.question_type == "radio":
            if q.options:
                chosen = random.choice(q.options)
                Answer.objects.create(
                    response=response,
                    question=q,
                    answer_text=chosen
                )
            else:
                Answer.objects.create(
                    response=response,
                    question=q,
                    answer_text="N/A"
                )

        elif q.question_type == "rating":
            val = random.randint(1, 5)
            Answer.objects.create(
                response=response,
                question=q,
                answer_value=val
            )

        elif q.question_type == "checkbox":
            if q.options:
                subset_size = random.randint(0, len(q.options))
                chosen_opts = random.sample(q.options, subset_size)
                Answer.objects.create(
                    response=response,
                    question=q,
                    answer_text=", ".join(chosen_opts)
                )
            else:
                Answer.objects.create(
                    response=response, question=q, answer_text="")

        elif q.question_type == "text":
            Answer.objects.create(
                response=response,
                question=q,
                answer_text="Test answer"
            )

        else:
            # fallback
            Answer.objects.create(
                response=response,
                question=q,
                answer_text="Unhandled question type"
            )


def main():
    print("=== Populating Sample Data with Requirements ===")

    # Step A: Create or fetch base companies with assigned course_type
    companies = create_companies()

    # Step B: Create some users in those companies (기업용) and some with no company (개인용)
    users_in_companies, users_no_company = [], []
    for c in companies:
        # create 5 new users in each company
        new_users = []
        for i in range(5):
            fname = random.choice(
                ["Alice", "Bob", "Carol", "Dave", "Eva", "Frank", "Gina", "Henry", "Iris", "Jack"])
            lname = f"({c.name[:3]})"  # just a silly suffix
            name = f"{fname} {lname}"
            email = f"{fname.lower()}{random.randint(100, 999)}@example.com"

            try:
                u = User.objects.create_user(
                    name=name,
                    email=email,
                    password="test1234",
                    company=c
                )
                new_users.append(u)
                print(f"[User] Created {u.name} in {c.name}")
            except IntegrityError:
                print(f"[User] {email} already exists, skip.")
        users_in_companies.extend(new_users)

    # Also create 10 users with no company at all
    for i in range(10):
        fname = random.choice(
            ["Zara", "Tom", "Ursula", "Victor", "Wendy", "Xander", "Yvonne", "Quinn", "Piper"])
        lname = random.choice(
            ["Moon", "Lee", "Smith", "Brown", "Garcia", "Kim"])
        name = f"{fname} {lname}"
        email = f"{fname.lower()}{random.randint(100, 999)}@example.com"

        try:
            u = User.objects.create_user(
                name=name,
                email=email,
                password="test1234",
                company=None
            )
            users_no_company.append(u)
            print(f"[User] Created {u.name} (No company)")
        except IntegrityError:
            print(f"[User] {email} already exists, skip.")

    # Step C: Create the pre/post responses for each user
    create_responses_and_answers(users_in_companies, users_no_company)

    print("✅ Done. '기업용' for those in companies, '개인용' for others, plus pre/post logic.")


if __name__ == "__main__":
    main()
