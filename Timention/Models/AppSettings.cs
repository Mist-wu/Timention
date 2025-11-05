using System;

namespace Timention.Models
{
    public class AppSettings
    {
        public int Hours { get; set; } = 0;
        public int Minutes { get; set; } = 25;
        public bool LaunchOnStartup { get; set; } = false;
        public bool SoundEnabled { get; set; } = true;
        public string ReminderText { get; set; } = "是时候休息一下了！";
        public string? ReminderImagePath { get; set; }
    }
}
