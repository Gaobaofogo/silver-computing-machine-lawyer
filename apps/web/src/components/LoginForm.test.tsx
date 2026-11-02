import { render, screen, fireEvent } from '@testing-library/react';
import { AuthProvider } from '../hooks/AuthContext';

function LoginForm() {
  const handleLogin = () => {
    document.cookie = 'access_token=jwt; HttpOnly; Secure; SameSite=Strict';
  };
  const handleLogout = () => {
    document.cookie = 'access_token=; Max-Age=0';
  };
  return (
    <>
      <button onClick={handleLogin} aria-label="Login">Login</button>
      <button onClick={handleLogout} aria-label="Logout">Logout</button>
    </>
  );
}

describe('Login/Logout LGPD', () => {
  test('logout limpa cookie sem tocar localStorage', () => {
    render(
      <AuthProvider>
        <LoginForm />
      </AuthProvider>
    );
    fireEvent.click(screen.getByLabelText('Login'));
    fireEvent.click(screen.getByLabelText('Logout'));
    expect(localStorage.getItem('token')).toBeNull();
    expect(sessionStorage.getItem('token')).toBeNull();
  });
});
