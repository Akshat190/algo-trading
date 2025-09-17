// ==================================================
// FUTURES WATCH DESIGN SYSTEM - COMPONENT IMPLEMENTATIONS
// ==================================================

import React, { useState, useMemo, useCallback, memo } from 'react';
import { useQuery } from '@tanstack/react-query';
import { Search, RefreshCw, TrendingUp } from 'lucide-react';

// ==================================================
// TYPE DEFINITIONS
// ==================================================

export interface MarketData {
  symbol: string;
  lotSize: number;
  returns: {
    current: number;
    near: number;
    far: number;
  };
  lastUpdated: string;
}

export type ExpiryType = 'near' | 'far';

export interface TableRow extends MarketData {
  y: number; // Lot × Current%
  x: number; // Lot × Future%  
  profit: number; // Y - X
  futureReturn: number; // Selected expiry return
}

// ==================================================
// 1. FUTURES TABLE COMPONENT
// ==================================================

interface FuturesTableProps {
  data: TableRow[];
  selectedExpiry: ExpiryType;
  onLotSizeChange: (symbol: string, lotSize: number) => void;
  loading?: boolean;
}

export const FuturesTable = memo<FuturesTableProps>(({
  data,
  selectedExpiry,
  onLotSizeChange,
  loading = false
}) => {
  return (
    <div className="bg-white rounded-lg border border-neutral-200 overflow-hidden">
      <div className="overflow-x-auto">
        <table className="w-full">
          {/* Sticky Header */}
          <thead className="sticky top-0 bg-neutral-50 z-60">
            <tr>
              <th className="w-24 font-semibold text-neutral-900 sticky left-0 bg-neutral-50 border-r px-3 py-3 text-left">
                SYMBOL
              </th>
              <th className="w-24 text-center font-semibold text-neutral-900 px-3 py-3">
                CURRENT%
              </th>
              <th className={`w-24 text-center font-semibold px-3 py-3 ${
                selectedExpiry === 'near' 
                  ? 'bg-futures-100 text-futures-900' 
                  : 'text-neutral-900'
              }`}>
                NEAR%
              </th>
              <th className={`w-24 text-center font-semibold px-3 py-3 ${
                selectedExpiry === 'far' 
                  ? 'bg-futures-100 text-futures-900' 
                  : 'text-neutral-900'
              }`}>
                FAR%
              </th>
              <th className="w-28 text-center font-semibold text-neutral-900 px-3 py-3">
                LOT SIZE
              </th>
              <th className="w-24 text-center font-semibold text-neutral-900 px-3 py-3">
                Y (Lot×Curr%)
              </th>
              <th className="w-24 text-center font-semibold text-neutral-900 px-3 py-3">
                X (Lot×Fut%)
              </th>
              <th className="w-24 text-center font-semibold text-neutral-900 px-3 py-3">
                PROFIT
              </th>
            </tr>
          </thead>

          {/* Table Body */}
          <tbody>
            {loading ? (
              <tr>
                <td colSpan={8} className="text-center py-8 text-neutral-500">
                  <div className="animate-pulse">
                    <div className="h-4 bg-neutral-200 rounded w-3/4 mx-auto"></div>
                  </div>
                </td>
              </tr>
            ) : data.length === 0 ? (
              <tr>
                <td colSpan={8} className="text-center py-8 text-neutral-500">
                  No stocks meet the criteria
                </td>
              </tr>
            ) : (
              data.map((row, index) => (
                <TableRowComponent
                  key={row.symbol}
                  row={row}
                  index={index}
                  selectedExpiry={selectedExpiry}
                  onLotSizeChange={onLotSizeChange}
                />
              ))
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
});

// ==================================================
// 2. TABLE ROW COMPONENT (Memoized for performance)
// ==================================================

interface TableRowProps {
  row: TableRow;
  index: number;
  selectedExpiry: ExpiryType;
  onLotSizeChange: (symbol: string, lotSize: number) => void;
}

const TableRowComponent = memo<TableRowProps>(({ 
  row, 
  index, 
  selectedExpiry, 
  onLotSizeChange 
}) => {
  return (
    <tr 
      className={`h-11 hover:bg-futures-50/50 transition-colors ${
        index % 2 === 0 ? 'bg-white' : 'bg-neutral-50'
      }`}
    >
      {/* Symbol (Pinned) */}
      <td className="font-medium text-neutral-900 sticky left-0 bg-inherit border-r px-3 py-2">
        {row.symbol}
      </td>

      {/* Current % */}
      <td className="text-center text-xs px-3 py-2">
        {row.returns.current.toFixed(2)}%
      </td>

      {/* Near % */}
      <td className={`text-center text-xs px-3 py-2 ${
        selectedExpiry === 'near' ? 'bg-futures-50/50' : ''
      }`}>
        {row.returns.near.toFixed(2)}%
      </td>

      {/* Far % */}
      <td className={`text-center text-xs px-3 py-2 ${
        selectedExpiry === 'far' ? 'bg-futures-50/50' : ''
      }`}>
        {row.returns.far.toFixed(2)}%
      </td>

      {/* Lot Size (Editable) */}
      <td className="text-center px-3 py-2">
        <LotSizeInput
          value={row.lotSize}
          onChange={(value) => onLotSizeChange(row.symbol, value)}
          symbol={row.symbol}
        />
      </td>

      {/* Y Value */}
      <td className="text-center text-xs px-3 py-2">
        {row.y.toFixed(2)}
      </td>

      {/* X Value */}
      <td className="text-center text-xs px-3 py-2">
        {row.x.toFixed(2)}
      </td>

      {/* Profit */}
      <td className="text-center text-xs px-3 py-2">
        <ProfitCell value={row.profit} showSign />
      </td>
    </tr>
  );
});

// ==================================================
// 3. LOT SIZE INPUT COMPONENT
// ==================================================

interface LotSizeInputProps {
  value: number;
  onChange: (value: number) => void;
  symbol: string;
  min?: number;
  max?: number;
}

export const LotSizeInput: React.FC<LotSizeInputProps> = ({
  value,
  onChange,
  symbol,
  min = 1,
  max = 999999
}) => {
  const handleChange = useCallback((e: React.ChangeEvent<HTMLInputElement>) => {
    const newValue = Number(e.target.value);
    if (newValue >= min && newValue <= max) {
      onChange(newValue);
    }
  }, [onChange, min, max]);

  return (
    <input
      type="number"
      value={value}
      onChange={handleChange}
      min={min}
      max={max}
      className="w-16 h-7 text-xs text-center border border-neutral-300 rounded focus:border-futures-500 focus:ring-1 focus:ring-futures-500 focus:outline-none"
      aria-label={`Edit lot size for ${symbol}`}
    />
  );
};

// ==================================================
// 4. PROFIT CELL COMPONENT
// ==================================================

interface ProfitCellProps {
  value: number;
  showSign?: boolean;
  decimals?: number;
}

export const ProfitCell: React.FC<ProfitCellProps> = ({
  value,
  showSign = false,
  decimals = 2
}) => {
  const formatValue = useMemo(() => {
    const formatted = value.toFixed(decimals);
    if (showSign && value > 0) {
      return `+${formatted}`;
    }
    return formatted;
  }, [value, showSign, decimals]);

  const colorClass = useMemo(() => {
    if (value > 0) return 'text-profit-positive';
    if (value < 0) return 'text-profit-negative';
    return 'text-neutral-500';
  }, [value]);

  return (
    <span className={`font-bold ${colorClass}`}>
      {formatValue}
    </span>
  );
};

// ==================================================
// 5. CONTROL BAR COMPONENT
// ==================================================

interface ControlBarProps {
  selectedExpiry: ExpiryType;
  onExpiryChange: (expiry: ExpiryType) => void;
  threshold: number;
  onThresholdChange: (threshold: number) => void;
  searchTerm: string;
  onSearchChange: (term: string) => void;
  onRollExpiry: () => void;
  onShowTopMovers: () => void;
}

export const ControlBar: React.FC<ControlBarProps> = ({
  selectedExpiry,
  onExpiryChange,
  threshold,
  onThresholdChange,
  searchTerm,
  onSearchChange,
  onRollExpiry,
  onShowTopMovers
}) => {
  return (
    <div className="bg-white border-b border-neutral-200 px-4 md:px-6 py-4">
      <div className="flex flex-wrap items-center justify-between gap-4">
        {/* Left Controls */}
        <div className="flex flex-wrap items-center gap-4">
          {/* Expiry Toggle */}
          <div className="flex items-center space-x-2">
            <label className="text-sm font-medium text-neutral-700">
              Expiry Compare:
            </label>
            <div className="flex bg-neutral-100 rounded-lg p-1">
              <button
                onClick={() => onExpiryChange('near')}
                className={`px-3 py-1 text-xs rounded-md transition-colors ${
                  selectedExpiry === 'near'
                    ? 'bg-futures-600 text-white'
                    : 'text-neutral-600 hover:text-neutral-800'
                }`}
                aria-label="Select near expiry"
              >
                Near
              </button>
              <button
                onClick={() => onExpiryChange('far')}
                className={`px-3 py-1 text-xs rounded-md transition-colors ${
                  selectedExpiry === 'far'
                    ? 'bg-futures-600 text-white'
                    : 'text-neutral-600 hover:text-neutral-800'
                }`}
                aria-label="Select far expiry"
              >
                Far
              </button>
            </div>
          </div>

          {/* Threshold Input */}
          <div className="flex items-center space-x-2">
            <label htmlFor="threshold" className="text-sm font-medium text-neutral-700">
              Threshold ≥
            </label>
            <input
              id="threshold"
              type="number"
              step="0.1"
              min="0"
              value={threshold}
              onChange={(e) => onThresholdChange(Number(e.target.value))}
              className="w-20 h-7 md:h-8 text-sm border border-neutral-300 rounded focus:border-futures-500 focus:ring-1 focus:ring-futures-500 focus:outline-none px-2"
              aria-label="Set threshold percentage"
            />
            <span className="text-sm text-neutral-600">%</span>
          </div>

          {/* Search Input */}
          <div className="flex items-center space-x-2">
            <div className="relative">
              <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-neutral-400" />
              <input
                type="text"
                placeholder="SYMBOL"
                value={searchTerm}
                onChange={(e) => onSearchChange(e.target.value)}
                className="pl-9 h-7 md:h-8 w-32 text-sm border border-neutral-300 rounded focus:border-futures-500 focus:ring-1 focus:ring-futures-500 focus:outline-none"
                aria-label="Search by symbol"
              />
            </div>
          </div>
        </div>

        {/* Right Actions */}
        <div className="flex items-center gap-2">
          <button
            onClick={onRollExpiry}
            className="inline-flex items-center h-7 md:h-8 px-3 text-xs border border-neutral-300 rounded hover:bg-neutral-50 transition-colors"
            aria-label="Roll expiry forward"
          >
            <RefreshCw className="h-3 w-3 mr-1" />
            Roll Expiry
          </button>
          
          <button
            onClick={onShowTopMovers}
            className="h-7 md:h-8 px-3 text-xs border border-neutral-300 rounded hover:bg-neutral-50 transition-colors"
            aria-label="Show top movers above 3%"
          >
            Top Movers ≥3%
          </button>
        </div>
      </div>
    </div>
  );
};

// ==================================================
// 6. STATUS INDICATOR COMPONENT
// ==================================================

interface StatusIndicatorProps {
  isLive?: boolean;
  lastUpdated?: string;
}

export const StatusIndicator: React.FC<StatusIndicatorProps> = ({
  isLive = true,
  lastUpdated
}) => {
  return (
    <div className="flex items-center space-x-1 text-sm text-neutral-600">
      <span>Auto-Refresh</span>
      <div 
        className={`w-2 h-2 rounded-full ${
          isLive ? 'bg-status-live animate-pulse' : 'bg-neutral-400'
        }`} 
      />
    </div>
  );
};

// ==================================================
// 7. HEADER COMPONENT
// ==================================================

export const FuturesHeader: React.FC = () => {
  return (
    <header className="bg-white border-b border-neutral-200 px-4 md:px-6 py-4">
      <div className="flex items-center justify-between">
        <div className="flex items-center space-x-3">
          <TrendingUp className="h-8 w-8 text-futures-600" />
          <h1 className="text-lg md:text-xl lg:text-2xl font-bold text-neutral-900">
            Futures Watch
          </h1>
        </div>
        <StatusIndicator />
      </div>
    </header>
  );
};

// ==================================================
// 8. CUSTOM HOOK - useFuturesQuery
// ==================================================

export const useFuturesQuery = (marketMode: 'normal' | 'volatile' = 'normal') => {
  return useQuery({
    queryKey: ['futures-data', marketMode],
    queryFn: async (): Promise<MarketData[]> => {
      const endpoint = marketMode === 'volatile' 
        ? '/api/market/volatile' 
        : '/api/market';
      
      const response = await fetch(endpoint);
      
      if (!response.ok) {
        throw new Error(`Failed to fetch market data: ${response.statusText}`);
      }
      
      return response.json();
    },
    refetchInterval: 30000, // 30 seconds
    refetchIntervalInBackground: true,
    staleTime: 25000, // Consider data stale after 25s
    cacheTime: 5 * 60 * 1000, // Cache for 5 minutes
    retry: 2,
    retryDelay: (attemptIndex) => Math.min(1000 * 2 ** attemptIndex, 30000),
  });
};

// ==================================================
// 9. CUSTOM HOOK - useFuturesCalculations
// ==================================================

export const useFuturesCalculations = (
  marketData: MarketData[],
  editableLotSizes: Record<string, number>,
  selectedExpiry: ExpiryType
) => {
  return useMemo((): TableRow[] => {
    if (!marketData.length) return [];

    return marketData.map(stock => {
      const lotSize = editableLotSizes[stock.symbol] ?? stock.lotSize;
      const y = lotSize * (stock.returns.current / 100); // Current position value
      const futureReturn = stock.returns[selectedExpiry];
      const x = lotSize * (futureReturn / 100); // Future position value
      const profit = x - y; // Profit = Future - Current (positive when future > current)

      return {
        ...stock,
        lotSize,
        y,
        x,
        profit,
        futureReturn,
      };
    });
  }, [marketData, editableLotSizes, selectedExpiry]);
};

// ==================================================
// 10. MAIN DASHBOARD COMPONENT
// ==================================================

export const FuturesWatchDashboard: React.FC = () => {
  const [selectedExpiry, setSelectedExpiry] = useState<ExpiryType>('near');
  const [threshold, setThreshold] = useState<number>(3.0);
  const [searchSymbol, setSearchSymbol] = useState<string>('');
  const [editableLotSizes, setEditableLotSizes] = useState<Record<string, number>>({});
  
  const { data: marketData = [], isLoading, error } = useFuturesQuery();
  const processedRows = useFuturesCalculations(marketData, editableLotSizes, selectedExpiry);
  
  // Sort and filter data
  const filteredRows = useMemo(() => {
    return processedRows
      .sort((a, b) => b.futureReturn - a.futureReturn)
      .filter(row => row.futureReturn >= threshold)
      .filter(row => 
        !searchSymbol.trim() || 
        row.symbol.toLowerCase().includes(searchSymbol.toLowerCase())
      );
  }, [processedRows, threshold, searchSymbol]);

  const handleLotSizeChange = useCallback((symbol: string, newLotSize: number) => {
    setEditableLotSizes(prev => ({
      ...prev,
      [symbol]: newLotSize
    }));
  }, []);

  const handleRollExpiry = useCallback(() => {
    // Implementation would update the market data
    console.log('Roll expiry triggered');
  }, []);

  if (error) {
    return (
      <div className="min-h-screen bg-neutral-50 flex items-center justify-center">
        <div className="p-6 text-center">
          <div className="text-status-error mb-2">Error loading market data</div>
          <button 
            onClick={() => window.location.reload()}
            className="text-futures-600 hover:text-futures-700 underline"
          >
            Retry
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-neutral-50">
      <FuturesHeader />
      
      <ControlBar
        selectedExpiry={selectedExpiry}
        onExpiryChange={setSelectedExpiry}
        threshold={threshold}
        onThresholdChange={setThreshold}
        searchTerm={searchSymbol}
        onSearchChange={setSearchSymbol}
        onRollExpiry={handleRollExpiry}
        onShowTopMovers={() => setThreshold(3.0)}
      />
      
      <div className="p-4 md:p-6">
        <FuturesTable
          data={filteredRows}
          selectedExpiry={selectedExpiry}
          onLotSizeChange={handleLotSizeChange}
          loading={isLoading}
        />
      </div>
    </div>
  );
};

export default FuturesWatchDashboard;
