# Futures Watch Design System Components

## Design Tokens

### Color Palette
```css
:root {
  /* Futures Watch Brand */
  --futures-50: #f0f9ff;
  --futures-100: #e0f2fe;
  --futures-200: #bae6fd;
  --futures-300: #7dd3fc;
  --futures-500: #3b82f6;
  --futures-600: #2563eb;
  --futures-700: #1d4ed8;
  --futures-900: #1e3a8a;
  
  /* Financial Data Colors */
  --profit-positive: #059669;
  --profit-negative: #dc2626;
  
  /* Status Colors */
  --status-live: #10b981;
  --status-refresh: #f59e0b;
  --status-error: #ef4444;
}
```

### Typography Scale
- **Heading 1**: `text-2xl font-bold` (24px, 32px line height)
- **Heading 2**: `text-xl font-semibold` (20px, 28px line height)
- **Body**: `text-sm` (14px, 20px line height)
- **Table Data**: `text-xs` (12px, 16px line height)
- **Labels**: `text-sm font-medium` (14px, 20px line height)

### Spacing Scale
- **Compact**: `p-1` (4px) - button padding
- **Cozy**: `p-2` (8px) - input padding
- **Comfortable**: `p-4` (16px) - card padding
- **Spacious**: `p-6` (24px) - page padding

## Core Components

### 1. FuturesTable Component

**Purpose**: Main data display table with sticky headers, zebra striping, and pinned columns.

**Tailwind Classes**:
```tsx
// Container
className="bg-white rounded-lg border border-neutral-200 overflow-hidden"

// Table wrapper
className="overflow-x-auto"

// Table header
className="sticky top-0 bg-neutral-50 z-60"

// Header cells
className="w-24 font-semibold text-neutral-900 text-center"

// Selected column highlight
className="bg-futures-100 text-futures-900"

// Pinned symbol column
className="sticky left-0 bg-neutral-50 border-r"

// Table rows
className="h-11 hover:bg-futures-50/50 transition-colors"

// Zebra striping
className={index % 2 === 0 ? 'bg-white' : 'bg-neutral-50'}

// Profit cell (positive)
className="font-bold text-profit-positive"

// Profit cell (negative)
className="font-bold text-profit-negative"
```

**Props Interface**:
```tsx
interface FuturesTableProps {
  data: MarketData[];
  selectedExpiry: 'near' | 'far';
  onLotSizeChange: (symbol: string, lotSize: number) => void;
  loading?: boolean;
}
```

### 2. ControlBar Component

**Purpose**: Top toolbar with filters, search, and action buttons.

**Tailwind Classes**:
```tsx
// Container
className="bg-white border-b border-neutral-200 px-6 py-4"

// Controls wrapper
className="flex flex-wrap items-center justify-between gap-4"

// Expiry toggle container
className="flex bg-neutral-100 rounded-lg p-1"

// Active toggle button
className="px-3 py-1 text-xs bg-futures-600 text-white rounded-md"

// Inactive toggle button
className="px-3 py-1 text-xs text-neutral-600 hover:text-neutral-800"

// Threshold input
className="w-20 h-8 text-sm border-neutral-300 focus:border-futures-500"

// Search input with icon
className="pl-9 h-8 w-32 text-sm"

// Action buttons
className="h-8 text-xs border-neutral-300 hover:bg-neutral-50"
```

### 3. LotSizeInput Component

**Purpose**: Inline editable number input for lot sizes.

**Tailwind Classes**:
```tsx
className="w-16 h-7 text-xs text-center border-neutral-300 focus:border-futures-500 focus:ring-1 focus:ring-futures-500"
```

**Props Interface**:
```tsx
interface LotSizeInputProps {
  value: number;
  onChange: (value: number) => void;
  symbol: string;
  min?: number;
  max?: number;
}
```

### 4. StatusIndicator Component

**Purpose**: Auto-refresh and live data status indicators.

**Tailwind Classes**:
```tsx
// Live indicator dot
className="w-2 h-2 bg-status-live rounded-full animate-pulse"

// Status text
className="text-sm text-neutral-600"

// Container
className="flex items-center space-x-1"
```

### 5. ProfitCell Component

**Purpose**: Formatted profit display with color coding.

**Tailwind Classes**:
```tsx
// Positive profit
className="font-bold text-profit-positive"

// Negative profit
className="font-bold text-profit-negative"

// Zero/neutral
className="font-bold text-neutral-500"
```

**Props Interface**:
```tsx
interface ProfitCellProps {
  value: number;
  showSign?: boolean;
  decimals?: number;
}
```

## Responsive Behavior

### Desktop (1440px+)
- Full table layout with all columns visible
- Comfortable spacing: `p-6`
- Large header: `text-2xl`

### Tablet (1024px - 1439px)
- Horizontal scroll maintained
- Reduced padding: `p-4`
- Medium header: `text-xl`

### Mobile (375px - 1023px)
- Single table with horizontal scroll
- Minimal padding: `p-4`
- Compact header: `text-lg`
- Smaller input sizes: `h-7` instead of `h-8`

### Responsive Utilities
```tsx
// Responsive padding
className="px-4 md:px-6"

// Responsive text sizes
className="text-lg md:text-xl lg:text-2xl"

// Responsive button sizes
className="h-7 md:h-8 text-xs"

// Responsive spacing
className="gap-2 md:gap-4"
```

## Accessibility Specifications

### ARIA Labels
```tsx
// Search input
aria-label="Search by symbol"

// Threshold input
aria-label="Set threshold percentage"

// Expiry toggles
aria-label="Select near expiry"
aria-label="Select far expiry"

// Lot size inputs
aria-label={`Edit lot size for ${symbol}`}

// Action buttons
aria-label="Roll expiry forward"
aria-label="Show top movers above 3%"
```

### Keyboard Navigation
- **Tab order**: Left to right, top to bottom
- **Focus styles**: `focus:ring-2 focus:ring-futures-500 focus:border-transparent`
- **Skip links**: For screen readers to skip to table content

### Reduced Motion
```tsx
// Conditional animations
className={`transition-colors ${
  !prefersReducedMotion && 'hover:bg-futures-50/50'
}`}

// Alternative for reduced motion users
@media (prefers-reduced-motion: reduce) {
  .animate-pulse {
    animation: none;
  }
  
  .transition-colors {
    transition: none;
  }
}
```

## Component Usage Examples

### Basic Table Implementation
```tsx
import { FuturesTable } from '@/components/ui/futures-table';

<FuturesTable
  data={marketData}
  selectedExpiry="near"
  onLotSizeChange={(symbol, lotSize) => {
    setLotSizes(prev => ({ ...prev, [symbol]: lotSize }));
  }}
  loading={isLoading}
/>
```

### Control Bar Implementation
```tsx
import { ControlBar } from '@/components/ui/control-bar';

<ControlBar
  selectedExpiry={selectedExpiry}
  onExpiryChange={setSelectedExpiry}
  threshold={threshold}
  onThresholdChange={setThreshold}
  searchTerm={searchTerm}
  onSearchChange={setSearchTerm}
  onRollExpiry={handleRollExpiry}
  onShowTopMovers={() => setThreshold(3.0)}
/>
```

## Performance Considerations

### Memoization
- Use `useMemo` for calculated values (Y, X, Z calculations)
- Use `useCallback` for event handlers
- Implement `React.memo` for table rows

### Virtual Scrolling
For large datasets (1000+ rows):
```tsx
import { FixedSizeList as List } from 'react-window';

<List
  height={600}
  itemCount={data.length}
  itemSize={44} // row height
  itemData={processedData}
>
  {TableRow}
</List>
```

### Optimistic Updates
```tsx
// Roll expiry with immediate UI update
const handleRollExpiry = () => {
  // Update UI immediately
  setOptimisticData(rollExpiry(currentData));
  
  // Then update server
  mutate({ action: 'rollExpiry' });
};
```

## Error States

### Loading State
```tsx
// Table loading skeleton
<TableRow>
  <TableCell colSpan={8} className="text-center py-8">
    <div className="animate-pulse">
      <div className="h-4 bg-neutral-200 rounded w-3/4 mx-auto"></div>
    </div>
  </TableCell>
</TableRow>
```

### Error State
```tsx
// Error message
<div className="p-6 text-center">
  <div className="text-status-error">Error loading market data</div>
  <button 
    onClick={retry}
    className="mt-2 text-futures-600 hover:text-futures-700"
  >
    Retry
  </button>
</div>
```

### Empty State
```tsx
// No data message
<TableRow>
  <TableCell colSpan={8} className="text-center py-8 text-neutral-500">
    No stocks meet the criteria
  </TableCell>
</TableRow>
```

## Testing Guidelines

### Unit Tests
- Test profit calculations (Y, X, Z formulas)
- Test sorting and filtering logic
- Test responsive breakpoints
- Test accessibility attributes

### Integration Tests
- Test API polling behavior
- Test toast notifications
- Test expiry rolling functionality
- Test search and filter interactions

### Visual Regression Tests
- Screenshot comparison for each breakpoint
- Test theme consistency
- Test color contrast ratios
- Test focus states
