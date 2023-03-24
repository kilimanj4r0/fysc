import { StrictMode } from 'react';
import ReactDOM from 'react-dom/client';
import App from './App';
import './index.css';
import reportWebVitals from './reportWebVitals';

const renderLayout = () => {
  const appLayout = (
    <StrictMode>
      <App />
    </StrictMode>
  );

  return appLayout;
};

const root = ReactDOM.createRoot(document.getElementById('root') as HTMLElement);
root.render(renderLayout());

reportWebVitals();
