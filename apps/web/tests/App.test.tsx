import { test, expect } from 'vitest';
import { render, screen } from '@testing-library/react';
import App from '../src/App';

test('renders Judis-Advocacia title', () => {
  render(<App />);
  expect(screen.getByText(/Judis-Advocacia/i)).toBeInTheDocument();
});
