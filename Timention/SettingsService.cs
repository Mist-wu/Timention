using System;
using System.IO;
using System.Text.Json;
using System.Threading.Tasks;
using Microsoft.Win32;
using Timention.Models;

namespace Timention
{
    public class SettingsService
    {
        private const string AppName = "Timention";
        private const string SettingsFileName = "settings.json";
        private static readonly string _appDataPath = Path.Combine(Environment.GetFolderPath(Environment.SpecialFolder.ApplicationData), AppName);
        private static readonly string _settingsFilePath = Path.Combine(_appDataPath, SettingsFileName);

        public async Task<AppSettings> LoadSettingsAsync()
        {
            if (!File.Exists(_settingsFilePath))
            {
                return new AppSettings();
            }

            try
            {
                var json = await File.ReadAllTextAsync(_settingsFilePath);
                return JsonSerializer.Deserialize<AppSettings>(json) ?? new AppSettings();
            }
            catch (Exception)
            {
                // Handle potential deserialization errors, e.g., corrupted file
                return new AppSettings();
            }
        }

        public async Task SaveSettingsAsync(AppSettings settings)
        {
            try
            {
                if (!Directory.Exists(_appDataPath))
                {
                    Directory.CreateDirectory(_appDataPath);
                }

                var json = JsonSerializer.Serialize(settings, new JsonSerializerOptions { WriteIndented = true });
                await File.WriteAllTextAsync(_settingsFilePath, json);
            }
            catch (Exception)
            {
                // Handle potential file I/O errors
            }
        }

        public void SetStartup(bool launchOnStartup)
        {
            try
            {
                const string registryKeyPath = @"SOFTWARE\Microsoft\Windows\CurrentVersion\Run";
                using (var key = Registry.CurrentUser.OpenSubKey(registryKeyPath, true))
                {
                    if (key == null) return;

                    if (launchOnStartup)
                    {
                        var executablePath = Environment.ProcessPath;
                        if (executablePath != null)
                        {
                            key.SetValue(AppName, $"\"{executablePath}\"");
                        }
                    }
                    else
                    {
                        key.DeleteValue(AppName, false);
                    }
                }
            }
            catch (Exception)
            {
                // Handle exceptions, e.g., access denied
            }
        }
    }
}
