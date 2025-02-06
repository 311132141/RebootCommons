"""
populate_surveys.py

Populates the database with questions, bridging them to SurveyType (개인용, 기업용) and CourseType,
and sets a 'category' field on each Question for easy filtering.
"""

import os
import django

# 1. Setup Django environment (edit 'backend.settings' to match your project name)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from survey.models import (
    SurveyType, CourseType,
    Question, SurveyTypeQuestion, CourseTypeQuestion
)


def main():
    # --------------------------------------------------------------------------
    # CREATE OR GET SURVEY TYPES (개인용, 기업용)
    # --------------------------------------------------------------------------
    st_personal, _ = SurveyType.objects.get_or_create(
        name='개인용',
        defaults={'description': '개인용 (Personal) 설문 타입'}
    )
    st_corporate, _ = SurveyType.objects.get_or_create(
        name='기업용',
        defaults={'description': '기업용 (Corporate) 설문 타입'}
    )

    # --------------------------------------------------------------------------
    # CREATE OR GET COURSE TYPES (비전하우스, 리더십과 혁신, 기업가정신과 혁신)
    # Each course appears under both personal & corporate
    # --------------------------------------------------------------------------
    ct_vision_personal, _ = CourseType.objects.get_or_create(
        survey_type=st_personal,
        name='비전하우스',
        defaults={'description': '비전하우스 (개인용)'}
    )
    ct_vision_corp, _ = CourseType.objects.get_or_create(
        survey_type=st_corporate,
        name='비전하우스',
        defaults={'description': '비전하우스 (기업용)'}
    )

    ct_leadership_personal, _ = CourseType.objects.get_or_create(
        survey_type=st_personal,
        name='리더십과 혁신',
        defaults={'description': '리더십과 혁신 (개인용)'}
    )
    ct_leadership_corp, _ = CourseType.objects.get_or_create(
        survey_type=st_corporate,
        name='리더십과 혁신',
        defaults={'description': '리더십과 혁신 (기업용)'}
    )

    ct_entrepreneur_personal, _ = CourseType.objects.get_or_create(
        survey_type=st_personal,
        name='기업가정신과 혁신',
        defaults={'description': '기업가정신과 혁신 (개인용)'}
    )
    ct_entrepreneur_corp, _ = CourseType.objects.get_or_create(
        survey_type=st_corporate,
        name='기업가정신과 혁신',
        defaults={'description': '기업가정신과 혁신 (기업용)'}
    )

    # --------------------------------------------------------------------------
    # HELPER: 5-point Rating Scale in Korean
    # --------------------------------------------------------------------------
    five_point_scale = [
        "전혀 그렇지 않다",
        "그렇지 않다",
        "보통이다",
        "그렇다",
        "매우 그렇다"
    ]

    # --------------------------------------------------------------------------
    # DEMOGRAPHIC QUESTIONS (기업용)
    # --------------------------------------------------------------------------
    q_corp_demo_gender, _ = Question.objects.get_or_create(
        text="귀하의 성별은?",
        question_type="radio",
        defaults={
            "options": ["남성", "여성"],
            "category": "demographic_corp"
        }
    )
    q_corp_demo_age, _ = Question.objects.get_or_create(
        text="귀하의 연령은?",
        question_type="radio",
        defaults={
            "options": ["20대", "30대", "40대", "50대", "60대"],
            "category": "demographic_corp"
        }
    )
    q_corp_demo_marital, _ = Question.objects.get_or_create(
        text="귀하의 결혼 유무는?",
        question_type="radio",
        defaults={
            "options": ["미혼", "기혼"],
            "category": "demographic_corp"
        }
    )
    q_corp_demo_education, _ = Question.objects.get_or_create(
        text="귀하의 최종 학력은?",
        question_type="radio",
        defaults={
            "options": [
                "고등학교 졸업",
                "전문대 졸업",
                "대학교 졸업",
                "석사 졸업",
                "박사 졸업"
            ],
            "category": "demographic_corp"
        }
    )
    q_corp_demo_tenure, _ = Question.objects.get_or_create(
        text="귀하가 재직중인 회사 근속 기간은?",
        question_type="radio",
        defaults={
            "options": [
                "1년 미만",
                "1년 이상~3년 미만",
                "3년 이상~5년 미만",
                "5년 이상~7년 이하"
            ],
            "category": "demographic_corp"
        }
    )
    q_corp_demo_jobfield, _ = Question.objects.get_or_create(
        text="귀하의 직군은?",
        question_type="radio",
        defaults={
            "options": [
                "사무/행정/경영 지원",
                "기획/홍보/마케팅",
                "IT/인터넷",
                "디자인",
                "영업/서비스",
                "연구/개발/설계",
                "생산/제조/기술",
                "교육",
                "건설",
                "의료/보건/복지",
                "미디어",
                "전문/특수직"
            ],
            "category": "demographic_corp"
        }
    )
    q_corp_demo_position, _ = Question.objects.get_or_create(
        text="귀하의 직급은?",
        question_type="radio",
        defaults={
            "options": [
                "사원",
                "주임",
                "대리",
                "과장",
                "차장",
                "부장 이상"
            ],
            "category": "demographic_corp"
        }
    )
    q_corp_demo_employment_type, _ = Question.objects.get_or_create(
        text="귀하의 근무 형태는?",
        question_type="radio",
        defaults={
            "options": ["정규직", "비정규직"],
            "category": "demographic_corp"
        }
    )
    q_corp_demo_income, _ = Question.objects.get_or_create(
        text="귀하의 소득(월소득 세전기준)은?",
        question_type="radio",
        defaults={
            "options": [
                "200만원 미만",
                "200만원 이상~300만원 미만",
                "300만원 이상~400만원 미만",
                "400만원 이상~500만원 미만",
                "600만원이상"
            ],
            "category": "demographic_corp"
        }
    )

    # --------------------------------------------------------------------------
    # DEMOGRAPHIC QUESTIONS (개인용)
    # --------------------------------------------------------------------------
    q_personal_demo_gender, _ = Question.objects.get_or_create(
        text="귀하의 성별은? (개인용)",
        question_type="radio",
        defaults={
            "options": ["남성", "여성"],
            "category": "demographic_personal"
        }
    )
    q_personal_demo_age, _ = Question.objects.get_or_create(
        text="귀하의 연령은? (개인용)",
        question_type="radio",
        defaults={
            "options": ["20대", "30대", "40대", "50대", "60대"],
            "category": "demographic_personal"
        }
    )
    q_personal_demo_marital, _ = Question.objects.get_or_create(
        text="귀하의 결혼 유무는? (개인용)",
        question_type="radio",
        defaults={
            "options": ["미혼", "기혼"],
            "category": "demographic_personal"
        }
    )
    q_personal_demo_education, _ = Question.objects.get_or_create(
        text="귀하의 최종 학력은? (개인용)",
        question_type="radio",
        defaults={
            "options": [
                "고등학교 졸업",
                "전문대 졸업",
                "대학교 졸업",
                "석사 졸업",
                "박사 졸업"
            ],
            "category": "demographic_personal"
        }
    )
    q_personal_demo_jobfield, _ = Question.objects.get_or_create(
        text="귀하의 직군은? (개인용)",
        question_type="radio",
        defaults={
            "options": [
                "사무/행정/경영 지원",
                "기획/홍보/마케팅",
                "IT/인터넷",
                "디자인",
                "영업/서비스",
                "연구/개발/설계",
                "생산/제조/기술",
                "교육",
                "건설",
                "의료/보건/복지",
                "미디어",
                "전문/특수직"
            ],
            "category": "demographic_personal"
        }
    )
    q_personal_demo_income, _ = Question.objects.get_or_create(
        text="귀하의 소득(월소득 세전기준)은? (개인용)",
        question_type="radio",
        defaults={
            "options": [
                "200만원 미만",
                "200만원 이상~300만원 미만",
                "300만원 이상~400만원 미만",
                "400만원 이상~500만원 미만",
                "600만원이상"
            ],
            "category": "demographic_personal"
        }
    )

    # --------------------------------------------------------------------------
    # LIFESTYLE QUESTIONS (공통 15 items, 5-point rating)
    # --------------------------------------------------------------------------
    lifestyle_texts = [
        "1. 삶의 여유를 가지고 생활하는 편이다.",
        "2. 하고 싶은 일을 할 충분한 에너지가 있다.",
        "3. 나만의 스타일이 있다는 이야기를 자주 듣는다.",
        "4. 새로운 패션이나 유행에 민감하다.",
        "5. 신제품이 출시되면 남보다 빨리 구매하는 편이다.",
        "6. 취미활동을 위한 모임이나 동호회 활동에 정기적으로 참여한다.",
        "7. 이사를 하지 않고 한 곳에서 오래 사 는 것이 좋다.",
        "8. 나는 제한된 근무를 선호한다.",
        "9. 노후를 대비하여 계획을 세우고 있다.",
        "10. 다양한 변화가 있는 생활을 좋아한다.",
        "11. 단순한 삶(심플·미니멀 라이프)을 살고 싶다.",
        "12. 새로운 것을 추구하기보다 전부터 해 오던 방식을 따르는 편이다.",
        "13. 자기개발을 위한 노력을 계속하는 편이다.",
        "14. 나의 건강과 노후에 관심이 많다.",
        "15. 건강을 위해 주기적인 운동을 하며 정기검진을 받고 있다."
    ]
    lifestyle_questions = []
    for txt in lifestyle_texts:
        q, _ = Question.objects.get_or_create(
            text=f"라이프스타일: {txt}",
            question_type="rating",
            defaults={
                "options": five_point_scale,
                "category": "lifestyle"
            }
        )
        lifestyle_questions.append(q)

    # --------------------------------------------------------------------------
    # 비전하우스: 긍정심리자본(자기효능감, 낙관주의, 희망, 회복탄력성)
    # Each subscale has 5 items. We'll categorize them "ppc_efficacy", "ppc_optimism", etc.
    # --------------------------------------------------------------------------
    efficacy_texts = [
        "나는 어려운 상황을 잘 극복할 수 있는 능력이 있다.",
        "나는 일을 효율적으로 다룰 수 있는 능력이 있다.",
        "나는 일이 잘못된 방향으로 진행될 때 빨리 바로잡는다.",
        "나는 어떤 일의 원인과 결과를 잘 찾아낼 수 있다.",
        "나는 항상 목표를 세우고 목표에 따라 일의 진행 상태를 확인할 수 있다."
    ]
    optimism_texts = [
        "나는 불확실한 상황에서도 최상의 결과를 기대한다.",
        "나는 내 미래에 대해 항상 낙관적이다.",
        "나는 새로운 일을 시작할 때 성공할 것이라고 기대한다.",
        "나는 '뜻이 있는 곳에 길이 있다' 고 생각한다.",
        "나는 대체로 모든 일들의 결과가 좋을 것으로 생각한다."
    ]
    hope_texts = [
        "나는 현재 목표를 인지하고 이를 위해 힘차게 나아가고 있다.",
        "나는 어려운 상황이 있더라도 이를 해결할 방법이 많다고 생각한다.",
        "나는 현재 내 삶에 적극적인 삶을 살고 있다고 생각한다.",
        "나는 목표에 도달할 수 있는 많은 방법을 생각해 낼 수 있다.",
        "나는 현재 목표한 계획에 따라 나아가고 있다고 생각한다."
    ]
    resilience_texts = [
        "나는 어려운 일을 겪더라도 빨리 회복하는 편이다.",
        "나는 스트레스를 받고 회복 과정이 오래 걸리지 않는다.",
        "나는 대체로 힘든 일을 벌려도 어려움 없이 잘 견뎌낸다.",
        "나는 결과보다 과정의 성장을 돕는다고 생각한다.",
        "나는 분명한 목표가 있는 삶을 살아가고 있다."
    ]

    def create_scale_questions(prefix, lines, category):
        objs = []
        for idx, line in enumerate(lines, start=1):
            text = f"{prefix} {idx}. {line}"
            qobj, _ = Question.objects.get_or_create(
                text=text,
                question_type="rating",
                defaults={"options": five_point_scale, "category": category}
            )
            objs.append(qobj)
        return objs

    efficacy_qs = create_scale_questions("긍정심리자본(자기효능감)", efficacy_texts, "ppc_efficacy")
    optimism_qs = create_scale_questions("긍정심리자본(낙관주의)", optimism_texts, "ppc_optimism")
    hope_qs = create_scale_questions("긍정심리자본(희망)", hope_texts, "ppc_hope")
    resilience_qs = create_scale_questions("긍정심리자본(회복탄력성)", resilience_texts, "ppc_resilience")

    # --------------------------------------------------------------------------
    # 리더십과 혁신(개인용, 기업용)
    # --------------------------------------------------------------------------
    # (개인용) reuses ppc_resilience for 회복탄력성. We'll keep the category as "ppc_resilience".

    # 셀프 리더십: 행동중심전략(4), 자연적보상(4), 건설적사고(4)
    selflead_behavior_texts = [
        "나는 업무의 진행 상황에 관심을 쓴다.",
        "나는 내가 업무를 얼마나 잘하는지에 대해 주의를 기울인다.",
        "나는 마음속에 나의 목표들을 인식하고 있다.",
        "나는 내일의 진행 정도를 기록한다."
    ]
    selflead_natural_texts = [
        "나는 업무상 책임 영역을 더 넓히려고 한다.",
        "나는 업무상 책임을 늘리는 방법에 집중한다.",
        "나는 다른 사람으로부터 얻어낼 수 있는 새로운 책임에 대해 자주 생각한다.",
        "나는 나에게 할당된 책임보다 더 열심히 일하려고 한다."
    ]
    selflead_constructive_texts = [
        "나는 자기 스스로 문제를 해결하려고 행동한다.",
        "나는 자신의 힘으로 문제를 해결하는 것을 좋아한다.",
        "나는 나에게 문제가 생기면 스스로 해결한다.",
        "나는 스스로 문제의 해결 방법을 끝까지 찾아낸다."
    ]

    selflead_behavior_qs = create_scale_questions("셀프 리더십(행동중심전략)", selflead_behavior_texts, "selflead_behavior")
    selflead_natural_qs = create_scale_questions("셀프 리더십(자연적보상)", selflead_natural_texts, "selflead_natural")
    selflead_constructive_qs = create_scale_questions("셀프 리더십(건설적사고)", selflead_constructive_texts, "selflead_constructive")

    # (기업용) 조직몰입: 정서적 몰입(5), 지속적 몰입(5), 규범적 몰입(5)
    org_affective_texts = [
        "나는 회사에 강한 소속감을 느끼고 있다.",
        "나는 회사의 일원임을 느끼고 있다.",
        "나는 회사의 문제나 위협을 나 자신의 문제처럼 느끼고 있다.",
        "나는 회사에 감정적 애착을 느끼고 있다.",
        "나는 앞으로 남은 직장생활을 현재의 직장에서 보내게 된다면 행복할 것이다."
    ]
    org_continuance_texts = [
        "내가 희망하더라도 지금 당장 회사를 그만두기는 어렵다.",
        "지금 회사를 그만둔다면 내 생활이 혼란스러워질 것이다.",
        "내가 회사를 그만두지 못하는 이유는 재취업할 곳이 적어서이다.",
        "내가 이 회사에 다니는 이유는 내가 원해서이기도 하지만 회사에서 날 필요로 하기 때문이다.",
        "지금 이 회사를 그만둔다면 손해 보는 것이 많을 것이다."
    ]
    org_normative_texts = [
        "나는 회사에 남아야 하는 의무감을 가지고 있다.",
        "다른 회사에서 좋은 조건을 제시한다 해도 현재 회사를 그만둔다면 옳지 않다고 느낀다.",
        "만약 이 회사를 그만둔다면 죄책감을 느낄 것이다.",
        "나는 이 회사가 충성심을 가질만한 가치가 있다고 생각한다.",
        "나는 회사 동료들에 대한 의무감으로 현재 회사를 당장 떠나지 못한다."
    ]

    org_affective_qs = create_scale_questions("조직몰입(정서적 몰입)", org_affective_texts, "org_affective")
    org_continuance_qs = create_scale_questions("조직몰입(지속적 몰입)", org_continuance_texts, "org_continuance")
    org_normative_qs = create_scale_questions("조직몰입(규범적 몰입)", org_normative_texts, "org_normative")

    # --------------------------------------------------------------------------
    # 기업가정신과 혁신: (혁신성, 진취성, 위험감수성) each 5 items
    # --------------------------------------------------------------------------
    innov_texts = [
        "나는 항상 새로운 제품이나 기술 등에 관심이 많다.",
        "나는 혁신적인 변화를 통해 우리 조직의 성과를 항상 시키려고 노력한다.",
        "나는 다른 사람의 세부도 독창적인 아이디어를 적극적으로 수용하는 편이다.",
        "나는 조직의 위계질서와 관행보다 독창적인 아이디어와 변화를 더 중요시한다.",
        "나는 새로운 도전에 대한 실패를 질책하지 않는다."
    ]
    proact_texts = [
        "나는 항상 경쟁회사의 전략에 관심을 갖고 있다.",
        "나는 시장에서 주도적 위치를 확보하기 위해 부단히 노력한다.",
        "나는 경쟁사와의 지나친 경쟁은 어쩔 수 없는 일이라 생각한다.",
        "나는 새로운 제품이나 서비스 개발에서 경쟁사를 앞지르려 노력한다.",
        "나는 고객의 니즈를 파악하기 위해 적극적으로 노력한다."
    ]
    risk_texts = [
        "나는 새로운 사업 분야에 적극적으로 진출하려고 노력한다.",
        "나는 다소 위험이 있더라도 과감하게 도전하려는 의지가 높은 편이다.",
        "나는 잠재적인 기회 포착을 위해 약간은 무모하더라도 공격적인 자세를 취한다.",
        "나는 불확실한 상황에서도 과감하게 의사결정을 하는 편이다.",
        "나는 저위험-저수익 사업보다는 고위험-고수익 사업을 추진하려는 성향이 있다."
    ]

    innov_qs = create_scale_questions("기업가정신(혁신성)", innov_texts, "entrepreneur_innov")
    proact_qs = create_scale_questions("기업가정신(진취성)", proact_texts, "entrepreneur_proact")
    risk_qs = create_scale_questions("기업가정신(위험감수성)", risk_texts, "entrepreneur_risk")

    # --------------------------------------------------------------------------
    # HELPER to link Questions to SurveyType
    # --------------------------------------------------------------------------
    def stq_create(survey_type_obj, question_obj, order):
        SurveyTypeQuestion.objects.get_or_create(
            survey_type=survey_type_obj,
            question=question_obj,
            defaults={"order": order, "is_required": True}
        )

    # 개인용 -> demographic
    personal_demo_list = [
        q_personal_demo_gender,
        q_personal_demo_age,
        q_personal_demo_marital,
        q_personal_demo_education,
        q_personal_demo_jobfield,
        q_personal_demo_income
    ]
    for i, qd in enumerate(personal_demo_list, start=1):
        stq_create(st_personal, qd, i)

    # 기업용 -> demographic
    corp_demo_list = [
        q_corp_demo_gender,
        q_corp_demo_age,
        q_corp_demo_marital,
        q_corp_demo_education,
        q_corp_demo_tenure,
        q_corp_demo_jobfield,
        q_corp_demo_position,
        q_corp_demo_employment_type,
        q_corp_demo_income
    ]
    offset = 1
    for qd in corp_demo_list:
        stq_create(st_corporate, qd, offset)
        offset += 1

    # Everyone -> lifestyle questions (category = "lifestyle")
    base_order = 100  # so they appear after demographics in ordering
    for i, ql in enumerate(lifestyle_questions, start=1):
        stq_create(st_personal, ql, base_order + i)
        stq_create(st_corporate, ql, base_order + i)

    # --------------------------------------------------------------------------
    # HELPER to link Questions to CourseType
    # --------------------------------------------------------------------------
    def ctq_create(course_type_obj, question_obj, order):
        CourseTypeQuestion.objects.get_or_create(
            course_type=course_type_obj,
            question=question_obj,
            defaults={"order": order, "is_required": True}
        )

    # --------------------------------------------------------------------------
    # A) 비전하우스(개인, 기업) -> 4 subscales x 5 items = 20 total
    # --------------------------------------------------------------------------
    sub_order = 1
    for qobj in (efficacy_qs + optimism_qs + hope_qs + resilience_qs):
        ctq_create(ct_vision_personal, qobj, sub_order)
        ctq_create(ct_vision_corp, qobj, sub_order)
        sub_order += 1

    # --------------------------------------------------------------------------
    # B) 리더십과 혁신(개인용): 회복탄력성(5) + 셀프 리더십(행동4, 자연4, 건설4) = total 17
    #    We'll reuse ppc_resilience for 회복탄력성, so those questions remain "ppc_resilience" category.
    # --------------------------------------------------------------------------
    sub_order = 1
    for qobj in resilience_qs:
        ctq_create(ct_leadership_personal, qobj, sub_order)
        sub_order += 1
    for qobj in (selflead_behavior_qs + selflead_natural_qs + selflead_constructive_qs):
        ctq_create(ct_leadership_personal, qobj, sub_order)
        sub_order += 1

    # --------------------------------------------------------------------------
    # C) 리더십과 혁신(기업용): 셀프 리더십(행동4, 자연4, 건설4) + 조직몰입(정서5, 지속5, 규범5) = 18
    # --------------------------------------------------------------------------
    sub_order = 1
    for qobj in (selflead_behavior_qs + selflead_natural_qs + selflead_constructive_qs):
        ctq_create(ct_leadership_corp, qobj, sub_order)
        sub_order += 1
    for qobj in (org_affective_qs + org_continuance_qs + org_normative_qs):
        ctq_create(ct_leadership_corp, qobj, sub_order)
        sub_order += 1

    # --------------------------------------------------------------------------
    # D) 기업가정신과 혁신(개인/기업): 혁신성(5), 진취성(5), 위험감수성(5) = 15 total
    # --------------------------------------------------------------------------
    sub_order = 1
    for qobj in (innov_qs + proact_qs + risk_qs):
        ctq_create(ct_entrepreneur_personal, qobj, sub_order)
        ctq_create(ct_entrepreneur_corp, qobj, sub_order)
        sub_order += 1

    print("=== All survey data populated successfully! ===")


if __name__ == "__main__":
    main()
