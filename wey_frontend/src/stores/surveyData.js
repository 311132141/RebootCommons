function generateIds(data) {
  let idCounter = 1; // Start ID counter

  // Helper function to assign IDs to an array of questions
  function assignIds(array) {
    return array.map((item) => ({
      ...item,
      id: idCounter++, // Assign a unique ID and increment the counter
    }));
  }

  return {
    courses: data.courses, // Courses do not require IDs to be changed
    demographics: {
      personal: assignIds(data.demographics.personal), // Assign IDs to personal questions
      corporate: assignIds(data.demographics.corporate), // Assign IDs to corporate questions
    },
    lifestyle: assignIds(data.lifestyle), // Assign IDs to lifestyle questions
    courseQuestions: Object.fromEntries(
      Object.entries(data.courseQuestions).map(([key, questions]) => [
        key,
        assignIds(questions), // Assign IDs to each course's questions
      ])
    ),
  };
}

// Input JSON data (with existing or missing IDs)
// const surveyDataWithoutIds = {
  export const surveyData = {
  courses: [
    { id: "visionHouse", name: "비전하우스" },
    { id: "leadership", name: "리더십과 혁신 교육" },
    { id: "entrepreneurship", name: "기업가정신" },
  ],
  demographics: {
    personal: [
      {
        text: "귀하의 성별은 무엇입니까?",
        type: "single",
        options: ["남성", "여성"],
      },
      {
        text: "귀하의 연령은 몇 세입니까?",
        type: "single",
        options: ["20대", "30대", "40대", "50대"],
      },
    ],
    corporate: [
      {
        text: "귀하의 직급은 무엇입니까?",
        type: "single",
        options: ["사원", "대리", "과장", "차장", "부장"],
      },
      {
        text: "귀하의 회사는 몇 명의 직원을 보유하고 있습니까?",
        type: "single",
        options: ["10명 이하", "10-50명", "50-100명", "100명 이상"],
      },
    ],
  },
  lifestyle: [
    {
      text: "삶의 여유를 가지고 생활하는 편입니까?",
      type: "likert",
      options: ["전혀 그렇지 않다", "그렇지 않다", "보통이다", "그렇다", "매우 그렇다"],
    },
    {
      text: "하고 싶은 일을 할 충분한 에너지가 있습니까?",
      type: "likert",
      options: ["전혀 그렇지 않다", "그렇지 않다", "보통이다", "그렇다", "매우 그렇다"],
    },
  ],
  courseQuestions: {
    "비전하우스": [
      {
        text: "나는 어려운 상황을 잘 극복할 수 있는 능력이 있다.",
        type: "likert",
        options: ["전혀 그렇지 않다", "그렇지 않다", "보통이다", "그렇다", "매우 그렇다"],
      },
      {
        text: "나는 일을 효과적으로 다룰 수 있는 능력이 있다.",
        type: "likert",
        options: ["전혀 그렇지 않다", "그렇지 않다", "보통이다", "그렇다", "매우 그렇다"],
      },
    ],
    "리더십과 혁신": [
      {
        text: "나는 업무의 진행 상황에 신경을 쓴다.",
        type: "likert",
        options: ["전혀 그렇지 않다", "그렇지 않다", "보통이다", "그렇다", "매우 그렇다"],
      },
      {
        text: "나는 내가 업무를 얼마나 잘하는지에 대해 주의를 기울인다.",
        type: "likert",
        options: ["전혀 그렇지 않다", "그렇지 않다", "보통이다", "그렇다", "매우 그렇다"],
      },
    ],
    "기업가정신과 혁신": [
      {
        text: "나는 항상 새로운 제품이나 기술 등에 관심이 많다.",
        type: "likert",
        options: ["전혀 그렇지 않다", "그렇지 않다", "보통이다", "그렇다", "매우 그렇다"],
      },
      {
        text: "나는 혁신적인 변화를 통해 우리 조직의 성과를 향상시키려고 노력한다.",
        type: "likert",
        options: ["전혀 그렇지 않다", "그렇지 않다", "보통이다", "그렇다", "매우 그렇다"],
      },
    ],
  },
};

