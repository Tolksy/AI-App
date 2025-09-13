# AI Scheduler - Smart Day Planning App

A modern, AI-powered scheduling application that helps you organize your days and optimize your time blocking for maximum productivity.

## Features

### 📅 Smart Calendar
- Interactive calendar view with monthly navigation
- Visual indicators for days with scheduled blocks
- Easy date selection and navigation

### ⏰ Time Blocking
- Create and manage time blocks with categories:
  - 💼 Work
  - 🤝 Meetings
  - ☕ Breaks
  - 👤 Personal
  - 🏃 Exercise
  - 📚 Learning
- Drag-and-drop style time block management
- Visual time grid from 6 AM to 10 PM
- Edit, delete, and modify existing blocks

### 🤖 AI Assistant
- Intelligent scheduling recommendations based on:
  - Current schedule analysis
  - Productivity research
  - Energy optimization patterns
  - Time blocking best practices
- Smart suggestions for:
  - Schedule optimization
  - Break recommendations
  - Energy management
  - Daily planning templates

### 💾 Data Persistence
- Automatic saving to browser localStorage
- Schedule persists between sessions
- No account required - works offline

## Getting Started

### Prerequisites
- Node.js (version 14 or higher)
- npm or yarn

### Installation

1. **Install dependencies:**
   ```bash
   npm install
   ```

2. **Start the development server:**
   ```bash
   npm run dev
   ```

3. **Open your browser:**
   Navigate to `http://localhost:3000`

### Building for Production

```bash
npm run build
```

The built files will be in the `dist` directory.

## How to Use

### Creating Time Blocks
1. Click on any time slot in the daily schedule
2. Fill in the block details:
   - Title (required)
   - Category (work, meeting, break, etc.)
   - Start and end times
   - Optional description
3. Click "Add Block" to save

### Using AI Suggestions
1. Click the "Get AI Help" button
2. Review the AI-generated suggestions
3. Click "Show details" to see recommended time blocks
4. Click "Apply Suggestion" to add blocks to your schedule

### Managing Your Schedule
- **Edit blocks:** Click on any existing time block
- **Delete blocks:** Click the trash icon on a time block
- **Navigate dates:** Use the calendar to select different days
- **View schedule:** See your blocks in the visual time grid

## AI Features

The AI assistant analyzes your schedule and provides intelligent recommendations:

### Schedule Optimization
- Identifies gaps in your schedule
- Suggests productive uses for available time
- Recommends optimal timing for different activities

### Break Management
- Suggests strategic break times
- Prevents burnout with regular rest periods
- Optimizes energy levels throughout the day

### Energy Management
- Aligns activities with natural energy rhythms
- Prevents afternoon crashes
- Maintains consistent performance

### Daily Planning
- Provides templates for well-structured days
- Balances work, breaks, and personal time
- Creates sustainable daily rhythms

## Technical Details

### Built With
- **React 18** - Modern React with hooks
- **Vite** - Fast build tool and dev server
- **date-fns** - Date manipulation library
- **Lucide React** - Beautiful icons
- **CSS3** - Modern styling with gradients and animations

### Project Structure
```
src/
├── components/          # React components
│   ├── Calendar.jsx    # Calendar view
│   ├── TimeBlock.jsx   # Time blocking interface
│   ├── AIAssistant.jsx # AI suggestions
│   └── ScheduleModal.jsx # Block creation/edit modal
├── services/           # Business logic
│   └── aiService.js    # AI recommendation engine
├── utils/             # Utility functions
│   └── timeUtils.js   # Time and date helpers
├── App.jsx            # Main application
├── main.jsx           # Application entry point
└── index.css          # Global styles
```

### AI Logic
The AI service simulates intelligent recommendations based on:
- Productivity research and best practices
- Energy management principles
- Time blocking methodologies
- Schedule analysis algorithms

## Future Enhancements

Potential features for future versions:
- Real AI integration (OpenAI, Claude, etc.)
- Team scheduling and collaboration
- Integration with calendar apps (Google Calendar, Outlook)
- Mobile app version
- Analytics and productivity insights
- Customizable categories and themes
- Recurring events and templates

## Contributing

Feel free to contribute to this project by:
- Reporting bugs
- Suggesting new features
- Submitting pull requests
- Improving documentation

## License

This project is open source and available under the MIT License.

---

**Happy Scheduling! 🚀**

Start building your perfect day with AI-powered time blocking.
