import React, { createContext, useState, useContext } from 'react';

const SeekerContext = createContext();

export const SeekerProvider = ({ children }) => {
  const [showSolo, setShowSolo] = useState(true);
  const [showCapstone, setShowCapstone] = useState(true);
  const [showGroup, setShowGroup] = useState(true);
  const [issueType, setIssueType] = useState('all');

  return (
    <SeekerContext.Provider value={{ showSolo, setShowSolo, showCapstone, setShowCapstone, showGroup, setShowGroup, issueType, setIssueType}}>
      {children}
    </SeekerContext.Provider>
  );
};

export const useSeeker = () => {
  return useContext(SeekerContext);
};