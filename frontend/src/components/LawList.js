import React from 'react';

export default function LawList({ laws, setTitle, selected}) {
    return (
      <div className="law-list">
          {laws.map((law, i) => {
            return <div key={i}>
              <button onClick={() => setTitle(law.title)} className={selected === law.title ? "selected" : "not-selected"}>
                {law.title}
              </button>
            </div>
          })}
      </div>
       
    )
};