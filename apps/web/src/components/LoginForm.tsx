import React from 'react';

export const LoginForm: React.FC = () => {
  const login = () => {
    document.cookie = 'access_token=jwt_demo; HttpOnly; Secure; SameSite=Strict; Path=/';
  };
  const logout = () => {
    document.cookie = 'access_token=; Max-Age=0; Path=/';
  };
  return (
    <div aria-label="Login e Logout">
      <button onClick={login} aria-label="Login">Login</button>
      <button onClick={logout} aria-label="Logout">Logout</button>
    </div>
  );
};
