import React from 'react';
import ReactDOM from 'react-dom/client';
import AnimatedMulti from './select';
import App from './echart_demo';
import ReportPage from './tableReport';





const root = ReactDOM.createRoot(document.getElementById('root'));

root.render(
  // 不注释掉 strictmode的话effect会执行两次，在多选框那个模块就会报错了
  // <React.StrictMode>
  <div>
    {/* <AnimatedMulti /> */}
    <ReportPage />
  </div>
  // </React.StrictMode>
);


// root.render(
//   <React.StrictMode>
//     <App />
//   </React.StrictMode>
// );

// If you want to start measuring performance in your app, pass a function
// to log results (for example: reportWebVitals(console.log))
// or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
