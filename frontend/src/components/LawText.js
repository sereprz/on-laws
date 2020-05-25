import React from 'react';
import Level1 from './Level1.js';


export default function LawText({title, sections}) {
  
  const level1 = [...new Set(sections.map(s => s.level1))]

  return (
      <div className='law'>
        <h1>{title}</h1>
          {level1.map((l1, i) => {
            const sectionSubset = sections.filter(s => s.level1 === l1);
            return <Level1 title={l1} sections={sectionSubset} key={i}></Level1>
          })}
      </div>
  )
}