import { renderHook } from '@testing-library/react';
import { useContext } from 'react';
import { AuthContext } from '../hooks/AuthContext';

describe('AuthContext — 04', () => {
  test('role eh apenas string, nao token', () => {
    const { result } = renderHook(() => useContext(AuthContext));
    // Red: AuthContext ainda nao existe
    expect(result.current.role).toBe('advogado');
  });
});
