import React, { createContext, useState } from 'react';

export const AuthContext = createContext<{ role: string }>({ role: 'advogado' });

export const AuthProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [role] = useState('advogado');
  return <AuthContext.Provider value={{ role }}>{children}</AuthContext.Provider>;
};
