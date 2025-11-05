using Microsoft.UI.Xaml;
using System;
using Timention.Models;
using System.Threading.Tasks;
using Windows.Storage.Pickers;
using WinRT.Interop;
using Microsoft.UI.Xaml.Controls;
using Microsoft.UI.Xaml.Media.Imaging;
using WinUIEx;

namespace Timention.UI
{
    public sealed class SettingsWindow : WindowEx
    {
        private readonly SettingsService _settingsService;
        private AppSettings _settings = new();

        private TextBox HoursTextBox;
        private TextBox MinutesTextBox;
        private TextBox ReminderTextBox;
        private ToggleSwitch StartupToggle;
        private ToggleSwitch SoundToggle;
        private Image ReminderImagePreview;
        private Button ClearImageButton;

        public SettingsWindow()
        {
            _settingsService = new SettingsService();
            InitializeComponent();
            InitializeWindow();
        }

        private void InitializeComponent()
        {
            var mainGrid = new Grid
            {
                RowDefinitions = {
                    new RowDefinition { Height = GridLength.Auto },
                    new RowDefinition { Height = GridLength.Auto },
                    new RowDefinition { Height = GridLength.Auto },
                    new RowDefinition { Height = GridLength.Auto },
                    new RowDefinition { Height = GridLength.Auto },
                    new RowDefinition { Height = new GridLength(1, GridUnitType.Star) },
                    new RowDefinition { Height = GridLength.Auto }
                },
                ColumnDefinitions = {
                    new ColumnDefinition { Width = GridLength.Auto },
                    new ColumnDefinition { Width = new GridLength(1, GridUnitType.Star) }
                },
                Margin = new Thickness(20)
            };
            mainGrid.Loaded += async (s, e) => await LoadSettingsAsync();

            // Time settings
            mainGrid.Children.Add(new TextBlock { Text = "Timer (HH:MM):", VerticalAlignment = VerticalAlignment.Center });
            var timePanel = new StackPanel { Orientation = Orientation.Horizontal, Margin = new Thickness(10,0,0,10) };
            HoursTextBox = new TextBox { Width = 50 };
            timePanel.Children.Add(HoursTextBox);
            timePanel.Children.Add(new TextBlock { Text = ":", VerticalAlignment = VerticalAlignment.Center, Margin = new Thickness(5,0,5,0) });
            MinutesTextBox = new TextBox { Width = 50 };
            timePanel.Children.Add(MinutesTextBox);
            Grid.SetColumn(timePanel, 1);
            mainGrid.Children.Add(timePanel);

            // Reminder Text
            var reminderLabel = new TextBlock { Text = "Reminder Text:", VerticalAlignment = VerticalAlignment.Center };
            Grid.SetRow(reminderLabel, 1);
            mainGrid.Children.Add(reminderLabel);
            ReminderTextBox = new TextBox { Margin = new Thickness(10,0,0,10) };
            Grid.SetRow(ReminderTextBox, 1);
            Grid.SetColumn(ReminderTextBox, 1);
            mainGrid.Children.Add(ReminderTextBox);

            // Toggles
            var startupLabel = new TextBlock { Text = "Launch on Startup:", VerticalAlignment = VerticalAlignment.Center };
            Grid.SetRow(startupLabel, 2);
            mainGrid.Children.Add(startupLabel);
            StartupToggle = new ToggleSwitch { Name = "StartupToggle", Margin = new Thickness(10,0,0,0) };
            StartupToggle.Toggled += Toggle_Toggled;
            Grid.SetRow(StartupToggle, 2);
            Grid.SetColumn(StartupToggle, 1);
            mainGrid.Children.Add(StartupToggle);

            var soundLabel = new TextBlock { Text = "Enable Sound:", VerticalAlignment = VerticalAlignment.Center };
            Grid.SetRow(soundLabel, 3);
            mainGrid.Children.Add(soundLabel);
            SoundToggle = new ToggleSwitch { Name = "SoundToggle", Margin = new Thickness(10,0,0,0) };
            SoundToggle.Toggled += Toggle_Toggled;
            Grid.SetRow(SoundToggle, 3);
            Grid.SetColumn(SoundToggle, 1);
            mainGrid.Children.Add(SoundToggle);

            // Image Preview and controls
            var imageLabel = new TextBlock { Text = "Reminder Image:", VerticalAlignment = VerticalAlignment.Center };
            Grid.SetRow(imageLabel, 4);
            mainGrid.Children.Add(imageLabel);
            var imageControlsPanel = new StackPanel { Orientation = Orientation.Horizontal, Margin = new Thickness(10,10,0,10) };
            var pickImageButton = new Button { Content = "Pick Image" };
            pickImageButton.Click += PickImageButton_Click;
            imageControlsPanel.Children.Add(pickImageButton);
            ClearImageButton = new Button { Content = "Clear Image", Visibility = Visibility.Collapsed, Margin = new Thickness(10,0,0,0) };
            ClearImageButton.Click += ClearImageButton_Click;
            imageControlsPanel.Children.Add(ClearImageButton);
            Grid.SetRow(imageControlsPanel, 4);
            Grid.SetColumn(imageControlsPanel, 1);
            mainGrid.Children.Add(imageControlsPanel);

            ReminderImagePreview = new Image { Stretch = Microsoft.UI.Xaml.Media.Stretch.Uniform, MaxHeight = 150, Margin = new Thickness(10,10,0,10) };
            Grid.SetRow(ReminderImagePreview, 5);
            Grid.SetColumn(ReminderImagePreview, 1);
            mainGrid.Children.Add(ReminderImagePreview);

            // Save Button
            var saveButton = new Button { Content = "Save and Close", HorizontalAlignment = HorizontalAlignment.Right, Margin = new Thickness(0,20,0,0) };
            saveButton.Click += SaveButton_Click;
            Grid.SetRow(saveButton, 6);
            Grid.SetColumnSpan(saveButton, 2);
            mainGrid.Children.Add(saveButton);

            this.Content = mainGrid;
        }

        private void InitializeWindow()
        {
            Title = "Timention Settings";
            // Further window styling can be done here.
        }

        private async Task LoadSettingsAsync()
        {
            _settings = await _settingsService.LoadSettingsAsync();
            HoursTextBox.Text = _settings.Hours.ToString("D2");
            MinutesTextBox.Text = _settings.Minutes.ToString("D2");
            ReminderTextBox.Text = _settings.ReminderText;
            StartupToggle.IsOn = _settings.LaunchOnStartup;
            SoundToggle.IsOn = _settings.SoundEnabled;
            UpdateReminderImagePreview();
        }

        private async void SaveButton_Click(object sender, RoutedEventArgs e)
        {
            if (int.TryParse(HoursTextBox.Text, out int hours) && int.TryParse(MinutesTextBox.Text, out int minutes))
            {
                _settings.Hours = hours;
                _settings.Minutes = minutes;
                _settings.ReminderText = ReminderTextBox.Text;
                // Note: Toggle states are saved on toggled events.
                await _settingsService.SaveSettingsAsync(_settings);
                App.RaiseSettingsChanged();
                this.Close();
            }
            // Optionally, provide feedback to the user.
        }

        private async void Toggle_Toggled(object sender, RoutedEventArgs e)
        {
            if (sender is ToggleSwitch toggle)
            {
                switch (toggle.Name)
                {
                    case "StartupToggle":
                        _settings.LaunchOnStartup = toggle.IsOn;
                        break;
                    case "SoundToggle":
                        _settings.SoundEnabled = toggle.IsOn;
                        break;
                }
                await _settingsService.SaveSettingsAsync(_settings);
                App.RaiseSettingsChanged();
            }
        }

        private async void PickImageButton_Click(object sender, RoutedEventArgs e)
        {
            var fileOpenPicker = new FileOpenPicker();
            var windowHandle = WindowNative.GetWindowHandle(this);
            InitializeWithWindow.Initialize(fileOpenPicker, windowHandle);

            fileOpenPicker.ViewMode = PickerViewMode.Thumbnail;
            fileOpenPicker.SuggestedStartLocation = PickerLocationId.PicturesLibrary;
            fileOpenPicker.FileTypeFilter.Add(".jpg");
            fileOpenPicker.FileTypeFilter.Add(".jpeg");
            fileOpenPicker.FileTypeFilter.Add(".png");
            fileOpenPicker.FileTypeFilter.Add(".bmp");

            var file = await fileOpenPicker.PickSingleFileAsync();
            if (file != null)
            {
                _settings.ReminderImagePath = file.Path;
                await _settingsService.SaveSettingsAsync(_settings);
                App.RaiseSettingsChanged();
                UpdateReminderImagePreview();
            }
        }

        private void ClearImageButton_Click(object sender, RoutedEventArgs e)
        {
            _settings.ReminderImagePath = null;
            _settingsService.SaveSettingsAsync(_settings);
            App.RaiseSettingsChanged();
            UpdateReminderImagePreview();
        }

        private void UpdateReminderImagePreview()
        {
            if (!string.IsNullOrEmpty(_settings.ReminderImagePath) && System.IO.File.Exists(_settings.ReminderImagePath))
            {
                try
                {
                    ReminderImagePreview.Source = new BitmapImage(new Uri(_settings.ReminderImagePath));
                    ClearImageButton.Visibility = Visibility.Visible;
                }
                catch
                {
                    ReminderImagePreview.Source = null;
                    ClearImageButton.Visibility = Visibility.Collapsed;
                }
            }
            else
            {
                ReminderImagePreview.Source = null;
                ClearImageButton.Visibility = Visibility.Collapsed;
            }
        }
    }
}
