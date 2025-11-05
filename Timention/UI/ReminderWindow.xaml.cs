using Microsoft.UI.Xaml;
using Microsoft.UI.Xaml.Controls;
using Microsoft.UI.Xaml.Input;
using Microsoft.UI.Xaml.Media.Imaging;
using System;
using System.Threading.Tasks;
using Timention.Models;
using Timention.Services;
using WinUIEx;

namespace Timention.UI
{
    public sealed class ReminderWindow : WindowEx
    {
        private TextBlock ReminderText;
        private Image ReminderImage;

        public ReminderWindow()
        {
            this.Title = "Reminder";
            SetupWindow();

            var grid = new Grid();
            grid.Loaded += async (s, e) => await InitializeContentAsync();
            grid.KeyDown += OnWindowKeyDown;

            ReminderText = new TextBlock
            {
                HorizontalAlignment = HorizontalAlignment.Center,
                VerticalAlignment = VerticalAlignment.Center,
                FontSize = 48
            };
            grid.Children.Add(ReminderText);

            ReminderImage = new Image
            {
                Stretch = Microsoft.UI.Xaml.Media.Stretch.Uniform,
                Visibility = Visibility.Collapsed
            };
            grid.Children.Add(ReminderImage);

            this.Content = grid;
        }

        private async Task InitializeContentAsync()
        {
            var settingsService = new SettingsService();
            var settings = await settingsService.LoadSettingsAsync();
            ReminderText.Text = settings.ReminderText;

            if (!string.IsNullOrEmpty(settings.ReminderImagePath) && System.IO.File.Exists(settings.ReminderImagePath))
            {
                try
                {
                    ReminderImage.Source = new BitmapImage(new Uri(settings.ReminderImagePath));
                    ReminderImage.Visibility = Visibility.Visible;
                }
                catch (Exception)
                {
                    // Handle image loading errors
                    ReminderImage.Visibility = Visibility.Collapsed;
                }
            }
            else
            {
                ReminderImage.Visibility = Visibility.Collapsed;
            }
        }

        private void SetupWindow()
        {
            this.AppWindow.SetPresenter(Microsoft.UI.Windowing.AppWindowPresenterKind.FullScreen);
            if (this.AppWindow.Presenter is Microsoft.UI.Windowing.OverlappedPresenter overlappedPresenter)
            {
                overlappedPresenter.IsAlwaysOnTop = true;
            }
            this.AppWindow.IsShownInSwitchers = false;
        }

        private void OnWindowKeyDown(object sender, KeyRoutedEventArgs e)
        {
            this.Close();
        }
    }
}
