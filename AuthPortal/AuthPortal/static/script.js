/**
 * RDSO Portal — UI Interaction Helpers
 * 
 * This file only handles frontend UI interactions:
 * - Tab switching between Sign In / Create Account
 * - Password visibility toggle
 * - Auto-opening the register tab when server returns validation errors
 * 
 * All authentication logic is handled server-side by Django.
 */
document.addEventListener('DOMContentLoaded', () => {

  // --- Tab Elements ---
  const tabLoginBtn = document.getElementById('tab-login-btn');
  const tabRegisterBtn = document.getElementById('tab-register-btn');

  // --- Screen Panes ---
  const paneLogin = document.getElementById('pane-login');
  const paneRegister = document.getElementById('pane-register');

  // --- Password Toggle ---
  const loginPassToggle = document.getElementById('login-pass-toggle');
  const loginPass = document.getElementById('login-pass');
  const eyeIconLogin = document.getElementById('eye-icon-login');

  // --- Auth Card (for detecting show_register flag) ---
  const authDeck = document.getElementById('auth-screen-deck');


  // --- Tab Switching ---
  function swapToLogin() {
    paneLogin.classList.add('active');
    paneRegister.classList.remove('active');
    tabLoginBtn.classList.add('active');
    tabRegisterBtn.classList.remove('active');
  }

  function swapToRegister() {
    paneRegister.classList.add('active');
    paneLogin.classList.remove('active');
    tabRegisterBtn.classList.add('active');
    tabLoginBtn.classList.remove('active');
  }

  tabLoginBtn.addEventListener('click', swapToLogin);
  tabRegisterBtn.addEventListener('click', swapToRegister);


  // --- Auto-open Register tab if server flagged validation errors ---
  if (authDeck && authDeck.dataset.showRegister === 'true') {
    swapToRegister();
  }


  // --- Password Visibility Toggle ---
  if (loginPassToggle && loginPass && eyeIconLogin) {
    loginPassToggle.addEventListener('click', () => {
      if (loginPass.type === 'password') {
        loginPass.type = 'text';
        eyeIconLogin.innerHTML = `<path d="M17.94 17.94A10.07 10.07 0 0 1 12 20c-7 0-11-8-11-8a18.45 18.45 0 0 1 5.06-5.94M9.9 4.24A9.12 9.12 0 0 1 12 4c7 0 11 8 11 8a18.5 18.5 0 0 1-2.16 3.19m-6.72-1.07a3 3 0 1 1-4.24-4.24"/><line x1="1" y1="1" x2="23" y2="23"/>`;
      } else {
        loginPass.type = 'password';
        eyeIconLogin.innerHTML = `<path d="M2.062 12.348a1 1 0 0 1 0-.696 10.75 10.75 0 0 1 19.876 0 1 1 0 0 1 0 .696 10.75 10.75 0 0 1-19.876 0z"/><circle cx="12" cy="12" r="3"/>`;
      }
    });
  }

});
