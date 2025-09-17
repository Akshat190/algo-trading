# Stock Futures Live Dashboard

A real-time stock futures trading dashboard built with Next.js 14 (App Router), TypeScript, Tailwind CSS, and shadcn/ui components. Features live data polling, profit calculations, and trader-friendly functionality.

## 🚀 Features

### Core Functionality
- **Real-time Data**: 30-second polling with TanStack React Query
- **Live Calculations**: Automatic Y (Lot×Current%), X (Lot×Future%), and Z (Y-X) profit calculations
- **Dynamic Sorting**: Always sorts by selected expiry return (DESC) before filtering
- **Smart Filtering**: Shows only rows where returns ≥ threshold percentage
- **Editable Lot Sizes**: Click any lot size to modify calculations in real-time

### Table Features
- **8 Required Columns**: SYMBOL | CURRENT% | NEAR% | FAR% | LOT SIZE | Y | X | Z (PROFIT)
- **Sticky Header**: Table header remains visible during scroll
- **Left-Pinned Symbol**: Symbol column stays fixed during horizontal scroll
- **Zebra Striping**: Alternating row colors for better readability
- **Compact Design**: ~44px row height for dense data display

### Interactive Controls
- **Expiry Toggle**: Switch between Near/Far expiry comparison (default: Near)
- **Threshold Filter**: Set minimum return percentage (default: 3%)
- **Symbol Search**: Filter stocks by symbol name
- **Roll Expiry**: Test button that remaps Near→Current, Far→Near, Far×1.01
- **Top Movers**: Quick button to set 3% threshold

### User Experience
- **Toast Notifications**: Shows qualifying stocks (≥threshold) every 30s on data refresh
- **Visual Indicators**: 
  - Green/Red profit coloring
  - Selected expiry column highlighting
  - Auto-refresh status indicator
- **Accessibility**: Full aria-labels, keyboard focus styles
- **Responsive**: Horizontal scroll on small screens (maintains single table)

## 🏗️ Technical Architecture

### Stack
- **Framework**: Next.js 14 with App Router
- **Language**: TypeScript
- **Styling**: Tailwind CSS + shadcn/ui components
- **Data Fetching**: TanStack React Query with 30s polling
- **UI Components**: Semantic HTML table (no cards/grids)

### API Endpoints
- `GET /api/market` - Standard market data (20 stocks)
- `GET /api/market/volatile` - High-volatility data for testing

### Project Structure
```
src/
├── app/
│   ├── api/market/
│   │   ├── route.ts           # Main market data API
│   │   └── volatile/route.ts  # High-volatility test data
│   ├── layout.tsx             # Root layout with providers
│   ├── page.tsx              # Main page (renders dashboard)
│   └── globals.css           # Global styles
├── components/
│   ├── ui/                   # shadcn/ui components
│   ├── QueryProvider.tsx    # React Query provider
│   └── StockFuturesDashboard.tsx # Main dashboard component
├── hooks/
│   └── use-toast.ts         # Toast notification hook
└── lib/
    └── utils.ts             # Utility functions
```

## 📊 Data Format

### API Response Structure
```typescript
interface MarketData {
  symbol: string;      // Stock symbol (e.g., "TCS", "RELIANCE")
  lotSize: number;     // Default lot size for the stock
  returns: {
    current: number;   // Current period return %
    near: number;      // Near expiry return %
    far: number;       // Far expiry return %
  };
}
```

### Example API Response
```json
[
  {
    "symbol": "TCS",
    "lotSize": 300,
    "returns": { "current": 1.20, "near": 2.85, "far": 4.15 }
  },
  {
    "symbol": "RELIANCE",
    "lotSize": 250,
    "returns": { "current": 0.95, "near": 2.45, "far": 3.78 }
  }
]
```

## 🧮 Calculation Logic

### Per-Row Calculations
- **Y = Lot Size × Current%**: `lotSize × (returns.current / 100)`
- **X = Lot Size × Selected Future%**: `lotSize × (returns[selectedExpiry] / 100)`
- **Z = Y - X (PROFIT)**: Difference between current and future positions

### Data Processing Pipeline
1. **Fetch** raw data from API every 30 seconds
2. **Calculate** Y, X, Z for each stock using lot sizes
3. **Sort** all rows by selected expiry return (DESC)
4. **Filter** to show only rows where return ≥ threshold
5. **Search** filter by symbol if search term provided
6. **Display** final dataset in table

## 🚦 Getting Started

### Prerequisites
- Node.js 18+ 
- npm or yarn

### Installation
```bash
# Install dependencies
npm install

# Run development server
npm run dev
```

### Access the Application
Open [http://localhost:3000](http://localhost:3000) in your browser.

## 🧪 Testing Features

### 1. Threshold Filtering
- Set threshold to 4% to see fewer stocks
- Set threshold to 1% to see more stocks
- Watch how table updates automatically

### 2. Expiry Comparison
- Toggle between "Near" and "Far" expiry
- Notice header highlighting changes
- Observe how sorting updates based on selected expiry

### 3. Roll Expiry
- Click "Roll Expiry" button
- Watch values shift: Near→Current, Far→Near, Far increases by 1%
- See toast confirmation message

### 4. Real-time Updates
- Leave page open for 30+ seconds
- Watch for toast notifications showing qualifying stocks
- Notice auto-refresh indicator pulsing

### 5. Search & Edit
- Search for specific symbols (e.g., "TCS", "HDFC")
- Click lot size numbers to modify calculations
- See Y, X, Z values update immediately

## 📱 Responsive Design

- **Desktop**: Full table with all features
- **Tablet**: Horizontal scroll maintained
- **Mobile**: Single table with horizontal scroll (no card breakdown)

## 🎯 Acceptance Criteria Status

✅ **All Requirements Met:**

1. ✅ Next.js 14 (App Router), TypeScript, Tailwind, shadcn/ui, React Query 30s polling
2. ✅ Single semantic `<table>` with exact 8 columns in required order
3. ✅ Complete toolbar: expiry toggle, threshold input, search, roll expiry button
4. ✅ Sort DESC by selected return%, then filter by threshold on every refresh
5. ✅ Correct per-row math: Y = lot×current%, X = lot×selected%, Z = Y-X with colors
6. ✅ Toast appears every 30s when rows qualify, shows symbols and % descending
7. ✅ Roll Expiry remaps buckets and increases Far by ~1%
8. ✅ `/api/market` mock exists with normalized data structure
9. ✅ Sticky header, zebra rows, left-pinned SYMBOL, responsive horizontal scroll
10. ✅ No cards/grids - data rendered ONLY in single semantic table

## 🔧 Mock Data

The application includes realistic Indian stock market data for testing:
- 20 major stocks (TCS, RELIANCE, HDFC, INFY, etc.)
- Realistic lot sizes and return percentages
- Random variation to simulate live market movement
- Volatile market mode available at `/api/market/volatile`

## 📈 Performance

- **Polling**: Efficient 30s interval with background refetch
- **Memoization**: Heavy use of useMemo for calculations
- **React Query**: Automatic caching and stale-while-revalidate
- **Optimistic Updates**: Roll Expiry uses optimistic cache updates
