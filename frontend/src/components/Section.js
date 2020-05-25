import React from 'react';

function getGradeLevel(flesh_score) {
    let gradeLevel = '';
  
    if (flesh_score < 0) {
      gradeLevel = 'q8-9';
    } else if (flesh_score >= 0 && flesh_score <= 30) {
      gradeLevel = 'q7-9';
    } else if (flesh_score > 30 && flesh_score <= 50) {
      gradeLevel = 'q6-9';
    } else if (flesh_score > 50 && flesh_score <= 60) {
      gradeLevel = 'q5-9';
    } else if (flesh_score > 60 && flesh_score <= 70) {
      gradeLevel = 'q4-9';
    } else if (flesh_score > 70 && flesh_score <= 80) {
      gradeLevel = 'q3-9';
    } else if (flesh_score > 80 && flesh_score <= 90) {
      gradeLevel = 'q2-9';
    } else if (flesh_score > 90 && flesh_score <= 100) {
      gradeLevel = 'q1-9';
    } else {
      gradeLevel = 'q0-9'
    }
    
    return gradeLevel
}

export default function Section(sectionObj) {

    const gradeLevel = getGradeLevel(sectionObj.sectionObj.flesh_score);

    return (
        <div className='section'>
            <h4>{sectionObj.sectionObj.level3}</h4>
            <p className={gradeLevel}>{sectionObj.sectionObj.text}</p>
        </div>
    )
}