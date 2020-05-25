import React, { useState, useEffect } from 'react';
import LawList from './components/LawList.js';
import LawText from './components/LawText.js';
import * as laws from './data/laws.json';

function App() {
  const [title, setTitle] = useState(laws.default[0].title)
  const [sections, setSections] = useState(laws.default[0].sections)

  console.log(title)

  useEffect(() => {
    const selectedLaw = laws.default.filter(law => {
      return law.title === title;
    })
    setSections(selectedLaw[0].sections)
  }, [title])
  
  return (
    <div className="App">
    <LawList laws={laws.default} setTitle={setTitle} selected={title}></LawList>
    <LawText title={title} sections={sections}></LawText>
    </div>
  );
}

export default App;
