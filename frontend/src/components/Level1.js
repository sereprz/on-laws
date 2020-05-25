import React from 'react';
import Level2 from './Level2.js';

export default function Level1({title, sections}) {
    
    const level2 = [...new Set(sections.map(s => s.level2))]
    
    return (
        <div>
            <h2>{title}</h2>
            {level2.map((l2, i) => {
                const sectionSubset = sections.filter(s => s.level2 === l2)
                return <Level2 title={l2} sections={sectionSubset} key={i}></Level2>
            })}
        </div>
    )
}