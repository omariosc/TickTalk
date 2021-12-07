function addDarkmodeWidget() {
  const options = {
    bottom: '16px',
    right: '16px',
    left: 'unset',
    time: '0.7s',
    mixColor: '#fff',
    backgroundColor: '#fff',
    buttonColorDark: '#100f2c',
    buttonColorLight: '#fff',
    saveInCookies: true,
    label: '🌓',
    autoMatchOsTheme: true
  }
  new Darkmode(options).showWidget();
}
window.addEventListener('load', addDarkmodeWidget);