# Rubik's Cube Solver Frontend

A modern React/Next.js frontend for solving Rubik's cubes using Kociemba's Two-Phase Algorithm. This application provides an intuitive interface for configuring cube states and displaying optimal solutions.

## Features

- 🎯 **Interactive Cube Interface**: Click-to-configure 3x3 grid for all 6 faces
- 🎨 **Color Selection**: Easy color picker for each sticker
- 🔀 **Scramble Function**: Generate random cube configurations
- ⚡ **Real-time Solving**: Connect to your Flask backend API
- 📱 **Responsive Design**: Works on desktop and mobile devices
- 🚀 **Vercel Ready**: Optimized for Vercel deployment

## Quick Start

### 1. Clone and Install

\`\`\`bash
git clone <your-repo-url>
cd rubiks-cube-solver
npm install
\`\`\`

### 2. Configure Environment

Create a `.env.local` file:

\`\`\`env
# For local development
NEXT_PUBLIC_API_URL=http://localhost:5000

# For production (replace with your backend URL)
# NEXT_PUBLIC_API_URL=https://your-backend-api.herokuapp.com
\`\`\`

### 3. Run Development Server

\`\`\`bash
npm run dev
\`\`\`

Visit `http://localhost:3000` to see the application.

## Backend API Requirements

Your Flask backend should provide these endpoints:

### POST /solve
\`\`\`json
{
  "cube_state": "UUUUUUUUURRRRRRRRRFFFFFFFFFDDDDDDDDDLLLLLLLLLBBBBBBBBB"
}
\`\`\`

Response:
\`\`\`json
{
  "success": true,
  "moves": ["R", "U", "R'", "U'", "R", "U", "R'"],
  "solve_time": 0.045
}
\`\`\`

### GET /scramble (Optional)
Response:
\`\`\`json
{
  "scramble": "R U R' U' R U R' F' R U R' U' R' F R"
}
\`\`\`

## Cube State Format

The cube state is represented as a 54-character string:
- Positions 0-8: Up face (White)
- Positions 9-17: Right face (Red)
- Positions 18-26: Front face (Green)
- Positions 27-35: Down face (Yellow)
- Positions 36-44: Left face (Orange)
- Positions 45-53: Back face (Blue)

Each character represents a sticker color:
- `U` = White (Up)
- `R` = Red (Right)
- `F` = Green (Front)
- `D` = Yellow (Down)
- `L` = Orange (Left)
- `B` = Blue (Back)

## Deployment

### Deploy to Vercel

1. **Push to GitHub**:
   \`\`\`bash
   git add .
   git commit -m "Initial commit"
   git push origin main
   \`\`\`

2. **Connect to Vercel**:
   - Go to [vercel.com](https://vercel.com)
   - Import your GitHub repository
   - Add environment variable: `NEXT_PUBLIC_API_URL`

3. **Deploy**: Vercel will automatically build and deploy your app

### Environment Variables

Set these in your Vercel dashboard:

- `NEXT_PUBLIC_API_URL`: Your backend API URL

## Project Structure

\`\`\`
├── app/
│   ├── page.tsx              # Main application page
│   ├── layout.tsx            # Root layout
│   └── globals.css           # Global styles
├── components/
│   ├── cube-interface.tsx    # Main cube configuration component
│   ├── cube-face.tsx         # Individual face component
│   ├── move-display.tsx      # Solution display component
│   └── ui/                   # Reusable UI components
├── lib/
│   ├── api.ts               # API communication functions
│   └── cube-utils.ts        # Cube state utilities
└── README.md
\`\`\`

## Customization

### Adding New Features

1. **3D Visualization**: Integrate Three.js for 3D cube rendering
2. **Move Animation**: Add step-by-step move visualization
3. **Solve History**: Store and display previous solutions
4. **Timer**: Add solving timer functionality

### Styling

The app uses Tailwind CSS. Customize colors and styling in:
- `tailwind.config.ts`
- Component className props
- `app/globals.css`

## Troubleshooting

### Common Issues

1. **API Connection Failed**:
   - Check if your Flask backend is running
   - Verify the `NEXT_PUBLIC_API_URL` environment variable
   - Check CORS settings in your Flask app

2. **Build Errors**:
   - Run `npm run build` locally to test
   - Check TypeScript errors
   - Verify all dependencies are installed

3. **Deployment Issues**:
   - Ensure environment variables are set in Vercel
   - Check build logs in Vercel dashboard
   - Verify your backend API is accessible from the internet

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

MIT License - feel free to use this project for your own cube solver implementations!
