import React from 'react';
import Section from './Section.js';

export default function Level2({ title, sections }) {
    return (
        <div>
            <h3>{title}</h3>
            {sections.map((s, i) => <Section sectionObj={s} key={i}></Section>)}
        </div>
    )
}