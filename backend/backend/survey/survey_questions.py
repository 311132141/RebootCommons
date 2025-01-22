SURVEY_QUESTIONS = {
    'common': {
        'questions': [
            {'id': 'gender', 'text': '귀하의 성별은?', 'options': ['남성', '여성']},
            {'id': 'age', 'text': '귀하의 연령은?', 'options': ['20대', '30대', '40대', '50대', '60대']},
            {'id': 'marital_status', 'text': '귀하의 결혼 유무는?', 'options': ['미혼', '기혼']},
            {'id': 'education', 'text': '귀하의 최종 학력은?', 'options': ['고등학교 졸업', '전문대 졸업', '대학교 졸업', '석사 졸업', '박사 졸업']},
        ]
    },
    '개인용': {
        'questions': [
            {'id': 'income', 'text': '귀하의 소득은?', 'options': ['200만원 미만', '200-300만원', '300-400만원', '400만원 이상']},
        ]
    },
    '기업용': {
        'questions': [
            {'id': 'position', 'text': '귀하의 직급은?', 'options': ['사원', '주임', '대리', '과장', '차장', '부장']},
        ]
    },
}
