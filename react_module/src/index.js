import React from 'react';
import ReactDOM from 'react-dom/client';
import AnimatedMulti from './select';
import App from './echart_demo';
import ReportPage from './tableReport';





const root = ReactDOM.createRoot(document.getElementById('root'));

root.render(
  <React.StrictMode>
    {/* <AnimatedMulti /> */}
    <ReportPage />
  </React.StrictMode>
);


// root.render(
//   <React.StrictMode>
//     <App />
//   </React.StrictMode>
// );

// If you want to start measuring performance in your app, pass a function
// to log results (for example: reportWebVitals(console.log))
// or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
