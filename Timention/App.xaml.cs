using System;
using System.Threading.Tasks;
using Microsoft.UI.Dispatching;
using Microsoft.UI.Xaml;
using Microsoft.UI.Xaml.Controls;
using Timention.Models;
using Timention.UI;
using H.NotifyIcon;
using Microsoft.UI.Xaml.Media;

namespace Timention
{
    public partial class App : Microsoft.UI.Xaml.Application
    {
        private SettingsWindow? _settingsWindow;
        private ReminderWindow? _reminderWindow;
        private readonly SettingsService _settingsService;
        private AppSettings _settings = new();
        private readonly DispatcherTimer _timer;
        private TimeSpan _remainingTime;
        private bool _isPaused = false;
        private TaskbarIcon? _trayIcon;
        private MenuFlyoutItem? _pauseResumeMenuItem;

        public static event EventHandler? SettingsChanged;

        public App()
        {
            this.InitializeComponent();

            _settingsService = new SettingsService();
            _timer = new DispatcherTimer { Interval = TimeSpan.FromSeconds(1) };
            _timer.Tick += Timer_Tick;
            SettingsChanged += OnSettingsChanged;
        }

        protected override async void OnLaunched(Microsoft.UI.Xaml.LaunchActivatedEventArgs args)
        {
            _settings = await _settingsService.LoadSettingsAsync();
            _settingsService.SetStartup(_settings.LaunchOnStartup);

            InitializeTrayIcon();

            ResetTimer();
        }

        private void InitializeTrayIcon()
        {
            _trayIcon = new TaskbarIcon
            {
                IconSource = new Microsoft.UI.Xaml.Media.Imaging.BitmapImage(new Uri("ms-appx:///Assets/placeholder.ico")),
                ToolTipText = "Timention"
            };

            var trayMenu = new MenuFlyout();

            var settingsItem = new MenuFlyoutItem { Text = "设置" };
            settingsItem.Click += SettingsMenuItem_Click;
            trayMenu.Items.Add(settingsItem);

            _pauseResumeMenuItem = new MenuFlyoutItem { Text = "暂停计时" };
            _pauseResumeMenuItem.Click += PauseResumeMenuItem_Click;
            trayMenu.Items.Add(_pauseResumeMenuItem);

            var resetItem = new MenuFlyoutItem { Text = "重置" };
            resetItem.Click += ResetMenuItem_Click;
            trayMenu.Items.Add(resetItem);

            trayMenu.Items.Add(new MenuFlyoutSeparator());

            var exitItem = new MenuFlyoutItem { Text = "退出" };
            exitItem.Click += ExitMenuItem_Click;
            trayMenu.Items.Add(exitItem);

            _trayIcon.ContextFlyout = trayMenu;
            _trayIcon.ForceCreate();
        }


        private void OnSettingsChanged(object? sender, EventArgs e)
        {
            Task.Run(async () =>
            {
                _settings = await _settingsService.LoadSettingsAsync();
                _settingsService.SetStartup(_settings.LaunchOnStartup);
                DispatcherQueue.GetForCurrentThread().TryEnqueue(ResetTimer);
            });
        }

        public static void RaiseSettingsChanged()
        {
            SettingsChanged?.Invoke(null, EventArgs.Empty);
        }

        private void Timer_Tick(object? sender, object e)
        {
            if (_isPaused) return;

            _remainingTime = _remainingTime.Subtract(TimeSpan.FromSeconds(1));
            if (_remainingTime.TotalSeconds <= 0)
            {
                _timer.Stop();
                ShowReminder();
            }
        }

        private void ShowReminder()
        {
            if (_reminderWindow != null) return;

            _reminderWindow = new ReminderWindow();
            _reminderWindow.Closed += (s, e) =>
            {
                _reminderWindow = null;
                ResetTimer();
            };
            _reminderWindow.Activate();
        }

        private void SettingsMenuItem_Click(object sender, Microsoft.UI.Xaml.RoutedEventArgs e)
        {
            if (_settingsWindow == null)
            {
                _settingsWindow = new SettingsWindow();
                _settingsWindow.Closed += (s, args) =>
                {
                    _settingsWindow = null;
                };
                _settingsWindow.Activate();
            }
            else
            {
                _settingsWindow.Activate();
            }
        }

        private void ExitMenuItem_Click(object sender, Microsoft.UI.Xaml.RoutedEventArgs e)
        {
            _trayIcon?.Dispose();
            Exit();
        }

        private void PauseResumeMenuItem_Click(object sender, Microsoft.UI.Xaml.RoutedEventArgs e)
        {
            _isPaused = !_isPaused;
            
            if (_pauseResumeMenuItem != null)
            {
                if (_isPaused)
                {
                    _timer.Stop();
                    _pauseResumeMenuItem.Text = "继续计时";
                }
                else
                {
                    _timer.Start();
                    _pauseResumeMenuItem.Text = "暂停计时";
                }
            }
        }

        private void ResetMenuItem_Click(object sender, Microsoft.UI.Xaml.RoutedEventArgs e)
        {
            ResetTimer();
        }

        private void ResetTimer()
        {
            _remainingTime = new TimeSpan(_settings.Hours, _settings.Minutes, 0);
            _isPaused = false;

            if (_pauseResumeMenuItem != null)
            {
                _pauseResumeMenuItem.Text = "暂停计时";
            }
            _timer.Start();
        }

        ~App()
        {
            SettingsChanged -= OnSettingsChanged;
        }
    }
}
