// JEE Advanced 2026 Score Calculator - Core JS Logic

// Define Constants & Marking Schemes
const SUBJECTS = {
  PHYSICS: 'physics',
  CHEMISTRY: 'chemistry',
  MATHEMATICS: 'math'
};

const Q_TYPES = {
  SCQ: 'scq',     // Single Correct Option
  MSQ: 'msq',     // One or More Correct Options
  NAT: 'nat',     // Numerical Answer Type
  MATCH: 'match', // List Match / Match the Column
  PARA: 'para'    // Paragraph with Numerical/SCQ Answers
};

// Global State
let state = {
  activePaper: 1, // 1 or 2
  activeSubject: SUBJECTS.PHYSICS,
  activeInstitute: 'allen', // 'allen', 'motion', 'resonance', 'pw'
  userResponses: {
    paper1: {}, // { qId/qNum: "Response" }
    paper2: {}
  },
  questionData: {
    paper1: [],
    paper2: []
  },
  instituteKeys: {
    paper1: {
      allen: {},
      motion: {},
      resonance: {},
      pw: {}
    },
    paper2: {
      allen: {},
      motion: {},
      resonance: {},
      pw: {}
    }
  }
};

// Generate highly realistic question data for JEE Advanced 2026
function initQuestionStructures() {
  // --- PAPER 1: 48 questions (16 per subject) ---
  // Subjects: Physics (Q1-16), Chemistry (Q17-32), Mathematics (Q33-48)
  const p1Sections = [
    { type: Q_TYPES.SCQ, count: 4, label: 'Section 1: Single Correct MCQs', marks: '+3 / -1' },
    { type: Q_TYPES.MSQ, count: 4, label: 'Section 2: Multi-Correct MCQs', marks: '+4 / -1 (Partial)' },
    { type: Q_TYPES.NAT, count: 4, label: 'Section 3: Numerical NAT', marks: '+4 / 0' },
    { type: Q_TYPES.MATCH, count: 4, label: 'Section 4: Matching Lists', marks: '+3 / -1' }
  ];

  let p1Physics = [];
  let p1Chem = [];
  let p1Math = [];

  // Helper to generate key values
  const choices = ['A', 'B', 'C', 'D'];
  const msqChoices = ['A,B', 'B,C', 'A,C', 'A,D', 'B,D', 'A,B,C', 'B,C,D', 'A,C,D', 'A,B,C,D'];
  const natChoices = ['3', '5', '0.5', '12.5', '0.25', '8', '2', '4.75', '0', '-2'];

  let qGlobalNum = 1;

  // PHYSICS (Q1 - Q16)
  for (let secIdx = 0; secIdx < p1Sections.length; secIdx++) {
    const sec = p1Sections[secIdx];
    for (let i = 0; i < sec.count; i++) {
      const qNum = qGlobalNum++;
      const qId = 830000 + qNum * 123;
      p1Physics.push({
        num: qNum,
        id: qId.toString(),
        subject: SUBJECTS.PHYSICS,
        type: sec.type,
        sectionIndex: secIdx,
        sectionLabel: sec.label,
        marksLabel: sec.marks
      });
    }
  }

  // CHEMISTRY (Q17 - Q32)
  for (let secIdx = 0; secIdx < p1Sections.length; secIdx++) {
    const sec = p1Sections[secIdx];
    for (let i = 0; i < sec.count; i++) {
      const qNum = qGlobalNum++;
      const qId = 830000 + qNum * 123;
      p1Chem.push({
        num: qNum,
        id: qId.toString(),
        subject: SUBJECTS.CHEMISTRY,
        type: sec.type,
        sectionIndex: secIdx,
        sectionLabel: sec.label,
        marksLabel: sec.marks
      });
    }
  }

  // MATHEMATICS (Q33 - Q48)
  for (let secIdx = 0; secIdx < p1Sections.length; secIdx++) {
    const sec = p1Sections[secIdx];
    for (let i = 0; i < sec.count; i++) {
      const qNum = qGlobalNum++;
      const qId = 830000 + qNum * 123;
      p1Math.push({
        num: qNum,
        id: qId.toString(),
        subject: SUBJECTS.MATHEMATICS,
        type: sec.type,
        sectionIndex: secIdx,
        sectionLabel: sec.label,
        marksLabel: sec.marks
      });
    }
  }

  state.questionData.paper1 = [...p1Physics, ...p1Chem, ...p1Math];

  // --- PAPER 2: 54 questions (18 per subject) ---
  // Subjects: Physics (Q1-18), Chemistry (Q19-36), Mathematics (Q37-54)
  const p2Sections = [
    { type: Q_TYPES.SCQ, count: 4, label: 'Section 1: Single Correct MCQs', marks: '+3 / -1' },
    { type: Q_TYPES.MSQ, count: 5, label: 'Section 2: Multi-Correct MCQs', marks: '+4 / -1 (Partial)' },
    { type: Q_TYPES.NAT, count: 5, label: 'Section 3: Numerical NAT', marks: '+4 / 0' },
    { type: Q_TYPES.PARA, count: 4, label: 'Section 4: Paragraph Questions (Numerical Answers)', marks: '+4 / -1' }
  ];

  let p2Physics = [];
  let p2Chem = [];
  let p2Math = [];

  qGlobalNum = 1;

  // PHYSICS (Q1 - Q18)
  for (let secIdx = 0; secIdx < p2Sections.length; secIdx++) {
    const sec = p2Sections[secIdx];
    for (let i = 0; i < sec.count; i++) {
      const qNum = qGlobalNum++;
      const qId = 940000 + qNum * 147;
      p2Physics.push({
        num: qNum,
        id: qId.toString(),
        subject: SUBJECTS.PHYSICS,
        type: sec.type,
        sectionIndex: secIdx,
        sectionLabel: sec.label,
        marksLabel: sec.marks
      });
    }
  }

  // CHEMISTRY (Q19 - Q36)
  for (let secIdx = 0; secIdx < p2Sections.length; secIdx++) {
    const sec = p2Sections[secIdx];
    for (let i = 0; i < sec.count; i++) {
      const qNum = qGlobalNum++;
      const qId = 940000 + qNum * 147;
      p2Chem.push({
        num: qNum,
        id: qId.toString(),
        subject: SUBJECTS.CHEMISTRY,
        type: sec.type,
        sectionIndex: secIdx,
        sectionLabel: sec.label,
        marksLabel: sec.marks
      });
    }
  }

  // MATHEMATICS (Q37 - Q54)
  for (let secIdx = 0; secIdx < p2Sections.length; secIdx++) {
    const sec = p2Sections[secIdx];
    for (let i = 0; i < sec.count; i++) {
      const qNum = qGlobalNum++;
      const qId = 940000 + qNum * 147;
      p2Math.push({
        num: qNum,
        id: qId.toString(),
        subject: SUBJECTS.MATHEMATICS,
        type: sec.type,
        sectionIndex: secIdx,
        sectionLabel: sec.label,
        marksLabel: sec.marks
      });
    }
  }

  state.questionData.paper2 = [...p2Physics, ...p2Chem, ...p2Math];

  // --- Preload Answer Keys ---
  const insts = ['allen', 'motion', 'resonance', 'pw'];

  // Paper 1
  state.questionData.paper1.forEach((q) => {
    insts.forEach((inst) => {
      let ans = '';
      if (q.type === Q_TYPES.SCQ || q.type === Q_TYPES.MATCH) {
        // Pseudo-random but consistent answer key
        const seed = parseInt(q.id) + inst.charCodeAt(0);
        ans = choices[seed % 4];
      } else if (q.type === Q_TYPES.MSQ) {
        const seed = parseInt(q.id) + inst.charCodeAt(0);
        ans = msqChoices[seed % msqChoices.length];
      } else if (q.type === Q_TYPES.NAT) {
        const seed = parseInt(q.id) + inst.charCodeAt(0);
        ans = natChoices[seed % natChoices.length];
      }
      state.instituteKeys.paper1[inst][q.num] = ans;
    });

    // Add a few deliberate discrepancies to showcase the feature
    if (q.num === 5 || q.num === 21 || q.num === 37) { // MSQ questions
      state.instituteKeys.paper1.allen[q.num] = 'A,C';
      state.instituteKeys.paper1.motion[q.num] = 'A,B,C';
      state.instituteKeys.paper1.resonance[q.num] = 'A,C';
      state.instituteKeys.paper1.pw[q.num] = 'A,C';
    }
    if (q.num === 10 || q.num === 26 || q.num === 42) { // NAT questions
      state.instituteKeys.paper1.allen[q.num] = '0.5';
      state.instituteKeys.paper1.motion[q.num] = '0.5';
      state.instituteKeys.paper1.resonance[q.num] = '1/2';
      state.instituteKeys.paper1.pw[q.num] = '0.5';
    }
  });

  // Paper 2
  state.questionData.paper2.forEach((q) => {
    insts.forEach((inst) => {
      let ans = '';
      if (q.type === Q_TYPES.SCQ) {
        const seed = parseInt(q.id) + inst.charCodeAt(0);
        ans = choices[seed % 4];
      } else if (q.type === Q_TYPES.MSQ) {
        const seed = parseInt(q.id) + inst.charCodeAt(0);
        ans = msqChoices[seed % msqChoices.length];
      } else if (q.type === Q_TYPES.NAT || q.type === Q_TYPES.PARA) {
        const seed = parseInt(q.id) + inst.charCodeAt(0);
        ans = natChoices[seed % natChoices.length];
      }
      state.instituteKeys.paper2[inst][q.num] = ans;
    });

    // Add discrepancies in Paper 2
    if (q.num === 6 || q.num === 24 || q.num === 43) { // MSQ
      state.instituteKeys.paper2.allen[q.num] = 'B,D';
      state.instituteKeys.paper2.motion[q.num] = 'B,D';
      state.instituteKeys.paper2.resonance[q.num] = 'A,B,D';
      state.instituteKeys.paper2.pw[q.num] = 'B,D';
    }
    if (q.num === 15 || q.num === 33 || q.num === 51) { // Paragraph numerical
      state.instituteKeys.paper2.allen[q.num] = '2';
      state.instituteKeys.paper2.motion[q.num] = '3';
      state.instituteKeys.paper2.resonance[q.num] = '2';
      state.instituteKeys.paper2.pw[q.num] = '2';
    }
  });
}

// Calculate score for a single question based on chosen response and a single key
function calculateSingleKeyScore(q, cleanResp, cleanCorrect) {
  // 1. Single Correct MCQ (SCQ) or Matching list
  if (q.type === Q_TYPES.SCQ || q.type === Q_TYPES.MATCH) {
    if (cleanResp === cleanCorrect) {
      return { score: 3, status: 'correct' };
    } else {
      return { score: -1, status: 'incorrect' };
    }
  }

  // 2. Numerical Answer Type (NAT) or Paragraph numerical
  if (q.type === Q_TYPES.NAT || q.type === Q_TYPES.PARA) {
    const isRange = cleanCorrect.includes('TO');
    const uNum = parseFloat(cleanResp);

    if (isNaN(uNum)) {
      return { score: 0, status: 'unattempted' };
    }

    if (isRange) {
      const parts = cleanCorrect.split('TO');
      const min = parseFloat(parts[0]);
      const max = parseFloat(parts[1]);
      if (!isNaN(min) && !isNaN(max) && uNum >= min && uNum <= max) {
        return { score: 4, status: 'correct' };
      }
    } else {
      const cNum = parseFloat(cleanCorrect);
      // Support fraction representation like 1/2 vs 0.5
      let correctMatches = false;
      if (cleanCorrect === '1/2' && uNum === 0.5) correctMatches = true;
      if (cleanCorrect === '1/4' && uNum === 0.25) correctMatches = true;
      if (cleanCorrect === '3/4' && uNum === 0.75) correctMatches = true;
      
      if (!isNaN(cNum) && Math.abs(uNum - cNum) < 1e-4) {
        correctMatches = true;
      }

      if (correctMatches) {
        return { score: 4, status: 'correct' };
      }
    }

    // Negative marking in Paper 2 Section 4 (Paragraph type questions) = -1
    if (q.type === Q_TYPES.PARA && state.activePaper === 2) {
      return { score: -1, status: 'incorrect' };
    }

    return { score: 0, status: 'incorrect' };
  }

  // 3. Multi-Correct MCQ (MSQ)
  if (q.type === Q_TYPES.MSQ) {
    const userOpts = cleanResp.split(',').map(o => o.trim()).filter(Boolean);
    const correctOpts = cleanCorrect.split(',').map(o => o.trim()).filter(Boolean);

    if (userOpts.length === 0) {
      return { score: 0, status: 'unattempted' };
    }

    // Check if any chosen option is incorrect
    const hasIncorrect = userOpts.some(o => !correctOpts.includes(o));
    if (hasIncorrect) {
      return { score: -1, status: 'incorrect' }; // In 2026 penalty is -1!
    }

    // All chosen options are correct. Now calculate marks
    const isPerfect = userOpts.length === correctOpts.length;
    if (isPerfect) {
      return { score: 4, status: 'correct' };
    }

    // Partial marking logic:
    // +3 if correct has 4 options and user selected 3 correct
    // +2 if correct has 3 or 4 options and user selected 2 correct
    // +1 if correct has 2, 3 or 4 options and user selected 1 correct
    const chosenCount = userOpts.length;
    if (chosenCount === 3 && correctOpts.length === 4) {
      return { score: 3, status: 'partial' };
    } else if (chosenCount === 2) {
      return { score: 2, status: 'partial' };
    } else if (chosenCount === 1) {
      return { score: 1, status: 'partial' };
    }

    return { score: 1, status: 'partial' }; // Fallback partial mark
  }

  return { score: 0, status: 'unattempted' };
}

// Calculate score for a single question based on chosen response and institute key (supporting alternative keys)
function calculateQuestionScore(q, userResp, correctAns) {
  if (!userResp || userResp.trim() === '' || userResp === '--') {
    return { score: 0, status: 'unattempted' };
  }

  const cleanResp = userResp.trim().toUpperCase();
  const cleanCorrect = correctAns.trim().toUpperCase();

  // If the answer key specifies multiple alternative correct options using "OR"
  if (cleanCorrect.includes('OR')) {
    const alts = cleanCorrect.split('OR').map(x => x.trim());
    let bestResult = null;
    
    for (let alt of alts) {
      const res = calculateSingleKeyScore(q, cleanResp, alt);
      if (!bestResult || res.score > bestResult.score) {
        bestResult = res;
      }
    }
    return bestResult;
  }

  return calculateSingleKeyScore(q, cleanResp, cleanCorrect);
}

// Calculate scores for everything in active state
function computeAllScores() {
  const paperKey = state.activePaper === 1 ? 'paper1' : 'paper2';
  const questions = state.questionData[paperKey];
  const activeKey = state.instituteKeys[paperKey][state.activeInstitute];
  const userRespMap = state.userResponses[paperKey];

  let totals = {
    score: 0,
    physicsScore: 0,
    chemScore: 0,
    mathScore: 0,
    attempted: 0,
    correct: 0,
    incorrect: 0,
    partial: 0,
    positiveMarks: 0,
    negativeMarks: 0
  };

  questions.forEach((q) => {
    const userResp = userRespMap[q.num] || '';
    const correctAns = activeKey[q.num] || '';
    const result = calculateQuestionScore(q, userResp, correctAns);

    q.currentScore = result.score;
    q.currentStatus = result.status;

    if (result.status !== 'unattempted') {
      totals.attempted++;
      if (result.status === 'correct') {
        totals.correct++;
        totals.positiveMarks += result.score;
      } else if (result.status === 'partial') {
        totals.partial++;
        totals.positiveMarks += result.score;
      } else if (result.status === 'incorrect') {
        totals.incorrect++;
        if (result.score < 0) {
          totals.negativeMarks += Math.abs(result.score);
        }
      }
    }

    totals.score += result.score;
    if (q.subject === SUBJECTS.PHYSICS) totals.physicsScore += result.score;
    if (q.subject === SUBJECTS.CHEMISTRY) totals.chemScore += result.score;
    if (q.subject === SUBJECTS.MATHEMATICS) totals.mathScore += result.score;
  });

  return totals;
}

// Compute cumulative (both Paper 1 and Paper 2) scores
function computeCumulativeScores() {
  const activeInst = state.activeInstitute;
  let totals = {
    score: 0,
    physics: 0,
    chemistry: 0,
    math: 0,
    paper1: 0,
    paper2: 0,
    attempted: 0,
    correct: 0,
    incorrect: 0
  };

  // Paper 1
  state.questionData.paper1.forEach((q) => {
    const resp = state.userResponses.paper1[q.num] || '';
    const key = state.instituteKeys.paper1[activeInst][q.num] || '';
    const res = calculateQuestionScore(q, resp, key);
    totals.score += res.score;
    totals.paper1 += res.score;
    if (q.subject === SUBJECTS.PHYSICS) totals.physics += res.score;
    if (q.subject === SUBJECTS.CHEMISTRY) totals.chemistry += res.score;
    if (q.subject === SUBJECTS.MATHEMATICS) totals.math += res.score;
    if (res.status !== 'unattempted') {
      totals.attempted++;
      if (res.status === 'correct' || res.status === 'partial') totals.correct++;
      else totals.incorrect++;
    }
  });

  // Paper 2
  state.questionData.paper2.forEach((q) => {
    const resp = state.userResponses.paper2[q.num] || '';
    const key = state.instituteKeys.paper2[activeInst][q.num] || '';
    const res = calculateQuestionScore(q, resp, key);
    totals.score += res.score;
    totals.paper2 += res.score;
    if (q.subject === SUBJECTS.PHYSICS) totals.physics += res.score;
    if (q.subject === SUBJECTS.CHEMISTRY) totals.chemistry += res.score;
    if (q.subject === SUBJECTS.MATHEMATICS) totals.math += res.score;
    if (res.status !== 'unattempted') {
      totals.attempted++;
      if (res.status === 'correct' || res.status === 'partial') totals.correct++;
      else totals.incorrect++;
    }
  });

  return totals;
}

// Parse Response Sheet text or HTML
function parseResponseSheet(pastedText) {
  if (!pastedText || pastedText.trim() === '') return 0;

  let parsedCount = 0;
  const lines = pastedText.split('\n');

  let currentQId = null;
  let currentStatus = null;
  let currentChosenOption = null;
  let currentGivenAnswer = null;

  let optionIds = {}; // { 1: id, 2: id, 3: id, 4: id }

  // Map of question ID to the parsed info
  let parsedMap = {};

  for (let i = 0; i < lines.length; i++) {
    const line = lines[i].trim();
    if (line === '') continue;

    // 1. Match Question ID
    const qidMatch = line.match(/(?:Question\s*ID\s*:\s*|Question\s*Id\s*:\s*|Q\.\s*Id\s*:\s*)(\d+)/i);
    if (qidMatch) {
      // If we already have a parsed question, save it first
      if (currentQId) {
        saveParsedQuestion(parsedMap, currentQId, currentStatus, currentChosenOption, currentGivenAnswer, optionIds);
      }
      // Reset for new question
      currentQId = qidMatch[1];
      currentStatus = null;
      currentChosenOption = null;
      currentGivenAnswer = null;
      optionIds = {};
      continue;
    }

    // 2. Match Status
    const statusMatch = line.match(/(?:Status\s*:\s*|Question\s*Status\s*:\s*)(Answered|Not\s*Answered|Marked\s*for\s*Review)/i);
    if (statusMatch) {
      currentStatus = statusMatch[1].trim();
      continue;
    }

    // 3. Match Option IDs (often Option 1 ID : 837283721)
    const optIdMatch = line.match(/(?:Option\s*([1-4])\s*ID\s*:\s*|Option\s*([1-4])\s*Id\s*:\s*)(\d+)/i);
    if (optIdMatch) {
      const optNum = optIdMatch[1] || optIdMatch[2];
      optionIds[optNum] = optIdMatch[3];
      continue;
    }

    // 4. Match Chosen Option (can be "2" or "A, B" or Option ID "837283723" or "--")
    const chosenMatch = line.match(/(?:Chosen\s*Option\s*:\s*|Option\s*Chosen\s*:\s*|Selected\s*Option\s*:\s*)(.*)/i);
    if (chosenMatch) {
      currentChosenOption = chosenMatch[1].trim();
      continue;
    }

    // 5. Match Given Answer (numerical keys)
    const givenMatch = line.match(/(?:Given\s*Answer\s*:\s*|Answer\s*Given\s*:\s*|Response\s*:\s*)(.*)/i);
    if (givenMatch) {
      currentGivenAnswer = givenMatch[1].trim();
      continue;
    }
  }

  // Save the last question in loop
  if (currentQId) {
    saveParsedQuestion(parsedMap, currentQId, currentStatus, currentChosenOption, currentGivenAnswer, optionIds);
  }

  // Now, merge the parsed values into our state based on matches of Question IDs!
  const paperKey = state.activePaper === 1 ? 'paper1' : 'paper2';
  const ourQuestions = state.questionData[paperKey];

  // Try matching. If Question IDs match directly, super. Otherwise, we can try to associate sequentially if they matched perfectly.
  // We match by:
  // - Scanning the parsedMap. If a parsed ID is found in our target paper's questions, we populate the response.
  ourQuestions.forEach((q) => {
    // Direct ID match
    let match = parsedMap[q.id];
    
    // If not matching directly, let's look if there is an ID match anywhere
    if (!match) {
      // Find by checking if the QID in the parsed text matches the last digits
      const keyMatch = Object.keys(parsedMap).find(id => id.endsWith(q.id) || q.id.endsWith(id));
      if (keyMatch) match = parsedMap[keyMatch];
    }

    if (match) {
      let finalResp = '--';
      if (match.status === 'Answered' || match.status === 'Marked for Review' || match.givenAnswer || match.chosenOption) {
        if (match.givenAnswer && match.givenAnswer !== '--') {
          finalResp = match.givenAnswer;
        } else if (match.chosenOption && match.chosenOption !== '--') {
          finalResp = match.chosenOption;
        }
      }
      state.userResponses[paperKey][q.num] = finalResp;
      parsedCount++;
    }
  });

  // If no direct ID matches (maybe they are mock IDs or sheet has different IDs), let's map them sequentially for any answered items
  if (parsedCount === 0) {
    // Sequential fallback: find all parsed answers and apply to questions sequentially
    const parsedList = Object.values(parsedMap);
    if (parsedList.length > 0) {
      const activeQuestions = ourQuestions.filter(q => q.subject === state.activeSubject);
      let pIdx = 0;
      activeQuestions.forEach((q) => {
        if (pIdx < parsedList.length) {
          const match = parsedList[pIdx++];
          let finalResp = '--';
          if (match.givenAnswer && match.givenAnswer !== '--') {
            finalResp = match.givenAnswer;
          } else if (match.chosenOption && match.chosenOption !== '--') {
            finalResp = match.chosenOption;
          }
          state.userResponses[paperKey][q.num] = finalResp;
          parsedCount++;
        }
      });
    }
  }

  return parsedCount;
}

// Helper to save current parsed state
function saveParsedQuestion(map, qId, status, chosen, given, optionIds) {
  let finalChosen = chosen;

  // If chosen option is a large number (Option ID), try matching with optionIds list
  if (chosen && chosen.match(/^\d+$/) && Object.keys(optionIds).length > 0) {
    const matchedOptNum = Object.keys(optionIds).find(num => optionIds[num] === chosen);
    if (matchedOptNum) {
      finalChosen = ['A', 'B', 'C', 'D'][parseInt(matchedOptNum) - 1];
    }
  } else if (chosen && chosen.match(/^[1-4]$/)) {
    // If chosen option is simply "1", "2", "3", "4", translate to A, B, C, D
    finalChosen = ['A', 'B', 'C', 'D'][parseInt(chosen) - 1];
  } else if (chosen && chosen.includes(',')) {
    // Handle multiple choice like "1, 3" -> "A,C"
    finalChosen = chosen.split(',')
      .map(c => c.trim())
      .map(c => {
        if (c.match(/^[1-4]$/)) return ['A', 'B', 'C', 'D'][parseInt(c) - 1];
        return c;
      })
      .join(',');
  }

  map[qId] = {
    id: qId,
    status: status || 'Answered',
    chosenOption: finalChosen || '--',
    givenAnswer: given || '--'
  };
}

// Find discrepancies between coaching institute keys
function findDiscrepancies() {
  const paperKey = state.activePaper === 1 ? 'paper1' : 'paper2';
  const questions = state.questionData[paperKey];
  const keys = state.instituteKeys[paperKey];

  let discrepancies = [];

  questions.forEach((q) => {
    const allenKey = (keys.allen[q.num] || '').trim();
    const motionKey = (keys.motion[q.num] || '').trim();
    const resonanceKey = (keys.resonance[q.num] || '').trim();
    const pwKey = (keys.pw[q.num] || '').trim();

    const uniqueAnswers = new Set([allenKey, motionKey, resonanceKey, pwKey].filter(Boolean));

    if (uniqueAnswers.size > 1) {
      discrepancies.push({
        num: q.num,
        id: q.id,
        subject: q.subject,
        type: q.type,
        allen: allenKey,
        motion: motionKey,
        resonance: resonanceKey,
        pw: pwKey
      });
    }
  });

  return discrepancies;
}

// Export / Import
function saveStateToLocalStorage() {
  localStorage.setItem('jee_adv_calculator_state', JSON.stringify({
    userResponses: state.userResponses,
    instituteKeys: state.instituteKeys
  }));
}

function loadStateFromLocalStorage() {
  const saved = localStorage.getItem('jee_adv_calculator_state');
  if (saved) {
    try {
      const parsed = JSON.parse(saved);
      if (parsed.userResponses) state.userResponses = parsed.userResponses;
      if (parsed.instituteKeys) state.instituteKeys = parsed.instituteKeys;
      return true;
    } catch (e) {
      console.error('Failed to load state', e);
    }
  }
  return false;
}

// Global Initialization
initQuestionStructures();
loadStateFromLocalStorage();

// Fetch latest keys asynchronously from live repository keys.json
async function loadRemoteKeys() {
  try {
    const response = await fetch('./keys.json');
    if (response.ok) {
      const remoteKeys = await response.json();
      if (remoteKeys.paper1) {
        state.instituteKeys.paper1 = remoteKeys.paper1;
      }
      if (remoteKeys.paper2) {
        state.instituteKeys.paper2 = remoteKeys.paper2;
      }
      console.log('Successfully fetched latest keys from live repository!');
      saveStateToLocalStorage();
      if (typeof updateUI === 'function') {
        updateUI();
      }
    }
  } catch (e) {
    console.warn('Could not fetch keys.json. Using local/cached keys instead.', e);
  }
}
loadRemoteKeys();

